// ============================================================================
// FILE: apps/web/src/app.js
//
// THINK OF THIS FILE AS: the entire web interface. All of it — every button,
// every list, every call to the API — is in this one file.
//
// WHAT IT IS AND IS NOT:
//   It is a DEVELOPER CONSOLE, not a product. It exists so you can exercise
//   every API endpoint by clicking rather than by typing curl commands, and so
//   a demonstration has something to show. A real support agent would get a
//   properly designed application; this is the workbench.
//
//   That framing explains the choices below: no framework (no React, no Vue),
//   no build step, no dependencies. It is plain JavaScript loaded directly by
//   the browser. Open index.html and it runs. For a tool of this size, that
//   simplicity is worth more than any framework's conveniences.
//
// HOW IT TALKS TO THE API:
//   Every request carries the same identity headers the API expects
//   (X-Tenant-Id, X-User-Id, X-Role) — see authHeaders below. Those are typed
//   into form fields at the top of the page, which is only acceptable because
//   the API trusts them anyway; see dependencies.py and docs/threat-model.md.
//
// THE SHAPE OF THE CODE, top to bottom:
//   1. state + elements  - what we know, and the page elements we control
//   2. request()         - the one function that talks to the API
//   3. render*()         - functions that redraw parts of the page
//   4. action functions  - one per button
//   5. initialize()      - wires buttons to actions and starts everything
//
// THE CENTRAL PATTERN: state -> render.
//   Nothing edits the page directly in response to data. Instead an action
//   updates `state`, then calls a render function that rebuilds that section
//   from scratch. Cruder than what a framework does, but easy to follow and
//   impossible to get into an inconsistent state.
// ============================================================================

// Everything the page currently knows. The single source of truth: if it is not
// in here, it is not on screen.
const state = {
  tickets: [],
  recommendations: [],
  runs: [],
  policies: [],
  selectedTicketId: null,           // which ticket the action buttons apply to
  selectedRecommendationId: null,   // which draft the approve button applies to
};

// Every page element the code touches, looked up ONCE at startup.
//
// Doing it here rather than repeatedly calling getElementById later is both
// faster and safer: it means the whole list of required element IDs is visible
// in one place, and a typo shows up immediately rather than as a mysterious
// null halfway through an action.
const elements = {
  // --- Connection and identity settings ---
  apiBaseUrl: document.getElementById("apiBaseUrl"),
  tenantId: document.getElementById("tenantId"),
  userId: document.getElementById("userId"),
  role: document.getElementById("role"),
  // --- The new-ticket form ---
  externalId: document.getElementById("externalId"),
  subject: document.getElementById("subject"),
  body: document.getElementById("body"),
  customerId: document.getElementById("customerId"),
  // --- The new-policy form ---
  policyName: document.getElementById("policyName"),
  policyContent: document.getElementById("policyContent"),
  // --- Status indicators ---
  apiStatus: document.getElementById("apiStatus"),
  readyStatus: document.getElementById("readyStatus"),
  selectionStatus: document.getElementById("selectionStatus"),
  // --- The lists that display data ---
  ticketList: document.getElementById("ticketList"),
  recommendationList: document.getElementById("recommendationList"),
  runList: document.getElementById("runList"),
  policyList: document.getElementById("policyList"),
  metricCards: document.getElementById("metricCards"),
  pilotFeedbackList: document.getElementById("pilotFeedbackList"),
  eventLog: document.getElementById("eventLog"),
};

// The API's address, tidied.
//
// The regular expression `/\/$/` matches a trailing slash and removes it, so
// both "http://localhost:8765" and "http://localhost:8765/" work. Without this,
// the second would build URLs with a doubled slash — which some servers accept
// and others reject, producing a confusing intermittent bug.
function apiBaseUrl() {
  return elements.apiBaseUrl.value.trim().replace(/\/$/, "");
}

// The identity headers sent with every request — the same ones get_current_actor
// reads in dependencies.py.
//
// `roleOverride` exists for one specific case: creating a policy requires the
// "lead" role, but the console is usually operated as "agent". Rather than
// making the user change the dropdown and change it back, createPolicy passes
// "lead" for that one call.
function authHeaders(roleOverride) {
  return {
    "Content-Type": "application/json",
    "X-Tenant-Id": elements.tenantId.value.trim(),
    "X-User-Id": elements.userId.value.trim(),
    "X-Role": roleOverride || elements.role.value,
  };
}

// THE ONE FUNCTION THAT TALKS TO THE API. Every call goes through here.
//
// Centralising it means the identity headers, the JSON handling, and the error
// handling are written once and applied consistently. No individual action can
// forget to send a header or forget to check for an error.
async function request(path, options = {}, roleOverride = null) {
  const response = await fetch(`${apiBaseUrl()}${path}`, {
    // `...options` spreads the caller's settings in, then headers are rebuilt
    // below so the auth headers are always present. The caller's own headers are
    // spread in last, so they can override if they genuinely need to.
    ...options,
    headers: {
      ...authHeaders(roleOverride),
      ...(options.headers || {}),
    },
  });

  // The reply may be JSON or plain text. GET /metrics/runtime returns Prometheus
  // text rather than JSON, so the content type has to be checked rather than
  // assumed — calling .json() on the Prometheus output would throw.
  const contentType = response.headers.get("content-type") || "";
  const body = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  // IMPORTANT: `fetch` does NOT throw on a 404 or a 500. It only rejects on a
  // network failure. A very common source of bugs — without this check, an error
  // response would flow onward and be treated as valid data.
  //
  // FastAPI puts its error message in a "detail" field, which is pulled out here
  // so the log shows "ticket not found" rather than a raw object.
  if (!response.ok) {
    const detail = typeof body === "object" && body !== null ? body.detail : body;
    throw new Error(`${response.status} ${detail || response.statusText}`);
  }
  return body;
}

// Updates one of the coloured status badges. The CSS class drives the colour;
// see styles.css for "ok", "warn", "error", and "neutral".
function setPill(element, label, mode) {
  element.textContent = label;
  element.className = `status-pill ${mode}`;
}

// Writes to the on-screen event log — the console's most useful feature.
//
// Every action logs its full request or response here, so you can see exactly
// what the API returned without opening the browser's developer tools. Newest
// entries go at the TOP (note the order of the template below), because the most
// recent thing is what you want to read.
//
// `JSON.stringify(payload, null, 2)` formats the object across multiple lines
// with two-space indentation, which makes a nested response readable.
function logEvent(label, payload) {
  const time = new Date().toLocaleTimeString();
  const rendered = typeof payload === "string" ? payload : JSON.stringify(payload, null, 2);
  elements.eventLog.textContent = `[${time}] ${label}\n${rendered}\n\n${elements.eventLog.textContent}`;
}

// Selects a ticket, and clears anything that belonged to the previous one.
//
// Note `selectedRecommendationId` is reset to null. Essential: a draft belongs
// to a specific ticket, so keeping the old selection would leave the approve
// button pointing at a draft from a different ticket — and the API would
// correctly reject it with a confusing 404.
function setSelectedTicket(ticketId) {
  state.selectedTicketId = ticketId;
  state.selectedRecommendationId = null;
  // Only the first 8 characters of the UUID are shown. Enough to recognise,
  // short enough to fit in a badge.
  const label = ticketId ? `Ticket ${ticketId.slice(0, 8)}` : "No ticket selected";
  setPill(elements.selectionStatus, label, ticketId ? "ok" : "neutral");
  renderTickets();
  renderRecommendations();
  renderRuns();
}

function setSelectedRecommendation(recommendationId) {
  state.selectedRecommendationId = recommendationId;
  renderRecommendations();
}

// Builds one clickable row. Used by every list on the page.
//
// TWO ACCESSIBILITY DETAILS worth noticing, since they are easy to omit:
//   `node.role = "button"` and `tabIndex = 0` make a plain <div> reachable by
//   keyboard and announced correctly by a screen reader. Without them this would
//   be mouse-only.
//   The keydown handler makes Enter and Space activate it, which is what a real
//   button does for free. `preventDefault()` stops Space from scrolling the page.
//
// A SECURITY DETAIL, and the more important one: the text is set via
// `.textContent`, never by putting it into the innerHTML string. innerHTML would
// interpret the content as HTML — so a ticket subject containing a <script> tag
// would EXECUTE. That is a cross-site scripting hole, and since ticket text
// comes from customers, it would be a genuinely exploitable one. textContent
// always treats the value as plain text.
function item(title, meta, selected, onClick) {
  const node = document.createElement("div");
  node.className = `list-item${selected ? " selected" : ""}`;
  node.role = "button";
  node.tabIndex = 0;
  // Only the fixed structure goes through innerHTML — never user data.
  node.innerHTML = `<span class="list-title"></span><span class="list-meta"></span>`;
  node.querySelector(".list-title").textContent = title;
  node.querySelector(".list-meta").textContent = meta;
  node.addEventListener("click", onClick);
  node.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onClick();
    }
  });
  return node;
}

// --- The render functions ---------------------------------------------------
//
// All four follow the same three steps: empty the container, show a message if
// there is nothing, otherwise build a row per item. Rebuilding from scratch each
// time is wasteful in principle and completely fine at this scale — and it makes
// a stale or inconsistent display impossible.

function renderTickets() {
  elements.ticketList.innerHTML = "";
  if (!state.tickets.length) {
    elements.ticketList.textContent = "No tickets loaded.";
    return;
  }
  state.tickets.forEach((ticket) => {
    elements.ticketList.appendChild(
      item(
        `${ticket.external_id}: ${ticket.subject}`,
        `${ticket.status} / ${ticket.priority} / ${ticket.id}`,
        ticket.id === state.selectedTicketId,     // highlights the selected row
        () => setSelectedTicket(ticket.id),
      ),
    );
  });
}

function renderRecommendations() {
  elements.recommendationList.innerHTML = "";
  if (!state.recommendations.length) {
    elements.recommendationList.textContent = "No recommendations loaded.";
    return;
  }
  state.recommendations.forEach((recommendation) => {
    elements.recommendationList.appendChild(
      item(
        // `source` comes first deliberately — it tells you whether this came
        // from the AI or the free keyword rules, which is the first thing you
        // want to know when comparing them.
        `${recommendation.source}: ${recommendation.category} / ${recommendation.priority}`,
        `${recommendation.confidence} / ${recommendation.id}`,
        recommendation.id === state.selectedRecommendationId,
        () => setSelectedRecommendation(recommendation.id),
      ),
    );
  });
}

function renderRuns() {
  elements.runList.innerHTML = "";
  if (!state.runs.length) {
    elements.runList.textContent = "No analysis runs loaded.";
    return;
  }
  state.runs.forEach((run) => {
    elements.runList.appendChild(
      item(
        // The status is what you watch after queueing an analysis: it moves from
        // "queued" through "running" to "succeeded".
        `${run.status}: ${run.model_provider || "provider"}`,
        `${run.output_recommendation_id || "no recommendation yet"} / ${run.id}`,
        false,                                    // runs are never "selected"
        () => logEvent("Analysis run", run),      // clicking dumps the full record
      ),
    );
  });
}

function renderPolicies() {
  elements.policyList.innerHTML = "";
  if (!state.policies.length) {
    elements.policyList.textContent = "No policies loaded.";
    return;
  }
  state.policies.forEach((policy) => {
    elements.policyList.appendChild(
      item(policy.name, `${policy.created_by_user_id} / ${policy.id}`, false, () => {
        logEvent("Policy", policy);
      }),
    );
  });
}

// Draws the metrics tiles from the five different metrics endpoints.
//
// The list-of-pairs approach keeps the layout data-driven: adding a tile is one
// line, and the loop below handles the rest.
function renderMetrics(reviewMetrics, costMetrics, pilotMetrics, pilotFeedback, runtimeMetrics) {
  const cards = [
    ["Recommendations", reviewMetrics.total_recommendations],
    ["Reviewed", reviewMetrics.reviewed_recommendations],
    ["Approval rate", reviewMetrics.approval_rate],     // the headline quality number
    ["Cost USD", costMetrics.estimated_cost_usd],
    ["Cost events", costMetrics.total_events],
    ["Pilot decision", pilotMetrics.exit_decision],     // expand / iterate / stop / roll_back
    // `|| "all"` because an empty category list means "no restriction", matching
    // the convention in pilot.py. Showing an empty tile would read as "none".
    ["Pilot categories", pilotMetrics.pilot_categories.join(", ") || "all"],
    ["Pilot accepted", pilotMetrics.accepted_drafts],
    ["Pilot rejected", pilotMetrics.rejected_drafts],
    ["Input tokens", costMetrics.input_tokens],
    ["Output tokens", costMetrics.output_tokens],
    // A rough liveness signal rather than a real measurement: the Prometheus
    // endpoint returns text, so this just counts its non-empty lines to show
    // that it responded with something.
    ["Runtime lines", runtimeMetrics.split("\n").filter(Boolean).length],
  ];
  elements.metricCards.innerHTML = "";
  cards.forEach(([label, value]) => {
    const node = document.createElement("div");
    node.className = "metric";
    node.innerHTML = `<div class="list-meta"></div><div class="metric-value"></div>`;
    // textContent again, not innerHTML — same reasoning as in item().
    node.querySelector(".list-meta").textContent = label;
    node.querySelector(".metric-value").textContent = String(value);
    elements.metricCards.appendChild(node);
  });
  renderPilotFeedback(pilotFeedback);
}

// Lists the specific drafts humans rejected or heavily rewrote.
//
// When there are none, it shows the API's `recommended_next_step` message rather
// than a bare "nothing here" — so an empty state still tells you what to do
// next, which in this case is usually "keep collecting reviews".
function renderPilotFeedback(pilotFeedback) {
  elements.pilotFeedbackList.innerHTML = "";
  if (!pilotFeedback.candidates.length) {
    elements.pilotFeedbackList.textContent = pilotFeedback.recommended_next_step;
    return;
  }
  pilotFeedback.candidates.forEach((candidate) => {
    elements.pilotFeedbackList.appendChild(
      item(
        `${candidate.decision}: ${candidate.category}`,
        `${candidate.notes || "No notes"} / edit distance ${candidate.edit_distance}`,
        false,
        // Clicking logs the whole record, which includes the AI's draft and the
        // human's final version side by side — the most instructive thing in the
        // entire console.
        () => logEvent("Pilot feedback candidate", candidate),
      ),
    );
  });
}

// --- The action functions, one per button -----------------------------------

// Checks both health endpoints.
//
// Note the two SEPARATE try/catch blocks. Deliberate: /ready is still checked
// even if /health failed, so you learn about both. One combined block would stop
// at the first failure and hide the more informative answer.
async function checkHealth() {
  try {
    const health = await request("/health", { method: "GET" });
    setPill(elements.apiStatus, health.status === "ok" ? "API ok" : "API issue", "ok");
    logEvent("Health", health);
  } catch (error) {
    setPill(elements.apiStatus, "API error", "error");
    logEvent("Health failed", error.message);
  }

  try {
    const ready = await request("/ready", { method: "GET" });
    // "warn" rather than "error" when not ready: the API answered, so it is
    // running — something it depends on is not. A meaningful distinction, and
    // the same one drawn in routes/health.py.
    setPill(elements.readyStatus, ready.status, ready.status === "ready" ? "ok" : "warn");
    logEvent("Readiness", ready);
  } catch (error) {
    setPill(elements.readyStatus, "not ready", "error");
    logEvent("Readiness failed", error.message);
  }
}

async function createTicket() {
  // Generates a unique external ID from the current timestamp if none was typed,
  // then writes it back into the form so you can SEE what was used. Without a
  // unique value, the second submission would be recognised as a duplicate by
  // routes/tickets.py and return the first ticket instead of creating one —
  // correct behaviour that looks like a bug when testing.
  const externalId = elements.externalId.value.trim() || `web-${Date.now()}`;
  elements.externalId.value = externalId;
  const payload = {
    external_id: externalId,
    channel: "web",
    subject: elements.subject.value.trim(),
    body: elements.body.value.trim(),
    customer_id: elements.customerId.value.trim() || null,   // empty becomes null, which the
                                                             // API schema allows
    metadata: { source: "web-console" },   // marks tickets created from here
  };
  const ticket = await request("/tickets", { method: "POST", body: JSON.stringify(payload) });
  logEvent("Ticket saved", ticket);
  await refreshTickets();
  setSelectedTicket(ticket.id);      // select it immediately, so the analysis buttons work
}

async function refreshTickets() {
  state.tickets = await request("/tickets", { method: "GET" });
  renderTickets();
  logEvent("Tickets loaded", { count: state.tickets.length });
}

// ANALYSIS PATH 2: call the AI and WAIT. The page will sit here for a few
// seconds against a real provider.
async function runSyncAnalysis() {
  if (!state.selectedTicketId) {
    // Thrown rather than shown directly — bindAction catches it and logs it, so
    // every action reports failures the same way.
    throw new Error("Select a ticket first.");
  }
  const recommendation = await request(
    `/tickets/${state.selectedTicketId}/ai-analysis`,
    { method: "POST" },
  );
  logEvent("Sync analysis saved", recommendation);
  await refreshRecommendations();
  setSelectedRecommendation(recommendation.id);   // ready to approve
}

// ANALYSIS PATH 3: queue it and return immediately.
//
// Note there is NO automatic polling here — you press "Refresh runs" yourself to
// see the status change. A real UI would poll on a timer; leaving it manual
// makes the asynchronous behaviour visible rather than hiding it, which is
// exactly what you want from a teaching console.
async function queueAnalysis() {
  if (!state.selectedTicketId) {
    throw new Error("Select a ticket first.");
  }
  const run = await request(`/tickets/${state.selectedTicketId}/analyze`, { method: "POST" });
  logEvent("Analysis queued", run);
  await refreshRuns();
}

// Both refresh functions guard against no ticket being selected, clearing their
// list rather than requesting a URL with "null" in it.
async function refreshRecommendations() {
  if (!state.selectedTicketId) {
    state.recommendations = [];
    renderRecommendations();
    return;
  }
  state.recommendations = await request(
    `/tickets/${state.selectedTicketId}/recommendations`,
    { method: "GET" },
  );
  renderRecommendations();
  logEvent("Recommendations loaded", { count: state.recommendations.length });
}

async function refreshRuns() {
  if (!state.selectedTicketId) {
    state.runs = [];
    renderRuns();
    return;
  }
  state.runs = await request(`/tickets/${state.selectedTicketId}/analysis`, { method: "GET" });
  renderRuns();
  logEvent("Analysis runs loaded", { count: state.runs.length });
}

// The human approval step — the safety mechanism at the heart of the product.
//
// The console only supports "approved". Rejecting or editing would need extra
// form fields for the edited text; this is the minimum needed to demonstrate the
// flow and produce data for the metrics.
async function approveRecommendation() {
  if (!state.selectedTicketId || !state.selectedRecommendationId) {
    throw new Error("Select a ticket and recommendation first.");
  }
  const review = await request(
    `/tickets/${state.selectedTicketId}/recommendations/${state.selectedRecommendationId}/reviews`,
    { method: "POST", body: JSON.stringify({ decision: "approved" }) },
  );
  logEvent("Recommendation approved", review);
}

async function createPolicy() {
  const payload = {
    // A timestamp is appended because policy names must be unique per company
    // (the constraint in models.py). Without it, saving twice would fail with a
    // duplicate-key error — correct, but unhelpful in a console you are poking at.
    name: `${elements.policyName.value.trim()} ${Date.now()}`,
    content: elements.policyContent.value.trim(),
  };
  // NOTE THE THIRD ARGUMENT: "lead". Creating a policy requires the lead or admin
  // role (POLICY_WRITE_ROLES in dependencies.py), and the console usually runs as
  // an agent — so this one call overrides the role rather than making you change
  // the dropdown and change it back.
  const policy = await request("/policies", { method: "POST", body: JSON.stringify(payload) }, "lead");
  logEvent("Policy saved", policy);
  await refreshPolicies();
}

async function refreshPolicies() {
  state.policies = await request("/policies", { method: "GET" });
  renderPolicies();
  logEvent("Policies loaded", { count: state.policies.length });
}

// Loads all five metrics endpoints AT ONCE.
//
// `Promise.all` runs them in parallel rather than one after another. Five
// sequential requests would take five times as long for no reason — none of them
// depends on another. The array destructuring on the left unpacks the results in
// the same order they were requested.
//
// The trade-off: if ANY of the five fails, the whole thing fails and no metrics
// appear. Acceptable here, where they are all read together anyway.
async function loadMetrics() {
  const [reviewMetrics, costMetrics, pilotMetrics, pilotFeedback, runtimeMetrics] = await Promise.all([
    request("/metrics/reviews", { method: "GET" }),
    request("/metrics/costs", { method: "GET" }),
    request("/metrics/pilot", { method: "GET" }),
    request("/metrics/pilot/feedback", { method: "GET" }),
    request("/metrics/runtime", { method: "GET" }),
  ]);
  renderMetrics(reviewMetrics, costMetrics, pilotMetrics, pilotFeedback, runtimeMetrics);
  logEvent("Metrics loaded", { reviewMetrics, costMetrics, pilotMetrics, pilotFeedback });
}

// Connects a button to an action, with error handling built in.
//
// THE VALUE OF THIS SMALL FUNCTION: the try/catch is written ONCE here rather
// than inside all eleven action functions. That is why the actions above can
// simply `throw` when something is wrong — the error always ends up in the event
// log, and an unhandled failure can never leave the console silently doing
// nothing.
function bindAction(id, action) {
  document.getElementById(id).addEventListener("click", async () => {
    try {
      await action();
    } catch (error) {
      logEvent("Action failed", error.message);
    }
  });
}

// The tab switching. Plain CSS classes: remove "active" from everything, then
// add it to the clicked tab and its panel.
//
// `tab.dataset.tab` reads a `data-tab="..."` attribute from the HTML, which
// holds the ID of the panel this tab controls. That keeps the tab-to-panel
// mapping in the markup rather than duplicated here.
function bindTabs() {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach((itemNode) => itemNode.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach((panel) => panel.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById(tab.dataset.tab).classList.add("active");
    });
  });
}

// Startup. Runs once, on the last line of this file.
function initialize() {
  // Guesses the API address from wherever this page is served, on port 8765 —
  // the port the API is published on in docker-compose.yml. So the console
  // usually works with no configuration at all.
  const defaultApiUrl = `${window.location.protocol}//${window.location.hostname}:8765`;
  // A previously saved address wins over the guess, so a custom setting survives
  // a page reload. `localStorage` is the browser's small persistent key-value
  // store.
  elements.apiBaseUrl.value = window.localStorage.getItem("supportopsApiBaseUrl") || defaultApiUrl;
  elements.externalId.value = `web-${Date.now()}`;
  elements.apiBaseUrl.addEventListener("change", () => {
    window.localStorage.setItem("supportopsApiBaseUrl", elements.apiBaseUrl.value.trim());
  });

  bindTabs();
  // Every button, wired to its action. The IDs must match those in index.html —
  // a mismatch throws immediately here, at startup, rather than producing a
  // button that silently does nothing when clicked.
  bindAction("checkHealthButton", checkHealth);
  bindAction("createTicketButton", createTicket);
  bindAction("refreshTicketsButton", refreshTickets);
  bindAction("syncAnalysisButton", runSyncAnalysis);
  bindAction("queueAnalysisButton", queueAnalysis);
  bindAction("refreshRecommendationsButton", refreshRecommendations);
  bindAction("refreshRunsButton", refreshRuns);
  bindAction("approveButton", approveRecommendation);
  bindAction("createPolicyButton", createPolicy);
  bindAction("refreshPoliciesButton", refreshPolicies);
  bindAction("loadMetricsButton", loadMetrics);

  // Draw the empty lists, so the page shows "No tickets loaded." rather than
  // blank space before anything is fetched.
  renderTickets();
  renderRecommendations();
  renderRuns();
  renderPolicies();
  logEvent("Console ready", { apiBaseUrl: apiBaseUrl() });
}

// Runs on load. No DOMContentLoaded wrapper is needed because index.html loads
// this script at the END of the body, by which point every element exists.
initialize();
