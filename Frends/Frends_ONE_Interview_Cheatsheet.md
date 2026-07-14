# Frends Interview — ONE Cheat Sheet (Remember-Fast)

**Use this file only.** It has two parts:
- **PART A — CONCEPTS:** what each thing *means* (simple words). This is what you *say*.
- **PART B — IMPLEMENTATION:** how you *actually build it* in Frends / .NET. This is what you *do*.

Answer every question in this shape: **What → Why → Example → What can fail + fix.**

The one story to reuse for everything:
> **Order Portal (REST + JSON)  →  Frends (validate, map, transform)  →  Legacy ERP (SOAP + XML).**

---

# MEMORY HOOKS (learn these lines first)

| Topic | Hook |
|---|---|
| SDLC / new integration | **Ask → Agree → Design → Build → Prove → Release → Run → Improve** |
| Middleware | **Receive → Check → Change → Send → Track** |
| API security | **Connection → Identity → Permission → Input → Operations** |
| OpenAPI | **Info → Servers → Paths → Models → Security** |
| JSON validation | **Syntax → Shape → Business → Outside data** |
| XML family | **XML holds. XSD checks. XPath finds. XSLT changes. WSDL describes. SOAP carries.** |
| SOAP message | **Envelope → Header → Body → Fault** |
| Frends platform | **Define → Deploy → Run → Observe** |
| Error types | **Data → Access → Temporary → Unknown → Internal** |
| Timeout | **Result is unknown → find by business ID → retry only if duplicate-safe → reconcile** |
| Incident | **Impact → Stop damage → Find → Fix → Check → Learn** |

**Three golden rules that impress interviewers:**
1. **Do not retry every error.** Retry only *temporary* + *duplicate-safe* + *bounded*.
2. **A timeout is unknown, not a failure.** Search the target before resending a write.
3. **OpenAPI/YAML *describes* security. The runtime (API Policy + Process) *enforces* it. Tests *prove* it.**

---

# PART A — CONCEPTS (say these)

## 1. SDLC & a new integration
- **SDLC** = Software Development Life Cycle = full path from idea → live → supported.
- **Waterfall** = big steps in order (stable/regulated work). **Agile** = small deliveries + frequent feedback. **DevOps** = adds automated release, monitoring, shared ops ownership. Most teams mix them.
- New integration in 8 steps: **Ask** (goal, owners, success) → **Agree** (contract, samples, mapping, error rules) → **Design** (sync/async, timeout, retry, idempotency, logging) → **Build** (thin happy path first, then failures) → **Prove** (test normal + invalid + duplicate + timeout + security + UAT) → **Release** (right config/secrets, smoke test, rollback plan) → **Run** (logs, alerts, runbook, replay, reconcile) → **Improve** (fix root cause).
- **Change vs new project:** for a change, do *impact analysis* — who uses the contract, is it backward compatible, in-flight messages, new version needed, regression tests. **Rule: prefer adding optional fields; use a new version for a breaking change.**

## 2. Middleware
- Middleware sits *between* systems so they can talk despite different protocol, format, security, or timing.
- It does: **Receive → Check → Change → Send → Track.**
- Why not connect directly? Reduces coupling; one place for protocol change (REST↔SOAP), transformation (JSON↔XML), security, orchestration, failure recovery, and visibility.
- **Two meanings of "middleware":** (a) *integration middleware* = Frends, between systems. (b) *ASP.NET Core middleware* = ordered HTTP pipeline inside one app (error handler → logging → authN → authZ → rate limit → endpoint). Don't confuse them.

## 3. HTTP & REST
- Request = **method + URL + headers + optional body.** Response = **status + headers + optional body.**
- Methods: **GET** read (safe, idempotent) · **POST** create/command (not idempotent) · **PUT** replace (idempotent) · **PATCH** partial (maybe) · **DELETE** remove (idempotent).
- **Idempotent** = repeating has the *same intended effect*; it does NOT mean the response is identical.
- Status groups: **2xx** success · **4xx** caller/request/access problem · **5xx** server/dependency problem.
- Codes to know cold: **200** ok · **201** created (+`Location`) · **202** accepted-not-finished · **204** no body · **400** bad/invalid · **401** authN missing/invalid · **403** known but not allowed · **404** not found · **409** conflict/duplicate · **415** wrong content-type · **422** semantic/business fail · **429** rate limited (honor `Retry-After`) · **500/502/503/504** server/gateway/unavailable/upstream-timeout.
- **Always ask: which system returned the code?** (caller ← gateway ← Frends ← target).

## 4. API security
- **Layers:** Connection (HTTPS/mTLS) → Identity (authN) → Permission (authZ, least privilege) → Input (treat all input as untrusted) → Operations (rate limit, timeout, secrets in vault, safe logs, monitoring).
- **AuthN vs AuthZ:** authN = *who are you* (401 if missing). authZ = *what may you do* (403 if not allowed). Badge proves identity; still may not open the server room.
- **OAuth2 client credentials** (service-to-service): client sends id+secret to identity provider → gets short-lived token → calls API with `Authorization: Bearer <token>` → API validates token + checks scope. **Secret goes to the identity provider, not the business API.** Cache the token until just before expiry; never per-call, never log it. Represents an *app*, not a user.
- **JWT = 5 checks:** who **signed** it (signature + allowed algorithm + trusted keys/JWKS), who **issued** it, who it's **for** (audience), is it **current** (expiry/not-before), what it **may do** (scope/role). **Decoding ≠ validating.**
- **JWT vs OAuth:** JWT is a token *format*; OAuth is an authorization *framework*. OAuth tokens can be JWT or opaque.
- **CORS** is a *browser* rule about which web origins may call from browser code. It is **not** authentication; server-to-server calls are not protected by it.
- Object-level check: a caller allowed `GET /orders/{id}` must not see *another* customer's order.

## 5. OpenAPI / YAML / JSON / Swagger
- **OpenAPI** = machine-readable HTTP API contract: URLs, methods, inputs, responses, schemas, security. **Swagger** = old spec name + tool names (Swagger UI/Editor). People say "Swagger file" meaning OpenAPI.
- Top level: **Info → Servers → Paths → Models(components) → Security.** Operation: summary, `operationId`, parameters, requestBody, responses, security. Schema: type, properties, required, items, enum, limits, `$ref`.
- **YAML vs JSON** = same model, two formats. YAML: indentation, spaces-not-tabs, quote ambiguous values. JSON: braces/quotes/commas. `.yml`=`.yaml`.
- **RAML** = a *different* API-description language (also YAML-based, not interchangeable). **RML** usually = RDF Mapping Language — ask the interviewer what they mean.
- Frends commonly supports **OpenAPI 3.0.1** (and legacy Swagger 2.0). Confirm tenant version.
- Security in OpenAPI: two list entries = **OR**; two schemes in one entry = **AND**; `security: []` on an operation removes the *documented* requirement (runtime policy may still enforce). Put `Authorization` in `securitySchemes`, normal headers in `parameters`, response headers under `responses→status→headers`.

## 6. JSON validation
- Four layers: **Syntax** (valid JSON, content-type, size) → **Shape** (required fields, nested required, types, limits, enum, unknown-field rule) → **Business** (amount>0, dates, allowed currency) → **Outside data/Reference** (customer exists, product active, caller allowed, order not already done).
- **`properties` describes possible fields; `required` (an array on the parent) makes them mandatory.** Each nested object needs its own `required`.
- **Missing ≠ null ≠ empty.** Required = *present*, not *non-null*. Use `minLength: 1` to block empty strings. OpenAPI 3.0 allows null only with `nullable: true`.
- `additionalProperties: false` rejects unknown fields — but can break forward-compatibility; choose deliberately. `format` and `default` may not be enforced by every validator.
- **Deserializing into a .NET object is NOT full validation.**

## 7. XML family
- **XML** holds hierarchical data, case-sensitive, one root, escaped reserved chars, namespaces. **Well-formed** = correct syntax; **valid** = well-formed + follows its XSD.
- **XSD** = rule book: elements/attributes, types, order (`sequence`), choice, `minOccurs`/`maxOccurs`, restriction/enum/pattern, namespace (`targetNamespace`), nil (`nillable`). It checks structure/values — it can't prove a customer exists.
- **XPath** = address: `/` exact path, `//` descendants, `@` attribute, `[...]` condition. **#1 interview trap: XPath returns nothing because the namespace URI wasn't bound to a prefix.**
- **XSLT** = declarative transform (XML → XML/text/HTML) using templates + XPath. Test namespaces, optional/missing/repeated elements, dates/decimals, encoding, and validate output against target XSD.
- One-liner: *"XSD asks 'is this XML allowed?', XPath asks 'where is the value?', XSLT asks 'what should this become?'"*
- **Missing** (no element) vs **empty** (`<Name/>`) vs **nil** (`xsi:nil="true"`, needs xsi namespace + XSD `nillable="true"`).

## 8. SOAP & WSDL
- **SOAP** = XML messaging protocol (usually over HTTP, not the same as REST). Parts: **Envelope** (required root) → **Header** (optional metadata/security/correlation) → **Body** (business payload) → **Fault** (standard error inside Body).
- **A SOAP Header is inside the XML message; an HTTP header is transport.** Not the same.
- **WSDL** describes the *service*: types(XSD), messages, operations(portType), binding, service/port(address). **XSD** describes the *data*. → *"WSDL describes the service; XSD describes the XML data."*
- SOAP 1.1 = `text/xml` + `SOAPAction` header; SOAP 1.2 = `application/soap+xml`. Different Envelope namespaces. **Follow the WSDL**; check *both* HTTP status and SOAP Fault. WS-Security only if the contract requires it.

## 9. Reliability concepts
- **Timeout** per network call, aligned to the caller's total deadline; inner timeout leaves room for error mapping/cleanup.
- **Retry only when ALL true:** failure plausibly transient · operation idempotent/duplicate-safe · attempts+delay bounded · fits deadline · won't amplify overload. Use **exponential backoff + jitter**; honor `Retry-After`. **Never** retry bad input, bad credentials, missing permission, permanent business rejection, or a timed-out write with unknown result.
- **Idempotency:** stable key → atomic durable claim with unique constraint → same key completed returns stored result → in-progress returns 202/status → same key + *different* content = **409** → forward same key downstream.
- **Circuit breaker** stops calls after repeated failures (states: closed/open/half-open). Protects resources; it is **not** a retry.
- **Unknown outcome:** timeout after send ≠ failure — server may have succeeded and lost the response. Query by business/idempotency key first.
- **Dead-letter/quarantine:** isolate poison/deterministic-bad data with context; don't retry-loop it; controlled replay.
- **Reconciliation:** compare expected business state across systems (catches lost responses, silent omissions, duplicates, partial completion).
- **Exactly-once rarely exists across systems.** Practical = at-least-once delivery + idempotent consumers + unique keys + checkpoints + reconciliation.
- **Outbox pattern:** a DB transaction can't include an unrelated HTTP call — commit business data + an outbound-event row together, then publish separately and idempotently.

## 10. Integration patterns (one line each)
- **Request-response** (need immediate result; coupled) · **Queue** (buffer/isolate; duplicates/backlog → need DLQ) · **Webhook** (source pushes; dedupe + verify signature) · **Polling** (source can't push; watermark + overlap) · **Schedule** (time-based; missing-run alert + timezone) · **File/batch** (bulk; control totals + quarantine) · **Pub-sub** (many consumers; versioned events) · **Passthrough/proxy** (no logic; policy only).
- **Orchestration** = one central Process controls order (Frends is strong here). **Choreography** = services react to events, no controller.
- **Sync only when the whole path fits the deadline;** otherwise persist/enqueue → return **202** → expose status.

## 11. Frends concepts
- Frends = **low-code integration platform**. Visual Processes connect APIs, files, DBs, messages. Low-code ≠ no engineering.
- Hierarchy: **Tenant → Environment (DEV/TEST/UAT/PROD) → Agent Group → Agent(s).** Processes deploy to an **Agent Group**, not one Agent.
- **Agent** = runtime that registers active Triggers and runs compiled Processes (Processes compile to .NET). **Hybrid:** Frends Cloud Agents + customer Self-Service Agents in one tenant → run execution near protected systems.
- Building blocks: **Trigger** starts a **Process**; **Task** = one packaged action; **Code Task** = small in-process C#; **Custom Task** = reusable .NET 8 lib packaged as NuGet; **Subprocess** = reusable flow (Manual Trigger defines its interface, caller *waits* — not concurrency); **Decision** (exclusive/inclusive), **Loop** (Foreach/While with max-iteration guard), **Scope + Catch**, **Return/Throw**.
- **API Trigger vs HTTP Trigger:** API Trigger is linked to an OpenAPI operation + API Management (policy, grouped deploy, monitoring). HTTP Trigger is a standalone endpoint, no contract.
- **API Policy** enforces access (identities, paths, methods, Agent Group, throttling, logging). **No policy ≠ public — access must be explicitly allowed; it fails closed.**
- **Promoted values** = searchable Instance columns that drive Monitoring Rules. **Never promote secrets/tokens/personal data** (they stay logged). **Monitoring Rules** catch repeated errors, *missing* runs, or long duration.

## 12. Power Platform (comparison focus)
- **Power Apps** = low-code UIs (canvas = start from screen; model-driven = start from Dataverse). **Power Automate** = workflow/approvals (cloud flows: automated/instant/scheduled). **Dataverse** = managed business data + security. **Connector** = typed actions; **Connection** = authenticated instance; **Connection reference** = solution binding. **Gateway** = on-prem connectivity (NOT a Frends Agent — Agent *executes*, gateway only *connects*). **Solution** = ALM package (unmanaged in DEV, managed downstream). **DLP** = restricts connector combos (NOT user/API authorization).
- **Choose Frends** for hybrid/backend integration, APIs, files/DBs, durable orchestration + ops. **Choose Power Platform** for Microsoft 365/Dynamics, user-facing apps, approvals, Dataverse, citizen dev. **They combine:** Power App collects order → Power Automate approves → Frends integrates to ERP.

## 13. .NET essentials
- `async`/`await` = non-blocking wait; **does not create a thread**; frees the thread during I/O. Avoid `.Result`/`.Wait()`; avoid `async void` (except event handlers). Pass `CancellationToken` through every layer; use explicit timeouts too.
- `Task.Run` = for CPU-bound work, not to hide I/O.
- **`IHttpClientFactory`** — don't new/dispose `HttpClient` per request.
- Catch an exception only to add context, translate, recover, or guarantee cleanup. Preserve stack trace with `throw;` (not `throw ex;`).
- **`System.Text` ≠ `System.Text.Json`.** `System.Text.Json` (built-in, fast, default for new work; `JsonDocument`/`JsonNode`) vs **Newtonsoft.Json** (NuGet, flexible, common in legacy; `JObject`/`JToken`). Defaults differ → **never switch libraries without contract tests.**
- Money = `decimal`; timestamps = `DateTimeOffset`/explicit UTC; ISO 8601 + UTF-8 at boundaries.
- Parameterized SQL always; short transactions; **never hold a DB transaction open during an HTTP call.**

---

# PART B — IMPLEMENTATION (do these)

## B1. HTTP request/response shape
```http
POST /api/v1/orders HTTP/1.1
Authorization: Bearer eyJ...
Content-Type: application/json
Accept: application/json
X-Correlation-ID: 563885df-...   # traces one attempt across systems
Idempotency-Key: ORD-1001        # suppresses duplicate business effect

{ "orderId":"ORD-1001", "customerId":"CUS-101", "amount":249.95, "currency":"USD" }
```
```http
HTTP/1.1 201 Created
Location: /api/v1/orders/ORD-1001
```
- **Correlation ID** = telemetry for one attempt. **Idempotency key** = one logical business operation across retries. Different jobs.
- Never put secrets/personal data in URLs (URLs get logged).

## B2. Minimal OpenAPI (recognize, don't memorize)
```yaml
openapi: 3.0.1
info: { title: Order API, version: 1.0.0 }
servers: [{ url: https://api.example.com }]
paths:
  /orders:
    post:
      operationId: createOrder
      security: [ { OAuth2: [orders.write] } ]
      parameters:
        - { name: X-Correlation-ID, in: header, required: false, schema: { type: string } }
      requestBody:
        required: true
        content: { application/json: { schema: { $ref: '#/components/schemas/Order' } } }
      responses:
        '202': { description: Accepted }
        '400': { description: Invalid }
        '401': { description: Invalid auth }
        '429':
          description: Too many requests
          headers: { Retry-After: { schema: { type: integer } } }
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows: { clientCredentials: { tokenUrl: https://id.example.com/token, scopes: { orders.write: Submit } } }
  schemas:
    Order:
      type: object
      additionalProperties: false
      required: [orderId, customerId, amount]
      properties:
        orderId:   { type: string, minLength: 1 }
        customerId:{ type: string, minLength: 1 }
        amount:    { type: number, minimum: 0.01 }
```

## B3. Async .NET API client (be ready to explain every line)
```csharp
public sealed record CreateOrderRequest(string OrderId, string CustomerId, decimal Amount, string Currency);

public sealed class OrderClient(HttpClient httpClient)   // DI: injected, factory-managed
{
    public async Task<CreateOrderResponse> CreateAsync(
        CreateOrderRequest request, string token, string correlationId, CancellationToken ct)
    {
        using var msg = new HttpRequestMessage(HttpMethod.Post, "orders")
        { Content = JsonContent.Create(request) };
        msg.Headers.TryAddWithoutValidation("X-Correlation-ID", correlationId);
        msg.Headers.TryAddWithoutValidation("Idempotency-Key", request.OrderId); // duplicate-safe
        using var resp = await httpClient.SendAsync(msg, HttpCompletionOption.ResponseHeadersRead, ct);
        resp.EnsureSuccessStatusCode();
        return await resp.Content.ReadFromJsonAsync<CreateOrderResponse>(cancellationToken: ct)
               ?? throw new JsonException("Empty body");
    }
}
```
Talk to: DI, cancellation, correlation *vs* idempotency, unknown timeout outcome, typed failures.

## B4. XSLT transform (source Order → ERP order)
```xml
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:ord="urn:company:orders" exclude-result-prefixes="ord">
  <xsl:output method="xml" indent="yes"/>
  <xsl:template match="/ord:Order">
    <ErpOrder>
      <OrderNumber><xsl:value-of select="@id"/></OrderNumber>
      <BuyerName><xsl:value-of select="ord:Customer"/></BuyerName>
    </ErpOrder>
  </xsl:template>
</xsl:stylesheet>
```
Namespace `ord:` must be bound or XPath finds nothing.

## B5. SOAP request + fault
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header><CorrelationId>abc-123</CorrelationId></soap:Header>
  <soap:Body><CreateOrder><OrderId>ORD-1001</OrderId></CreateOrder></soap:Body>
</soap:Envelope>
```
```xml
<soap:Fault><faultcode>soap:Client</faultcode><faultstring>Invalid order amount</faultstring></soap:Fault>
```

## B6. Idempotency registry + atomic claim (the killer detail)
```sql
CREATE TABLE dbo.IntegrationOrder (
  IdempotencyKey nvarchar(100) PRIMARY KEY,
  OrderId nvarchar(50) UNIQUE, RequestHash char(64),
  Status varchar(24), HttpStatus smallint, ResponseBody nvarchar(max),
  ExternalOrderId nvarchar(100), CorrelationId varchar(64),
  AttemptCount int DEFAULT 0, CreatedUtc datetime2 DEFAULT SYSUTCDATETIME());
```
Atomic claim (locks prevent two requests both passing "check-then-insert"):
```sql
BEGIN TRAN;
SELECT @Existing = IdempotencyKey FROM dbo.IntegrationOrder WITH (UPDLOCK, HOLDLOCK)
 WHERE IdempotencyKey=@Key OR OrderId=@OrderId;
IF @Existing IS NULL
  INSERT dbo.IntegrationOrder(IdempotencyKey,OrderId,RequestHash,Status,CorrelationId)
  VALUES(@Key,@OrderId,@Hash,'PROCESSING',@Corr);
SELECT * FROM dbo.IntegrationOrder WHERE IdempotencyKey=COALESCE(@Existing,@Key);
COMMIT;
```
| Existing state | Decision |
|---|---|
| No row | insert PROCESSING, continue |
| Same key/hash + COMPLETED | return stored result (`replayed:true`), no downstream call |
| Same key/hash + PROCESSING | return **202** / status |
| Same key, **different hash** | return **409** |
| REJECTED | return stored rejection |
- **Hash the *normalized* request** (trim, uppercase currency, UTC timestamp) but **exclude** volatile values (correlation id, current time) so equal requests = equal hash.

## B7. Frends Order Process — shapes in order
```
Submit Order API (API Trigger + Policy)
 → Initialize (correlation id, idempotency key, SHA-256 hash)
 → Validate Order (collect ALL errors → 400 Problem)
 → Claim Order (atomic SQL idempotency)  → branch new/duplicate/conflict
 → Get Customer (parameterized SQL: exists? active?)
 → Map Downstream Order
 → Get OAuth token (client_credentials)
 → Submit Downstream (POST, timeout, same Idempotency-Key + Correlation header)
 → Classify Response (2xx / 4xx / 429 / 5xx)
 → Complete Order / Record Failure (durable)
 → Return HTTP Response (+ correlation id in header & body)
```
- **Environment variables** (via `#env`): base URLs, token URL, client id/secret(secret), scope, connection string(secret), timeout, max attempts. Secrets never logged.
- **Frends references:** `#trigger` (input/metadata) · `#var` (mutable vars) · `#env` (config, e.g. `#env.CRM.BaseUrl`) · `#result` / `#result[Shape Name]` (task output) · `#process` (env, agent, version, exec id, cancellation) · `#var.error` (in Catch).
- **Never read `#result[Shape]` from a branch that may not have run** — initialize a `#var` before the branch and assign on each path. In **Catch**, don't read the failed task's result — use error context + pre-initialized vars.

## B8. Downstream status classification (Frends, HTTP-throw disabled)
```
2xx     → parse + complete
400/422 → permanent rejection, no retry
401/403 → identity/scope failure, alert (at most one token refresh)
409     → query/inspect idempotent state
429     → honor Retry-After, bounded delay
5xx     → bounded retry only if duplicate-safe (same key)
other   → unexpected contract response (502-style), don't blind-repeat
```

## B9. Retry timeline (concept made concrete)
```
Attempt1 → 503 → wait 2s → Attempt2 → 503 → wait 5s → Attempt3 → fail
→ STOP, save safe failure, alert / move to recovery
```
Exact numbers vary; the point is a **clear bound**.

## B10. Timeout recovery (write with unknown result)
```
Frends sends ORD-1001 → ERP creates it → response lost → Frends sees timeout
→ DO NOT resend yet → search ERP for ORD-1001
   found     → record success
   not found → retry only with duplicate protection
→ reconcile source vs target
```

## B11. Frends deploy / rollback / logging
- **Release path:** DEV → TEST → UAT → PROD → smoke test → monitor. Deploy **referenced Subprocesses first** and define all target Environment Variables. Deploy an **API + its linked Processes as ONE unit**. Choose "Deploy" vs "Deploy and activate Triggers" deliberately.
- **Rollback:** deploy the previous known-good version to the Agent Group; confirm trigger state; **reconcile side effects** (rolling back code does NOT undo an order/payment — that needs a compensation step).
- **Log levels:** Only Errors / Default / Everything (Everything = temporary investigation only). Use **"Skip logging result and parameters"** on secret-bearing shapes.
- **Detect a schedule that never ran:** Monitoring Rule on *expected/absent* executions — a run that didn't happen has no failed Instance to alert on.

## B12. Testing ladder (what proves what)
| Layer | Proves | Example |
|---|---|---|
| Contract | matches OpenAPI/WSDL/XSD | response matches schema |
| Mapping | fields → correct target | XSLT output correct |
| Unit/Component | isolated logic | 400 not retried |
| Integration | real boundary works | test Agent reaches test SQL/API |
| Negative/Security | bad input/token rejected | expired token → 401 |
| Failure/Recovery | retry/replay/dup works | 429 honors delay |
| Smoke | prod path alive | one test order completes |
| Reconciliation | business result correct | source/target counts match |
| UAT | business accepts | manager sign-off |
- Frends: **Task test** (isolated, no `#trigger`/`#result` context) · **Run once** (full Process → inspect Instance) · **.NET unit tests** for Custom Tasks.

---

# TOP 20 QUESTIONS — instant cues

| # | Question | Say this |
|---|---|---|
| 1 | Tell me about yourself | role → systems → your work → why this role |
| 2 | What is SDLC? | Plan→Design→Build→Test→Release→Support (Agile/Waterfall/DevOps mix) |
| 3 | New integration? | Ask→Agree→Design→Build→Prove→Release→Run→Improve |
| 4 | Requirement changes mid-build? | confirm reason+impact → update contract/mapping/tests/estimate → tell owners → no hidden change |
| 5 | What do you gather first? | owners, data, security, scale, failure behavior, success criteria |
| 6 | Describe a middleware project | Portal REST/JSON → Frends validate+map+transform → SOAP/XML ERP |
| 7 | Design a Frends Process? | Trigger → clear Tasks → errors/Catch → config outside → logs/promoted values |
| 8 | Frends vs Power Platform vs .NET? | systems/hybrid → Frends; user apps/approvals → PP; special reusable code → .NET |
| 9 | HTTP request/response? | method/URL/headers/body → status/headers/body |
| 10 | Test an integration? | contract→mapping→negative→security→recovery→UAT→smoke |
| 11 | REST vs SOAP? | HTTP/JSON/OpenAPI vs XML/WSDL/XSD; neither always better |
| 12 | XML/XSD/XPath/XSLT? | holds / checks / finds / changes |
| 13 | SOAP & WSDL? | Envelope/Header/Body/Fault; WSDL=service, XSD=data |
| 14 | What's in OpenAPI? | Info→Servers→Paths→Models→Security |
| 15 | Headers in OpenAPI? | auth=securitySchemes, request=parameters, response=responses→headers |
| 16 | Validate JSON? | Syntax→Shape→Business→Outside data; properties≠required; missing≠null≠empty |
| 17 | Secure an API? | HTTPS→identity→permission→input→operations; OpenAPI describes, policy enforces |
| 18 | Retry & timeout? | temporary+duplicate-safe+bounded only; timeout=unknown→check target first |
| 19 | DEV works, UAT fails? | same request → compare URL/route/env-vars/secret/cert/DNS/proxy/permission/version/data via correlation id |
| 20 | System.Text.Json vs Newtonsoft? | built-in modern default vs mature flexible/legacy; contract-test before switching |

**Common mistakes to avoid saying:** "retry every 5xx" · "HTTPS = full security" · "OpenAPI security secures the API" · treating missing/null/empty as same · ignoring XML namespaces · "deserialization = validation" · "deployment done" without checking the target · claiming work you didn't do.

---

# PRODUCTION TROUBLESHOOTING (quick checks)
- **Request never reaches Process:** URL/method/DNS → TLS cert → gateway/API Policy → path/method/Agent Group/API Trigger → Agent health → Instances/logs.
- **401:** token/key/cert, issuer, audience, time. **403:** scope/role/policy/record ownership.
- **404:** environment, base URL, route, API version, method, deployment, trigger.
- **500:** use correlation id → first internal error → null data/mapping/settings/version.
- **502/503/504:** target response / health-load / upstream time (write = unknown result).
- **Postman works, app fails:** compare method, URL, headers, body/encoding, token, cert, proxy/DNS/timeout.
- **XPath returns nothing:** namespace URI+prefix, root/full path, case, missing/empty/nil, SOAP Envelope, encoding, schema change.
- **Retry storm:** stop retries, protect target, add limit+wait, drain slowly.
- **Expired cert:** find owner, renew, check chain, add expiry alert. **Never disable TLS validation as a fix.**

---

# ONE-PAGE MORNING RECALL
- **Answer shape:** What → Why → Example → Failure + fix.
- **Lifecycle:** Plan→Design→Build→Test→Release→Support.
- **Middleware:** Receive→Check→Change→Send→Track. Story: Portal REST/JSON → Frends → SOAP/XML ERP.
- **Security:** Connection→Identity→Permission→Input→Operations. *OpenAPI describes; API Policy + Process enforce.*
- **OpenAPI:** Info→Servers→Paths→Models→Security. auth=securitySchemes, header=parameters.
- **JSON:** Syntax→Shape→Business→Outside. properties describes, required mandates. missing≠null≠empty.
- **XML:** XML data → XSD rules → XPath find → XSLT change. WSDL=service, SOAP=Envelope/Header/Body/Fault.
- **Failure:** bad data→stop+correct · temporary→bounded safe retry · timeout→check target before retry.
- **Frends:** Trigger→Process→Tasks→Agent runs it→Instance+logs+promoted values show what happened. Deploy to Agent Group; roll back to known-good version.
- **Final:** use *real* experience, say what *you* did, give one safe example. Don't invent numbers. Sleep before the interview.
