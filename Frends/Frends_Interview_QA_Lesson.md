# Frends Integration Interview — Complete Q&A Lesson (Memory-Optimized)

**How to use this file**
- Every item is a **question → simple answer → memory cue**.
- Read the answer, cover it, say it aloud, check. Learn the **cue** first — it pulls the whole answer back.
- Keep the one story in your head and reuse it everywhere:
  **Order Portal (REST + JSON) → Frends (check, map, transform) → Legacy ERP (SOAP + XML).**
- Answer shape for ANY question: **What → Why → Example → What can fail + fix.**

**Master cues (learn these 12 lines and half the interview is done):**
| Area | Cue |
|---|---|
| New integration | Ask → Agree → Design → Build → Prove → Release → Run → Improve |
| Middleware | Receive → Check → Change → Send → Track |
| Security | Connection → Identity → Permission → Input → Operations |
| OpenAPI | Info → Servers → Paths → Models → Security |
| JSON check | Syntax → Shape → Business → Outside data |
| XML family | XML holds · XSD checks · XPath finds · XSLT changes · WSDL describes · SOAP carries |
| SOAP | Envelope → Header → Body → Fault |
| Frends | Define → Deploy → Run → Observe |
| Errors | Data → Access → Temporary → Unknown → Internal |
| Timeout | Result unknown → find by ID → retry only if duplicate-safe → reconcile |
| Retry | Transient + duplicate-safe + bounded → else don't |
| Incident | Impact → Stop → Find → Fix → Check → Learn |

---

# SECTION 1 — SDLC & DELIVERY (the process view)

**Q1. What is SDLC?**
The full life of a software change: from idea, through build and test, to release, support, and improvement. *Cue: Plan → Design → Build → Test → Release → Support (a loop).*

**Q2. Waterfall vs Agile vs DevOps?**
Waterfall = big steps in order (good for stable/regulated work). Agile = small deliveries + frequent feedback. DevOps = adds automated release, monitoring, shared ops ownership. Most teams mix them. *Cue: big-steps / small-feedback / automate-and-own.*

**Q3. How do you take a new integration to production?**
Eight steps: **Ask** the goal/owners/success → **Agree** the contract/samples/mapping/error rules → **Design** flow/timeout/retry/idempotency/logging → **Build** a thin happy path then add failures → **Prove** with normal + invalid + duplicate + timeout + security + UAT tests → **Release** with right config/secrets/smoke test/rollback → **Run** with logs/alerts/runbook/replay → **Improve** by fixing root causes. *Cue: Ask–Agree–Design–Build–Prove–Release–Run–Improve.*

**Q4. What do you gather BEFORE designing?**
Business goal, system owners, trigger type, contract + sample messages, field mapping, volume/size/speed/SLA, security + sensitive data, error/duplicate behavior, and success criteria. *Cue: owners, data, security, scale, failure.*

**Q5. New project vs a change to an existing integration?**
New project = create owners, contracts, environments, security, release path, monitoring. Change = do impact analysis: who uses the contract, is it backward compatible, in-flight messages, new version needed, regression tests. *Cue: build-the-rails vs check-who-breaks.*

**Q6. Backward-compatible vs breaking change?**
Safe: add optional response field, add optional request field with default, add a new endpoint. Breaking: rename/remove/retype a field, make an optional field required, change enum/error meaning, change auth. **Rule: prefer optional additions; version breaking changes.** *Cue: add = safe, change/remove = break.*

**Q7. Requirements change mid-build — what do you do?**
Confirm the reason and impact, update contract/mapping/tests/estimate/acceptance, tell all owners. Never hide a contract change inside the Process. *Cue: confirm → update → communicate → no hidden change.*

**Q8. A defect is found in UAT — what do you do?**
Reproduce with the same input/environment, decide if it's code/config/data/permission/unclear-requirement, fix the cause, add a regression test, redeploy the normal way, ask the user to retest. *Cue: reproduce → classify → fix cause → regression → retest.*

**Q9. When is an integration "Done"?**
Contract + acceptance approved; security/validation/mapping/errors work; normal + negative + recovery + UAT pass; every environment configured; deploy/smoke/rollback/replay exist; logs/metrics/alerts useful; support owner + runbook exist. *Cue: contract, tests, config, release, monitoring, owner.*

---

# SECTION 2 — MIDDLEWARE & ARCHITECTURE (the big-picture view)

**Q10. What is middleware?**
Software that sits between systems so they can talk despite different protocol, format, security, or timing. *Cue: Receive → Check → Change → Send → Track.*

**Q11. Why use middleware instead of connecting systems directly?**
Reduces coupling; gives one place for protocol change (REST↔SOAP), transformation (JSON↔XML), security, orchestration, failure recovery, and visibility. One system can change with less effect on the other. *Cue: one place for change, safety, and sight.*

**Q12. There are two meanings of "middleware" — what are they?**
(a) *Integration middleware* = between systems (Frends). (b) *ASP.NET Core middleware* = an ordered HTTP pipeline inside one app (error → logging → authN → authZ → rate limit → endpoint). *Cue: between-systems vs inside-one-app.*

**Q13. Orchestration vs choreography?**
Orchestration = one central Process controls the order of steps (Frends is strong here; risk = big central dependency). Choreography = services react to events with no controller (less coupling, harder to reason end-to-end). *Cue: conductor vs dancers.*

**Q14. Synchronous vs asynchronous integration?**
Sync = caller waits for the final result (use for fast, reliable work; risk = slow target blocks caller). Async = accept now, finish later, return **202** + status/callback (use for slow/unreliable work; you must add status, monitoring, reconciliation). *Cue: wait vs accept-and-follow-up.*

**Q15. When do you choose async (202) over sync?**
When work is slow or variable, the target is sometimes down, a queue/durable store is needed, or the caller doesn't need the answer immediately. **Rule: sync only if the whole path fits the deadline.** *Cue: won't-fit-the-deadline → 202.*

---

# SECTION 3 — HTTP & REST (the protocol view)

**Q16. What is in an HTTP request and response?**
Request = method + URL + headers + optional body. Response = status code + headers + optional body. *Cue: verb-address-headers-body / status-headers-body.*

**Q17. What do GET/POST/PUT/PATCH/DELETE mean, and which are idempotent?**
GET read (safe, idempotent) · POST create/command (not idempotent) · PUT replace (idempotent) · PATCH partial (maybe) · DELETE remove (idempotent). *Cue: only POST/PATCH aren't safely repeatable.*

**Q18. What does "idempotent" really mean?**
Repeating the same request has the **same intended effect** as doing it once. It does NOT mean the response is identical. *Cue: same effect, not same reply.*

**Q19. What are the status code groups?**
2xx success · 3xx redirect/cache · 4xx caller/request/access problem · 5xx server/dependency problem. *Cue: 2 ok, 4 your fault, 5 their fault.*

**Q20. Explain 200 / 201 / 202 / 204.**
200 done · 201 created (add `Location`) · 202 accepted-not-finished (give status/callback) · 204 success no body. *Cue: done, made, accepted, empty.*

**Q21. Explain 400 / 401 / 403 / 404 / 409 / 415 / 422 / 429.**
400 bad/invalid · 401 authN missing/invalid · 403 known but not allowed · 404 not found · 409 conflict/duplicate · 415 wrong content-type · 422 valid syntax but business rule failed · 429 rate limited (honor `Retry-After`). *Cue: bad, who-are-you, not-allowed, missing, clash, wrong-format, bad-meaning, slow-down.*

**Q22. Explain 500 / 502 / 503 / 504.**
500 unexpected server error · 502 bad response from upstream · 503 temporarily unavailable · 504 upstream timed out (write result may be unknown). *Cue: crash, bad-upstream, down, upstream-slow.*

**Q23. First thing to ask when you see an error code?**
Which system returned it — caller ← gateway ← Frends ← target. The fix depends on the layer. *Cue: whose code is this?*

**Q24. Which important headers do you use and why?**
`Authorization` (token) · `Content-Type` (body format) · `Accept` (wanted format) · `X-Correlation-ID` (trace one attempt) · `Idempotency-Key` (stop duplicates) · `Retry-After` (when to try again) · `Location` (new/status resource). **Never log the Authorization header.** *Cue: who, what-format, want-format, trace, dedupe, wait, where.*

**Q25. REST vs SOAP?**
REST = HTTP methods/URLs, usually JSON, described by OpenAPI. SOAP = XML Envelope/Header/Body/Fault, described by WSDL + XSD, can use WS-* features. Neither is always better — choose by existing contract, security, tooling, transactions. *Cue: HTTP-JSON-OpenAPI vs XML-WSDL-XSD.*

---

# SECTION 4 — API SECURITY (the safety view)

**Q26. How do you secure an API?**
In layers: **Connection** (HTTPS/mTLS) → **Identity** (authenticate the caller) → **Permission** (authorize the exact action + record, least privilege) → **Input** (validate everything, treat as untrusted) → **Operations** (rate limits, timeouts, secrets in a vault, safe errors, safe logs, monitoring). *Cue: Connection–Identity–Permission–Input–Operations.*

**Q27. Authentication vs authorization?**
AuthN = who are you (401 if missing/invalid). AuthZ = what may you do (403 if not allowed). Badge proves identity; still may not open the server room. *Cue: who vs what.*

**Q28. Explain the OAuth2 client-credentials flow.**
Service-to-service: client sends id + secret to the identity provider → gets a short-lived access token → calls the API with `Authorization: Bearer <token>` → API validates token + checks scope. Secret goes to the identity provider, NOT the business API. Represents an app, not a user. *Cue: secret→IdP→token→bearer→scope.*

**Q29. Should you get a new token per call?**
No. Cache the token until just before expiry and reuse it. Never log the token. *Cue: cache, don't spam.*

**Q30. What do you validate in a JWT?**
Five checks: who **signed** it (signature + allowed algorithm + trusted keys/JWKS), who **issued** it, who it's **for** (audience), is it **current** (expiry/not-before), what it **may do** (scope/role). **Decoding ≠ validating.** *Cue: signed, issued, for, current, may-do.*

**Q31. JWT vs OAuth — what's the difference?**
JWT is a token *format*. OAuth is an authorization *framework*. OAuth tokens may be JWT or opaque strings. *Cue: format vs framework.*

**Q32. Does the OpenAPI security section secure the API?**
No. OpenAPI *describes* the requirement. The gateway / Frends API Policy / Process *enforce* it, and tests *prove* it. *Cue: describe → enforce → prove.*

**Q33. What is CORS, and is it security?**
A browser rule about which web origins may call the API from browser code. It is NOT authentication — a server-to-server client is not protected by it. *Cue: browser-origin rule, not auth.*

**Q34. What is object-level authorization?**
Even with a valid token, a caller allowed `GET /orders/{id}` must not see another customer's order. Check ownership, not just identity. *Cue: your token ≠ everyone's data.*

**Q35. API key vs OAuth token vs mTLS?**
API key = simple shared secret, weak identity. OAuth token = short-lived identity + permissions (validate it). mTLS = both sides prove certificates (needs ownership + renewal). Always use HTTPS. *Cue: shared-secret / short-lived / certificate.*

**Q36. What must never appear in logs or URLs?**
Secrets, tokens, Authorization headers, private keys, connection strings, unnecessary personal data. URLs get logged, so keep them clean too. *Cue: no secrets in logs or links.*

**Q37. Which security tests do you run?**
No token, invalid token, expired token, wrong issuer/audience, missing scope/role, another user's record, wrong method/content-type, oversized/malformed body, too many requests, and check error/log redaction. *Cue: every bad-auth + bad-input + abuse case.*

---

# SECTION 5 — OPENAPI / YAML / JSON (the contract view)

**Q38. What is OpenAPI, and what is Swagger?**
OpenAPI = machine-readable HTTP API contract (URLs, methods, inputs, responses, schemas, security). Swagger = the old spec name + today's tool names (Swagger UI/Editor). People say "Swagger file" meaning OpenAPI. *Cue: contract; Swagger = old name + tools.*

**Q39. What are the main parts of an OpenAPI file?**
**Info → Servers → Paths → Models(components) → Security.** Operation has summary/operationId/parameters/requestBody/responses/security. Schema has type/properties/required/items/enum/limits/$ref. *Cue: Info–Servers–Paths–Models–Security.*

**Q40. YAML vs JSON for OpenAPI?**
Same model, two formats. YAML = indentation, spaces-not-tabs, quote ambiguous values, allows comments. JSON = braces/quotes/commas, no comments. `.yml` = `.yaml`. *Cue: same content, different clothes.*

**Q41. RAML? RML?**
RAML = a different API-description language (also YAML-based, not interchangeable with OpenAPI). RML usually = RDF Mapping Language — ask the interviewer which they mean. *Cue: RAML ≠ OpenAPI; RML → ask.*

**Q42. Where do headers go in OpenAPI?**
Auth headers → `securitySchemes` (not a normal parameter). Normal request headers (e.g. `X-Correlation-ID`) → operation `parameters`. Response headers → `responses → status → headers`. *Cue: auth=scheme, request=param, response=under-response.*

**Q43. What do the OpenAPI security combinations mean?**
Two entries in the security list = **OR** (either works). Two schemes in one entry = **AND** (both needed). `security: []` on an operation removes the *documented* requirement (runtime policy may still enforce). *Cue: separate=OR, together=AND.*

**Q44. How do you validate required JSON fields?**
Four layers: **Syntax** (valid JSON, content-type, size) → **Shape** (required fields, nested required, types, limits, enum, unknown-field rule) → **Business** (amount>0, dates, allowed values) → **Outside data** (customer exists, product active, caller allowed, not already done). *Cue: Syntax–Shape–Business–Outside.*

**Q45. Difference between `properties` and `required`?**
`properties` *describes* possible fields. The parent's `required` array *makes* selected fields mandatory. Each nested object needs its own `required`. *Cue: describe vs demand.*

**Q46. Missing vs null vs empty?**
Missing = field not present. Null = present but no value. Empty = present but `""`. Required means *present*, not *non-null*; use `minLength: 1` to block empty strings; OpenAPI 3.0 allows null only with `nullable: true`. *Cue: not-there / there-but-null / there-but-blank.*

**Q47. What does `additionalProperties: false` do — and its risk?**
Rejects unknown fields. Risk: it can break forward-compatible additions from producers. Choose strictness on purpose. *Cue: strict, but may break the future.*

**Q48. Is deserializing JSON into a .NET object "validation"?**
No. Parsing/mapping to an object is not full validation — you still need required-field, type, business-rule, and permission checks. *Cue: object built ≠ request valid.*

**Q49. What does a safe validation error look like?**
Status + correlationId + field-level errors (path, code, message). No stack traces, SQL, or secrets. *Cue: helpful fields, zero internals.*

---

# SECTION 6 — XML / XSD / XPATH / XSLT (the data-transform view)

**Q50. One line for each of XML/XSD/XPath/XSLT/WSDL/SOAP?**
XML holds data · XSD checks rules · XPath finds values · XSLT changes structure · WSDL describes the service · SOAP carries the message. *Cue: holds-checks-finds-changes-describes-carries.*

**Q51. Well-formed vs valid XML?**
Well-formed = correct syntax (tags match, one root, quoted attributes). Valid = well-formed AND follows its XSD. *Cue: syntax vs syntax+rules.*

**Q52. What can an XSD define — and not check?**
Defines: elements/attributes, data types, child order (`sequence`), `choice`, `minOccurs`/`maxOccurs`, restriction/enum/pattern, namespace (`targetNamespace`), nil (`nillable`). Cannot prove a real customer exists — that's a business/reference check. *Cue: structure + values, not real-world facts.*

**Q53. What is XPath, and its #1 interview trap?**
XPath addresses XML nodes: `/` exact path, `//` descendants, `@` attribute, `[...]` condition. **Trap: it returns nothing because the XML uses a namespace but the namespace URI wasn't bound to a prefix in the XPath.** *Cue: empty result → check namespace.*

**Q54. What is XSLT and when do you use it?**
A declarative transform (XML → XML/text/HTML) using templates + XPath. Use for repeatable, schema-driven XML mappings. Test namespaces, optional/missing/repeated elements, dates/decimals, encoding, and validate the output against the target XSD. *Cue: template-driven reshape.*

**Q55. One-line difference: XSD vs XPath vs XSLT?**
XSD: "Is this XML allowed?" XPath: "Where is the value?" XSLT: "What should this XML become?" Validate / select / transform. *Cue: allowed? where? become?*

**Q56. Missing vs empty vs nil in XML?**
Missing = no element. Empty = `<Name/>`. Nil = explicitly no value (`xsi:nil="true"`, needs the xsi namespace + XSD `nillable="true"`). *Cue: gone / blank / marked-empty.*

**Q57. What are XML namespaces, and what identifies them?**
They prevent name collisions. The **URI** is the identity; the prefix (`ord:`, `a:`) is just a short alias — two prefixes can mean the same namespace. *Cue: URI is real, prefix is nickname.*

**Q58. How do you keep XML parsing safe?**
Disable unsafe DTD/external-entity processing (prevents XXE), limit size/time, validate the schema, and don't log sensitive payloads. *Cue: no external entities, bound size, validate, redact.*

---

# SECTION 7 — SOAP & WSDL (the enterprise-service view)

**Q59. What are the parts of a SOAP message?**
**Envelope** (required root) → **Header** (optional metadata/security/correlation) → **Body** (business payload) → **Fault** (standard error inside the Body). *Cue: Envelope–Header–Body–Fault.*

**Q60. SOAP Header vs HTTP header?**
SOAP Header is inside the XML message. HTTP header is transport metadata on the request. Different things. *Cue: inside-XML vs on-the-wire.*

**Q61. WSDL vs XSD?**
WSDL describes the *service*: types, messages, operations, binding, endpoint address. XSD describes the *data types* in the messages. *Cue: WSDL=service, XSD=data.*

**Q62. SOAP 1.1 vs 1.2?**
1.1 = `text/xml` + `SOAPAction` HTTP header. 1.2 = `application/soap+xml` (action in the content-type). Different Envelope namespaces. **Follow the WSDL.** *Cue: text/xml+SOAPAction vs soap+xml.*

**Q63. When calling a SOAP service, what do you always check?**
Correct WSDL operation + binding, SOAP version, endpoint, content-type, `SOAPAction`/WS-Security if required, namespace-correct envelope, finite timeout + correlation, and parse **both** HTTP status and SOAP Fault. *Cue: right op, right version, both errors.*

---

# SECTION 8 — RELIABILITY & FAILURE (the resilience view)

**Q64. What are the five error groups?**
**Data** (bad field/XML → correct it) · **Access** (bad token/role → fix identity/permission) · **Temporary** (short outage → retry if safe) · **Unknown** (timeout after send → check target first) · **Internal** (bad mapping/config/code → investigate). *Cue: Data–Access–Temporary–Unknown–Internal.*

**Q65. When is it safe to retry?**
Only when ALL are true: failure plausibly transient, operation idempotent/duplicate-safe, attempts + delay bounded, total time fits the deadline, and retrying won't amplify overload. *Cue: transient + safe + bounded + in-time + gentle.*

**Q66. What must you NEVER retry?**
Bad input, bad credentials, missing permission, permanent business rejection, and a timed-out write with unknown result. *Cue: don't repeat "your fault" or "unknown write".*

**Q67. What is exponential backoff with jitter?**
Wait longer after each failure (exponential) and add small randomness (jitter) so many workers don't retry at the same instant and overload a recovering system. Honor `Retry-After`. *Cue: wait-more + random spread.*

**Q68. What is a circuit breaker?**
It stops calls to a failing target for a while so both sides recover; states are closed → open → half-open probe. It is NOT a retry mechanism. *Cue: pause the calls, not repeat them.*

**Q69. Why is a timeout ambiguous, and what do you do?**
A timeout only means "no answer in time" — the server may have succeeded and lost the response. So: stop blind retries, search the target by order/idempotency key, record success if found, retry only if duplicate work is impossible, then reconcile. *Cue: unknown → look-up before resend.*

**Q70. What is idempotency and how do you implement it?**
Duplicate protection for one logical operation. Receive a stable key → atomically create a durable record with a unique constraint → if the same key completed, return the stored result → if in progress, return 202/status → forward the same key downstream → record the final outcome. Same key + *different* content = **409**. *Cue: one key, one effect, replay the result.*

**Q71. Correlation ID vs idempotency key?**
Correlation ID = ties telemetry/logs for one end-to-end attempt. Idempotency key = identifies one logical business operation across repeated attempts. *Cue: trace-the-attempt vs identify-the-operation.*

**Q72. What is a dead-letter queue / quarantine?**
A place for messages that exhausted retries or are deterministically bad. Don't retry-loop them; store context (key, correlation, redacted error, attempts), fix the cause, replay in a controlled way. *Cue: park the poison, fix, replay.*

**Q73. What is reconciliation?**
Comparing expected business state across systems (source vs target counts/totals). It catches lost responses, silent omissions, duplicates, and partial completion that "technical success" misses. *Cue: do the numbers match?*

**Q74. Can distributed systems guarantee exactly-once?**
Rarely across independent systems. Practical design = at-least-once delivery + idempotent consumers + unique keys + checkpoints + reconciliation. *Cue: aim for effectively-once, not exactly-once.*

**Q75. What is the outbox pattern?**
A DB transaction can't atomically include an unrelated HTTP call. So commit the business change AND an outbound-event row in one transaction, then publish the event separately and idempotently. *Cue: save data + event together, send later.*

**Q76. Why not hold a DB transaction open during an HTTP call?**
Network latency is unbounded; open transactions hold locks/connections and cause blocking/deadlocks. Commit short local state, call out, then update or reconcile. *Cue: short transaction, then call.*

---

# SECTION 9 — INTEGRATION PATTERNS (the design-choice view)

**Q77. Name the main integration patterns and their key risk.**
Request-response (coupled latency) · Queue/message (duplicates, backlog → DLQ) · Webhook (duplicate/out-of-order → verify signature, dedupe) · Polling (delay → watermark, overlap) · Schedule (missed/duplicate runs → missing-run alert, timezone) · File/batch (partial rows → control totals, quarantine) · Pub-sub (schema/order/lag → versioned events) · Passthrough/proxy (extra hop → policy only). *Cue: sync, queue, push, pull, clock, file, broadcast, relay.*

**Q78. Queue vs synchronous API — when?**
Sync = short work needing an immediate result. Queue = buffering, load smoothing, dependency isolation, independent retry when eventual completion is OK. *Cue: need-answer-now vs can-wait-and-buffer.*

**Q79. Webhook vs polling — when?**
Webhook when the source can push reliably (verify signature + timestamp, dedupe, block replay). Poll with a durable watermark + small overlap + dedupe when it can't push. *Cue: push-if-you-can, poll-if-you-must.*

**Q80. How do you process a large file or table safely?**
Deterministic pagination (`WHERE Id > @LastId ORDER BY Id`), bounded batches + bounded concurrency, per-item outcomes, advance the checkpoint only after success, quarantine poison rows, continue independent rows, then reconcile counts/totals. Don't `Split(',')` CSV or log whole payloads. *Cue: page, batch, checkpoint, quarantine, reconcile.*

**Q81. How do you handle dates, decimals, and CSV at boundaries?**
Dates = ISO 8601 + `DateTimeOffset`/explicit UTC, never treat unspecified local as UTC. Money = `decimal`, carry currency separately, define rounding, avoid culture-dependent parsing. CSV = define delimiter/quoting/encoding/header, use a real parser, keep row numbers for errors. *Cue: ISO dates, decimal money, real CSV parser.*

---

# SECTION 10 — FRENDS ARCHITECTURE (the platform view)

**Q82. What is Frends?**
A low-code integration platform: you build visual Processes that connect APIs, files, databases, messages, and systems. Low-code still needs real engineering (contracts, security, tests, monitoring). *Cue: visual integration, real engineering.*

**Q83. What is the Frends hierarchy?**
**Tenant → Environment (DEV/TEST/UAT/PROD) → Agent Group → Agent(s).** Processes deploy to an **Agent Group**, not a single Agent. *Cue: tenant-env-group-agent.*

**Q84. Tenant, Environment, Agent Group, Agent — define each.**
Tenant = central place to develop/administer/deploy/monitor. Environment = lifecycle boundary with its own Environment Variables. Agent Group = deployment/execution target (its Agents share deployed versions). Agent = runtime that registers active Triggers and runs compiled Processes. *Cue: control-panel / lifecycle / target / runtime.*

**Q85. How does a Process actually run?**
An active Trigger is registered by an Agent → its event starts one Process Instance → the Agent runs the compiled Process in the .NET runtime → results/failures go to Instance logging per configured level. Processes are modeled in BPMN + C# and compile to .NET. *Cue: trigger→instance→agent runs .NET.*

**Q86. Process vs Subprocess?**
Process = the externally/automatically started boundary; begins with a Trigger, ends in Return/Throw. Subprocess = reusable internal orchestration with a Manual Trigger defining its interface; gets its own Instance but the **caller waits** (not a concurrency tool). *Cue: outer-flow vs reusable-inner-flow-you-wait-for.*

**Q87. Standard Task vs Code Task vs Custom Task vs external service?**
Standard Task = supported packaged action (output via `#result`). Code Task = small in-process C# (mapping/filter/calc). Custom Task = reusable tested .NET 8 library packaged as NuGet (must be public, static, return a value, not overloaded). External service = independent lifecycle/scaling/security boundary. *Cue: built-in / inline / packaged / separate.*

**Q88. What Triggers exist in Frends?**
Manual (also the only Subprocess trigger), File, Schedule, Conditional, HTTP (standalone), API (linked to OpenAPI + API Management), Messaging (AMQP/Service Bus/RabbitMQ/Event Hub/TCP). Non-manual triggers must be **active** to fire. *Cue: manual, file, clock, condition, http, api, message.*

**Q89. HTTP Trigger vs API Trigger?**
HTTP Trigger = standalone endpoint, no OpenAPI/API Management (simple internal use). API Trigger = linked to an OpenAPI operation → contract-driven, API Policies, grouped deployment, API monitoring (prefer for governed external APIs). *Cue: bare-endpoint vs governed-contract.*

**Q90. What is an API Policy, and what if there's none?**
The runtime control in front of API operations — identities, paths, methods, Agent Groups, throttling, logging. **No policy ≠ public: access must be explicitly allowed; it fails closed.** *Cue: policy enforces; no policy = locked, not open.*

**Q91. Explain the key Frends references.**
`#trigger` (input/metadata) · `#var` (mutable variables) · `#env` (config, e.g. `#env.CRM.BaseUrl`) · `#result` / `#result[Shape Name]` (task output) · `#process` (env, agent group, version, exec id, cancellation token) · `#var.error` (in Catch). *Cue: trigger, var, env, result, process, error.*

**Q92. Why not read `#result[Shape]` from a branch that might not run?**
That shape may not have executed, so the reference is unreliable. Initialize a `#var` before the branch and assign into it on each path. *Cue: init-before-branch, assign-per-path.*

**Q93. What are the Frends shape categories?**
Events (Trigger, Return, Intermediate Return, Throw, Catch) · Decisions (Exclusive = one path, Inclusive = multiple) · Activities (Task, Call Subprocess, Assign Variable, Code Task, Shared State, DMN) · Scopes (Named, Foreach, While with max-iteration guard) · Sequence Flow · Long-running (checkpoint + resume). *Cue: events, decisions, activities, scopes, flow.*

**Q94. How does Frends do error handling?**
**Catch** handles an exception inside the active flow (map/compensate/record/return/rethrow). An **unhandled-error Subprocess** runs *after* the Process stops — for alerting/cleanup, NOT resume. A Task's **Retry on failure** uses increasing delays — enable only for transient, duplicate-safe ops. Don't turn every error into a "successful" instance. *Cue: Catch=inside, unhandled-sub=after, retry=transient-only.*

**Q95. How does Frends support hybrid integration?**
One tenant can run Frends Cloud Agents and customer-managed Self-Service Agents together, so execution happens near cloud or protected on-prem systems; expose only required network paths; use Environment Variables for target endpoints/credentials. *Cue: run near the system that needs protecting.*

**Q96. How would you design high availability in Frends?**
Multiple Agents in one Agent Group + suitable shared state + load-balancer/gateway design. Watch shared dependencies (they can still be single points of failure). Deploy to the group, not one Agent. Don't keep duplicate-control data only in one Agent's memory. *Cue: many agents, shared state, watch the shared bits.*

---

# SECTION 11 — FRENDS IMPLEMENTATION (the build view)

**Q97. Walk through building the Order Process in Frends.**
API Trigger + Policy → Initialize (correlation id, idempotency key, SHA-256 hash of normalized request) → Validate (collect all errors → 400 Problem) → Claim Order (atomic SQL idempotency) → Get Customer (parameterized SQL: exists/active?) → Map downstream → Get OAuth token → Submit downstream (POST, timeout, same Idempotency-Key + correlation header) → Classify response → Complete/Record Failure (durable) → Return (correlation id in header + body). *Cue: trigger–init–validate–claim–enrich–map–token–send–classify–persist–return.*

**Q98. Why hash the normalized request, and what do you exclude?**
So two logically-equal requests produce the same hash (to detect true duplicates vs conflicts). Normalize first (trim, uppercase currency, UTC timestamp) and **exclude volatile values** like correlation id and current time. *Cue: equal requests, equal hash — no volatile bits.*

**Q99. How do you make the idempotency claim safe against a race?**
Do the check-and-insert in one atomic transaction with locking (`UPDLOCK, HOLDLOCK`) plus a unique constraint as the final defense. A separate "check then insert" lets two concurrent requests both pass. *Cue: atomic claim + unique constraint.*

**Q100. What are the branches after the idempotency claim?**
New row → continue. Same key/hash + completed → return stored result (`replayed:true`), no downstream call. Same key/hash + processing → 202/status. Same key + different hash → 409. Rejected → return stored rejection. *Cue: new/replay/inflight/conflict/rejected.*

**Q101. How do you enrich the customer safely?**
Parameterized query for `ExternalCustomerId` + `IsActive`. One active row → continue; none → 422 not-found; inactive → 422 inactive; multiple rows → data-integrity alert; DB down → retryable → 503. *Cue: parameterized lookup, branch on the result.*

**Q102. How do you handle the OAuth token in the Process?**
Prefer a reusable auth Subprocess or a Task that accepts OAuth config; cache/reuse a valid token until near expiry. Getting one per Process is acceptable only as a time-boxed demo — say so. Never log the secret/token. *Cue: reusable + cached; never logged.*

**Q103. How do you configure the downstream HTTP call?**
POST to `#env...BaseUrl + "/orders"`, JSON body, Bearer token, headers `Idempotency-Key` + `X-Correlation-Id`, finite timeout from `#env`, bounded duplicate-safe transport retries, and **disable HTTP-error-throwing** so you classify statuses yourself. *Cue: same keys forwarded, finite timeout, manual classify.*

**Q104. How do you classify the downstream response?**
2xx → parse+complete · 400/422 → permanent, no retry · 401/403 → identity/scope, alert (≤1 token refresh) · 409 → query idempotent state · 429 → honor Retry-After, bounded delay · 5xx → bounded retry if duplicate-safe · other → unexpected contract. *Cue: ok/permanent/identity/conflict/slow/server/weird.*

**Q105. In a Catch, why can't you read the failed Task's result?**
The Task failed, so its result is unreliable. Use the Catch error context and variables initialized *before* the call; set a safe pre-initialized `Outcome`, update durable state, promote failure category, return a safe 503 or rethrow after recording. *Cue: use error-context + pre-init vars only.*

**Q106. Downstream succeeded but the local DB update failed — what now?**
Don't create a new idempotency key. Record/alert an ambiguous partial-completion, query downstream by order/key (or replay the same key only if its contract is idempotent), and repair local state via reconciliation. *Cue: same key, reconcile — never a new order.*

**Q107. What must you promote — and never promote?**
Promote small, safe, searchable identifiers: OrderId, CorrelationId, Outcome, maybe AttemptCount. **Never promote** secrets, tokens, or personal data — promoted values are logged even when normal logging is suppressed. *Cue: promote IDs, never secrets.*

**Q108. What are the Frends log levels and the redaction tool?**
Only Errors (minimum) / Default (step results with limits) / Everything (inputs/outputs/expressions — temporary investigation only). Use **"Skip logging result and parameters"** on secret-bearing shapes. *Cue: errors/default/everything + skip-secrets.*

---

# SECTION 12 — DEPLOYMENT, OPS & MONITORING (the run view)

**Q109. What is the Frends release path?**
DEV → TEST → UAT → PROD → smoke test → monitor. Deploy referenced Subprocesses first, define all target Environment Variables, deploy an API + its linked Processes as ONE unit, and choose "Deploy" vs "Deploy and activate Triggers" deliberately. *Cue: promote same version, deps first, API+processes together.*

**Q110. How do you roll back safely?**
Deploy the previous known-good version to the Agent Group, confirm trigger state + health, and **reconcile side effects**. Rolling back code does NOT undo an order/payment — that needs a separate compensation step. Use "Switch version" only to continue development from an old definition. *Cue: redeploy known-good + compensate side effects.*

**Q111. What do you check before a production release?**
Correct Process/Subprocess/Task versions, environment values, secret/certificate references, API Policy + Agent Group, network access, trigger state, and rollback steps. *Cue: versions, config, secrets, policy, network, triggers, rollback.*

**Q112. What is a Process Instance?**
One execution of a Process — it records status, duration, results, and step details per the log settings. Promoted values make it searchable. *Cue: one run, fully recorded.*

**Q113. What logs, metrics, and alerts do you keep?**
Logs: correlation id, safe business id, process+version, environment, step/target, status, duration, retry attempt, safe error type. Metrics: request/success/failure count, duration, retries/timeouts, queue backlog, missing runs. Alerts: actionable only. *Cue: trace fields, count/duration/backlog, act-worthy alerts.*

**Q114. How do you detect a scheduled Process that silently never ran?**
A Monitoring Rule on **expected/absent** executions in a time window — a run that never happened has no failed Instance to alert on. Then check trigger activation, schedule/timezone, Agent health, deployment, source availability. *Cue: alert on absence, not just errors.*

**Q115. What are promoted values and Monitoring Rules?**
Promoted values = searchable Instance columns (safe business/correlation/outcome IDs) that can drive rules. Monitoring Rules detect repeated errors, unexpected/missing executions, or excessive duration and can email or trigger a Process. *Cue: searchable IDs + rules that watch them.*

**Q116. How do you choose a production log level?**
Use the minimum needed for operations/privacy/audit. Temporarily raise one Process during an incident, then restore it. Secret-bearing shapes skip parameters/results regardless. *Cue: minimum normally, raise-then-restore in incidents.*

---

# SECTION 13 — TESTING (the proof view)

**Q117. What do you test beyond the happy path?**
Contract, mapping, unit/component, integration, negative, security, performance, recovery (timeout/retry/replay/duplicate), regression, UAT, smoke, reconciliation. *Cue: contract→mapping→negative→security→recovery→UAT→smoke→reconcile.*

**Q118. What does each test layer prove?**
Unit = isolated logic. Contract = matches OpenAPI/WSDL/XSD. Integration = real boundary works. Smoke = deployed critical path alive. Failure = recovery policy works. Reconciliation = business result correct. *Cue: logic / schema / boundary / alive / recovers / correct.*

**Q119. What are the Frends testing tools?**
**Task test** = isolated Task with concrete inputs (no `#trigger`/`#result` context). **Run once** = full saved Process → inspect the Instance. **.NET unit tests** for Custom Tasks. Verify business outcomes + log redaction, not just a green status. *Cue: task-test, run-once, .NET-tests.*

**Q120. How do you compare a new API against an old one?**
Send the **same** request to both; compare status, headers/content-type, body, validation/error format, side effects, duplicate behavior, duration, logs, and final target state. Same input or the comparison is unfair. *Cue: same request, compare everything.*

---

# SECTION 14 — .NET FOR INTEGRATION (the code view)

**Q121. Does `await` create a new thread?**
No. It registers a continuation and frees the thread while async I/O is pending — improving scalability, not making the target faster. *Cue: no thread, just non-blocking wait.*

**Q122. When use `Task.Run`, and what to avoid?**
For genuine CPU-bound work — not to hide synchronous I/O. Avoid `.Result`/`.Wait()` (block threads, risk deadlock) and `async void` (except event handlers). *Cue: CPU-bound only; no .Result.*

**Q123. Why cancellation AND timeout?**
Different concerns: cancellation asks work to stop; a timeout stops waiting after a duration (often implemented via cancellation). Pass a `CancellationToken` through every layer. *Cue: stop-request vs stop-waiting.*

**Q124. Why `IHttpClientFactory`?**
It manages handlers/connections and supports named/typed clients + injection. Don't new/dispose `HttpClient` per request. *Cue: reuse handlers, don't churn clients.*

**Q125. When should you catch an exception?**
Only to add context, translate, recover, or guarantee cleanup — at one ownership boundary. Preserve the stack trace with `throw;` (never `throw ex;`). Don't use exceptions for normal validation. *Cue: add-value or don't catch; `throw;` not `throw ex;`.*

**Q126. `System.Text` vs `System.Text.Json` vs `Newtonsoft.Json`?**
`System.Text` = broad text/encoding namespace. `System.Text.Json` = built-in JSON (fast, default for new work; `JsonDocument`/`JsonNode`). `Newtonsoft.Json` = flexible NuGet library, common in legacy (`JObject`/`JToken`). Defaults differ → **never switch libraries without contract tests.** *Cue: text / built-in-json / legacy-json.*

**Q127. What JSON edge cases do you test?**
Property names + casing, missing vs null, enums, dates/time zones, unknown fields, reference loops, special types, custom converters. *Cue: case, null, enum, date, unknown, loop, converter.*

**Q128. What types for money and time at boundaries?**
`decimal` for money (carry currency separately), `DateTimeOffset`/explicit UTC + ISO 8601 for time, UTF-8 + stable machine formats at system edges. *Cue: decimal money, offset time, ISO+UTF-8.*

---

# SECTION 15 — POWER PLATFORM (the comparison view)

**Q129. What are the main Power Platform parts?**
Power Apps (low-code UIs) · Power Automate (workflow/approvals) · Dataverse (managed business data + security) · Connector (typed actions) · Connection (authenticated instance) · Connection reference (solution binding) · Gateway (on-prem connectivity) · Solution (ALM package) · DLP (connector restrictions). *Cue: apps, flows, data, connectors, gateway, solution, DLP.*

**Q130. Canvas vs model-driven app?**
Canvas = start from the screen/experience, highly customizable, Dataverse + connector sources. Model-driven = start from the Dataverse model, generated data-dense UI. *Cue: screen-first vs data-first.*

**Q131. Connector vs connection vs connection reference?**
Connector = defines service operations. Connection = an authenticated instance. Connection reference = solution metadata binding components to the right target-environment connection. *Cue: definition / login / binding.*

**Q132. Is a Power Platform gateway the same as a Frends Agent?**
No. The gateway mainly provides *connectivity* to on-prem sources. A Frends Agent *executes* Processes. *Cue: connect vs execute.*

**Q133. What do DLP policies do — and not do?**
They restrict which connectors and combinations can be used to reduce accidental data movement. They do NOT replace user/API/data-source authorization. *Cue: limit connectors, not permissions.*

**Q134. How does Dataverse security work?**
Effective access combines license/environment access, security roles, table privileges/access depth, record ownership, teams/sharing, and optional column security. **Sharing the app alone does not grant data access.** *Cue: many layers; app-share ≠ data-access.*

**Q135. Frends vs Power Platform — how do you choose?**
Frends for hybrid/backend integration, APIs, files/DBs, durable orchestration + ops. Power Platform for Microsoft 365/Dynamics, user-facing apps, approvals, Dataverse, citizen dev. They combine: Power App collects → Power Automate approves → Frends integrates to ERP. *Cue: system-integration vs user-apps; use both.*

---

# SECTION 16 — SYSTEM DESIGN SCENARIOS (put it together)

**Q136. Design a REST-to-SOAP order integration end-to-end.**
Expose a contract-first order API in Frends (API Policy auth) → establish correlation + idempotency → validate contract + business rules → atomically claim in SQL → enrich + map → call ERP SOAP with the same idempotency key + finite timeout → classify status **and** Fault → store final result for replay → reconcile ambiguous timeouts/partial completion → structured redacted logs + alerts for failure rate and missing runs. *Cue: secure–correlate–validate–claim–map–call–classify–persist–reconcile–observe.*

**Q137. The ERP call times out — do you retry?**
No immediate resend — the result is unknown. Search the ERP by order/idempotency key; if it exists, record success; retry only if duplicate work is impossible; then reconcile. *Cue: look-up before resend.*

**Q138. It works in DEV but fails (or 401) in UAT — how do you debug?**
Send the same request; compare URL/route, environment variables, secrets/certificate, DNS/firewall/proxy, API Policy/permissions, Process/Task versions, and test data — using the correlation id to compare logs step by step. For 401 specifically: which system returned it, token endpoint, issuer/audience/time, scope/role, can the UAT Agent reach the target, correct version deployed. *Cue: same request → compare env/secret/network/access/version via correlation id.*

**Q139. Postman works but the app fails — why?**
Compare the real method, URL, headers, body/encoding, token, certificate, and proxy/DNS/timeout — one of them differs. *Cue: compare the actual bytes on the wire.*

**Q140. XPath returns nothing on visible XML — checklist?**
Namespace URI + prefix binding, root/full path, case, missing/empty/nil element, SOAP Envelope wrapping, encoding, schema/version change. Fix the path, add a regression test, replay only affected records. *Cue: namespace first, then path/case/wrapper.*

**Q141. A retry storm is overloading a target — what do you do?**
Stop the retries, protect the target (circuit breaker), add a bounded limit + backoff + jitter, honor `Retry-After`, and drain the backlog slowly. *Cue: stop, protect, bound, drain.*

**Q142. A queue keeps redelivering the same message — how do you cope?**
Assume at-least-once delivery: make the consumer idempotent (dedupe by business key), acknowledge only after safe completion, bound retries, move poison messages to a DLQ, and replay after fixing the cause. *Cue: idempotent consumer + DLQ.*

**Q143. Design a scheduled file/batch import.**
Watch for a complete file → validate name/size/encoding → stable file id/checksum → stream + bounded batches → per-row outcomes → checkpoint after success → quarantine bad rows → archive processed files → reconcile control totals → alert on missing scheduled runs. *Cue: complete-file, stream, checkpoint, quarantine, reconcile.*

**Q144. Design for high volume / large payloads.**
Async intake (202 + status), queue for buffering, bounded concurrency tuned to downstream + DB pool + Agent CPU, keyset pagination, streaming (don't load all in memory), don't log full payloads, and monitor backlog/duration. *Cue: accept-fast, buffer, bound, stream, watch backlog.*

**Q145. How would you make an unreliable third-party API safe to depend on?**
Finite timeouts, bounded retry with backoff + jitter, circuit breaker, idempotency keys, cache tokens, treat responses as untrusted input (defensive parsing + contract tests), and reconcile. *Cue: timeout, bound-retry, breaker, idempotent, verify, reconcile.*

---

# SECTION 17 — INCIDENTS & PRODUCTION SUPPORT (the on-call view)

**Q146. What are the incident steps?**
**Impact** (who/what/when) → **Stop damage** (pause unsafe retries/trigger) → **Find** (trace one correlation id) → **Fix** (smallest safe change) → **Check** (smoke test + compare records) → **Learn** (add a test/alert/runbook step). *Cue: Impact–Stop–Find–Fix–Check–Learn.*

**Q147. A request never reaches the Process — checklist?**
URL/method/DNS/network → TLS cert → gateway/API Policy → path/method/Agent Group/API Trigger → Agent health → Process Instances/logs. *Cue: outside-in: network→cert→policy→trigger→agent→logs.*

**Q148. Quick meaning of 401 vs 403 vs 404 in production?**
401 → token/key/cert, issuer, audience, time. 403 → scope/role/policy/record ownership. 404 → environment, base URL, route, API version, method, deployment, trigger. *Cue: identity / permission / address.*

**Q149. 500 vs 502/503/504 in production?**
500 → use correlation id, find the first internal error (null data/mapping/settings/version). 502 → bad upstream response/network. 503 → health/load/maintenance. 504 → upstream time; treat a write result as unknown. *Cue: internal / bad-upstream / down / upstream-slow.*

**Q150. An expired certificate broke a flow — how do you handle it?**
Find the owner, renew safely, verify the trust chain, add an expiry alert. **Never** disable TLS validation as a fix. *Cue: renew + alert, never disable TLS.*

**Q151. Partial success across multiple systems — what do you do?**
Save the completed step, retry only the failed step, compensate if needed, and reconcile. Rolling back code doesn't undo business side effects. *Cue: keep-done, retry-rest, compensate, reconcile.*

---

# SECTION 18 — BEHAVIORAL & CLOSING (the you view)

**Q152. "Tell me about yourself."**
Four parts: current role/experience → systems + integrations you know (REST, SOAP, JSON, XML, low-code) → your main relevant strengths → why this role fits your next step. *Cue: role → systems → strengths → why-this.*

**Q153. "Describe a middleware project you worked on."**
Use STAR + the seven-part order: Problem (which systems/why) → Contract (in/out) → Flow (what Frends did) → Reliability (failure/duplicates) → Security (access) → Operations (find/recover) → Result (real value). Say **I** for your work, **we** for the team; use only real facts and no invented numbers. *Cue: problem-contract-flow-reliability-security-ops-result.*

**Q154. "Why low-code / integration?"**
You enjoy solving problems *between* systems — agreeing contracts, mapping data, handling errors, making flows easy to support. Low-code makes flows visible and speeds common work; API + .NET knowledge covers the technical details. *Cue: love the space between systems.*

**Q155. Good questions to ask the interviewer?**
Which integrations first? How do you review/test Frends changes? How are releases/rollbacks handled? Who supports production? Which security/logging rules are required? What does success in 90 days look like? *Cue: work, process, ops, expectations.*

**Q156. Common mistakes that lose points — name them.**
Long answer before the meaning · only the happy path · "HTTPS = full security" · "OpenAPI secures the API" · retrying every timeout · treating missing/null/empty as same · ignoring XML namespaces · "deserialization = validation" · "deployment done" without checking the target · claiming work you didn't do. *Cue: avoid the ten traps.*

---

# SECTION 19 — DEEP-DIVE / SPECIALIST ANGLES (the "senior probe" view)

## Database & SQL

**Q157. What does ACID mean?**
Atomicity (all-or-nothing) · Consistency (valid state to valid state) · Isolation (concurrent transactions don't corrupt each other) · Durability (committed data survives a crash). *Cue: all-or-nothing, valid, separated, permanent.*

**Q158. Why do indexes help and hurt?**
They speed reads/filters/joins but add cost to writes and storage. Index the actual lookup/filter/join columns, not everything. *Cue: faster reads, slower writes.*

**Q159. Keyset vs offset pagination for large growing tables?**
Offset (`OFFSET/LIMIT`) gets slower and can skip/repeat rows as data changes. Keyset (`WHERE Id > @LastId ORDER BY Id`) is deterministic and stable. Use keyset for big batch reads. *Cue: keyset = stable, offset = drifts.*

**Q160. How do you avoid locks, deadlocks, and pool exhaustion?**
Keep transactions short, never call HTTP inside a transaction, use the right isolation level, open connections late/close early, rely on pooling, and monitor slow queries/locks/deadlocks. *Cue: short transactions, no HTTP inside, pool + monitor.*

**Q161. Zero rows vs a database failure — why care?**
"No customer found" is a valid business result; a connection/timeout error is an infrastructure failure. Handle them differently — don't treat an outage as "not found". *Cue: empty ≠ broken.*

## Messaging & delivery semantics

**Q162. At-most-once vs at-least-once vs exactly-once delivery?**
At-most-once = may lose messages, never duplicates. At-least-once = never loses, may duplicate (most real queues). Exactly-once = rare across systems. **So design idempotent consumers.** *Cue: lose / duplicate / (pretend with idempotency).*

**Q163. How do queues actually redeliver — visibility timeout and ack?**
A consumer receives a message, it's hidden (visibility timeout), and it reappears if not acknowledged in time. Acknowledge only after safe completion; if the worker dies mid-work, the message returns. *Cue: ack after done, or it comes back.*

**Q164. How do you keep message order when it matters?**
Order is not guaranteed by default. Preserve it only when required — partition/group by a business key (session/sequence), or add a version/sequence number and reject out-of-order updates. *Cue: group by key or version the message.*

**Q165. What are competing consumers?**
Multiple workers read from one queue to scale throughput — great for parallelism, but breaks strict ordering and needs idempotency + shared state. *Cue: more workers = more speed, less order.*

## DevOps, CI/CD & source control

**Q166. What does a CI/CD pipeline do for a Custom Task?**
Automates restore → build → test → pack (NuGet) → publish on a tag. It's configuration (YAML: stages/jobs/steps). Keeps releases repeatable and reviewed. *Cue: restore-build-test-pack-publish.*

**Q167. How do you source-control Frends work?**
Custom Task source/tests/project/dependency files + pipeline YAML go in Git. For Process/API artifacts, use Frends version history + Diff/Changelog and the org's approved export/source-control automation. *Cue: code in Git, Processes via version history + export.*

**Q168. What is a release inventory?**
The list that makes a release repeatable: Process/Subprocess + API contract versions, Custom Task NuGet versions, required Environment Variable keys, DB/downstream contract changes, monitoring changes, test evidence + approval, deploy/rollback steps, reprocessing implications. *Cue: everything needed to redo the release exactly.*

**Q169. Why treat configuration as controlled data, and what is separation of duties?**
An undocumented production edit is a hidden risk — version and review config like code. Separation of duties = different people build, review, approve, and operate where risk requires it. *Cue: config is reviewed data; split builder/reviewer/approver/operator.*

## Security threat modeling

**Q170. What is STRIDE?**
A threat checklist: **S**poofing (identity), **T**ampering (data), **R**epudiation (untracked change), **I**nformation disclosure (leaks), **D**enial of service, **E**levation of privilege. Map a control to each. *Cue: Spoof-Tamper-Repudiate-Info-DoS-Elevate.*

**Q171. Give one control for each STRIDE threat in an integration.**
Spoofing → OAuth/cert + short-lived token. Tampering → TLS + validation. Repudiation → named accounts + audit + approvals. Info disclosure → redaction + least-privilege logs. DoS → rate/body/concurrency limits + queues. Elevation → separate identities + minimum DB rights. *Cue: identity, TLS, audit, redact, limit, least-privilege.*

**Q172. What is least privilege, and why a service identity?**
Grant only the scopes/DB rights/folders needed; give each integration a named, non-personal service identity separated by environment. Runtime Processes must never use admin credentials. *Cue: only what's needed, per-integration identity.*

**Q173. How do you rotate secrets safely?**
Track owner/purpose/expiry, alert before expiry, overlap old + new during rotation, verify new before revoking old, and if a secret appears in a log treat it as compromised and rotate immediately. *Cue: overlap, verify, then revoke.*

**Q174. What is SSRF and how do you prevent it?**
Server-Side Request Forgery = tricking your server into calling an attacker-chosen URL. Prevent by not fetching caller-supplied URLs without an allow-list + network egress controls. *Cue: don't call caller-supplied URLs; allow-list.*

**Q175. How do you prevent injection (SQL/XML)?**
Parameterize SQL (never concatenate input), restrict the DB account, allow-list values; for XML disable external entities (XXE) and validate the schema. *Cue: parameterize + allow-list + no external entities.*

## Networking

**Q176. Inbound vs outbound network paths — why check both?**
Inbound: caller → DNS → TLS → gateway/API Policy → API Trigger → Process. Outbound: Process/Agent → DNS → proxy/firewall → TLS → target. An API can accept inbound traffic and still fail outbound. *Cue: two paths — receiving and calling.*

**Q177. What is mTLS and where does it fit?**
Mutual TLS = both sides present certificates to prove identity. It proves *transport* identity but does NOT replace business authorization. Certificates need ownership, renewal, and expiry alerts. *Cue: both-sides certs; still authorize.*

## Caching & concurrency

**Q178. How do you handle concurrent updates safely (optimistic concurrency)?**
Use `ETag` + `If-Match`: the client sends the version it read; if it changed, the server returns **412 Precondition Failed** and the client reloads and retries. Prevents lost updates. *Cue: send the version you read; 412 = reload.*

**Q179. What caching should you use and avoid?**
Cache OAuth tokens until near expiry. Use `Cache-Control`/`304 Not Modified` for cacheable reads; use `Cache-Control: no-store` for sensitive responses. Don't cache stale business-critical data blindly. *Cue: cache tokens + safe reads, never secrets.*

## Data, privacy & observability

**Q180. How do you handle PII and data retention?**
Classify personal/sensitive data, minimize what you store/log, apply retention + deletion policy, never put PII/secrets in URLs/correlation IDs/idempotency keys, and know audit/RTO/RPO requirements. *Cue: classify, minimize, retain-then-delete.*

**Q181. What are RTO and RPO?**
RTO = target time to restore service after an outage. RPO = maximum acceptable data loss (how far back you can lose). They drive backup/replication/failover design. *Cue: how-fast-back vs how-much-lost.*

**Q182. What are the three pillars of observability?**
Logs (what happened, with context) · Metrics (counts, duration, rates, backlog) · Traces (one request across systems via correlation id). Together they let you understand the system from outside. *Cue: logs-metrics-traces.*

**Q183. What is distributed tracing, and how do you get it cheaply?**
Following one request across multiple systems. Propagate a **correlation ID** on every hop and log it everywhere — that lets support reconstruct the full path without a full tracing platform. *Cue: one id, every hop, every log.*

## Frends extras

**Q184. How do you package a Custom Task?**
A method must be **public, static, return a value, not overloaded**; add unit tests, XML documentation, supported metadata, and secret-sensitive parameter attributes; build with `dotnet pack` into a NuGet package and import it. *Cue: public-static-returns; test, doc, pack.*

**Q185. What is the Shared State Task for, and its caution?**
Sharing small state across Agents/runs (e.g. a simple flag/counter). Caution: for real duplicate protection use a durable shared store with atomic claims — don't rely on one Agent's memory. *Cue: shared flag, but not durable idempotency.*

**Q186. What is a DMN Task?**
Decision Model and Notation — a table-driven business-rules decision shape. Use it to keep complex branching rules readable and maintainable instead of nested conditions. *Cue: rules as a table, not spaghetti.*

**Q187. What is a passthrough (proxy) API in Frends?**
An API that proxies to an upstream API with no Process transformation/orchestration — minimal implementation, still can apply policies. Use when there's no logic to add. *Cue: relay only, still policed.*

---

# ONE-PAGE MORNING RECALL
- **Answer shape:** What → Why → Example → Failure + fix.
- **SDLC:** Ask–Agree–Design–Build–Prove–Release–Run–Improve.
- **Middleware:** Receive–Check–Change–Send–Track. Story: Portal REST/JSON → Frends → SOAP/XML ERP.
- **Security:** Connection–Identity–Permission–Input–Operations. *OpenAPI describes; API Policy + Process enforce; tests prove.*
- **OpenAPI:** Info–Servers–Paths–Models–Security. auth=securitySchemes, header=parameters.
- **JSON:** Syntax–Shape–Business–Outside. properties describes, required demands. missing≠null≠empty.
- **XML:** holds–checks–finds–changes–describes–carries. SOAP = Envelope–Header–Body–Fault.
- **Reliability:** retry only transient+duplicate-safe+bounded · timeout=unknown→look-up first · idempotency=one key one effect · reconcile.
- **Frends:** Tenant→Env→Agent Group→Agent. Trigger→Process→Tasks→Instance+logs+promoted values. API Policy enforces; deploy to group; roll back to known-good + compensate.
- **Incident:** Impact–Stop–Find–Fix–Check–Learn.
- **Final:** use real experience, say what *you* did, one safe example, no invented numbers. Sleep.
