# Frends Integration Interview: 8-Hour Learning Guide

## Read This First

This guide is for **one day of preparation**. It focuses on the non-coding parts of a Frends, middleware, API, and Power Platform interview.

The goal is not to memorize a textbook. The goal is to remember a few strong ideas and explain them in simple words.

### Priority labels

- **P0 - Must know:** Learn this before the interview.
- **P1 - Good to know:** Study this only after P0.
- **Reference:** Look it up if needed. Do not memorize it tonight.

### How to answer any interview question

Use this four-part answer:

1. **Meaning:** What is it?
2. **Purpose:** Why do we use it?
3. **Example:** How did or would you use it?
4. **Safety:** What can fail, and how do you handle it?

Example:

> XSD is a set of rules for XML. It checks the allowed fields, order, data types, and repeated values. I use it before sending XML to another system. If validation fails, I stop the message, record a safe error, and do not call the target system.

### How to study each topic

For every P0 section:

1. Read the memory hook.
2. Close the file and say it aloud.
3. Read the 30-second answer.
4. Close the file and explain it in your own words.
5. Answer the recall questions without looking.
6. Check the answer key.

Do not copy every sentence exactly. Remember the order and key words.

## Minimum Viable Route

The full file is complete reference material. You do **not** need to memorize every line.

For the eight-hour study day, use this route:

1. Read the whole-interview map in Section 2.
2. In every P0 section, learn only the memory hook, spoken answer, one example, and recall questions.
3. Open a detailed list only when your diagnostic score for that topic is `0` or `1`.
4. Use Section 14 for closed-book retrieval. The earlier sections contain the full answers.
5. Complete two scenarios in Section 16 and the mock interview in Section 18.
6. Tomorrow morning, read only Section 19.

After each study block ask:

> Can I explain the topic without notes, give one example, and name one failure risk?

If yes, continue. If no, review only the missed answer. Do not reread the whole section.

---

# 1. Your Exact 8-Hour Plan

This schedule is exactly 480 minutes, including breaks.

| Time | Minutes | Focus | Output |
|---|---:|---|---|
| 00:00-00:15 | 15 | Quick test and mental map | Find weak areas |
| 00:15-01:10 | 55 | SDLC and a new integration | Say the full lifecycle aloud |
| 01:10-01:20 | 10 | Break | No screen |
| 01:20-02:30 | 70 | HTTP, OpenAPI, JSON, API security | Explain one secure API contract |
| 02:30-02:40 | 10 | Break | Walk and drink water |
| 02:40-03:30 | 50 | XML, XSD, XPath, XSLT, SOAP | Explain the XML family |
| 03:30-03:45 | 15 | Food break | No study |
| 03:45-04:50 | 65 | Frends and the middleware story | Tell one project story |
| 04:50-05:00 | 10 | Break | No screen |
| 05:00-05:50 | 50 | Failures, release, monitoring, incidents | Solve four failure cases |
| 05:50-06:00 | 10 | Break | Walk |
| 06:00-06:30 | 30 | .NET concepts and Power Platform | Compare tools without code |
| 06:30-06:40 | 10 | Break | Reset |
| 06:40-07:15 | 35 | Top questions from memory | Answer 15 cards |
| 07:15-07:20 | 5 | Break | Breathe slowly |
| 07:20-08:00 | 40 | Final mock interview | Record and score yourself |

### Spaced recall checkpoints

- At **01:20**, recall the SDLC steps before starting APIs.
- At **03:45**, recall SDLC, API security, and the XML family.
- At **06:40**, answer all 15 P0 questions without notes.
- Tomorrow morning, read only the one-page sheet near the end.

### 15-minute start test

Answer each question in one minute. Mark it:

- `0` = I cannot answer.
- `1` = I know some words but cannot explain clearly.
- `2` = I can give a clear answer and example.

Questions:

1. How do you take a new integration from request to production?
2. What does middleware do?
3. How do you secure an API?
4. What are the main parts of an OpenAPI file?
5. How do you check that required JSON fields are present?
6. What is the difference between XML, XSD, XPath, and XSLT?
7. What are the parts of a SOAP message?
8. How do you handle a timeout without creating duplicates?

Study every `0` first. Then study every `1`.

---

# 2. The Whole Interview on One Map

Most questions fit into this flow:

```text
Business request
  -> contract
  -> secure entry
  -> validate
  -> transform
  -> call another system
  -> handle the result
  -> log and monitor
  -> recover from failure
  -> release and support
```

Use one example throughout this guide:

```text
Order Portal
  -> REST API with JSON
  -> Frends middleware
  -> SOAP API with XML
  -> Legacy ERP
```

This one example lets you explain REST, JSON, OpenAPI, security, Frends, XML, XSD, XSLT, SOAP, retries, release, and monitoring.

## Seven memory hooks - P0

### New integration

**Ask -> Agree -> Design -> Build -> Prove -> Release -> Run -> Improve**

### Middleware

**Receive -> Validate -> Route -> Transform -> Deliver -> Recover -> Observe**

### XML family

**XML has data. XSD checks. XPath finds. XSLT changes. SOAP carries. WSDL describes.**

### JSON validation

**Parse -> Shape -> Meaning -> Reference**

### API security

**Protect the connection -> identify the caller -> check permission -> validate input -> limit abuse -> protect secrets -> keep evidence**

### Timeout

**The result is unknown -> find by business ID -> retry only when duplicate-safe -> reconcile**

### Incident

**Impact -> Stabilize -> Find -> Fix -> Verify -> Learn**

---

# 3. SDLC and a New Integration - P0

## Simple meaning

SDLC means **Software Development Life Cycle**. It is the full path from an idea to a working and supported production solution.

Agile, Waterfall, and DevOps organize the work in different ways. The core questions are still the same: what do we need, how will we build it, how will we prove it works, and how will we support it?

## 60-second answer: SDLC models

> Waterfall moves through larger sequential stages and fits stable or strongly regulated requirements. Agile delivers in smaller increments and uses frequent feedback. DevOps extends delivery into automated release, monitoring, and shared operational ownership. Many integration teams use a hybrid: Agile delivery inside required architecture, security, UAT, and change-control gates. Every model still covers planning, requirements, design, development, testing, deployment, operation, maintenance, and retirement.

Your role can include requirements, contract review, mapping, Process design, testing, release evidence, monitoring, incident support, and documentation. State only the parts you actually owned.

## Memory hook

**Ask -> Agree -> Design -> Build -> Prove -> Release -> Run -> Improve**

## The eight steps

### 1. Ask - understand the need

Ask:

- What business problem are we solving?
- Who owns the source system and target system?
- Who will use the result?
- What does success look like?
- Is this a new project or a change to an existing flow?

Output: a clear goal, owner, scope, and success measure.

### 2. Agree - remove unknowns

Agree on:

- Trigger: API call, schedule, file, message, or webhook.
- Source and target systems.
- Request and response examples.
- OpenAPI, WSDL, XSD, or file contract.
- Field mapping and business rules.
- Volume, payload size, speed, and service level.
- Authentication, authorization, and sensitive data.
- Error behavior, duplicate behavior, and support owner.
- Acceptance criteria.

Also ask about non-functional requirements:

- Peak volume, payload size, latency, and availability.
- Source of truth and owner for every important field.
- Date, timezone, decimal, currency, encoding, and default rules.
- Personal data classification, audit, retention, RTO, and RPO.
- Who owns replay, reconciliation, and out-of-hours support.

Output: approved contract, examples, mapping, and acceptance criteria.

### 3. Design - decide how it should work

Decide:

- Synchronous or asynchronous flow.
- REST, SOAP, queue, file, or database pattern.
- Where validation happens.
- How data is transformed.
- Timeout and retry rules.
- Idempotency, which means preventing the same request from doing the work twice.
- Logging, correlation ID, alerts, and reprocessing.
- Environment settings and secret storage.
- Test plan, release plan, and rollback plan.

Output: a small flow diagram and written decisions.

### 4. Build - create a thin working path

First build one small end-to-end happy path. Then add validation, errors, security, retries, and monitoring.

In Frends, use clear Process and Subprocess names. Keep environment URLs and secrets outside the Process. Review the work with another person.

Output: reviewed and versioned integration.

### 5. Prove - test normal and abnormal cases

Test:

- Valid request and correct result.
- Missing, null, empty, wrong-type, and extra fields.
- Invalid or expired credentials.
- Caller without permission.
- Duplicate request.
- Timeout, rate limit, and target `5xx` error.
- Bad XML, wrong namespace, and SOAP Fault.
- Expected volume and payload size.
- Reprocessing and reconciliation.
- User acceptance testing, called UAT.

Output: test evidence and UAT approval.

### 6. Release - move it safely

Before release, confirm:

- Correct Process and dependency versions.
- Environment URLs, secrets, certificates, and permissions.
- Change approval and release owner.
- Deployment order.
- Smoke test, which is a small production test.
- Rollback steps.

After deployment, run the smoke test and watch the first real messages.

Output: approved release and verified production result.

### 7. Run - operate and support it

Support needs:

- Logs with correlation ID and business ID.
- Counts, duration, failures, retries, and backlog metrics.
- Alerts that lead to an action.
- A runbook with diagnosis and recovery steps.
- A controlled replay or reprocessing method.
- A way to compare source and target records.

Output: an integration that can be supported, not only executed.

### 8. Improve - learn from use

Review incidents and slow steps. Fix root causes. Update tests, alerts, documents, and the runbook. Plan the retirement of old API versions.

Output: fewer repeated problems.

## 90-second interview answer: How do you handle a new integration?

> I use eight steps: Ask, Agree, Design, Build, Prove, Release, Run, and Improve. First, I understand the business goal, owners, source, target, volume, security needs, and success criteria. Then I agree the contract, sample messages, field mapping, required fields, error rules, and acceptance criteria.
>
> I design the trigger, data flow, validation, transformation, authentication, timeout, retry, idempotency, logging, and monitoring. I build a small end-to-end path first, then add failure handling. I test the happy path and also invalid data, duplicates, timeouts, security, target failures, and recovery.
>
> I release through the approved environments with checked configuration, a smoke test, and a rollback plan. After release, I monitor the first messages, reconcile the result, provide a runbook, and improve the flow when we learn something new.

## New project versus a new feature

### New project

You may need to create the first:

- Ownership model.
- Contracts and naming rules.
- Development, test, UAT, and production environments.
- Security model.
- Deployment path.
- Monitoring and support process.

### Change to an existing integration

Start with impact analysis:

- Which consumers use the current contract?
- Is the change backward compatible?
- Do old messages still exist in a queue?
- Does the API need a new version?
- Which regression tests must run again?
- Can old and new versions run together during migration?

**Simple rule:** prefer adding optional fields. Use a new API version for a breaking change.

## Common follow-up situations

### Requirements change during development

> I first confirm the business reason and impact. I update the acceptance criteria, contract, mapping, tests, estimate, and release plan. I tell all affected owners. I do not make a hidden contract change inside the Process.

### A defect is found in UAT

> I reproduce it with the same input and environment. I decide whether the issue is code, configuration, data, permission, or an unclear requirement. I fix the cause, add a regression test, redeploy through the normal path, and ask the user to retest the failed case.

### It works in DEV but fails in UAT

> I compare method, URL, route, environment variables, secrets, certificate, DNS, firewall, proxy, permissions, Task version, and test data. I use the correlation ID to compare logs at every step. I change only after I have evidence of the difference.

## Definition of Done

An integration is done when:

- The contract and acceptance criteria are approved.
- Security, validation, mapping, and errors work.
- Normal, negative, recovery, and UAT tests pass.
- Every environment has the correct configuration and secrets.
- Deployment, smoke test, rollback, and replay steps exist.
- Logs, metrics, alerts, and correlation IDs are useful.
- A support owner and runbook exist.

## Recall - close the notes

1. Say the eight lifecycle steps.
2. Name five questions you ask before design.
3. What is different about a change to an existing API?
4. What is required before production release?
5. What do you compare when DEV works but UAT fails?

<details>
<summary>Answer key</summary>

1. Ask, Agree, Design, Build, Prove, Release, Run, Improve.
2. Goal, owners, systems, trigger, contract, mapping, volume, security, failures, success criteria.
3. Consumers, compatibility, versions, migration, in-flight data, and regression tests.
4. Approval, configuration, tests, deployment order, smoke test, rollback, monitoring, and ownership.
5. URL, route, configuration, secrets, certificate, DNS, network, permission, versions, data, and logs.

</details>

---

# 4. One Middleware Project Story - P0

## Simple meaning

Middleware sits between systems. It helps them communicate even when they use different protocols, data formats, security, or timing.

It can:

- Receive and route messages.
- Validate contracts.
- Change JSON to XML or one XML format to another.
- Call several systems in the correct order.
- Apply common security rules.
- Handle retries and reprocessing.
- Give one place for logs and monitoring.

## Memory hook

**Receive -> Validate -> Route -> Transform -> Deliver -> Recover -> Observe**

## The example project

```text
Order Portal
  | REST + JSON + OAuth access token
  v
Frends API Policy and API Trigger
  | validate request and caller
  v
Order Intake Process
  | correlation ID and duplicate check
  | map to a simple internal order model
  | create canonical XML
  | transform with XSLT to ERP XML
  | validate final ERP XML with target XSD
  v
SOAP call to Legacy ERP
  | inspect HTTP result and SOAP Fault
  v
Return status, store result, log, alert, and reconcile
```

### Why Frends is useful here

The Order Portal understands REST and JSON. The ERP understands SOAP and XML. Frends keeps each system independent from the other system's details.

Frends becomes the place for:

- Protocol change: REST to SOAP.
- Data change: JSON to XML.
- Contract checks: JSON schema and XSD.
- Security policy.
- Orchestration, which means controlling the order of steps.
- Failure recovery and observability.

Observability means being able to understand the system from logs, metrics, and traces.

## 90-second answer: Describe a middleware project

> A useful example is an order integration between a portal and a legacy ERP. The portal sent REST requests with JSON, while the ERP accepted SOAP messages with XML. Frends sat between them.
>
> The API Policy checked the caller. The API Trigger started the Process. The Process created or kept a correlation ID, validated required fields and business rules, and checked the order ID to avoid duplicate work. It mapped the request to an internal order model, created canonical XML, transformed it into the ERP format with XSLT, validated the final ERP XML against the target XSD, and sent a SOAP request.
>
> I separated permanent errors from temporary errors. Bad input and permanent SOAP Faults were not retried. Timeouts and selected temporary failures used limited retries only when duplicate handling was safe. Logs contained the correlation ID, order ID, stage, duration, and safe error details. We also had alerts, a replay method, and reconciliation between the portal and ERP.
>
> The work followed contract review, testing, UAT, controlled deployment, smoke testing, and production monitoring. The main value was that both systems stayed simpler and support could see and recover failed work.

## Make this answer honest

Do not claim work that you did not do. Change the example to match your experience:

- Replace Order Portal and ERP with your real systems.
- Replace OAuth, XSLT, queue, or other parts if you did not use them.
- Say **we** for team work and **I** for your own work.
- Give only real results. Do not invent percentages.

Use this speaking order:

1. **Problem:** Which systems and why?
2. **Contract:** What came in and went out?
3. **Flow:** What did Frends do?
4. **Reliability:** How did you handle failure and duplicates?
5. **Security:** How was access controlled?
6. **Operations:** How did support find and recover problems?
7. **Result:** What real value did it provide?

Use this role sentence:

> I owned [requirements, mapping, Process design, testing, release, or support]. The team owned [other work]. My hardest decision was [decision], and I proved it through [test, log, metric, or business result].

## Important design choice: synchronous or asynchronous

### Synchronous

The caller waits for the final result.

Use it when:

- Work is fast.
- The target is reliable.
- The caller needs an immediate result.

Risk: a slow target keeps the caller waiting.

### Asynchronous

The API accepts the request and completes it later. It may return `202 Accepted` with a status URL or use a callback.

Use it when:

- Work is slow.
- The target is sometimes unavailable.
- A queue or durable store is needed.
- The caller does not need the final result immediately.

Risk: you must provide status, monitoring, reconciliation, and recovery.

## Important failure: target succeeded but response was lost

This is an **unknown result**, not a normal failure.

Do this:

1. Stop blind retries.
2. Search the target by order ID or idempotency key.
3. If the target already completed the work, record success.
4. Retry only if the target proves the work did not happen.
5. Reconcile source and target records.

## Recall - close the notes

1. Say the seven middleware actions.
2. Why use middleware instead of a direct connection?
3. Tell the project story in the seven-part speaking order.
4. When would you choose an asynchronous API?
5. What do you do when the target may have succeeded but the response was lost?

<details>
<summary>Answer key</summary>

1. Receive, Validate, Route, Transform, Deliver, Recover, Observe.
2. To reduce coupling and centralize protocol change, transformation, security, orchestration, failures, and visibility.
3. Problem, Contract, Flow, Reliability, Security, Operations, Result.
4. For slow or unreliable work when the final answer is not needed immediately.
5. Find the result using a stable business ID, avoid blind retry, then reconcile.

</details>

# 5. HTTP and REST Basics - P0

## 70-minute API block

- 8 minutes: HTTP request, methods, and status groups.
- 15 minutes: API security answer and one negative test.
- 20 minutes: OpenAPI map and security scheme.
- 12 minutes: JSON validation answer.
- 15 minutes: close the file and speak the answers.

Memorize the hooks and spoken answers. Treat field lists and YAML examples as recognition material.

## Simple meaning

HTTP is the request and response protocol used by web APIs.

An HTTP request has:

- **Method:** what action is requested.
- **URL:** which resource is requested.
- **Headers:** metadata about the request.
- **Body:** optional data sent to the API.

An HTTP response has:

- **Status code:** the result category.
- **Headers:** metadata about the response.
- **Body:** result or error details.

## Common methods

| Method | Simple purpose | Normal property |
|---|---|---|
| `GET` | Read data | Should not change data |
| `POST` | Create or start work | Often not idempotent |
| `PUT` | Replace a known resource | Should be idempotent |
| `PATCH` | Partly update a resource | Depends on design |
| `DELETE` | Remove a resource | Intended final state is repeatable |

Idempotent means repeating the same request has the same intended effect. It does not mean the response must be identical.

## Status code groups

| Group | Meaning | Common examples |
|---|---|---|
| `2xx` | Success | `200` OK, `201` Created, `202` Accepted, `204` No Content |
| `3xx` | Redirect or cache behavior | `304` Not Modified |
| `4xx` | Caller request problem | `400`, `401`, `403`, `404`, `409`, `422`, `429` |
| `5xx` | Server or dependency problem | `500`, `502`, `503`, `504` |

### Codes interviewers often ask about

- `200 OK`: request succeeded.
- `201 Created`: a resource was created. It normally includes a `Location` for the new resource.
- `202 Accepted`: work was accepted but is not finished. Provide a status resource, `Location`, or callback.
- `204 No Content`: success with no response body.
- `400 Bad Request`: malformed or contract-invalid input.
- `401 Unauthorized`: authentication is missing or invalid.
- `403 Forbidden`: caller is known but not allowed.
- `404 Not Found`: route or resource was not found.
- `405 Method Not Allowed`: route exists but the method is unsupported.
- `409 Conflict`: state conflict, such as a duplicate ID.
- `415 Unsupported Media Type`: request `Content-Type` is not supported.
- `422 Unprocessable Content`: valid syntax but failed semantic rules, if this is the API convention.
- `429 Too Many Requests`: rate limit was reached.
- `500 Internal Server Error`: unexpected server failure.
- `502 Bad Gateway`: gateway received a bad upstream response.
- `503 Service Unavailable`: service cannot handle the request now.
- `504 Gateway Timeout`: gateway waited too long for upstream.

**Interview rule:** do not retry every error. Correct `4xx` input or access problems. Retry only selected temporary failures, with a limit and duplicate protection.

## Important request headers

| Header | Why it exists |
|---|---|
| `Authorization` | Carries a bearer token or other credential |
| `Content-Type` | Format of the request body, such as `application/json` |
| `Accept` | Response formats the caller accepts |
| `X-Correlation-ID` | Connects logs across systems |
| `Idempotency-Key` | Helps prevent repeated create work |
| `If-Match` | Supports safe update using an ETag |

Never log the full `Authorization` header, API key, password, or secret.

## REST versus SOAP

### REST API

- Uses HTTP resources and methods.
- Often uses JSON, but can use other formats.
- Usually described by OpenAPI.

### SOAP API

- Uses an XML Envelope, Header, Body, and Fault.
- Often has a WSDL contract and XSD data types.
- Can use advanced WS-* message features.

Neither is always better. Choose based on the existing contract, security, transaction, tooling, and business needs.

---

# 6. API Security - P0

## Memory hook

**Protect -> Identify -> Authorize -> Validate -> Limit -> Hide -> Observe**

In simple words:

1. Protect the connection.
2. Identify the caller.
3. Check what the caller may do.
4. Treat all input as untrusted.
5. Limit abuse.
6. Protect secrets and sensitive data.
7. Keep safe evidence in logs and alerts.

## 90-second interview answer: How do you secure an API?

> I apply security in layers. First, I use HTTPS so traffic is encrypted. I may use mutual TLS when both systems must prove certificate identity. Next, I authenticate the caller, often with OAuth 2.0 for service-to-service calls. For a JWT token, I validate the signature, issuer, audience, expiry, and required scope or role.
>
> Authentication tells me who is calling. Authorization decides whether that caller may use this operation and resource. I apply least privilege. I also validate the method, content type, body size, required fields, data types, allowed values, and business rules.
>
> At the gateway or Frends API Policy, I restrict routes and methods and apply throttling or rate limits. Secrets and certificates stay in protected environment configuration or a vault, not in code, OpenAPI examples, or logs. Errors do not expose stack traces. Logs mask sensitive data but keep the correlation ID and security events.
>
> Finally, I test missing, invalid, and expired tokens, wrong permissions, malformed input, excessive requests, and unauthorized access to another user's resource.

## Authentication versus authorization

- **Authentication:** Who or what is calling?
- **Authorization:** Is that identity allowed to do this action on this resource?

Simple example:

- A valid employee badge proves identity.
- The badge still may not open the server room.

`401` normally means missing or invalid authentication. `403` normally means the identity is known but lacks permission.

## OAuth 2.0 client credentials

Use this for many service-to-service integrations:

1. The client authenticates to the identity provider.
2. The identity provider returns a short-lived access token.
3. The client calls the API with `Authorization: Bearer <token>`.
4. The API validates the token.
5. The API checks the required scope or role.

The client secret goes to the identity provider. It should not be sent to the business API.

Cache the access token until shortly before it expires. Do not request a new token for every API call, log the token, or treat a service identity as a human user.

## What to validate in a JWT

Ask five questions:

- Who signed it? Validate with a trusted library, allowed algorithms, and trusted keys or JWKS.
- Who issued it?
- Who is it for, meaning the audience?
- Is it current, using expiry and not-before time?
- What may it do, using scope or role?

Do not only decode a token. Decoding is not validation.

## API key, OAuth, and mTLS

| Method | Simple use | Main warning |
|---|---|---|
| API key | Identify and meter a simple client | It is a bearer secret with limited identity details |
| OAuth token | Short-lived identity and permissions | Validate token and authorization claims |
| mTLS | Both systems prove certificate identity | Certificates need ownership, renewal, and expiry alerts |

Always use HTTPS. Choose based on risk and the systems involved.

## Frends API Policy

In Frends, an API Policy is the runtime control in front of API operations. Depending on the tenant and setup, it can control identities, paths, methods, Agent Groups, throttling, and logging.

**Important difference:**

- OpenAPI **describes** the security requirement.
- The Frends API Policy, gateway, identity provider, and Process **enforce** it.
- Tests **prove** that it is enforced.

Writing `securitySchemes` in YAML does not secure a running API by itself.

Explicitly configure whether Frends API access is public or authenticated, and configure policy logging deliberately. Also check object-level authorization. A caller allowed to use `GET /orders/{id}` must not automatically see another customer's order.

## Security-related headers

### Request headers

- `Authorization`: token or credential.
- `X-API-Key`: API key, if this method is chosen.
- `Content-Type`: body format.
- `X-Correlation-ID`: trace identifier.
- `Idempotency-Key`: duplicate-safe create request.

### Response headers

- Correct `Content-Type`.
- `Cache-Control: no-store` for sensitive responses.
- `Strict-Transport-Security` for HTTPS browser-facing services.
- `X-Content-Type-Options: nosniff` for browser protection.
- `Retry-After` with `429` or temporary unavailability when useful.

Headers such as Content Security Policy mainly protect browser use. They have limited value for a pure server-to-server JSON client. They do not replace authentication or authorization.

Additional rules:

- mTLS proves certificate identity but does not replace business authorization.
- Validate or replace a caller-provided correlation ID before logging it.
- For webhooks, verify a signature and timestamp and block replay.
- Do not fetch a caller-supplied URL without allowlisting and network controls; this reduces SSRF risk.
- Do not use wildcard CORS origins with credentialed browser requests.

## CORS in one answer

> CORS is a browser rule that controls which web origins may call an API from browser code. It is not authentication. A server-to-server client is not protected by CORS, so the API still needs real authentication and authorization.

## Security tests

Test:

- No token.
- Changed or invalid token.
- Expired token.
- Wrong issuer or audience.
- Missing scope or role.
- Access to another user's object.
- Wrong HTTP method.
- Wrong content type.
- Very large or malformed body.
- Injection-like input.
- Too many requests.
- Error response and log redaction.
- Expired certificate or secret rotation in a safe test environment.

## Recall - close the notes

1. Say the seven security layers.
2. Authentication versus authorization?
3. What five questions do you ask when validating a JWT?
4. Does an OpenAPI security section enforce security?
5. Why is CORS not API authentication?

<details>
<summary>Answer key</summary>

1. Protect, Identify, Authorize, Validate, Limit, Hide, Observe.
2. Identity versus permission for an action and resource.
3. Who signed it, who issued it, who it is for, whether it is current, and what it may do.
4. No. The runtime policy, gateway, identity provider, and application enforce it.
5. CORS is a browser-origin rule. Non-browser clients can still call the API.

</details>

# 7. OpenAPI, YAML, JSON, and Swagger - P0

## Simple meaning

OpenAPI is a machine-readable API contract. It tells people and tools:

- Which URLs and methods exist.
- What inputs are allowed.
- What responses can return.
- Which data shapes are used.
- Which security method is required.

Swagger is the old name of the specification and also the name of tools such as Swagger UI and Swagger Editor. People often say “Swagger file” when they mean an OpenAPI file.

## Memory hook

**Identity -> Servers -> Routes -> Reuse -> Security**

- **Identity:** OpenAPI version and API information.
- **Servers:** Base URLs.
- **Routes:** Paths, methods, input, and responses.
- **Reuse:** Shared schemas and other components.
- **Security:** Authentication requirements.

## YAML versus JSON

YAML and JSON can describe the same OpenAPI document.

| YAML | JSON |
|---|---|
| Uses indentation | Uses braces and brackets |
| Shorter for people | More explicit for machines |
| Comments are possible | Standard JSON has no comments |
| Indentation errors can change meaning | Commas and quotes must be correct |

`.yml` and `.yaml` are both common YAML extensions.

**RAML** is another API description language. It is not the same as OpenAPI. If a company uses OpenAPI, follow the OpenAPI structure and supported version.

RAML means RESTful API Modeling Language. If an interviewer says **RML**, ask what they mean. RML often means RDF Mapping Language and is not an OpenAPI format.

### YAML basics - recognize, do not memorize

- Use spaces, not tabs.
- Indentation defines nesting.
- `key: value` is a mapping.
- `-` starts a list item.
- Quote values that a YAML parser may treat as a date, boolean, or number.
- Lint the file after editing or converting it.

## Main OpenAPI fields

| Field | Simple purpose |
|---|---|
| `openapi` | Version of the OpenAPI standard |
| `info` | Title, description, and API version |
| `servers` | Base URLs |
| `paths` | Routes and HTTP methods |
| `components` | Reusable schemas, responses, parameters, and security schemes |
| `security` | Default security requirement |
| `tags` | Groups related operations |

## Fields inside an operation

Remember **Name -> Input -> Output -> Protection**.

- Name: `summary`, `description`, `operationId`, `tags`.
- Input: `parameters` and `requestBody`.
- Output: `responses`.
- Protection: `security`.

## Fields inside a schema

- Shape: `type`, `format`, `properties`, `items`.
- Required fields: `required`.
- Allowed values: `enum`.
- Limits: `minimum`, `maximum`, `minLength`, `maxLength`, `pattern`.
- Extra fields: `additionalProperties`.
- Reuse: `$ref`.
- Documentation: `description` and `example`.
- Combinations: `allOf`, `oneOf`, and `anyOf`.

In OpenAPI 3.0, nullable values use `nullable: true`. OpenAPI 3.0 supports only a JSON Schema subset. OpenAPI 3.1 aligns with JSON Schema 2020-12 and represents null through its schema types. Use the version supported by the Frends tenant.

`format` and `default` may be documentation hints rather than enforced behavior. A default value is not normally inserted automatically. Test the actual validator and apply business defaults explicitly.

## Small OpenAPI example - recognize, do not memorize

```yaml
openapi: 3.0.1
info:
  title: Order API
  version: 1.0.0

servers:
  - url: https://api.example.com

paths:
  /orders:
    post:
      operationId: createOrder
      summary: Accept an order
      security:
        - OAuth2: [orders.write]
      parameters:
        - name: X-Correlation-ID
          in: header
          required: false
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Order'
      responses:
        '202':
          description: Order accepted
        '400':
          description: Invalid request
        '401':
          description: Invalid authentication
        '403':
          description: Not allowed
        '429':
          description: Too many requests

components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: https://identity.example.com/oauth2/token
          scopes:
            orders.write: Submit orders
  schemas:
    Order:
      type: object
      additionalProperties: false
      required: [orderId, customerId, amount]
      properties:
        orderId:
          type: string
          minLength: 1
        customerId:
          type: string
          minLength: 1
        amount:
          type: number
          minimum: 0.01
```

## How security is written in OpenAPI

### Bearer token

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

### API key in a header

```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - ApiKeyAuth: []
```

### OAuth 2.0 client credentials

```yaml
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: https://identity.example.com/oauth2/token
          scopes:
            orders.read: Read orders
            orders.write: Submit orders
```

### Rules that are often missed

- Global `security` applies to operations unless an operation overrides it.
- Two separate entries in the security list mean **OR**.
- Two schemes inside one entry mean **AND**.
- Operation-level `security: []` removes the OpenAPI security requirement for that operation. A Frends API Policy may still enforce runtime authentication.
- Describe `Authorization` through `securitySchemes`, not as a normal header parameter.
- Describe a custom header such as `X-Correlation-ID` through operation `parameters`.
- OpenAPI documents the rule. Runtime policy must enforce it.

### Response header example

```yaml
responses:
  '429':
    description: Too many requests
    headers:
      Retry-After:
        description: Seconds before another attempt
        schema:
          type: integer
```

Authentication uses `securitySchemes`. A normal request header uses `parameters`. A response header uses `responses -> status -> headers`. `Content-Type` and `Accept` are normally represented by the declared media types under `content`.

## Strong OpenAPI rules for an interview

1. Use the OpenAPI version supported by the target platform.
2. Give each operation a stable and unique `operationId`.
3. A path parameter must match the URL placeholder and must be required.
4. Use `requestBody` for an OpenAPI 3 body.
5. Give every response a description.
6. Quote YAML response codes such as `'200'`.
7. Use the correct media type, such as `application/json`.
8. Put reusable models in `components` and use `$ref`.
9. Define required fields at every object level.
10. Include normal and error responses.
11. Do not put real tokens, secrets, or personal data in examples.
12. Validate the file with a linter and test the real API against the contract.
13. Prefer additive changes. Version breaking changes.

For current Frends work, use the OpenAPI version supported by the tenant; Frends documentation commonly shows OpenAPI 3.0.1 support. Keep 3.1 knowledge as a comparison, not as an assumption.

## 60-second answer: Explain an OpenAPI file

> OpenAPI is the contract for an HTTP API. I remember it as Identity, Servers, Routes, Reuse, and Security. The top level contains the OpenAPI version, information, base servers, paths, reusable components, and security. Each operation has a name, parameters or request body, responses, and security. Schemas define object properties, required fields, types, limits, and allowed values. YAML and JSON are only two formats for the same model. The file helps documentation, testing, and tooling, but the gateway and application must still enforce validation and security.

---

# 8. Validate Required JSON Fields - P0

## Memory hook

**Parse -> Shape -> Meaning -> Reference**

## The four checks

### 1. Parse - is it valid JSON?

Check:

- Correct JSON syntax.
- Correct `Content-Type`.
- Body size is within the limit.

Malformed JSON normally returns `400`.

### 2. Shape - does it match the contract?

Check:

- Root is the expected type, usually an object.
- Required properties are present.
- Each property has the correct type and format.
- Strings, numbers, and arrays are within allowed limits.
- Values match any `enum`.
- Unknown properties follow the chosen rule.
- Nested objects have their own required fields.

### 3. Meaning - is the business request valid?

Examples:

- Amount must be greater than zero.
- End date cannot be before start date.
- Currency must be allowed for the country.
- A field is required only when another field has a certain value.

### 4. Reference - do external facts allow it?

Examples:

- Customer exists.
- Product is active.
- Caller may submit for that customer.
- Order ID is not already completed.

## Required fields example

```yaml
Order:
  type: object
  additionalProperties: false
  required:
    - orderId
    - customer
    - amount
  properties:
    orderId:
      type: string
      minLength: 1
    customer:
      type: object
      required:
        - customerId
        - email
      properties:
        customerId:
          type: string
        email:
          type: string
          format: email
    amount:
      type: number
      minimum: 0.01
```

## What this example means

- The root must contain `orderId`, `customer`, and `amount`.
- The nested customer must contain `customerId` and `email`.
- `properties` describes possible fields. It does not make them required.
- `required` checks presence.
- A required string also needs `minLength: 1` if an empty string is not allowed.
- Null is different from missing. The schema must explicitly allow null when it is valid.
- `additionalProperties: false` rejects unknown fields. It does not check missing fields.
- Rejecting unknown fields can break forward-compatible additions. Choose strictness deliberately.
- Schema checks do not prove that the customer exists or that the caller is allowed.
- A required property can still be null in OpenAPI 3.0 only when its schema allows null with `nullable: true`.
- A `format` such as email may not be enforced by every validator.

## Where to validate in Frends

Use layers:

1. API/OpenAPI boundary for the basic contract where supported.
2. Process validation for business and conditional rules.
3. Target-system or reference checks for external facts.

Do not assume that importing an OpenAPI file automatically enforces every schema rule in every runtime. Test the actual Frends behavior.

## Safe validation response

```json
{
  "title": "Request validation failed",
  "status": 400,
  "correlationId": "bfa1c82d",
  "errors": [
    {
      "path": "$.customer.email",
      "code": "required",
      "message": "email is required"
    }
  ]
}
```

Return useful field errors, but do not return stack traces or secret values.

## Tests for one required field

For each important field, test:

- Field is missing.
- Field is null.
- String is empty.
- Wrong data type.
- Value is too small, too large, or outside the allowed list.
- Extra unknown field.
- Valid boundary value.

## 60-second interview answer: How do you validate JSON?

> I use four layers: Parse, Shape, Meaning, and Reference. First, I parse valid JSON and check content type and size. Next, I validate the OpenAPI or JSON Schema: object type, required fields, nested required fields, types, formats, ranges, arrays, allowed values, and unknown fields. Then I apply business rules and finally check outside facts such as whether the customer exists and whether the caller is allowed. I return a safe field-level `400` or the organization's documented `422` response. I test missing, null, empty, wrong-type, extra, and boundary cases.

## Recall - close the notes

1. Name the five main groups in an OpenAPI file.
2. How do YAML and JSON differ for OpenAPI?
3. How do you define bearer security?
4. What is the difference between `properties` and `required`?
5. Say the four JSON validation layers.
6. Does `additionalProperties: false` make fields required?

<details>
<summary>Answer key</summary>

1. Identity, Servers, Routes, Reuse, Security.
2. They are different serializations of the same OpenAPI model.
3. A security scheme with `type: http` and `scheme: bearer`, then apply it with `security`.
4. `properties` describes fields. The parent's `required` array makes them mandatory.
5. Parse, Shape, Meaning, Reference.
6. No. It controls unknown fields.

</details>

# 9. XML, XSD, XPath, XSLT, WSDL, and SOAP - P0

## One-line memory map

| Technology | One job |
|---|---|
| XML | Holds hierarchical data |
| XSD | Defines the allowed XML rules |
| XPath | Finds nodes and values in XML |
| XSLT | Changes XML into another structure |
| WSDL | Describes a SOAP service |
| SOAP | Carries an XML message |

Say this aloud:

> XML has data. XSD checks it. XPath finds it. XSLT changes it. WSDL describes the service. SOAP carries the message.

## XML - simple meaning

XML is a text format for hierarchical data. XML is case-sensitive.

### Parts inside an XML document

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- One example order -->
<ord:Order xmlns:ord="urn:company:orders" id="ORD-1001">
  <ord:Customer>A &amp; B Ltd</ord:Customer>
  <ord:Amount currency="USD">125.50</ord:Amount>
  <ord:Note><![CDATA[Leave at door <after 5pm>]]></ord:Note>
</ord:Order>
```

| Part | Example | Meaning |
|---|---|---|
| Declaration | `<?xml ...?>` | XML version and encoding |
| Root element | `ord:Order` | One top-level element |
| Child element | `ord:Customer` | Structured business data |
| Attribute | `id="ORD-1001"` | Metadata about an element |
| Text | `125.50` | Value inside an element |
| Namespace | `xmlns:ord="urn:company:orders"` | Identifies a vocabulary |
| Entity | `&amp;` | Escaped reserved character |
| CDATA | `<![CDATA[...]]>` | Text that may contain markup characters |
| Comment | `<!-- ... -->` | Human note, not business data |

### Element versus attribute

Use an element for structured, repeatable, or important business data. Use an attribute for short metadata about an element.

Attributes:

- Cannot contain child elements.
- Have no meaningful order.
- Must be quoted.

Do not turn this into a strict universal rule. Follow the agreed XSD or target contract.

### Well-formed versus valid XML

- **Well-formed:** XML syntax is correct. Tags match, nesting is correct, attributes are quoted, and there is one root.
- **Valid:** It is well-formed and also follows the XSD rules.

### Missing, empty, and nil

These are different:

```xml
<!-- Missing: no Name element -->

<!-- Empty: element exists with no content -->
<Name/>

<!-- Nil: explicitly no value -->
<Name xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:nil="true"/>
```

Nil needs the `xsi` namespace and the XSD element must allow it with `nillable="true"`. Occurrence rules still decide whether the element may be missing.

## XML namespaces

Namespaces prevent name collisions. A prefix is only a short alias.

These prefixes can mean the same namespace:

```xml
<a:Order xmlns:a="urn:company:orders"/>
<ord:Order xmlns:ord="urn:company:orders"/>
```

The URI `urn:company:orders` is the identity, not the prefix `a` or `ord`.

**Most common interview problem:** XPath returns nothing because the XML uses a namespace but the XPath did not bind and use that namespace.

## XSD - the XML rule book

XSD can define:

- Elements and attributes.
- Text, number, date, and other data types.
- Child element order.
- Required and optional values.
- Repeated values.
- Allowed values, patterns, and ranges.
- Namespaces.
- Whether nil is allowed.

### XSD words to recognize - do not memorize

| XSD item | Simple meaning |
|---|---|
| `xs:element` | Defines an element |
| `xs:attribute` | Defines an attribute |
| `xs:simpleType` | A value without child structure |
| `xs:complexType` | A value with children or attributes |
| `xs:sequence` | Children must appear in this order |
| `xs:choice` | One of the listed choices |
| `minOccurs` | Minimum number of occurrences |
| `maxOccurs` | Maximum number of occurrences |
| `xs:restriction` | Adds limits |
| `xs:enumeration` | Allowed values |
| `xs:pattern` | Allowed text pattern |
| `targetNamespace` | Namespace defined by this schema |
| `xs:include` | Adds another XSD in the same namespace |
| `xs:import` | Uses an XSD from another namespace |

### Small XSD example - recognize, do not memorize

```xml
<xs:schema
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    targetNamespace="urn:company:orders"
    xmlns:ord="urn:company:orders"
    elementFormDefault="qualified">

  <xs:element name="Order">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Customer" type="xs:string"/>
        <xs:element name="Amount" type="xs:decimal"/>
        <xs:element name="Note" type="xs:string" minOccurs="0"/>
      </xs:sequence>
      <xs:attribute name="id" type="xs:string" use="required"/>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

This means:

- The root is `Order`.
- `Customer` comes before `Amount`.
- `Note` is optional because `minOccurs="0"`.
- `id` is a required attribute.
- Elements belong to `urn:company:orders`.

XSD checks structure and values. It cannot prove that a real customer exists. That is a business or reference check.

## XPath - the address

XPath selects XML nodes or values.

```xpath
/ord:Order/ord:Customer
/ord:Order/@id
//ord:Line[ord:Quantity > 0]
```

- `/` follows an exact path from the root.
- `//` searches descendants.
- `` selects an attribute.
- `[...]` adds a condition.

When the XML has a namespace, bind that URI to a prefix in the XPath tool and use the prefix in the expression.

## XSLT - the transformation

XSLT reads XML, uses XPath to find values, and creates XML, HTML, or text output.

Common parts:

- `xsl:template`: rule for a matching node.
- `match`: which source node starts a rule.
- `xsl:value-of`: reads a value.
- `xsl:for-each`: repeats for selected nodes.
- `xsl:if` and `xsl:choose`: conditions.
- `xsl:apply-templates`: continues template processing.
- `xsl:param` and `xsl:variable`: named values.
- `xsl:output`: output type and settings.

### Small XSLT example - recognize, do not memorize

```xml
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:ord="urn:company:orders"
    exclude-result-prefixes="ord">

  <xsl:output method="xml" indent="yes"/>

  <xsl:template match="/ord:Order">
    <ErpOrder>
      <OrderNumber>
        <xsl:value-of select="@id"/>
      </OrderNumber>
      <CustomerName>
        <xsl:value-of select="ord:Customer"/>
      </CustomerName>
    </ErpOrder>
  </xsl:template>
</xsl:stylesheet>
```

This changes the source `ord:Order` into an `ErpOrder`.

### What to test in an XSLT

- Correct namespaces.
- Optional and missing elements.
- Repeated elements.
- Date and decimal formats.
- Empty and nil values.
- Special characters and encoding.
- Output against the target XSD.
- XSLT version supported by the runtime.

## XSD versus XPath versus XSLT

Use this exact short answer:

> XSD asks, “Is this XML allowed?” XPath asks, “Where is the value?” XSLT asks, “What should this XML become?” XSD validates, XPath selects, and XSLT transforms.

## SOAP - the XML message

## Memory hook

**Envelope -> Header -> Body -> Fault**

```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <CorrelationId>abc-123</CorrelationId>
  </soap:Header>
  <soap:Body>
    <CreateOrder>
      <OrderId>ORD-1001</OrderId>
    </CreateOrder>
  </soap:Body>
</soap:Envelope>
```

- **Envelope:** required outer container and SOAP version.
- **Header:** optional message metadata, security, addressing, or correlation.
- **Body:** required business request or response.
- **Fault:** standard SOAP error inside the Body.

A SOAP Header is inside the XML message. An HTTP header belongs to the transport request. They are not the same.

## WSDL - the SOAP service description

WSDL 1.1 normally describes:

- `types`: XSD data types.
- `message`: input and output messages.
- `portType`: operations.
- `binding`: protocol and message format.
- `service` and `port`: endpoint address.

Short answer:

> WSDL describes the SOAP service and how to call it. XSD describes the XML data allowed inside the messages.

## SOAP 1.1 versus SOAP 1.2 - P1

- SOAP 1.1 commonly uses `text/xml`.
- SOAP 1.2 commonly uses `application/soap+xml`.
- They use different Envelope namespace URIs.
- SOAP 1.1 commonly uses the `SOAPAction` HTTP header.
- SOAP 1.2 normally carries the action as an `application/soap+xml` content-type parameter.
- Follow the WSDL and target service contract.

Always inspect both the HTTP status and SOAP Fault. A useful business fault can exist inside the SOAP response.

TLS protects the network connection. WS-Security can add message tokens, signatures, or encryption when the SOAP contract requires it.

## REST JSON to SOAP XML flow

1. Receive the REST request.
2. Validate JSON shape and business rules.
3. Map it to a clear internal model.
4. Create canonical XML and validate it when a canonical XSD exists.
5. Transform with XSLT into the ERP structure.
6. Validate the final XML against the ERP XSD.
7. Add the SOAP Envelope and required Header.
8. Send with the correct SOAP version, action, content type, and security.
9. Inspect HTTP status and SOAP Fault.
10. Map the result back to the REST contract.
11. Log, monitor, and recover safely.

## XML security

For untrusted XML:

- Disable unsafe DTD and external entity processing where possible.
- Limit document size and processing time.
- Validate the expected schema.
- Do not log passwords, tokens, WS-Security headers, or full sensitive payloads.

This helps prevent XML External Entity attacks, often called XXE.

## 90-second interview answer: Explain the XML family

> XML stores hierarchical data. A well-formed XML document has correct syntax, while a valid document also follows its XSD. XSD defines elements, attributes, types, order, required and repeated values, namespaces, and limits. XPath selects nodes and values. XSLT uses XPath and templates to transform one XML structure into another.
>
> In SOAP, the Envelope is the outer message, the optional Header carries metadata or security, the Body carries business data, and a Fault carries a standard error. WSDL describes the SOAP operations, messages, binding, and endpoint, while XSD describes the data types. In an integration I pay special attention to namespaces, optional values, encoding, schema validation, SOAP Faults, and safe XML parser settings.

## Recall - close the notes

1. Say the six XML-family jobs.
2. Well-formed versus valid?
3. Missing versus empty versus nil?
4. What do `sequence`, `choice`, `minOccurs`, and `maxOccurs` mean?
5. Why can XPath return no result for a visible element?
6. Say the four SOAP parts.
7. SOAP Header versus HTTP header?
8. WSDL versus XSD?

<details>
<summary>Answer key</summary>

1. XML data, XSD rules, XPath address, XSLT transformation, WSDL service description, SOAP message.
2. Correct syntax versus correct syntax plus schema conformance.
3. No element, an element with no content, and an element explicitly marked with no value.
4. Ordered children, alternative children, minimum count, maximum count.
5. The namespace URI was not bound and used in the XPath.
6. Envelope, Header, Body, Fault.
7. SOAP Header is XML message metadata. HTTP header is transport metadata.
8. WSDL describes the SOAP service. XSD describes the XML structure and values.

</details>

# 10. Frends from an Interview View - P0

## Simple meaning

Frends is a low-code integration platform. You build visual Processes that connect APIs, files, databases, messages, and other systems.

Low-code does not remove engineering. You still need good contracts, security, validation, testing, deployment, monitoring, and support.

## Frends mental map

```text
Tenant
  -> Environments
      -> Agent Groups
          -> Agents that execute work

API request -> API Policy -> API Trigger -> Process
Other Trigger ---------------------------> Process
      -> Tasks, Decisions, Loops, Scopes, and Subprocesses
          -> Return result

Process Instances, logs, promoted values, metrics, and alerts
  -> operations and support
```

## Main terms

| Term | Simple meaning |
|---|---|
| Tenant | The main Frends organization boundary |
| Environment | DEV, TEST, UAT, PROD, or another managed stage |
| Agent | Runtime worker that executes integrations |
| Agent Group | A group of Agents targeted by integrations or policies |
| Process | Visual integration workflow |
| Trigger | Starts a Process by API, schedule, file, message, or event |
| Task | One action, such as an HTTP call or file operation |
| Decision | Chooses a branch based on a condition |
| Loop | Repeats work for items |
| Scope and Catch | Groups work and handles errors at a useful boundary |
| Subprocess | Reusable or separately managed flow called by a Process |
| API Policy | Runtime API access and behavior control |
| Process Instance | One execution of a Process |
| Promoted value | Searchable business or technical value for an execution |
| Environment variable | Setting that changes by environment |

## How the order integration maps to Frends

1. An OpenAPI operation defines the REST contract.
2. An API Policy controls incoming access.
3. An API Trigger starts the Order Intake Process.
4. The Process creates or keeps a correlation ID.
5. A validation step checks contract and business rules.
6. A Decision stops invalid work with a safe client response.
7. A Task or Subprocess checks the idempotency key.
8. Mapping creates the internal order model.
9. XML creation and XSLT produce the ERP shape, then target-XSD validation checks it.
10. An HTTP or SOAP Task calls the ERP.
11. A Scope and Catch classify errors.
12. Return maps the result to the API contract.
13. Promoted values expose order ID and correlation ID for support.

## How to keep a Process readable

- Name every step by business action: `Validate order`, not `Task 4`.
- Keep one clear responsibility in a Process or Subprocess.
- Use a Subprocess for repeated or separately owned logic.
- Keep expressions small and easy to test.
- Put URLs, timeouts, and environment settings in configuration.
- Put secrets in protected storage.
- Give Tasks clear input and output shapes.
- Use Decisions for visible business branches.
- Catch errors at a boundary where you can add useful context.
- Comment **why** a surprising choice exists, not what an obvious step does.
- Avoid one giant Process with many unrelated branches.

## Process versus Subprocess versus custom Task

- Use a **Process** for an end-to-end business flow.
- Use a **Subprocess** for reusable visual integration logic or a clear child flow.
- Use an existing **Task** for a normal connector or action.
- Use a **custom Task** only when reusable technical logic cannot be expressed clearly with supported Tasks.

Simple interview rule:

> Start with built-in Frends capabilities. Use custom .NET only when it gives a clear and reusable benefit.

## Environment configuration

Keep these outside hard-coded Process logic:

- Base URLs.
- Connection settings.
- Timeouts.
- Feature flags.
- Certificate references.
- Client IDs and secret references.
- Queue or folder names.

Before promotion, compare the configuration needed in the target environment. Never copy a production secret into a document or test payload.

## Deployment and versioning

Use this release lane:

**Requirement -> Review -> DEV -> TEST -> UAT -> Approval -> PROD -> Smoke test -> Monitor -> Reconcile**

Check:

- Process and Subprocess versions.
- Task or package dependencies.
- Environment variables and secret references.
- API Policy and Agent Group target.
- Certificates, network routes, and permissions.
- Trigger state.
- Deployment order.
- Rollback version and steps.

Rollback may mean deploying the last known good Process version, restoring configuration, or disabling the new trigger. The exact plan must be prepared before release.

## What to observe in Frends

Useful information:

- Process name and version.
- Environment and Agent Group.
- Start and end time.
- Duration.
- Success or failure.
- Error category.
- Retry attempt.
- Correlation ID.
- Safe business ID, such as order ID.
- Downstream operation and status code.

Do not log:

- Passwords or secrets.
- Access tokens.
- Full `Authorization` headers.
- Connection strings.
- Full sensitive customer payloads.

Promoted values are logged and searchable. Promote safe identifiers only; never promote a token, secret, or sensitive personal value.

An Agent Group may contain several Agents. Do not use one Agent's local memory or local file as shared idempotency state or a distributed lock. Use a suitable shared durable store with atomic concurrency control.

## 90-second interview answer: How would you design a Frends Process?

> I begin with the business flow and contract, not the visual canvas. I define the trigger, input, output, security, mapping, failure rules, and support needs. In Frends, I use an API Policy and API Trigger for an incoming API. The Process validates input, creates a correlation ID, makes clear Decisions, calls focused Tasks or Subprocesses, transforms the data, and returns a contract-safe result.
>
> I keep names business-focused, move environment settings and secrets outside the Process, and avoid a very large flow. I use Scope and Catch around meaningful failure boundaries. I classify permanent and temporary errors, add duplicate protection before retry, and promote a safe business ID for support.
>
> I test normal, negative, security, timeout, and recovery cases. I then promote the correct versions and configuration through environments, run a smoke test, watch Process Instances and alerts, and keep a rollback and reprocessing method.

## Likely Frends questions

### Why low-code instead of custom code?

> Low-code makes common integration steps visible, faster to build, and easier for support to follow. Custom code is still useful for specialized reusable logic. I choose the simplest option that remains testable, secure, maintainable, and supported.

### How do you reuse logic?

> I first look for a supported Task. For repeated workflow logic, I use a focused Subprocess with a clear input and output. For specialized technical logic, I consider a reviewed and tested custom Task.

### How do you handle errors?

> I catch errors at a meaningful boundary, keep the original cause, add operation and correlation context, classify the error, retry only eligible temporary failures, and return or record a safe result. I make failed work searchable and reprocessable.

Check the actual HTTP Task behavior: an HTTP `4xx` or `5xx` response may need explicit status inspection or a configured throw option. An unhandled-error Subprocess can record or notify after failure, but it cannot resume the failed Process.

## Recall - close the notes

1. Explain Tenant, Environment, Agent Group, and Agent.
2. What are the main parts of a Frends Process?
3. How would the order example map into Frends?
4. Process versus Subprocess versus custom Task?
5. What should be an environment setting?
6. What information should be searchable for support?

<details>
<summary>Answer key</summary>

1. Organization, lifecycle stage, runtime target group, and runtime worker.
2. Trigger, Tasks, Decisions, Loops, Scopes/Catches, Subprocesses, and Return.
3. Policy, API Trigger, validation, duplicate check, mapping, XML/XSLT, SOAP call, error handling, Return, promoted values.
4. End-to-end flow, reusable child flow, and specialized reusable .NET action.
5. URLs, connections, timeouts, feature flags, certificate and secret references.
6. Correlation ID, business ID, Process/version, stage, status, duration, attempt, and safe error.

</details>

# 11. Reliability, Release, and Production Support - P0

## First classify the failure

| Failure type | Examples | Normal action |
|---|---|---|
| Permanent input | Missing field, invalid value, bad XML | Reject and correct input |
| Authentication | Missing, invalid, or expired credential | Fix identity or credential |
| Authorization | Caller lacks role or resource access | Fix permission or request |
| Conflict | Duplicate ID or wrong resource state | Find current state and resolve |
| Temporary dependency | Connection reset, selected `5xx`, rate limit | Limited retry when safe |
| Unknown result | Timeout after sending work | Check target before retry |
| Internal defect | Null error, wrong mapping, unexpected exception | Stop, investigate, fix, test |
| Configuration | Wrong URL, certificate, secret, route, or permission | Correct through controlled change |

**Memory rule:** reject permanent failures. Retry temporary failures. Investigate unknown results before retrying.

## Retry

A good retry has:

- An error that is likely temporary.
- A small maximum attempt count.
- Increasing delay, called backoff.
- Some randomness, called jitter, so many clients do not retry together.
- A timeout on each attempt.
- Idempotency or another duplicate-safe design.
- Logs and metrics for each attempt.

Do not retry:

- Most validation errors.
- Invalid authentication or missing permission.
- A permanent business rejection.
- A timeout when the target may already have completed non-idempotent work.

## Idempotency

Idempotency prevents a repeated request from causing repeated business work.

One simple design:

1. Caller sends a stable `Idempotency-Key` or business ID.
2. Integration stores the key and request result.
3. A repeated request with the same key returns the stored result.
4. The target also uses a unique business key where possible.

The store must handle two requests arriving at the same time. A simple “check then insert” can race unless the key is unique and the operation is atomic.

## Timeout - the most important failure answer

Memory hook:

**Status unknown -> trace by key -> retry only when duplicate-safe -> reconcile**

90-second answer:

> A timeout only tells me that I did not receive the response in time. It does not prove the target failed. I keep the correlation ID and business or idempotency key. I check the target through a lookup, status API, log, or reconciliation record. If the target completed the work, I record success. If it proves no work happened, I may retry under a limited policy. For a create or payment operation, I never blindly retry without duplicate protection. I also review timeout settings and target duration, then monitor the rate of unknown outcomes.

## Circuit breaker - P1

A circuit breaker stops repeated calls to a failing dependency.

- **Closed:** calls flow normally.
- **Open:** calls are blocked for a short time.
- **Half-open:** a small test call checks recovery.

Retry handles a small temporary failure. A circuit breaker protects both systems during a wider outage. It is not a replacement for idempotency or recovery.

## Partial failure

Example: the ERP order succeeds, but sending the confirmation fails.

Possible actions:

- Retry only the confirmation.
- Store the completed ERP result and continue later.
- Use a compensation action if the business allows reversal.
- Mark the item for human review.
- Reconcile both systems.

Do not pretend a distributed flow is one database transaction. Make each completed step and recovery action explicit.

## Queues and delivery - P1

Many queues provide **at-least-once delivery**, so the same message may arrive more than once.

- Make the consumer idempotent.
- Acknowledge only after durable success.
- Put poison messages in a dead-letter queue after a bounded attempt count.
- Record the reason and safe identifiers.
- Replay at a controlled rate after the cause is corrected.
- Preserve order by business key only when the business requires it.
- Reconcile because queue delivery alone does not prove the target result.

When a dependency returns `429` with `Retry-After`, respect that guidance and still use a maximum retry limit.

## Logging and correlation

Each important log should help answer:

- Which request?
- Which Process and version?
- Which environment?
- Which step and target operation?
- What happened?
- How long did it take?
- Was it retried?
- What should support do next?

Use one correlation ID across systems. Also keep a safe business ID such as order ID. Do not use a random exception message as the only search key.

## Metrics and alerts

Useful metrics:

- Requests and completed records.
- Success and failure rate.
- Duration and slow percentiles.
- Retry count.
- Timeout count.
- Rate-limit responses.
- Queue depth or backlog age.
- Dead-letter or manual-review count.
- Missing expected executions.

A useful alert says what changed, how serious it is, and what support should check. Avoid an alert for every single temporary error.

## Release checklist

Before production:

- Contract and mapping approved.
- Normal and negative tests passed.
- UAT approved.
- API Policy, identity, and permissions tested.
- URLs, secrets, certificates, and network route verified.
- Versions and dependency order recorded.
- Logging, metrics, and alert routing checked.
- Reprocessing and reconciliation tested.
- Smoke test prepared.
- Rollback decision, owner, and steps written.
- Support and business owners informed.

After deployment:

1. Confirm the expected version and configuration.
2. Run the smoke test.
3. Find the execution by correlation ID.
4. Check the real target result.
5. Watch errors, duration, and backlog.
6. Reconcile the first business records.

## Incident response memory hook

**Impact -> Stabilize -> Find -> Fix -> Verify -> Learn**

### 1. Impact

What users, records, and time range are affected? Is data lost, delayed, duplicated, or exposed?

### 2. Stabilize

Stop unsafe retries, pause a trigger, reduce traffic, or use a known safe fallback. Preserve evidence.

### 3. Find

Trace one request using correlation ID and business ID. Find the first point where expected and actual behavior differ.

### 4. Fix

Make the smallest controlled correction. Use the release process.

### 5. Verify

Run a smoke test, monitor, and reconcile affected records. Do not call it fixed only because an error stopped.

### 6. Learn

Record the root cause, timeline, detection gap, and action owner. Add a test, alert, validation rule, or runbook step.

## Troubleshooting questions and answer paths - Reference

### Request never reaches the Process

Check in this order:

1. Caller URL, method, DNS, and connectivity.
2. TLS certificate and handshake.
3. Gateway or load balancer logs.
4. API Policy identity, path, method, and Agent Group.
5. Route and API Trigger state.
6. Agent health and inbound network access.
7. Process Instances and correlation ID.

### `401` or `403`

- `401`: check token presence, signature, issuer, audience, time, API key, or certificate.
- `403`: check scope, role, policy, method, resource ownership, and Agent Group target.

Do not solve `403` by weakening all access.

### `404`

Check the base URL, environment, path, API version, HTTP method, deployment, route, and trigger activation. A gateway `404` may be different from a business resource `404`.

### `500`

Use correlation ID to find the first internal exception. Check mapping assumptions, null values, Task input, custom component version, and the safe error boundary. Do not return the stack trace to the caller.

### `502`, `503`, or `504`

- `502`: gateway received a bad upstream result. Check upstream connection and response.
- `503`: service is unavailable or overloaded. Check health, capacity, maintenance, and throttling.
- `504`: upstream did not respond in time. Treat a write result as unknown until checked.

### Postman works but the application fails

Capture and compare the real requests:

- Method and full URL.
- Headers.
- Body and encoding.
- Content type and accept header.
- Token audience, scope, and expiry.
- Certificate.
- Proxy, DNS, and network path.
- Timeout.

Do not compare what the application “should send.” Compare what it actually sends.

### DEV works but UAT fails

Compare:

- URL and route.
- Environment variables and secret references.
- Certificate and trust chain.
- DNS, firewall, proxy, and Agent access.
- Policy, identity, scope, and role.
- Process, Subprocess, and Task versions.
- Test data and target permissions.
- Time and timezone.

### XML parser or XPath returns null

Check:

- Namespace URI and prefix binding.
- Exact path and root element.
- Case sensitivity.
- Missing versus empty element.
- SOAP Envelope around the business body.
- Encoding and hidden characters.
- Schema or version change.

### Intermittent timeout

Compare successful and failed executions:

- Target duration and time of day.
- Payload size.
- Connection pool or capacity.
- DNS and proxy path.
- Rate limit and retry pattern.
- Queue or thread backlog.
- Dependency health.

Use percentiles and a time range. One average can hide slow requests.

### Duplicate payment or order

First stop unsafe retries. Find all records with the business and idempotency keys. Determine the real target state. Use the approved reversal or compensation process, protect the customer, then fix the duplicate-control race and add a concurrency test.

## Recall - close the notes

1. Which errors should be retried?
2. What makes a retry safe?
3. Why is a timeout an unknown result?
4. Say the six incident steps.
5. What do you compare when Postman works but the application fails?
6. What do you check when XPath returns null?

<details>
<summary>Answer key</summary>

1. Only selected temporary errors.
2. Limit, backoff, timeout, duplicate protection, logs, and a temporary failure.
3. The target may have completed the work before the response was lost.
4. Impact, Stabilize, Find, Fix, Verify, Learn.
5. Actual method, URL, headers, body, encoding, token, certificate, network, and timeout.
6. Namespace, exact path, case, empty/missing value, Envelope, encoding, and schema version.

</details>

# 12. Essential .NET Perspective - P0/P1

You do not need to become a .NET developer tonight. Be able to explain how .NET affects integrations.

## .NET in one minute

> .NET is a managed application platform. C# is a common language used with it. The runtime executes managed code and provides memory management, type safety, exceptions, networking, configuration, logging, and libraries. Frends hides much of the code behind visual Processes and Tasks, but .NET knowledge helps when using expressions, understanding data types and errors, reviewing a custom Task, or troubleshooting serialization and HTTP behavior.

## System.Text is not System.Text.Json

- `System.Text` contains text tools such as UTF-8 `Encoding` and `StringBuilder`.
- `System.Text.Json` is the built-in modern .NET JSON serializer and JSON document API.
- `Newtonsoft.Json`, also called Json.NET, is a separate package.

At system boundaries, agree UTF-8 encoding, use `DateTimeOffset` or a clear UTC rule for timestamps, use `decimal` for money, and use invariant formats for machine-to-machine numbers and dates.

## Integration middleware versus ASP.NET Core middleware - P1

If the interviewer says “middleware,” clarify which meaning they intend.

- **Integration middleware** connects systems, transforms data, routes messages, and handles delivery.
- **ASP.NET Core middleware** is an ordered HTTP request pipeline.

An ASP.NET Core middleware component can inspect a request, call the next component, act on the response, or stop the pipeline. Common cross-cutting steps are exception handling, forwarded headers and HTTPS, correlation/logging, routing, authentication, authorization, rate limiting, and endpoints. Order matters. Put cross-cutting policy in middleware; keep business rules in the application or Process layer.

## Concepts to recognize - P1

| Concept | Simple meaning | Integration use |
|---|---|---|
| CLR/runtime | Executes managed .NET code | Runs Tasks and libraries |
| Type | Defines the shape of a value | Prevents invalid mapping assumptions |
| Assembly/package | Versioned compiled library | Task and dependency version |
| NuGet | .NET package system | Adds reviewed dependencies |
| Garbage collection | Reclaims managed memory | Does not remove the need to close external resources |
| Exception | Reports an abnormal failure | Must be classified, logged safely, and handled |
| Configuration | Values outside business logic | URLs, timeouts, feature flags |
| Dependency injection | Supplies services and dependencies | Makes custom code easier to test and configure |
| Async/await | Waits for I/O without blocking a worker | HTTP, file, database, and message calls |
| Cancellation | Stops work that is no longer useful | Shutdown, caller cancellation, or time budget |

## Async and HTTP

Simple answer:

> Integration work spends a lot of time waiting for networks, files, and databases. Async/await lets the worker wait without blocking a thread. I still need an explicit timeout, cancellation where supported, safe resource use, and error handling. Async does not make a slow dependency faster and does not make retries safe.

For custom .NET HTTP logic:

- Reuse managed HTTP clients or use the platform's client factory pattern.
- Set a time limit.
- Pass cancellation when appropriate.
- Validate status, headers, and body.
- Avoid logging tokens or sensitive bodies.
- Dispose response content or streams correctly.
- Add retry only for eligible failures and duplicate-safe operations.

Use built-in Frends HTTP Tasks when they meet the need.

## Exceptions

Good handling:

1. Catch at a boundary where you can act.
2. Keep the original error and stack information internally.
3. Add safe context: operation, correlation ID, and target.
4. Classify it as input, access, temporary, configuration, or defect.
5. Return a safe contract error.
6. Do not silently ignore it.

Avoid a broad catch that says “success” or removes the original cause.

## System.Text.Json versus Newtonsoft.Json - P0

Both convert between JSON and .NET values. This is called serialization and deserialization.

| System.Text.Json | Newtonsoft.Json |
|---|---|
| Built into modern .NET | Separate, mature package |
| Fast and commonly preferred for new .NET work | Very flexible and common in older systems |
| Strong modern .NET integration | Rich converters and JSON object model |

Standalone `System.Text.Json` property matching is case-sensitive by default, while ASP.NET web defaults are commonly case-insensitive. Unknown properties are normally ignored unless stricter behavior is configured. Always test the real host settings.
| Defaults can be stricter | Often easier for unusual legacy JSON |

### What can behave differently?

- Property naming and case matching.
- Null and missing values.
- Enum text versus number handling.
- Date and time parsing.
- Unknown properties.
- Comments and trailing commas.
- Reference loops.
- Polymorphic types.
- Custom converters.

For document-style access, System.Text.Json offers `JsonDocument` and `JsonNode`. Newtonsoft.Json offers `JObject` and `JToken`.

Do not enable unsafe Newtonsoft.Json type-name deserialization for untrusted JSON. Type metadata can create serious security risk when the allowed types are not tightly controlled.

Do not switch libraries without contract tests.

## 60-second answer: Which JSON library would you use?

> For a modern .NET integration, I normally start with System.Text.Json because it is built in, fast, and well supported. I would use Newtonsoft.Json when an existing solution depends on it or needs a feature or legacy behavior that is difficult to reproduce. The important point is not only performance. I compare naming, nulls, enums, dates, unknown fields, converters, and the exact JSON contract. Deserialization only creates a .NET object. I still validate required fields, business rules, authorization, and reference data.

## Serialization is not validation

These are separate:

- **Parsing:** Is the JSON syntax readable?
- **Deserialization:** Can it become a .NET value?
- **Schema validation:** Does it match the API contract?
- **Business validation:** Is the request allowed and meaningful?

A missing number might become a default value in some models. That is why the contract and required-field tests still matter.

## When to use custom .NET in Frends

Use custom code when:

- No supported Task handles the need clearly.
- The logic is technical, reusable, and stable.
- It can be tested and versioned.
- The team can own and support it.

Avoid custom code when:

- A built-in Task already solves the problem.
- It hides simple business flow from support.
- It embeds environment settings or secrets.
- It adds a package with no clear owner.

## .NET recall

1. Why does async help integration work?
2. System.Text.Json versus Newtonsoft.Json?
3. Why is deserialization not validation?
4. When is a custom Task reasonable?

<details>
<summary>Answer key</summary>

1. It avoids blocking a worker while waiting for I/O. It still needs timeout and error handling.
2. Built-in modern default versus mature flexible package; choose through contract needs and tests.
3. Creating an object does not prove required, business, permission, or reference rules.
4. For tested, reusable technical logic not clearly covered by supported Tasks.

</details>

---

# 13. Power Platform Perspective - P1

## Main parts

| Part | Simple purpose |
|---|---|
| Power Apps | Builds business user applications |
| Power Automate | Builds event, approval, and workflow automation |
| Dataverse | Managed business data platform |
| Connectors | Standard connection to services |
| Custom connector | Wraps a custom API for Power Platform use |
| On-premises data gateway | Provides controlled access to supported on-premises data sources |
| Solution | Packages apps, flows, connection references, and other components |
| Environment variable | Changes a setting by environment |
| Connection reference | Points a solution component to a connection |
| DLP policy | Controls which connector groups may be used together |

DLP means Data Loss Prevention.

## Power Platform lifecycle

Use the same SDLC:

1. Understand the user and business process.
2. Choose Apps, Automate, Dataverse, or an API.
3. Define data, permissions, connectors, limits, and ownership.
4. Build inside the correct environment.
5. Put components in a Solution.
6. Use environment variables and connection references.
7. Test normal, permission, failure, and volume cases.
8. Promote through environments.
9. Monitor runs, failures, ownership, and connector limits.
10. Support and improve.

Normal ALM practice is an unmanaged Solution in DEV and a managed Solution in controlled downstream environments. Actual credentials and connections are created or mapped in the target environment; a Solution carries connection references, not the secrets.

Use source control and pipelines where available. Prefer a durable service identity where the connector and policy support it, rather than one employee's account.

## Frends versus Power Platform

| Frends | Power Platform |
|---|---|
| Strong focus on system integration and middleware | Strong focus on business apps and workflow automation |
| Visual Processes for APIs, files, messages, and system flows | Apps and flows close to Microsoft 365 and business users |
| Useful for detailed transformations and integration operations | Useful for approvals, forms, user tasks, and standard connectors |
| Agent model can support controlled runtime placement | Cloud services with gateway options for supported on-premises access |

There is overlap. Choose using:

- Business user experience.
- Protocol and transformation complexity.
- Throughput and latency.
- Connector availability.
- On-premises access.
- Security and data policy.
- Error recovery and monitoring.
- Licensing and support ownership.

## Good combined design

Example:

1. A Power App collects an order request.
2. Power Automate manages approval.
3. A secured Frends API receives the approved request.
4. Frends validates, transforms, and calls the legacy SOAP ERP.
5. Frends returns or publishes status.
6. The app shows the user the result.

Power Platform handles the human workflow. Frends handles the system integration.

## 60-second comparison answer

> I see Frends mainly as an integration and middleware platform, while Power Platform is especially strong for business apps, approvals, and Microsoft-connected automation. Both are low-code and both require SDLC, security, environment management, monitoring, and ownership. I choose based on the user experience, protocol and transformation complexity, volume, recovery needs, connectors, on-premises access, policy, licensing, and the team that will support it. They can work together, with Power Platform handling the human workflow and Frends exposing a secure integration API.

## Power Platform risks to mention

- Personal owner account becomes disabled.
- Connection or consent expires.
- Connector throttling is reached.
- A flow is built outside a managed Solution.
- Environment values are hard-coded.
- DLP policy blocks a connector combination.
- User has app access but not data permission.
- On-premises gateway is offline.
- No support owner or run history retention plan exists.

Also remember:

- Dataverse security roles and row ownership control data access. Sharing an app does not automatically grant all required data access.
- DLP controls connector combinations; it is not user authorization.
- Power Automate Scopes and “configure run after” support try/catch/finally-style error paths.
- Configure retry and concurrency deliberately, and make repeated actions duplicate-safe.
- Check connector licensing, request limits, throttling, run history, and gateway high availability.
- A custom connector can expose an OpenAPI-described API to Power Platform.

# 14. The 15 Must-Know Interview Cards - P0

## Round 1: questions only

Do not look at the answers yet. Give yourself:

- 30 seconds for a definition question.
- 90 seconds for a process or scenario question.

### Card 1

**Walk me through a new integration from request to production.**

### Card 2

**Describe a middleware project and your role.**

### Card 3

**How would you design a clear Frends Process?**

### Card 4

**How do you secure an API end to end?**

### Card 5

**What is authentication versus authorization, and how does OAuth client credentials work?**

### Card 6

**What are the main sections and rules in an OpenAPI YAML or JSON file?**

### Card 7

**How do you define a security header and a normal custom header in OpenAPI?**

### Card 8

**How do you validate that all required JSON fields are present and valid?**

### Card 9

**Explain XML, XSD, XPath, and XSLT.**

### Card 10

**Explain a SOAP message. What is the difference between WSDL and XSD?**

### Card 11

**How do you handle retries, timeouts, and duplicate requests?**

### Card 12

**The integration works in DEV but fails in UAT. What do you do?**

### Card 13

**How do you investigate `401`, `403`, `404`, `500`, `502`, `503`, and `504`?**

### Card 14

**What do you need for deployment, monitoring, rollback, and support?**

### Card 15

**Compare System.Text.Json with Newtonsoft.Json, and explain where Frends and Power Platform fit.**

---

## Round 2: short answer key

### Card 1 answer - new integration

> I use Ask, Agree, Design, Build, Prove, Release, Run, and Improve. I clarify the goal and owners, agree the contract and acceptance criteria, design security and failures, build a small end-to-end path, test normal and abnormal cases, release with checked configuration and rollback, monitor and reconcile production, then improve from real use.

Key words: contract, mapping, security, idempotency, tests, smoke test, runbook.

Avoid: starting with the tool before explaining the business need.

### Card 2 answer - middleware project

> I connected a REST/JSON source to a SOAP/XML target through Frends. The flow authenticated the caller, validated input, kept a correlation ID, prevented duplicates, mapped the data, validated XML with XSD, transformed it with XSLT, called the SOAP service, and mapped the result back. Temporary and permanent errors were separated, and support had logs, alerts, replay, and reconciliation.

Key words: decouple, transform, orchestrate, recover, observe.

Avoid: claiming technology or results you did not really use.

### Card 3 answer - Frends Process

> I define the contract and business flow first. In Frends I use a suitable Trigger, clear business names, small Tasks, visible Decisions, focused Subprocesses, and Catch blocks at meaningful boundaries. I keep URLs and secrets in environment configuration. I add correlation, safe promoted values, error classification, duplicate protection, tests, deployment checks, and monitoring.

Key words: readable, reusable, configurable, observable.

Avoid: one very large Process and hard-coded settings.

### Card 4 answer - API security

> I use layers: HTTPS, caller authentication, operation and resource authorization, strict input validation, method and rate limits, protected secrets, safe errors, and audit evidence. For tokens I validate signature, issuer, audience, time, and scope or role. OpenAPI documents security, while the gateway or Frends API Policy enforces it.

Key words: Protect, Identify, Authorize, Validate, Limit, Hide, Observe.

Avoid: saying HTTPS or CORS is enough.

### Card 5 answer - identity and OAuth

> Authentication proves who or what is calling. Authorization checks what that identity may do. With client credentials, a service authenticates to the identity provider, receives a short-lived access token, sends it as a bearer token to the API, and the API validates it and checks the required permission.

Key words: identity, permission, token, audience, scope.

Avoid: sending the client secret to the business API.

### Card 6 answer - OpenAPI

> I remember Identity, Servers, Routes, Reuse, and Security. The document has the OpenAPI version, API info, base servers, paths and methods, reusable components, and security. Operations describe inputs and responses. Schemas describe properties, required fields, types, formats, limits, and allowed values. YAML and JSON carry the same model.

Key words: `openapi`, `info`, `servers`, `paths`, `components`, `security`.

Avoid: confusing the API version with the OpenAPI standard version.

### Card 7 answer - headers in OpenAPI

> Authentication belongs in `components.securitySchemes` and is applied through `security`. For example, bearer authentication uses type HTTP and scheme bearer. An API key uses type API key, location header, and its header name. A normal header such as correlation ID is an operation parameter with location header. The runtime must still enforce or emit the described behavior.

Key words: describe, enforce, verify.

Avoid: modeling `Authorization` as a normal parameter.

### Card 8 answer - JSON validation

> I use Parse, Shape, Meaning, and Reference. I check JSON syntax and size, then schema type, required fields, nested requirements, formats, ranges, allowed and extra fields. Next I check business rules. Finally I check outside facts and authorization. I test missing, null, empty, wrong-type, extra, and boundary values.

Key words: parent `required` array, nested rules, safe `400`.

Avoid: believing `properties` makes fields mandatory.

### Card 9 answer - XML family

> XML holds hierarchical data. XSD defines the allowed structure and values. XPath finds nodes and values. XSLT uses XPath and templates to transform XML. A well-formed document has correct XML syntax; a valid document also follows its XSD. I pay special attention to namespaces, because a missing namespace binding often makes XPath return no result.

Key words: data, rules, address, change.

Avoid: saying XSD transforms XML.

### Card 10 answer - SOAP

> A SOAP message has an Envelope, optional Header, Body, and Fault. The Header carries message metadata or security; the Body carries business data. WSDL describes operations, messages, binding, and endpoint. XSD describes the XML data types. A SOAP Header is part of XML, while an HTTP header is transport metadata.

Key words: Envelope, Header, Body, Fault.

Avoid: checking only HTTP status and ignoring a SOAP Fault.

### Card 11 answer - retry and duplicate safety

> I retry only selected temporary failures, with a limit, backoff, timeout, logs, and duplicate protection. A timeout gives an unknown result because the target may have succeeded. I search by business or idempotency key before retrying a write. I reject permanent input errors and reconcile source and target after uncertain outcomes.

Key words: unknown result, idempotency, limited retry, reconcile.

Avoid: blindly retrying every `5xx` or timeout.

### Card 12 answer - DEV versus UAT

> I reproduce the same request and use its correlation ID. I compare full URL and route, environment variables, secrets, certificate, DNS, firewall, proxy, API Policy, permissions, Process and dependency versions, target data, and time settings. I find the first actual difference before changing anything.

Key words: same request, compare environments, evidence.

Avoid: immediately changing code that already passed in DEV.

### Card 13 answer - status investigation

> I first identify which layer returned the code. For `401` I check the credential and token validation. For `403` I check permission. For `404` I check route, version, method, and resource. For `500` I trace the internal error. For `502`, `503`, and `504` I inspect gateway and dependency health, capacity, response, and timing. A timed-out write remains an unknown result.

Key words: layer, correlation, first difference, dependency.

Avoid: assuming every status came from the Frends Process.

### Card 14 answer - production readiness

> I need approved contracts and UAT, correct versions and configuration, tested identities and network access, a deployment order, smoke test, rollback plan, and owner. Operations need correlation and business IDs, safe logs, metrics, useful alerts, a runbook, replay controls, and reconciliation. After release I verify the real target result and watch the first executions.

Key words: release, verify, observe, recover, own.

Avoid: calling deployment successful only because no error appeared.

### Card 15 answer - .NET and platform choice

> System.Text.Json is built into modern .NET and is a good default. Newtonsoft.Json is a mature, flexible package often used for legacy or special JSON behavior. I compare the real contract and test casing, nulls, enums, dates, unknown fields, and converters. Frends is mainly for system integration and middleware. Power Platform is especially strong for business apps and workflows. They can work together.

Key words: contract tests, integration, human workflow.

Avoid: saying deserialization proves the request is valid.

# 15. Broader Non-Coding Question Bank - P1

Study this only after the 15 P0 cards. Use the cue words to build your own answer.

## Requirements and SDLC

1. **How do you handle unclear requirements?**  
   Cues: assumptions, sample messages, both owners, acceptance criteria, decision record.

2. **Agile versus Waterfall versus DevOps?**  
   Cues: ways to organize delivery; SDLC stages still exist; feedback speed; automation and operations.

3. **What information do you need for an API integration?**  
   Cues: owner, contract, examples, security, volume, SLA, mapping, failures, test system, support.

4. **How do you handle a breaking API change?**  
   Cues: consumers, new version, parallel support, migration, contract tests, deprecation date.

5. **What if the requirement changes during UAT?**  
   Cues: classify change versus defect, impact, approval, contract, tests, schedule, communication.

6. **What is your Definition of Done?**  
   Cues: contract, security, tests, UAT, configuration, release, rollback, monitor, runbook, owner.

## API design

7. **Synchronous versus asynchronous API?**  
   Cues: immediate result versus accepted work, latency, reliability, `202`, status or callback.

8. **REST versus SOAP?**  
   Cues: HTTP resource style and often JSON versus XML message contract and WSDL; choose by need.

9. **`400` versus `422`?**  
   Cues: malformed or contract-invalid versus semantic rule, follow one documented convention.

10. **How do you version an API?**  
    Cues: prefer compatible additions, version breaking changes, migration and deprecation.

11. **What is an API gateway or Frends API Policy for?**  
    Cues: entry control, identity, route/method, throttling, logging; business authorization can still be deeper.

12. **How do you compare a new API with an old or baseline API?**  
    Cues: same request; compare status, body, headers, content type, validation, side effects, timing, logs.

13. **What is an ETag and `If-Match` for?**  
    Cues: resource version, optimistic concurrency, prevent lost update.

14. **Rate limit versus timeout?**  
    Cues: control request amount versus limit waiting time; both need clear client behavior.

## Data and messages

15. **Schema validation versus business validation?**  
    Cues: allowed shape and type versus business meaning and external facts.

16. **How do you handle a new optional field?**  
    Cues: backward compatibility, defaults, old consumers, mappings, contract test.

17. **How do you handle a new required field?**  
    Cues: usually breaking, version or migration, old stored messages, consumer readiness.

18. **What is a canonical data model?**  
    Cues: internal stable shape, isolates systems, useful for several mappings, avoid unnecessary complexity.

19. **What is a dead-letter queue?**  
    Cues: messages that cannot complete, reason and context, correction, controlled replay, alert.

20. **What is eventual consistency?**  
    Cues: systems may differ for a period, status, retry, reconciliation, user expectation.

21. **How do you preserve message order?**  
    Cues: partition by business key, sequence/version check, do not assume global order.

## Security and operations

22. **How do you rotate a secret or certificate?**  
    Cues: owner, expiry alert, overlap if possible, protected update, test, rollback, remove old.

23. **What if a certificate expires in production?**  
    Cues: impact, stop unsafe retries, renew through owner, trust chain, controlled deploy, verify, add alert.

24. **What is least privilege?**  
    Cues: only needed operation, resource, environment, and duration.

25. **What should never be logged?**  
    Cues: token, secret, password, full auth header, connection string, unnecessary personal payload.

26. **What causes a retry storm?**  
    Cues: many clients retry together, no backoff/jitter/limit, dependency gets worse, circuit breaker/throttle.

27. **How do you reprocess failed work safely?**  
    Cues: correct cause, identify exact records, duplicate protection, approval, controlled rate, verify, reconcile.

28. **How do you prove no records were lost?**  
    Cues: source count, accepted count, target count, stable business IDs, status store, reconciliation exceptions.

## Power Platform

29. **Why can a Power Automate flow stop after an employee leaves?**  
    Cues: personal owner or connection, use managed ownership, service identity where supported, runbook.

30. **What is DLP in Power Platform?**  
    Cues: policy groups connectors to reduce unsafe movement of business data.

---

# 16. Four Scenario Drills - P0

## Scenario 1: Build a REST-to-SOAP integration

Prompt:

> A new portal sends JSON. A legacy ERP accepts SOAP XML. Explain the work from request to production.

Answer path:

1. Business goal, owners, volume, SLA, and data sensitivity.
2. OpenAPI, WSDL, XSD, examples, field mapping, and acceptance criteria.
3. REST entry security and caller permission.
4. JSON Parse, Shape, Meaning, and Reference checks.
5. Correlation and idempotency.
6. Internal mapping, XML, XSD, and XSLT.
7. SOAP Envelope, Header, action, content type, and Fault.
8. Timeout, retry, unknown result, and reconciliation.
9. Negative, security, failure, volume, and UAT tests.
10. Configuration, release, smoke test, monitor, rollback, and runbook.

## Scenario 2: The ERP timed out after an order was sent

Prompt:

> The Process got a timeout. The caller wants you to retry now.

Answer path:

1. Explain that the result is unknown.
2. Stop blind retries.
3. Use order ID, idempotency key, and correlation ID.
4. Search the ERP or reconciliation record.
5. Record success if the order exists.
6. Retry only if absence is proven and duplicate handling is safe.
7. Reconcile affected records.
8. Review timeout, target duration, and monitoring.

## Scenario 3: DEV works, UAT fails with `401`

Prompt:

> The same Process works in DEV. In UAT the target returns `401`.

Answer path:

1. Reproduce with the same request and correlation ID.
2. Confirm which system returned `401`.
3. Compare target URL and token endpoint.
4. Compare secret or certificate reference.
5. Check token signature, issuer, audience, time, and scope.
6. Check UAT identity registration and permission.
7. Check Agent clock and certificate chain.
8. Fix configuration through the normal path and add a pre-release check.

## Scenario 4: XML mapping suddenly returns empty values

Prompt:

> The source system released a change. The XML is visible, but XPath returns empty values.

Answer path:

1. Save a safe example and compare it with the old contract.
2. Check namespace URI, root name, path, case, and SOAP wrapper.
3. Check missing, empty, or nil values.
4. Check XSD and version change.
5. Correct namespace-aware XPath or XSLT.
6. Validate source and output.
7. Add regression examples and contract-change monitoring.
8. Reprocess only the affected records safely.

---

# 17. Prepare Your Real Project Story

Interviewers can tell when an answer is generic. Fill this in with facts from your real work.

## One-page truth sheet

- Business problem: ______________________________________________
- Source system and owner: _______________________________________
- Target system and owner: _______________________________________
- Trigger: _______________________________________________________
- Input format and contract: _____________________________________
- Output format and contract: ____________________________________
- Security method: _______________________________________________
- My personal role: ______________________________________________
- Main Process steps: ____________________________________________
- Hardest mapping or rule: _______________________________________
- Timeout and retry behavior: ____________________________________
- Duplicate protection: __________________________________________
- Logs and monitoring: ___________________________________________
- Test types: ____________________________________________________
- Release and rollback: __________________________________________
- One real problem I solved: _____________________________________
- Real result or value: __________________________________________

## STAR format

- **Situation:** Give only the needed context.
- **Task:** State your responsibility.
- **Action:** Explain what you personally did and why.
- **Result:** Give the real result and lesson.

### STAR prompt 1 - new feature

> A new integration or feature arrived. How did you take it through the full lifecycle?

### STAR prompt 2 - production incident

> Tell me about an integration failure. How did you find, fix, and prevent it?

### STAR prompt 3 - changing requirement

> Tell me about a requirement or contract that changed during delivery.

For each story, prepare:

- A 30-second version.
- A 90-second version.
- One technical follow-up.
- One teamwork follow-up.

Do not memorize a script word for word. Memorize **Situation -> Task -> three Actions -> Result**.

---

# 18. Final 40-Minute Mock Interview

Record your voice. Do not read.

## 00:00-00:05 - introduction

Answer:

- Tell me about yourself.
- Why integration and low-code platforms?

## 00:05-00:15 - project and lifecycle

Answer Cards 1, 2, and 3.

## 00:15-00:25 - contracts and security

Answer Cards 4, 6, 8, 9, and 10. Keep each answer short.

## 00:25-00:35 - production scenario

Choose two of the four scenario drills. Let yourself ask clarifying questions before answering.

## 00:35-00:40 - review

Score each area from `0` to `2`:

| Area | 0 | 1 | 2 |
|---|---|---|---|
| Clear structure | Rambling | Some order | Clear start, middle, end |
| Correct meaning | Wrong | Partly correct | Correct in simple words |
| Example | None | Generic | Real or clear example |
| Failure and security | Missing | Mentioned | Specific safe behavior |
| Ownership | Unclear | Mostly “we” | Clear team and personal role |

Maximum score: 10.

Review only answers scoring `0` or `1`. Do not restart the full guide.

## Speaking rules

- Start with the direct answer.
- Use four to seven key points.
- Give one example.
- Stop after 60 to 90 seconds.
- Let the interviewer ask for detail.
- If you do not know, say what you would check and how you would reduce risk.
- Do not invent experience.

# 19. Tomorrow Morning: One-Page Recall

Read only this section tomorrow morning.

## Your answer shape

**Meaning -> Purpose -> Example -> Safety**

Start directly. Use four to seven points. Stop after 60 to 90 seconds.

## Lifecycle

**Ask -> Agree -> Design -> Build -> Prove -> Release -> Run -> Improve**

Ask for goal, owners, systems, contract, mapping, volume, SLA, security, failures, acceptance criteria, and support.

Done means: approved contract, tested security and errors, UAT, correct configuration, smoke test, rollback, logs, alerts, replay, reconciliation, runbook, and owner.

## Middleware

**Receive -> Validate -> Route -> Transform -> Deliver -> Recover -> Observe**

Story order: **Problem -> Contract -> Flow -> Reliability -> Security -> Operations -> Result**

Example: REST/JSON portal -> Frends -> XML/XSLT -> SOAP ERP.

## API

HTTP request: **method + URL + headers + body**.  
HTTP response: **status + headers + body**.

- `401` = identity missing or invalid.
- `403` = identity known but not allowed.
- `404` = route or resource missing.
- `429` = rate limit.
- `500` = internal failure.
- `502` = bad upstream response.
- `503` = unavailable.
- `504` = upstream timeout.

## API security

**Protect -> Identify -> Authorize -> Validate -> Limit -> Hide -> Observe**

JWT checks: **Signature -> Issuer -> Audience -> Expiration -> Scope**.

OpenAPI describes. Frends policy or gateway enforces. Tests verify.

## OpenAPI

**Identity -> Servers -> Routes -> Reuse -> Security**

Main fields: `openapi`, `info`, `servers`, `paths`, `components`, `security`.

Authentication uses `securitySchemes`. A normal custom header uses a header `parameter`.

## JSON validation

**Parse -> Shape -> Meaning -> Reference**

`properties` describes fields. The parent `required` list makes them mandatory. Nested objects need their own required list. Missing, null, and empty are different.

## XML family

**XML has data. XSD checks. XPath finds. XSLT changes. WSDL describes. SOAP carries.**

Well-formed = correct XML syntax. Valid = also follows XSD.

Namespaces use the URI as identity. Wrong namespace binding often causes an empty XPath result.

SOAP: **Envelope -> Header -> Body -> Fault**.

## Reliability

Retry only selected temporary failures, with a limit, backoff, timeout, logs, and duplicate protection.

Timeout means **result unknown**. Search by business or idempotency key before retry. Then reconcile.

Incident: **Impact -> Stabilize -> Find -> Fix -> Verify -> Learn**.

## Final reminder

Use your real experience. Say what **you** did. If you do not know, explain what you would check and how you would make the decision safely.

---

# 20. Compact Glossary - Reference

| Term | Simple meaning |
|---|---|
| API | Contract that lets software communicate |
| API Policy | Runtime rules in front of API operations |
| Backoff | Longer wait between retry attempts |
| Canonical model | Internal data shape that separates source from target |
| Circuit breaker | Temporarily blocks calls to a failing dependency |
| Contract test | Checks that real behavior matches the API or message contract |
| Correlation ID | Identifier used to trace one request across systems |
| DLP | Power Platform policy controlling connector data movement |
| Idempotency | Repeating a request does not repeat the intended business effect |
| JWT | Common signed token format carrying claims |
| mTLS | TLS where both sides present certificates |
| OAuth 2.0 | Framework for obtaining and using access tokens |
| Orchestration | Controlling the order of several integration actions |
| Reconciliation | Comparing systems to find missing, duplicate, or different records |
| Regression test | Proves an old working behavior still works after change |
| Rollback | Return to a known safe version or configuration |
| Runbook | Steps for support to diagnose and recover |
| SLA | Agreed service level |
| Smoke test | Small test proving the released path is alive |
| TLS/HTTPS | Encrypts network traffic and authenticates the server certificate |
| UAT | User Acceptance Testing |
| WSDL | SOAP service description |
| XSD | XML schema rules |

---

# 21. OpenAPI JSON Form - Reference

This JSON describes the same kind of objects as the YAML examples:

```json
{
  "openapi": "3.0.1",
  "info": {
    "title": "Order API",
    "version": "1.0.0"
  },
  "paths": {
    "/orders": {
      "post": {
        "security": [
          {
            "BearerAuth": []
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/Order"
              }
            }
          }
        },
        "responses": {
          "202": {
            "description": "Accepted"
          }
        }
      }
    }
  },
  "components": {
    "securitySchemes": {
      "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
      }
    },
    "schemas": {
      "Order": {
        "type": "object",
        "required": ["orderId"],
        "properties": {
          "orderId": {
            "type": "string",
            "minLength": 1
          }
        }
      }
    }
  }
}
```

YAML and JSON differ in writing style, not OpenAPI meaning.

---

# 22. OpenAPI Object Map - Reference

Do not memorize this section. Use it when an interviewer asks for deeper YAML or JSON attributes.

## Parameter object

| Field | Meaning |
|---|---|
| `name` | Parameter name |
| `in` | `path`, `query`, `header`, or `cookie` |
| `required` | Whether it must be supplied; path parameters are always required |
| `description` | Human explanation |
| `schema` | Type and validation rules |
| `style` / `explode` | How arrays or objects are serialized |
| `example` / `examples` | Safe sample values |

## Request body object

- `required`: whether a body is required.
- `content`: media types such as `application/json`.
- `schema`: the request model.
- `example` or `examples`: safe sample messages.
- `encoding`: per-property encoding details for relevant media types.

## Response object

- `description`: required human meaning.
- `headers`: response headers such as `Retry-After`.
- `content`: media types and response schema.
- `links`: describes a possible relationship to another operation.

## Reusable components

`components` can hold schemas, responses, parameters, examples, request bodies, headers, security schemes, callbacks, and links. Reuse them with `$ref`.

## Swagger 2.0 versus OpenAPI 3.x

- Swagger 2.0 uses `swagger: "2.0"`, `host`, `basePath`, and `schemes`.
- OpenAPI 3 uses `openapi` and `servers`.
- Swagger 2.0 commonly uses body parameters and `definitions`.
- OpenAPI 3 uses `requestBody` and `components.schemas`.
- Convert with a tool, then review security, media types, null handling, and examples.

---

# 23. SDLC Evidence and API Testing - P1/Reference

## What each stage should produce

| Stage | Evidence or artifact | Exit check |
|---|---|---|
| Ask | Business goal, owner, scope | Problem and success are clear |
| Agree | User story, acceptance criteria, examples, mapping | Both system owners agree |
| Design | Data-flow diagram, contract, decision record, threat and failure review | Risks and behavior are understood |
| Build | Reviewed Process/version and configuration list | Thin path and failure paths work |
| Prove | Test cases, results, UAT evidence | Acceptance criteria pass |
| Release | Change record, deployment, smoke, rollback and communication plan | Target environment is ready |
| Run | Dashboard, alerts, runbook, replay and reconciliation steps | Support accepts ownership |
| Improve | Incident review, actions, updated tests and docs | Action owners and dates exist |

## Acceptance criteria

Use examples that can be tested:

> Given a valid order and an authorized caller, when the request is accepted, then the API returns the documented result and the same order appears once in the ERP.

Also write negative criteria for missing fields, access failure, duplicate work, timeout, and target rejection.

## Test levels

| Test | What it proves |
|---|---|
| Lint/static check | OpenAPI, JSON, XSD, or XSLT is structurally valid |
| Unit/mapping | One rule or transformation gives the expected result |
| Component | One Process or Subprocess works with controlled dependencies |
| Contract | Consumer and provider agree on messages and responses |
| Integration | Real connected systems communicate correctly |
| End-to-end | Full business path and final state work |
| Negative/security | Bad input and unauthorized actions are rejected safely |
| Performance | Volume, payload, latency, and concurrency targets are met |
| Resilience | Timeout, rate limit, outage, retry, and recovery work safely |
| Regression | Existing behavior still works after change |
| UAT | Business users accept the result |
| Smoke | Released production path is alive |
| Reconciliation | Source and target records agree |

Useful tools can include an OpenAPI linter, Postman/Bruno/curl for REST, SoapUI or an equivalent client for SOAP/WSDL, an XML/XSD validator, and the test and monitoring tools approved by the company. The interview point is the test purpose, not a brand name.

## Compare a new API with a baseline

Send the same meaningful request and compare:

1. Status code.
2. Response headers and content type.
3. Response body and field meaning.
4. Validation and error format.
5. Side effects and duplicate behavior.
6. Timing and timeout behavior.
7. Correlation logs and final target state.

Do not change a correct contract only to copy an old defect.

---

# 24. Integration Pattern Selector - P1/Reference

| Pattern | Choose it when | Main risks and controls |
|---|---|---|
| Synchronous API | Caller needs a quick final answer | Timeout, coupling, rate limit; use clear time budget |
| Asynchronous API | Work is slow or target availability varies | Status/callback, durable state, idempotency, reconciliation |
| Webhook | Provider pushes an event | Signature, timestamp, replay defense, retry contract |
| Queue/event | Buffering and loose coupling are needed | Redelivery, DLQ, ordering by key, backlog, idempotent consumer |
| File/SFTP | Partner or legacy system exchanges batches | Atomic pickup, checksum, encoding, duplicate file, archive/quarantine |
| Database/polling | No supported API/event exists | Least privilege, watermark, transaction, load, missed/duplicate rows |
| Schedule/batch | Work runs at a known time or window | Overlap lock, timezone/DST, chunking, checkpoint, partial batch |

## File flow

Use a temporary name while a file is being written, then atomically rename or otherwise signal completion. Validate name, size, encoding, delimiter, header/trailer, control totals, and content. Record a checksum or stable file ID. Move completed files to an archive and invalid files to quarantine. Never reprocess an entire file blindly after partial success.

## Database flow

Use a least-privilege identity and parameterized operations. For polling, keep a durable watermark plus a safe overlap and deduplicate. Understand transaction boundaries. Change Data Capture can reduce polling but still needs checkpoint, ordering, retention, and replay planning.

## Mapping checklist

For every field decide:

- Source of truth and owner.
- Required, optional, null, empty, and default behavior.
- Type, length, precision, and scale.
- Date, timezone, and daylight-saving rule.
- Decimal and currency rule.
- Code or enum translation.
- Array order and minimum/maximum count.
- Character encoding and escaping.
- Sensitive-data classification and log masking.

## Performance and backpressure

Measure normal and peak volume, payload size, latency percentiles, and target limits. Use bounded concurrency, batching or pagination where suitable, timeouts, queue limits, and controlled retry. Backpressure means slowing or buffering intake when the target cannot keep up.

---

# 25. Create and Release a Frends API - P1/Reference

Use this end-to-end answer:

1. Create or import the supported OpenAPI definition.
2. Review paths, operations, request/response models, examples, and security.
3. Create the API Trigger and attach the correct Process.
4. Build validation, mapping, target call, Return, and error paths.
5. Create the API Policy for the required paths, methods, identities, Agent Groups, throttling, and logging.
6. Add environment values, protected secrets, certificates, and dependency versions.
7. Test the Process directly, then test through the real API entry path.
8. Deploy through DEV, TEST, UAT, and PROD using the approved lifecycle.
9. Run a production smoke test and find its Process Instance by correlation ID.
10. Check the real downstream result, monitoring, alerts, replay controls, and reconciliation.

## Inbound versus outbound connectivity

- **Inbound:** caller -> DNS/TLS -> gateway or API Policy -> API Trigger -> Process.
- **Outbound:** Process/Agent -> DNS/proxy/firewall/TLS -> target service.

The Agent must be placed where it can reach required on-premises or private systems. Check both the network path and the application identity.

---

# 26. Production Scenario Pack - P1/Reference

| Scenario | First useful answer path |
|---|---|
| Gateway sees request; Process does not | Policy path/method -> Agent Group -> route/Trigger -> Agent health -> correlation logs |
| Slow but finally succeeds | Percentile timing -> slow stage -> target capacity -> payload/volume -> timeout budget; do not add blind retry |
| PROD database differs from DEV | Schema/version -> connection target -> permissions -> data/collation/timezone -> migration evidence |
| Intermittent `502` | Which gateway -> upstream connection/response -> time pattern -> load/DNS/proxy -> bounded retry |
| Expired certificate | Stabilize -> identify owner/chain -> renew and deploy safely -> verify -> add expiry alert |
| Duplicate broker message | Expect redelivery -> atomic idempotency key -> acknowledge after durable result -> reconcile |
| Retry storm | Stop or limit retries -> protect dependency -> backoff/jitter -> circuit breaker -> drain backlog slowly |
| Upstream `429` | Respect `Retry-After` -> reduce concurrency/rate -> bounded retry -> monitor quota |
| Poison message or DLQ | Record reason -> correct data or logic -> approve replay -> replay slowly -> verify |
| Wrong message order | Partition/serialize by business key -> sequence or version check -> make stale updates harmless |
| Eventual consistency | Explain temporary difference -> expose status -> retry/reconcile -> define acceptable delay |
| Rollback after writes | Roll back code/config separately from business compensation and in-flight-message recovery |

---

# 27. Behavioral and Interviewer Questions - P0/P1

## 45-second “Tell me about yourself”

Use four lines:

1. Your current role and years or type of experience.
2. The systems and integration problems you work with.
3. Your strongest relevant skills: contracts, Frends, APIs, XML/JSON, reliability, or support.
4. Why this role is the next logical step.

Do not list every tool. Connect your experience to the role.

## Why integration or low-code?

> I like solving the boundary between systems: agreeing clear contracts, transforming data safely, handling failure, and making the flow supportable. Low-code makes the business flow visible and speeds up common work, while .NET and API knowledge help me handle the technical edges correctly.

## Behavioral prompts to prepare

- A requirement was unclear.
- A stakeholder disagreed with your design.
- You found a mistake in your own work.
- Production failed under time pressure.
- Quality and a deadline conflicted.
- You improved monitoring or support.
- You learned a new platform quickly.
- You explained a technical issue to a non-technical person.

For each, use Situation -> Task -> three Actions -> Result -> Lesson.

## Five useful questions for the interviewer

1. What integrations and business systems would I own first?
2. How do you review, test, deploy, and roll back Frends changes?
3. How are production support, on-call work, and incident ownership organized?
4. Which API security, logging, and environment standards are mandatory?
5. What would good performance in the first 90 days look like?

Add real scale to your project truth sheet: records per day, peak volume, normal latency, SLA, users or systems affected, and a measurable result. Use only facts you can defend.

---

# 28. Official References - Reference

Do not read all of these tonight. Use them only to confirm a detail.

## Frends

- [Frends integration lifecycle](https://docs.frends.com/docs/frends-6.1.0/management-and-operations/integration-lifecycle)
- [Deploying integrations](https://docs.frends.com/guides/integration-management/deploying-integrations)
- [Setting up API Policies](https://docs.frends.com/guides/api-management/setting-up-api-policies)
- [Creating an API with Frends](https://docs.frends.com/guides/api-management/how-to-create-an-api-with-frends)
- [API Trigger reference](https://docs.frends.com/reference/triggers/api-trigger)

## API, JSON, and security

- [OpenAPI Specification](https://spec.openapis.org/oas/v3.1.1.html)
- [OpenAPI security guide](https://learn.openapis.org/specification/security.html)
- [JSON Schema object validation](https://json-schema.org/understanding-json-schema/reference/object)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

## XML and SOAP

- [W3C XML](https://www.w3.org/TR/xml/)
- [W3C XML Namespaces](https://www.w3.org/TR/REC-xml-names/)
- [W3C XSD](https://www.w3.org/TR/xmlschema11-1/)
- [W3C XSLT](https://www.w3.org/TR/xslt/)
- [W3C XPath](https://www.w3.org/TR/xpath-31/)
- [W3C SOAP 1.2](https://www.w3.org/TR/soap12/)

## .NET and Power Platform

- [System.Text.Json overview](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/overview)
- [Migrate from Newtonsoft.Json to System.Text.Json](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/migrate-from-newtonsoft)
- [Power Platform application lifecycle management](https://learn.microsoft.com/power-platform/alm/)
- [Power Platform data loss prevention policies](https://learn.microsoft.com/power-platform/admin/wp-data-loss-prevention)

---

# Final Stop Rule

When the eight hours finish:

1. Stop adding new topics.
2. Read the one-page recall once.
3. Prepare your real project truth sheet.
4. Sleep.

Clear, honest, structured answers will help more than another hour of passive reading.
