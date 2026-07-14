# Frends, .NET, APIs, and Power Platform

## Complete 8-Hour Interview Preparation Guide

**Target:** Mid-level .NET integration developer interviewing for a Frends-focused role  
**Study time:** Exactly 8 hours, including breaks  
**Primary focus:** API/integration engineering, a hands-on Frends design, security, SDLC, DevOps, and production support  
**Secondary focus:** Power Platform comparison  
**Prepared:** July 13, 2026

---

## Table of Contents

1. [How to Use This Guide](#1-how-to-use-this-guide)
2. [Exact 8-Hour Schedule](#2-exact-8-hour-schedule)
3. [Diagnostic and Essential .NET Refresh](#3-diagnostic-and-essential-net-refresh)
4. [API, Protocol, Data, and Integration Engineering](#4-api-protocol-data-and-integration-engineering)
5. [Frends Architecture and Development](#5-frends-architecture-and-development)
6. [Hands-On Frends Order Integration](#6-hands-on-frends-order-integration)
7. [Power Platform Essentials](#7-power-platform-essentials)
8. [Security, SDLC, DevOps, and Production Support](#8-security-sdlc-devops-and-production-support)
9. [Interview Question Bank and Mock Interview](#9-interview-question-bank-and-mock-interview)
10. [Final Recall Sheet](#10-final-recall-sheet)
11. [Official References](#11-official-references)

---

# 1. How to Use This Guide

This is not a book to read passively. It is an eight-hour interview workout. The goal is to **retrieve, apply, and explain** the important material tomorrow.

## The 20-15-10-5 study cycle

For a normal 50-minute block:

1. **20 minutes - Learn:** Read only the marked high-priority material.
2. **15 minutes - Apply:** Trace a worked example or perform the exercise.
3. **10 minutes - Retrieve:** Close the guide and answer aloud from memory.
4. **5 minutes - Correct:** Check your answer and write only missing keywords.

The longer API and lab blocks have their own timing instructions.

## Confidence system

- **Green:** I can define it, give an example, and discuss one failure mode.
- **Yellow:** I recognize it but cannot explain it cleanly.
- **Red:** I do not understand it or confuse it with another concept.

Spend correction time on red and yellow items. Do not reread green items.

## Technical-answer framework

```text
1. Definition
2. Concrete example
3. Main risk or tradeoff
4. Mitigation
5. Monitoring or testing
```

Example:

> Idempotency means repeating the same logical request has no additional business effect. For an order API, I would use the order ID or an idempotency key with a durable unique record. The risk is that an HTTP timeout may occur after the downstream order was created. I would query the destination before retrying and keep retries bounded. I would monitor duplicates, unknown outcomes, and reconciliation differences.

## Cognitive rules for today

- Speak answers aloud. Recognition is not interview recall.
- Draw architectures from memory rather than copying them.
- Use one order-processing scenario across all topics to reduce cognitive load.
- Stop a failed recall attempt after roughly two minutes, check the answer, and try again later.
- Keep one final recall page. Do not create extensive separate notes.
- During breaks, move away from the screen. Avoid social media and new technical material.
- Finish at least one hour before sleep. A normal full night of sleep is more valuable than late-night passive rereading.

---

# 2. Exact 8-Hour Schedule

| Clock | Duration | Activity | Required output |
|---|---:|---|---|
| 00:00-00:10 | 10 min | Diagnostic | Red/yellow/green topic list |
| 00:10-00:45 | 35 min | Essential C# and .NET | Explain async, DI, disposal, testing |
| 00:45-00:55 | 10 min | Break | Move and hydrate |
| 00:55-02:05 | 70 min | APIs, protocols, data, integration | Draw request flow and failure policy |
| 02:05-02:15 | 10 min | Break | No technical input |
| 02:15-03:00 | 45 min | Frends architecture | Redraw Frends mental model |
| 03:00-03:15 | 15 min | Food and movement | Leave the desk |
| 03:15-04:30 | 75 min | Hands-on Frends order exercise | Working design plus failure tests |
| 04:30-04:40 | 10 min | Break | No technical input |
| 04:40-05:45 | 65 min | Security, SDLC, DevOps, operations | Incident and deployment walkthrough |
| 05:45-05:55 | 10 min | Break | Move and hydrate |
| 05:55-06:25 | 30 min | Power Platform comparison | Two-minute Frends comparison |
| 06:25-06:35 | 10 min | Break | No technical input |
| 06:35-07:20 | 45 min | Mixed interview and system design | Timed spoken answers |
| 07:20-07:30 | 10 min | Break | Reset before mock interview |
| 07:30-08:00 | 30 min | Mock interview and consolidation | Final recall sheet |

**Total: 480 minutes = 8 hours.**

---

# 3. Diagnostic and Essential .NET Refresh

## 3.1 Ten-minute diagnostic

Close the rest of this document. Give yourself one minute per question.

1. Explain `Process`, `Subprocess`, `Task`, `Trigger`, `Agent`, and `Agent Group` in Frends.
2. What does `async`/`await` do, and why should library code accept a `CancellationToken`?
3. Describe the OAuth 2.0 client-credentials flow.
4. Differentiate a timeout, HTTP `429`, HTTP `400`, and HTTP `500`.
5. A downstream `POST` times out. Is retrying safe?
6. When should logic use a Frends Code Task, Custom Task, Subprocess, or external .NET service?
7. What should never be written to production logs?
8. How would you deploy and roll back a Frends Process?
9. How would you detect that a scheduled integration did not run at all?
10. Compare Frends with Power Automate in two minutes.

### Diagnostic key

| Question | Essential keywords |
|---|---|
| 1 | BPMN Process, reusable Subprocess, operation Task, event Trigger, runtime Agent, deployment target Agent Group |
| 2 | Non-blocking wait, continuation, propagated cancellation, timeout/user shutdown |
| 3 | Token endpoint, client identity/credential, scoped token, Bearer token, expiry |
| 4 | Local/transport limit, throttling, caller/contract error, server/dependency error |
| 5 | Outcome unknown; idempotency key or destination lookup before retry |
| 6 | Small local mapping, reusable orchestration, packaged code, independently owned/scaled service |
| 7 | Secrets, tokens, auth headers, private keys, connection strings, unnecessary personal data |
| 8 | Test exact version/dependencies/configuration, Agent Group deployment, smoke test, older known-good version |
| 9 | Expected-execution or missing-execution monitoring, not only error alerts |
| 10 | Frends for hybrid backend integration; Power Platform for Microsoft/user-centric apps and workflows |

## 3.2 C# and .NET essentials

### `async` and `await`

- An `async` method normally returns `Task`, `Task<T>`, `ValueTask`, or `ValueTask<T>`.
- `await` asynchronously waits and later continues the method; it does not automatically create a thread.
- Async I/O improves scalability because a thread is not blocked while network, file, or database I/O is pending.
- Avoid `.Result`, `.Wait()`, and unnecessary `Task.Run` around I/O work.
- Pass a `CancellationToken` through every supporting layer.
- Use explicit timeouts as well as cancellation. They solve related but different problems.
- Avoid `async void` except event handlers because callers cannot await or reliably observe failures.

### Exception handling

- Catch only when you can add context, translate, recover, or guarantee cleanup.
- Preserve the stack trace with `throw;`, not `throw ex;`.
- Do not use exceptions for ordinary validation branches.
- Separate transient dependency failures from permanent business/contract failures.
- Do not log the same exception at every layer; choose an ownership boundary.
- Never swallow an exception without a deliberate, observable outcome.

### Interfaces, dependency injection, and SOLID

- **Single responsibility:** One component has one cohesive reason to change.
- **Open/closed:** Extend behavior through abstractions instead of continually modifying one central conditional.
- **Liskov substitution:** Implementations honor their abstraction's promises.
- **Interface segregation:** Prefer focused interfaces over large dependency surfaces.
- **Dependency inversion:** High-level behavior depends on abstractions, not infrastructure details.

Dependency injection makes dependencies explicit and replaceable in tests. It does not mean every class needs an interface. Add abstractions at external boundaries or where multiple implementations/testing justify them.

### Resource management

- `IDisposable` represents deterministic cleanup of unmanaged or owned resources.
- `using`/`await using` ensures cleanup on failure.
- Do not create and dispose `HttpClient` per request. Use `IHttpClientFactory` or a deliberately long-lived client.
- Open database connections late, close them early, and rely on pooling.
- Know whether disposing a stream wrapper also closes its underlying source.

### Configuration and secrets

- Use typed options/configuration for normal settings.
- Separate development, test, and production values.
- Do not hard-code credentials or commit them to source control.
- Validate required configuration during startup or deployment checks.
- Common configuration keys may have different values in every environment.

### Testing layers

| Layer | What it proves | Example |
|---|---|---|
| Unit | Isolated logic | Invalid amount is rejected |
| Component | One Process/API component | `400` is not retried |
| Contract | Schema compatibility | Response matches OpenAPI |
| Integration | Real boundary works | Test Agent reaches test SQL/API |
| Smoke | Critical deployed path works | One test order completes |
| Failure | Recovery policy works | `429` honors delay and stops |
| Reconciliation | Business result is correct | Source/destination counts match |

## 3.3 Async API client example

```csharp
using System.Net.Http.Json;
using System.Text.Json;

public sealed record CreateOrderRequest(
    string OrderId, string CustomerId, decimal Amount, string Currency);

public sealed record CreateOrderResponse(
    string OrderId, string Status, string CorrelationId);

public sealed class OrderClient(HttpClient httpClient)
{
    private static readonly JsonSerializerOptions JsonOptions =
        new(JsonSerializerDefaults.Web);

    public async Task<CreateOrderResponse> CreateAsync(
        CreateOrderRequest request,
        string accessToken,
        string correlationId,
        CancellationToken cancellationToken)
    {
        using var message = new HttpRequestMessage(HttpMethod.Post, "orders")
        {
            Content = JsonContent.Create(request, options: JsonOptions)
        };
        message.Headers.TryAddWithoutValidation("X-Correlation-ID", correlationId);
        message.Headers.TryAddWithoutValidation("Idempotency-Key", request.OrderId);

        using var response = await httpClient.SendAsync(
            message, HttpCompletionOption.ResponseHeadersRead, cancellationToken);
        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<CreateOrderResponse>(
                   JsonOptions, cancellationToken)
               ?? throw new JsonException("The response body was empty.");
    }
}
```

Be ready to explain injection, cancellation, correlation versus idempotency, unknown timeout outcomes, and typed failures.

## 3.4 Closed-book .NET recall

1. Does `await` create a new thread?
2. When should you use `Task.Run`?
3. Why is `.Result` undesirable?
4. Cancellation versus timeout?
5. Why use `IHttpClientFactory`?
6. When should you catch an exception?
7. How would you unit-test `OrderClient`?
8. What should be tested without a network dependency?

### Model answers

1. No. It registers a continuation and releases the thread while asynchronous I/O is incomplete.
2. Primarily for appropriate CPU-bound work, not to disguise synchronous I/O.
3. It blocks a thread, reduces throughput, and can contribute to deadlocks in some contexts.
4. Cancellation requests that work stop; a timeout stops waiting after a duration and is often implemented with cancellation.
5. It manages handlers/connections while supporting named or typed configuration and injection.
6. When you can recover, translate, add context at an ownership boundary, or guarantee cleanup.
7. Inject a controlled `HttpMessageHandler`; assert method, headers, and body; return known responses; verify mapping and cancellation.
8. Validation, mapping, status classification, idempotency decisions, and retry-decision logic.

---

# 4. API, Protocol, Data, and Integration Engineering

## 4.1 Exact 70-minute routine

| Minutes | Activity |
|---:|---|
| 0-4 | Closed-book pre-test |
| 4-16 | HTTP and status codes |
| 16-19 | Recall without notes |
| 19-29 | Authentication and OAuth |
| 29-32 | Draw OAuth from memory |
| 32-43 | OpenAPI, YAML, SOAP/XML/XSLT, JSON |
| 43-46 | Explain the data path aloud |
| 46-59 | Patterns and reliability |
| 59-64 | Work the failure matrix |
| 64-70 | Deliver the final design answer |

Before reading, answer:

1. When is a retry unsafe?
2. What is the difference between `401`, `403`, and `429`?
3. How do you know whether a timed-out `POST` succeeded?
4. Why should a database transaction not remain open during an HTTP call?

## 4.2 HTTP request and response anatomy

```http
POST /api/v1/orders HTTP/1.1
Host: integration.example.com
Authorization: Bearer eyJ...
Content-Type: application/json
Accept: application/json
X-Correlation-ID: 563885df-e152-4d31-a64d-4819d97b9997
Idempotency-Key: ORD-1001

{
  "orderId": "ORD-1001",
  "customerId": "CUS-101",
  "amount": 249.95,
  "currency": "USD"
}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/orders/ORD-1001
X-Correlation-ID: 563885df-e152-4d31-a64d-4819d97b9997

{
  "orderId": "ORD-1001",
  "status": "accepted",
  "correlationId": "563885df-e152-4d31-a64d-4819d97b9997"
}
```

An HTTP request has a method, target URI, headers, and optional body. A response has a status code, headers, and optional body.

### Important headers

| Header | Purpose |
|---|---|
| `Authorization` | Credential/token for the request |
| `Content-Type` | Format of the body being sent |
| `Accept` | Formats the client can receive |
| `Location` | URI of a created or redirected resource |
| `Retry-After` | Server guidance after throttling/unavailability |
| `ETag` / `If-Match` | Conditional update and optimistic concurrency |
| `Cache-Control` | Caching rules |
| `X-Correlation-ID` | Cross-system trace identifier |
| `Idempotency-Key` | Stable key suppressing duplicate business effects |

Do not put secrets or sensitive personal data in URLs because URLs are commonly logged.

## 4.3 HTTP methods

| Method | Typical meaning | Safe? | Idempotent? |
|---|---|---:|---:|
| `GET` | Read a representation | Yes | Yes |
| `HEAD` | Read headers without body | Yes | Yes |
| `POST` | Create or execute a command | No | No |
| `PUT` | Replace/create at a known URI | No | Yes |
| `PATCH` | Partially update | No | Not guaranteed |
| `DELETE` | Remove a resource | No | Yes |

**Safe** means the intended operation is read-only. **Idempotent** means repeating the same request has the same intended effect as performing it once. It does not mean every response is identical.

## 4.4 HTTP status codes

| Code | Meaning | Interview use/retry decision |
|---:|---|---|
| `200 OK` | Completed success | Read/update or replayed stored result |
| `201 Created` | Resource created | Prefer a `Location` header |
| `202 Accepted` | Accepted, not completed | Persist/queue first; expose status |
| `204 No Content` | Success without body | Delete/update without representation |
| `304 Not Modified` | Cache remains valid | Conditional GET |
| `400 Bad Request` | Malformed/invalid request | Do not retry unchanged |
| `401 Unauthorized` | Authentication missing/invalid | Renew/fix credential, not ordinary retry |
| `403 Forbidden` | Identity lacks permission | Fix authorization |
| `404 Not Found` | Resource absent | Usually permanent; context matters |
| `405 Method Not Allowed` | Wrong method | Fix caller/contract |
| `409 Conflict` | State/idempotency conflict | Query or resolve current state |
| `412 Precondition Failed` | ETag/precondition failed | Reload and resolve concurrency |
| `415 Unsupported Media Type` | Wrong `Content-Type` | Fix request |
| `422 Unprocessable Content` | Semantic validation failed | Correct business data |
| `429 Too Many Requests` | Rate limited | Bounded delay; honor `Retry-After` |
| `500 Internal Server Error` | Unexpected server failure | Sometimes bounded retry |
| `502 Bad Gateway` | Unusable upstream response | Often transient |
| `503 Service Unavailable` | Temporarily unavailable | Often transient; honor delay |
| `504 Gateway Timeout` | Upstream timed out | Outcome may be unknown |

Never say "retry every `5xx`." Retry only when the operation is duplicate-safe, the error is plausibly transient, and delay/attempts are bounded.

## 4.5 Authentication and authorization

- **Authentication:** Who or what is calling?
- **Authorization:** What may that identity do?

| Mechanism | Typical use | Main concern |
|---|---|---|
| API key | Simple client identification | Long-lived shared secret; limited identity semantics |
| Basic | Legacy username/password over TLS | Credential exposure and rotation |
| OAuth 2.0 client credentials | Service-to-service access | Scope, audience, credential lifecycle |
| JWT bearer token | Signed access-token format | Signature, issuer, audience, expiry, claims |
| Client certificate/mTLS | Strong service/transport identity | Distribution and rotation |

### OAuth 2.0 client-credentials flow

```text
Frends Process/client
    |
    | POST token endpoint:
    | client identity + credential + requested scope
    v
Authorization server
    |
    | short-lived access token
    v
Frends Process/client
    |
    | Authorization: Bearer <token>
    v
Resource API validates signature/issuer/audience/expiry/claims
```

Interview points:

- Client credentials represents an application, not a signed-in user.
- Cache a valid token until near expiry instead of requesting one per record.
- Never log the token or client secret.
- Validate issuer, signature, audience, expiry, and required permissions.
- A valid token does not automatically authorize every business object.
- JWT is a token format; OAuth is an authorization framework. OAuth tokens can be JWTs or opaque strings.

## 4.6 API contract design

A good API contract is explicit, consistent, bounded, versioned deliberately, independent from internal tables, and documented with realistic examples.

Usually backward compatible:

- Add an optional response property when consumers tolerate unknown fields.
- Add an optional request property with default behavior.
- Add a new endpoint.

Usually breaking:

- Rename/remove a property or change its type.
- Make an optional request property required.
- Change enum/status/error semantics without consumer tolerance.
- Change authentication or required permissions.

Use a consistent error model such as Problem Details-style fields:

```json
{
  "type": "https://example.internal/problems/validation",
  "title": "Order validation failed",
  "status": 400,
  "code": "validation_error",
  "correlationId": "563885df-e152-4d31-a64d-4819d97b9997",
  "errors": [
    { "field": "amount", "message": "Amount must be greater than zero." }
  ]
}
```

Do not return stack traces, SQL, credentials, internal URLs, or raw downstream errors to callers.

## 4.7 Swagger and OpenAPI

**Swagger** originally named the description specification and tools. The specification became the **OpenAPI Specification (OAS)**. Today Swagger commonly names tools such as Swagger UI and Swagger Editor. Say "OpenAPI contract," while recognizing teams often say "Swagger file."

Current Frends documentation primarily supports OpenAPI `3.0.1`, with `2.0` retained for legacy APIs. Confirm tenant/runtime support before using newer OAS features.

### OpenAPI/Swagger rules to remember

1. Use a platform-supported OAS version.
2. Provide `info.title` and a semantic API version.
3. Give each operation a stable, unique `operationId`.
4. Choose paths/methods according to resource semantics.
5. Document every expected success and error response.
6. Quote YAML response keys such as `'200'` so they remain strings.
7. Put reusable schemas and security schemes under `components`.
8. Use `$ref` to avoid duplicated schemas.
9. Define request and response media types explicitly.
10. Mark required fields with the schema-level `required` array.
11. Add constraints: length, range, pattern, enum, and format.
12. Define security requirements, but enforce them with the platform/API Policy.
13. Include realistic examples without secrets or real personal data.
14. Validate the document using an OpenAPI validator/editor.
15. Treat the contract as a reviewed, versioned SDLC artifact.
16. Contract-test implementation responses.
17. Coordinate breaking changes with a new version or migration plan.

### Common mistakes

- Using property-level `required: true` instead of schema `required: [field]`.
- Documenting authentication but not enforcing it.
- Returning undocumented codes or shapes.
- Using a server URL incompatible with the deployed Frends route.
- Reusing one vague object for every request and response.
- Exposing database models directly.
- Omitting error schemas/examples.
- Assuming every consumer ignores added fields.

### Interview order API in OpenAPI 3.0.1

```yaml
openapi: 3.0.1
info:
  title: Interview Order API
  version: 1.0.0
servers:
  - url: /api/interview-orders
paths:
  /orders:
    post:
      operationId: submitOrder
      summary: Validate and submit an order
      parameters:
        - in: header
          name: Idempotency-Key
          required: true
          schema:
            type: string
            minLength: 1
            maxLength: 100
        - in: header
          name: X-Correlation-Id
          required: false
          schema:
            type: string
            maxLength: 64
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrderRequest'
      responses:
        '200':
          description: Previously completed result replayed
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
        '201':
          description: Order created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/OrderResponse'
        '202':
          description: Order already being processed
        '400':
          description: Invalid request
          content:
            application/problem+json:
              schema:
                $ref: '#/components/schemas/Problem'
        '409':
          description: Idempotency or state conflict
        '503':
          description: Temporary dependency failure
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    OrderRequest:
      type: object
      additionalProperties: false
      required: [orderId, customerId, amount, currency, requestedAt]
      properties:
        orderId:
          type: string
          minLength: 1
          maxLength: 50
          example: ORD-1001
        customerId:
          type: string
          minLength: 1
          maxLength: 50
          example: CUS-101
        amount:
          type: number
          format: decimal
          minimum: 0.01
          example: 249.95
        currency:
          type: string
          pattern: '^[A-Z]{3}$'
          example: USD
        requestedAt:
          type: string
          format: date-time
    OrderResponse:
      type: object
      required: [orderId, status, correlationId, replayed]
      properties:
        orderId:
          type: string
        status:
          type: string
          enum: [submitted, processing, rejected]
        externalOrderId:
          type: string
          nullable: true
        correlationId:
          type: string
        replayed:
          type: boolean
    Problem:
      type: object
      required: [title, status, code, correlationId]
      properties:
        type:
          type: string
          format: uri
        title:
          type: string
        status:
          type: integer
        code:
          type: string
        correlationId:
          type: string
security:
  - bearerAuth: []
```

In Frends, API Policies determine actual access. The OpenAPI security section documents the intended scheme but does not replace enforcement.

## 4.8 YAML, RAML, and RML

### YAML (`.yaml` or `.yml`)

YAML is a human-readable data serialization language. OpenAPI documents are commonly written in YAML or JSON.

- Indentation is significant; use spaces, not tabs.
- A mapping is a key/value structure.
- A sequence uses `-` items.
- Quote ambiguous values where a parser may infer the wrong type.
- Keep reusable definitions centralized and validate the document.
- Never commit secrets merely because YAML is convenient.

`.yaml` and `.yml` represent the same format; `.yaml` is often preferred for clarity.

### RAML

**RAML** means RESTful API Modeling Language. It is another YAML-based language for describing REST APIs, but it is not OpenAPI. Use RAML-aware tooling or a tested conversion rather than assuming an OpenAPI parser accepts it.

### RML

"RML" can mean different technologies. In data integration it often means **RDF Mapping Language**, which describes mappings from heterogeneous data into RDF. It is not a normal synonym for RAML. If an interviewer says "RML," ask which meaning their project uses. If they mean RAML, confirm before answering.

## 4.9 XML fundamentals

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ord:Order xmlns:ord="urn:example:orders:v1">
  <ord:OrderId>ORD-1001</ord:OrderId>
  <ord:CustomerId>CUS-101</ord:CustomerId>
  <ord:Amount currency="USD">249.95</ord:Amount>
</ord:Order>
```

- XML is case-sensitive, well-formed, and has one root element.
- Start/end tags must nest correctly; reserved characters must be escaped.
- Namespaces disambiguate elements with the same local name.
- **XSD** defines allowed structure and data types.
- **XPath** selects nodes.
- **XSLT** transforms XML into XML, text, or HTML.

Common failures:

- Ignoring namespaces in XPath.
- Assuming element order is irrelevant when an XSD defines a sequence.
- Culture-dependent decimal/date parsing.
- Loading unbounded XML entirely into memory.
- Enabling unsafe external-entity resolution.
- Transforming without validating source and target contracts.

## 4.10 XSLT

XSLT is a declarative XML transformation language.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>
  <xsl:template match="/Order">
    <PurchaseOrder>
      <ExternalId><xsl:value-of select="OrderId"/></ExternalId>
      <Total currency="USD"><xsl:value-of select="Amount"/></Total>
    </PurchaseOrder>
  </xsl:template>
</xsl:stylesheet>
```

Interview points:

- Use XSLT when XML mappings are declarative and schema-driven.
- Handle namespaces explicitly.
- Compile/cache stable transformations where supported.
- Test missing/optional/repeating elements and target schemas.
- Prevent uncontrolled extension functions or external resource access.

## 4.11 SOAP, WSDL, and the SOAP envelope

SOAP is an XML-based messaging protocol. It commonly uses HTTP but is not identical to HTTP or REST.

- **WSDL:** Service contract describing operations, messages, bindings, and endpoints.
- **XSD:** XML data types used in the messages.
- **Envelope:** Required root container for a SOAP message.
- **Header:** Optional cross-cutting metadata such as security or addressing.
- **Body:** Operation payload.
- **Fault:** Standard SOAP error structure inside the Body.

### SOAP request envelope

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ord="urn:example:orders:v1">
  <soapenv:Header>
    <ord:CorrelationId>563885df-e152-4d31-a64d-4819d97b9997</ord:CorrelationId>
  </soapenv:Header>
  <soapenv:Body>
    <ord:CreateOrderRequest>
      <ord:OrderId>ORD-1001</ord:OrderId>
      <ord:CustomerId>CUS-101</ord:CustomerId>
      <ord:Amount>249.95</ord:Amount>
      <ord:Currency>USD</ord:Currency>
    </ord:CreateOrderRequest>
  </soapenv:Body>
</soapenv:Envelope>
```

### SOAP fault

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <soapenv:Fault>
      <faultcode>soapenv:Client</faultcode>
      <faultstring>Invalid order amount</faultstring>
      <detail><errorCode>ORDER_001</errorCode></detail>
    </soapenv:Fault>
  </soapenv:Body>
</soapenv:Envelope>
```

SOAP 1.1 and SOAP 1.2 have different namespaces/content types. Follow the WSDL binding rather than guessing. Some services also require `SOAPAction`, WS-Security, or WS-Addressing headers.

### REST-style HTTP versus SOAP

| Area | REST-style API | SOAP service |
|---|---|---|
| Contract | Often OpenAPI | WSDL plus XSD |
| Payload | Usually JSON; other formats possible | XML envelope |
| Operations | HTTP resource semantics | WSDL operations/messages |
| Errors | HTTP status plus error body | SOAP Fault, often plus HTTP status |
| Security ecosystem | OAuth/TLS/gateway conventions | May include WS-Security |
| Best fit | Web/mobile/integration APIs | Established contract-heavy enterprise systems |

Do not claim one is universally better. Choose based on existing systems, contract/security requirements, tooling, and operations.

### SOAP interview checklist

1. Locate the correct WSDL operation and binding.
2. Confirm SOAP version, endpoint, content type, and `SOAPAction` requirements.
3. Generate or validate the exact namespace-qualified envelope.
4. Apply the required authentication/WS-Security mechanism.
5. Set a finite timeout and correlation information.
6. Parse both HTTP errors and SOAP Faults.
7. Validate response elements/types and handle missing optional nodes.
8. Redact credentials and sensitive XML from logs.
9. Contract-test against representative fault messages.

## 4.12 JSON in .NET: System.Text.Json and Newtonsoft.Json

### `System.Text.Json`

- Built into modern .NET and integrated with ASP.NET Core.
- High-performance, UTF-8-focused APIs.
- Supports attributes, converters, DOM APIs, and source generation.
- Usually the default for new .NET code.
- Its defaults differ from Newtonsoft.Json, so migrations require tests.

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

public sealed record OrderDto(
    [property: JsonPropertyName("orderId")] string OrderId,
    [property: JsonPropertyName("amount")] decimal Amount);

var options = new JsonSerializerOptions(JsonSerializerDefaults.Web)
{
    PropertyNameCaseInsensitive = true,
    DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
};

OrderDto? order = JsonSerializer.Deserialize<OrderDto>(json, options);
string output = JsonSerializer.Serialize(order, options);
```

Use `JsonDocument`/`JsonElement` for read-only traversal and `JsonNode` for a mutable DOM. Dispose `JsonDocument` because it owns pooled memory.

### Newtonsoft.Json (`Json.NET`)

- Mature external NuGet library.
- Uses `JsonConvert`, `JsonSerializerSettings`, `JObject`, `JArray`, and `JToken`.
- Common in older .NET systems and code requiring its established converters/features.
- Flexible defaults can differ materially from `System.Text.Json`.

```csharp
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public sealed class LegacyOrderDto
{
    [JsonProperty("orderId")]
    public string OrderId { get; init; } = string.Empty;

    [JsonProperty("amount")]
    public decimal Amount { get; init; }
}

var settings = new JsonSerializerSettings
{
    NullValueHandling = NullValueHandling.Ignore,
    MissingMemberHandling = MissingMemberHandling.Error
};

var order = JsonConvert.DeserializeObject<LegacyOrderDto>(json, settings);
var orderId = JObject.Parse(json)["orderId"]?.Value<string>();
```

### Comparison

| Area | `System.Text.Json` | Newtonsoft.Json |
|---|---|---|
| Distribution | Included in modern .NET | NuGet package |
| DOM | `JsonDocument`, `JsonElement`, `JsonNode` | `JObject`, `JArray`, `JToken` |
| Attributes | `JsonPropertyName`, `JsonIgnore` | `JsonProperty`, `JsonIgnore` |
| New-project choice | Usually preferred | Use when requirements justify it |
| Legacy compatibility | May need converters/settings | Often already established |

### JSON safety and correctness

- Prefer typed DTOs for known contracts.
- Validate business rules after syntactic deserialization.
- Set naming, case, enum, null, date, unknown-member, and number behavior deliberately.
- Avoid unsafe polymorphic type handling for untrusted JSON.
- Do not log complete payloads by default.
- Test null versus missing, unknown fields, large/decimal numbers, dates, and enums.
- Do not switch libraries without contract tests.

## 4.13 Related formats and mappings

### CSV and flat files

- Define delimiter, quoting/escaping, encoding, header, newline, decimal/date formats, and null representation.
- Do not parse CSV with `Split(',')`; quoted delimiters and newlines exist.
- Stream large files and checkpoint bounded batches.
- Preserve the source row number for error reporting.
- Decide whether one invalid row fails the file, is quarantined, or allows other rows to continue.

### Date/time

- Prefer ISO 8601 at API boundaries.
- Preserve UTC or explicit offsets using `DateTimeOffset`.
- Do not silently treat unspecified local time as UTC.
- Identify timezone and daylight-saving rules for schedules/business timestamps.

### Decimal and currency

- Use `decimal` semantics for financial values in .NET.
- Carry currency separately.
- Define scale and rounding explicitly.
- Avoid culture-dependent parsing at integration boundaries.

### Mapping discipline

| Source | Transformation | Destination |
|---|---|---|
| `orderId` | Trim; validate length/characters | `externalReference` |
| `customerId` | Parameterized SQL lookup | `customer.id` |
| `amount` | Decimal; validate range/scale | `total.amount` |
| `currency` | Invariant uppercase; allow-list | `total.currency` |
| `requestedAt` | Parse offset; output UTC ISO 8601 | `submittedAt` |
| Correlation ID | Validate or generate | Header and metadata |
| Idempotency key | Preserve unchanged | Downstream header |

## 4.14 Integration patterns

| Pattern | Use when | Main advantage | Main risk | Operational requirement |
|---|---|---|---|---|
| Request-response | Caller needs immediate result | Simple contract | Coupled latency/availability | Timeout, statuses, idempotency |
| Queue/message | Work can complete later | Buffering/isolation | Duplicates/backlog | DLQ, age metric, consumer health |
| Webhook | Source can push events | Low polling cost | Duplicate/out-of-order delivery | Authentication, retry, dedupe |
| Polling | Source cannot push | Broad compatibility | Delay/repeated reads | Watermark, overlap, rate limit |
| Schedule | Work follows time | Predictable | Missed/duplicate runs | Missing-run alert, timezone |
| File/batch | Bulk legacy exchange | Efficient bulk transfer | Partial rows/large payload | Control totals, quarantine, archive |
| Publish-subscribe | Multiple consumers | Loose coupling | Schema/order/consumer lag | Versioned events and monitoring |
| Passthrough/proxy | No logic/transformation needed | Minimal implementation | Extra hop without value | Policy, latency, upstream health |

Use synchronous processing only when the full path reliably fits inside caller/gateway deadlines. For slow or variable work, persist or enqueue first, return `202`, and expose status/callback behavior.

### Orchestration versus choreography

- **Orchestration:** A central Process controls sequence. It is visible and coordinated but can become a large central dependency.
- **Choreography:** Services react to events without one controller. It reduces central coupling but makes end-to-end reasoning/consistency harder.

Frends is naturally strong at orchestration. Do not force every domain event into one giant Process.

## 4.15 Reliability patterns

### Timeouts

Every network call needs a finite timeout aligned to the caller's total deadline. Inner dependency timeouts must leave time for error mapping and cleanup. A connection timeout, operation/read timeout, caller timeout, and business completion deadline are different concerns.

### Retry rules

Retry only when all are true:

1. Failure is plausibly transient.
2. Operation is idempotent or duplicate-protected.
3. Delay and attempts are bounded.
4. Total time fits the deadline/SLA.
5. Retrying will not amplify dependency overload.

Use exponential backoff and jitter to avoid synchronized retry storms. Honor `Retry-After` when practical.

### Circuit breaker

A circuit breaker temporarily stops calls after repeated failures, allowing the dependency and caller resources to recover. It is not a retry mechanism. States are closed, open, and half-open recovery probes.

### Idempotency

1. Receive a stable idempotency/business key.
2. Atomically create a durable processing record with a unique constraint.
3. If the same key completed, return the recorded result.
4. If in progress, return/await according to the contract.
5. Forward the same key downstream.
6. Record the final outcome and external identifier.
7. Use identical controls during reprocessing.

If the same idempotency key arrives with different normalized request content, return a conflict. Never reinterpret a key as a new operation.

### Unknown outcome

A timeout after sending a request does not prove failure. The server may have completed the operation and lost the response. Query by idempotency/business key before resubmitting a non-idempotent action.

### Dead-letter/quarantine

Do not repeatedly retry deterministic bad data. Quarantine it with business key, correlation ID, redacted error, source/schema version, attempt history, owner/status, and a controlled replay path.

### Reconciliation

Reconciliation compares expected business state across systems. It finds lost responses, silent omissions, duplicates, and partial completion that technical success metrics miss.

### Exactly-once reality

Exactly-once processing is rarely guaranteed across independent systems. A practical design combines at-least-once delivery, idempotent consumers, unique keys, checkpoints, and reconciliation.

## 4.16 SQL and transaction essentials

- Use parameterized SQL; never concatenate untrusted input.
- Grant minimum database permissions.
- Keep transactions short; do not hold locks while calling HTTP services.
- Understand atomicity, consistency, isolation, and durability.
- Index actual lookup/filter/join patterns; indexes add write/storage cost.
- Distinguish zero rows from database failure.
- Use deterministic keyset pagination for large growing tables.
- Monitor slow queries, locks, deadlocks, pool exhaustion, and connectivity.

A database transaction cannot atomically include an unrelated HTTP API. For database-plus-message reliability, know the **outbox pattern**: commit business data and an outbound-event row together, then publish the event separately and idempotently.

### Minimal idempotency registry

```sql
CREATE TABLE dbo.IntegrationOrder
(
    IdempotencyKey  nvarchar(100) NOT NULL PRIMARY KEY,
    OrderId         nvarchar(50)  NOT NULL UNIQUE,
    RequestHash     char(64)      NOT NULL,
    Status          varchar(24)   NOT NULL,
    HttpStatus      smallint      NULL,
    ResponseBody    nvarchar(max) NULL,
    ExternalOrderId nvarchar(100) NULL,
    CorrelationId   varchar(64)   NOT NULL,
    AttemptCount    int           NOT NULL DEFAULT 0,
    LastError       nvarchar(2000) NULL,
    CreatedUtc      datetime2(3)  NOT NULL DEFAULT SYSUTCDATETIME(),
    UpdatedUtc      datetime2(3)  NOT NULL DEFAULT SYSUTCDATETIME()
);
```

The claim must be atomic. A separate unprotected "check then insert" permits two concurrent requests to pass the check. Use a transaction/locking pattern plus unique constraints.

| Existing state | Decision |
|---|---|
| No row | Insert `PROCESSING`; continue |
| Same key/hash, `COMPLETED` | Return stored result; do not call downstream |
| Same key/hash, `PROCESSING` | Return `202` or expose status |
| Same key/order, different hash | Return `409` |
| `FAILED_RETRYABLE` | Use controlled reprocessing policy |
| `REJECTED` | Return stored permanent rejection |

## 4.17 Batching and large data

1. Read a deterministic page, for example `WHERE Id > @LastId ORDER BY Id`.
2. Process a bounded batch with bounded concurrency.
3. Record each item outcome.
4. Advance the checkpoint only after the defined success boundary.
5. Quarantine poison records with source position/reason.
6. Continue independent records if business rules permit.
7. Reconcile counts and totals afterward.

Set concurrency from downstream limits, database pool capacity, Agent CPU/memory, ordering requirements, and business tolerance. Do not log entire large payloads or every successful row.

## 4.18 Failure matrix

| Failure | Retry? | Immediate action | Alert? | Recovery |
|---|---:|---|---:|---|
| Validation/`422` | No | Return/quarantine reason | Trend only | Correct data, controlled replay |
| `401` | Usually no | Stop repeated attempts; fix identity | Yes | Verify credential, then replay |
| `403` | No | Fix scope/permission | Yes | Replay after authorization fix |
| `404` | Context dependent | Decide eventual/permanent absence | Threshold | Replay only if record later exists |
| `409` | No blind retry | Query canonical state | Usually no | Reconcile result |
| `429` | Bounded | Honor delay; reduce concurrency | If sustained | Queue/delay safely |
| Timeout | Maybe | Outcome is unknown | Threshold | Query destination before retry |
| `500`/`502`/`503` | Often bounded | Back off; protect dependency | Threshold | Retry/replay same key |
| Invalid JSON/XML response | Usually no | Preserve safe sample; investigate contract | Yes | Replay after producer/mapping fix |
| Database unavailable | Bounded | Prevent connection/retry storm | Yes | Restore, resume, drain backlog |
| Downstream success/local failure | No new operation | Reconciliation required | Yes | Repair local state by same key |
| Poison record | No repeated retry | Quarantine and continue safe work | Summary | Correct and audited replay |

## 4.19 Two-minute end-to-end answer

```text
Caller
  -> OAuth/API Policy + contract validation
  -> correlation ID + durable idempotency claim
  -> parameterized SQL enrichment
  -> explicit mapping
  -> downstream token + finite timeout + same idempotency key
  -> status/exception classification
  -> durable final result or recoverable failure
  -> safe response + logs/metrics/alerts/reconciliation
```

Say aloud:

> I would expose a contract-first order API in Frends, authenticate it with an API Policy, establish correlation and idempotency identifiers, validate contract and business rules, and atomically claim the request in SQL. I would enrich and map it, then call the downstream service with the same idempotency key. Only classified transient failures are retried within a deadline. The result is stored for duplicate replay. Ambiguous timeouts and downstream-success/local-failure cases are reconciled instead of blindly resubmitted. Logs are structured and redacted, with searchable identifiers and alerts for failure rates and missing executions.

## 4.20 API and integration interview questions

### 1. What makes an API RESTful?

It uses HTTP semantics and resource-oriented representations through a uniform, stateless interface. Focus on meaningful methods/statuses, stable contracts, cache/idempotency behavior, and avoid claiming every HTTP API is strictly REST.

### 2. `PUT` versus `PATCH`?

`PUT` conventionally replaces/creates the representation at a known URI and is idempotent. `PATCH` applies a partial change and is idempotent only if its patch semantics are designed that way.

### 3. `201` versus `202`?

Return `201` after creation is complete. Return `202` when work is only accepted; persist or enqueue first and provide status/callback behavior.

### 4. How do you make `POST` idempotent?

Require a key, atomically store it with a hash of normalized request content, and save the final response. Replay the stored result for the same content and return `409` for changed content under the same key.

### 5. Why is a timeout ambiguous?

The caller only knows it did not receive a response. The server may have failed, still be processing, or committed successfully; recovery requires lookup, idempotency, or reconciliation.

### 6. Which failures should be retried?

Only plausibly transient failures such as throttling, selected `5xx`, and network faults, when the operation is duplicate-safe, attempts/delays are bounded, and the deadline permits it.

### 7. How do you handle `429`?

Honor `Retry-After`, use bounded delayed retries, reduce concurrency/calls, and alert on sustained throttling because retries alone can amplify load.

### 8. What is exponential backoff with jitter?

Delay grows after failures and randomness prevents many workers from retrying simultaneously. It reduces pressure on a recovering dependency.

### 9. What is a circuit breaker?

It stops calls after repeated failures and later admits limited recovery probes. It protects resources but does not replace retry, queues, idempotency, or monitoring.

### 10. Authentication versus authorization?

Authentication establishes identity. Authorization decides which actions/resources that identity may access.

### 11. Explain OAuth client credentials.

A confidential service authenticates to an authorization server and receives an application access token for approved scopes. It is service-to-service and contains no end-user identity.

### 12. Why use OpenAPI?

It makes paths, inputs, responses, schemas, and security explicit; supports documentation/tooling; and enables validation and contract tests. Frends links its API operations to Processes.

### 13. Does OpenAPI security secure the endpoint?

No. It documents the requirement. The gateway/platform/API Policy must enforce it.

### 14. YAML versus JSON for OpenAPI?

Both represent the same model. YAML is concise but indentation/type inference can cause errors; JSON is explicit but verbose. Validate either.

### 15. RAML versus OpenAPI?

They are different API-description specifications. Both may use YAML syntax, but their structures/tools are not interchangeable.

### 16. What is a SOAP envelope?

The required SOAP XML root container with an optional Header and required Body. Standard SOAP errors appear as Faults.

### 17. WSDL versus XSD?

WSDL describes service operations, messages, bindings, and endpoints. XSD defines XML element/type structures used by the messages.

### 18. Why does an XPath often miss apparently matching XML?

Namespaces. Elements in a namespace must be selected using a correctly bound prefix even if the source uses a default namespace.

### 19. When use XSLT?

For declarative repeatable XML transformations, especially schema-driven mappings. Test namespaces, edge cases, safe resolver settings, and the target schema.

### 20. `System.Text.Json` versus Newtonsoft.Json?

Prefer `System.Text.Json` for new modern .NET work unless established behavior/features require Newtonsoft.Json. Defaults, DOMs, attributes, converters, and polymorphism differ, so migration needs contract tests.

### 21. Why not parse CSV with `Split(',')`?

CSV supports quoting, escaped quotes, embedded delimiters, and sometimes embedded newlines. Use a parser with an explicit dialect.

### 22. Why use parameterized SQL?

It separates values from executable SQL syntax, preventing injection and improving data-type/quoting correctness.

### 23. Why not keep a transaction open during HTTP?

Network latency is unbounded and holds locks/connections, causing blocking/deadlocks. Commit short local state, call externally, then update or reconcile.

### 24. What is the outbox pattern?

Commit a business change and an outbound-message record in one database transaction, then publish the message separately and idempotently.

### 25. How do you process a large table or file?

Use deterministic pagination/streaming, bounded batches and concurrency, durable checkpoints, per-item outcomes, quarantine, control totals, and reconciliation.

### 26. Queue or synchronous API?

Use synchronous processing when short work requires an immediate result. Use a queue for buffering, load smoothing, dependency isolation, and independent retry when eventual completion is acceptable.

### 27. Polling or webhook?

Use webhooks when a source can push reliably. Poll with a durable watermark, overlap, and deduplication when it cannot.

### 28. Correlation ID versus idempotency key?

Correlation connects telemetry for one end-to-end attempt/transaction. Idempotency identifies one logical business operation across repeated attempts.

### 29. What is a dead-letter queue?

It isolates messages that exhausted retry or cannot be processed. It requires ownership, alerting, diagnostic context, correction, and controlled replay.

### 30. Can distributed processing guarantee exactly once?

Usually not across independent systems. Use at-least-once delivery plus idempotency, unique constraints, checkpoints, and reconciliation.

---

# 5. Frends Architecture and Development

## 5.1 Exact 45-minute routine

| Minutes | Activity |
|---:|---|
| 0-8 | Learn the runtime mental model |
| 8-18 | Process/Subprocess/Task/Trigger/shapes |
| 18-25 | References and error handling |
| 25-32 | API management and policies |
| 32-38 | Deployment, versions, logging, monitoring |
| 38-45 | Redraw and explain everything closed-book |

## 5.2 Frends mental model

```text
Frends Tenant / Control Panel
  |
  +-- Development Environment
  |     +-- Agent Group
  |           +-- Agent(s)
  |
  +-- Test Environment
  |     +-- Agent Group
  |           +-- Agent(s)
  |
  +-- Production Environment
        +-- Agent Group
              +-- Agent(s)

Trigger -> Process -> Tasks / Code Tasks / Subprocesses -> Return or Throw
                         |
                         +-> Process Instance logs and promoted values
```

- **Tenant/Control Panel:** Central place to develop, administer, deploy, and monitor integrations.
- **Environment:** Logical lifecycle boundary such as Development, Test, or Production. Environment Variables supply target-specific values under common names.
- **Agent Group:** Deployment/execution target inside an Environment. Its Agents share deployed versions/settings.
- **Agent:** Runtime software that registers active Triggers and executes compiled Processes.
- **Hybrid architecture:** Frends Cloud Agents and customer-managed Self Service Agents can coexist so execution occurs near cloud or protected on-premises systems.
- **High availability:** Multiple Agents can participate in one Agent Group; coordinated workloads require suitable shared state and traffic/load-balancing design.

Processes are deployed to an Agent Group, not to a single chosen Agent.

## 5.3 Choosing a Frends construct

| Construct | Use it for | Key behavior |
|---|---|---|
| Process | Complete externally/automatically triggered integration | Begins with Trigger; flow ends in Return/Throw; BPMN plus C#, compiled to .NET |
| Subprocess | Reusable orchestration/shared logic | Manual Trigger defines interface; called synchronously; own Instance; caller waits |
| Standard Task | Supported connector/common operation | Packaged C# action; output through `#result` |
| Code Task | Small process-local mapping/filter/calculation | Multi-line C# inside Process; keep cohesive |
| Custom Task | Reusable tested code/libraries/package ownership | .NET 8 class library packaged as NuGet and imported |
| External service | Separately scaled/owned/security-bounded domain capability | Independent lifecycle from Frends |

A Custom Task method must be public/static, return a value, and not be overloaded. Use tests, XML documentation, supported metadata, and secret-sensitive parameter attributes; package it with `dotnet pack`.

## 5.4 Triggers and shapes

Common Triggers:

- **Manual:** User or Run once invocation; only Trigger for a Subprocess.
- **File:** Watches a mapped directory.
- **Schedule:** Starts at configured time/interval.
- **Conditional:** Periodically calls a Subprocess whose result controls starting.
- **HTTP:** Standalone endpoint without OpenAPI/API Management.
- **API:** Linked to an OpenAPI operation and API Management.
- **Messaging:** Options include AMQP, Azure Service Bus, RabbitMQ, Event Hub, and TCP depending on installed capabilities.

Non-manual Triggers must be active to respond.

Shape categories:

- **Events:** Trigger, Return, Intermediate Return, Throw, Catch.
- **Decisions:** Exclusive selects one true path; Inclusive can select multiple matches.
- **Activities:** Task, Call Subprocess, Assign Variable, Code Task, Shared State Task, DMN Task.
- **Scopes:** Named Scope, Foreach, While. While includes a maximum-iteration safeguard.
- **Sequence Flow:** Executable connection between shapes.
- **Long running:** Checkpoint plus scheduled/signal resume can persist dormant state.

## 5.5 Reference values

| Reference | Meaning |
|---|---|
| `#trigger` | Input and metadata from the Trigger |
| `#var` | Mutable Process variables |
| `#env` | Central environment configuration, such as `#env.CRM.BaseUrl` |
| `#result` | Most recently completed Task/Scope output |
| `#result[HTTP Request]` | Named result from a particular executed shape |
| `#process` | Environment, Agent Group, Agent, version, execution ID, cancellation token, etc. |
| `#var.error` | Exception details in Catch/error-handler context |

Do not read a named result from a branch that may not have executed. Initialize a variable before the branch and assign into it on each applicable path.

## 5.6 Error handling

- Use **Catch** when the current flow can map, compensate, record, continue safely, or return a controlled failure.
- An **unhandled-error Subprocess** runs after the failed Process stops. It supports alerting/cleanup, not resuming that execution.
- A Task's **Retry on failure** uses increasing delays. Enable it only for transient, duplicate-safe operations.
- Timeouts, `429`, and selected `5xx` may be transient. Validation, authentication/configuration, and most `4xx` need correction.
- Always design a safe reprocessing route; retry alone is not recovery.
- Do not convert every error into a successful Process instance. Preserve truthful operational status.

## 5.7 API Management

1. Define/import an OpenAPI specification. Current guidance centers on OAS `3.0.1`; OAS `2.0` supports legacy APIs.
2. Link each operation to a Process through an API Trigger, or generate a matching Process from API Management.
3. Implement and validate contract-compliant responses.
4. Add an API Policy.
5. Deploy the API and its linked Processes together.
6. Activate linked Process Triggers.

API Policies can target URLs, methods, and Agent Groups and configure authentication, throttling, and request logging. Current documented access methods include OAuth, Private Application, API key, and explicit public access.

**Important:** No Policy/access configuration does not mean public access. Access must be explicitly allowed.

API connection logging and Process execution logging are separate. Deploy linked Processes through API deployment to avoid version mismatches. A passthrough API proxies to an upstream API where no Process transformation/orchestration is needed and can still use policies.

### HTTP Trigger versus API Trigger

| HTTP Trigger | API Trigger |
|---|---|
| Standalone endpoint | Linked to OpenAPI operation |
| No API Management contract | Contract-driven input/output |
| Simpler internal endpoint | Policy, grouped deployment, API monitoring |
| Use for limited standalone scenarios | Prefer for governed external APIs |

## 5.8 Lifecycle and rollback

- Develop in Development; deploy selected versions to Test/Production Agent Groups.
- Saving increments the build/patch version; major/minor are developer controlled.
- Use Changelog and Diff during review.
- Deploy referenced Subprocesses and define every target Environment Variable first.
- Choose Deploy or Deploy and activate Triggers deliberately.
- Runtime rollback: deploy an older known-good version to the affected Agent Group.
- To continue development from an old definition, Switch version creates a new latest version without deleting history.
- For an API, deploy/roll back the API and linked Processes as one release unit.

## 5.9 Logging and monitoring

One **Process Instance** represents one execution and records status, duration, results, and step details according to log settings.

| Log level | Use |
|---|---|
| Only Errors | Minimum data and overhead |
| Default | Step results with input/large-data restrictions |
| Everything | Inputs, outputs, expressions; temporary development/investigation use |

- Agent Group defaults can be overridden per Process.
- Use **Skip logging result and parameters** for tokens, secrets, personal information, or large data.
- **Promoted values** are searchable Instance columns and can drive Monitoring Rules. Promote small non-sensitive business identifiers only.
- **Monitoring Rules** detect repeated errors, unexpected/missing executions, or excessive duration and can email or trigger a Process.
- **API Monitoring** covers inbound request events/statuses.
- **Agent/system logs** cover wider runtime problems.

To detect a schedule that never ran, monitor expected execution count/absence. No run means there is no failed Process Instance to alert on.

## 5.10 Testing in Frends

- Use Task test for an isolated Task with concrete inputs; it cannot depend on prior `#trigger`/`#result` context.
- Use Run once for the saved complete Process and inspect the Process Instance.
- Test Custom Tasks using normal .NET unit and controlled integration tests.
- Test contract, authentication, happy path, invalid data, duplicate, timeout, throttling, downstream failure, logging/redaction, and reprocessing.

## 5.11 Frends interview questions

### 1. What is a Frends Process?

An end-to-end integration flow modeled with supported BPMN, enhanced by C# expressions/Code Tasks, converted to C#, compiled with .NET, and executed by an Agent. It begins with a Trigger and normally finishes through Return or Throw.

### 2. Process versus Subprocess?

A Process is the externally or automatically started boundary. A Subprocess is reusable internal orchestration with a Manual Trigger defining parameters. It gets a separate Instance/execution context, but its caller waits, so it is not a concurrency tool.

### 3. Standard Task versus Code Task versus Custom Task?

Start with an official Task for supported common operations. Use Code Task for small process-specific logic. Use Custom Task for reusable/tested packaged code or additional libraries. Use an external service for independent ownership, scaling, or security boundaries.

### 4. How does execution work?

An active Trigger is registered by an Agent. Its event starts a Process Instance and the Agent runs the compiled Process in the .NET runtime. Results/failures go to Instance logging according to configured levels.

### 5. Environment, Agent Group, and Agent?

An Environment represents lifecycle/configuration context. Its Agent Group is the deployment/execution target and physical placement. Agents are the runtime processes executing definitions deployed to that group.

### 6. How does Frends support hybrid integration?

One tenant can manage Frends Cloud Agents and Self Service Agents in customer infrastructure/other clouds. Place execution near protected systems, expose only required network paths, and use Environment Variables for target-specific endpoints/credentials.

### 7. How would you design high availability?

Use multiple Agents in an Agent Group with appropriate shared state and load-balancer/gateway design. Monitor shared dependencies because they may remain single failure points. Deployments still target the group, not one Agent.

### 8. Explain the key references.

`#trigger` is invocation data, `#var` mutable flow state, `#env` environment configuration, `#result` shape output, and `#process` execution metadata. Avoid named results from branches that may not run; initialize a variable across branches.

### 9. HTTP Trigger versus API Trigger?

HTTP Trigger creates a standalone endpoint without OpenAPI/API Management. API Trigger links a Process to an OpenAPI operation, enabling contract-driven behavior, API Policies, grouped deployment, and API monitoring.

### 10. How do you create and secure a Frends API?

Create/import OpenAPI, link a Process per operation, implement contract responses, add a scoped API Policy, deploy API and Processes together, and activate Triggers. Use TLS, least-privilege OAuth/keys, throttling, validation, and safe logging.

### 11. What happens if an API has no Policy?

It is not automatically public. Current documented behavior requires a Policy to permit access, including explicit public access. The incomplete configuration therefore fails closed.

### 12. How do you deploy safely?

Test in Development, deploy dependent Subprocesses first, verify target Environment Variables, deploy the selected version to Test, execute happy/failure smoke tests, promote the same version, activate deliberately, and monitor initial Instances.

### 13. How do you roll back?

Deploy the previous known-good version to the Agent Group, confirm Trigger state and health, and reconcile external side effects. Use Switch version only when development should continue from an older definition. Roll back an API with linked Processes as a unit.

### 14. How do you troubleshoot a failure?

Identify impact, Environment, Process version, execution/correlation/business IDs. Inspect the first failed shape, classify data/auth/config/network/dependency/code, check Agent/API logs, stop unsafe retries, recover, reprocess idempotently, and verify business outcomes.

### 15. What are promoted values?

Searchable Process Instance columns that can drive Monitoring Rules. Promote order/correlation/outcome identifiers, never secrets or sensitive payloads, because promotion remains logged despite normal level suppression.

### 16. How do you choose a production log level?

Use the minimum needed for operations/privacy/audit. Temporarily raise one Process during an incident and then restore it. Secret-bearing shapes skip parameters/results regardless of overall level.

### 17. Catch versus unhandled-error Subprocess?

Catch handles an exception inside the active flow and can map/compensate/return/rethrow. An unhandled-error Subprocess runs after the original Process stops, so it supports alerting/cleanup rather than resume.

### 18. How do you detect a scheduled Process that silently stopped?

Create a Monitoring Rule for expected execution count/absence in a time window. Then check Trigger activation, schedule/timezone, Agent health, deployment, and source availability.

### 19. How do you test Frends work?

Use isolated Task tests, Run once plus Process Instance review, automated .NET tests for Custom Tasks, contract/integration tests, and deliberate failure tests. Verify business outcomes and log redaction, not only a green status.

### 20. How do you prevent retry duplicates?

Classify the failure, bound retries, carry a stable durable idempotency key, and treat a timeout as unknown. Query/reconcile destination state before resubmitting and apply the same controls to reprocessing.

## 5.12 Closed-book Frends checkpoint

Draw the mental model from memory, then answer in two minutes:

> A request reaches a policy-protected OpenAPI operation and starts an API-triggered Process on an Agent in the deployed Agent Group. The Process uses `#trigger`, `#env`, variables, Tasks, and Subprocesses; it returns or throws. One Process Instance captures the execution. Promoted identifiers make it searchable. Versions move through Environment/Agent Group deployments, and an older known-good version supports runtime rollback. Monitoring covers both failures and missing executions.

---

# 6. Hands-On Frends Order Integration

## 6.1 Lab goal and definition of done

Build and explain:

```text
API Trigger
  -> initialize correlation and normalized request
  -> validate
  -> atomically claim idempotency key
  -> enrich customer
  -> map downstream request
  -> call downstream with OAuth + same idempotency key
  -> classify result
  -> store final response/failure
  -> return consistent HTTP response
```

By minute 75 you need:

- One linked API operation or Manual Trigger fallback.
- Correlation and idempotency identifiers.
- Validation and consistent errors.
- Durable claim, or clearly labeled simulation.
- Customer enrichment and explicit mapping.
- One outbound HTTP call with timeout.
- Bounded retry and Catch handling.
- Success, duplicate, permanent, and transient branches.
- Promoted operational identifiers.
- A two-minute closed-book explanation.

Task names and parameter labels vary by installed package/version. Use the tenant's installed HTTP/database Tasks and inspect their result objects through autocomplete/documentation.

## 6.2 Exact 75-minute schedule

| Time | Work |
|---|---|
| 00:00-00:05 | Create Process and choose real/simulated dependencies |
| 00:05-00:13 | Import API, link Process, configure access |
| 00:13-00:20 | Add environment variables |
| 00:20-00:29 | Initialize, normalize, hash, validate |
| 00:29-00:39 | Add idempotency claim |
| 00:39-00:47 | Enrich customer and map payload |
| 00:47-00:59 | Configure OAuth/HTTP, retries, Catch |
| 00:59-01:06 | Persist outcome and return responses |
| 01:06-01:12 | Run intentional failure tests |
| 01:12-01:15 | Close editor and explain from memory |

If SQL or OAuth endpoints are unavailable, simulate only those boundaries. Do not spend the lab debugging infrastructure. State exactly what the real Task would do.

## 6.3 Input contract

Use the OpenAPI document from Section 4 and this payload:

```json
{
  "orderId": "ORD-1001",
  "customerId": "CUS-101",
  "amount": 249.95,
  "currency": "USD",
  "requestedAt": "2026-07-13T14:30:00Z"
}
```

Validation rules:

| Field | Rule |
|---|---|
| `Idempotency-Key` | Required; bounded printable value |
| `orderId` | Required; 1-50 allowed characters; business unique |
| `customerId` | Required; 1-50 allowed characters |
| `amount` | Decimal greater than zero; agreed upper bound |
| `currency` | Supported uppercase ISO currency code |
| `requestedAt` | ISO 8601 timestamp with offset |
| Correlation ID | Accept safe bounded header or create GUID |

## 6.4 Preflight and environment variables

Choose:

- **Full:** Reachable SQL and downstream test API.
- **Hybrid:** SQL plus mock HTTP endpoint.
- **Simulation:** Static customer/configurable mock status while retaining production design.

Create:

| Variable | Type | Example/purpose |
|---|---|---|
| `OrderDemo.DownstreamBaseUrl` | Text | Downstream base URL |
| `OrderDemo.TokenUrl` | Text | OAuth token endpoint |
| `OrderDemo.ClientId` | Text/secret per policy | Application ID |
| `OrderDemo.ClientSecret` | Secret | Never log |
| `OrderDemo.Scope` | Text | Downstream scope |
| `OrderDemo.SqlConnectionString` | Secret | SQL connection |
| `OrderDemo.TimeoutSeconds` | Number | `10` |
| `OrderDemo.MaxAttempts` | Number | `3` |

Reference them through `#env`, for example `#env.OrderDemo.DownstreamBaseUrl`.

## 6.5 Create and secure the API

1. In Development API Management, create the API from Section 4's OAS `3.0.1` contract.
2. Link `POST /orders` to a new Process so API Trigger/Return shapes match.
3. Create/select an API Policy.
4. For a lab, use a development-only key if OAuth policy setup is unavailable.
5. In the interview, state production would use approved OAuth/claims plus least privilege.
6. Deploy/activate only after configuration is ready.

If permissions are missing, use a Manual Trigger with the same payload and preserve the API Trigger in your architecture explanation.

## 6.6 Name the Process shapes

```text
Submit Order API
|- Initialize Request
|- Validate Order
|- Valid Request?
|- Claim Order
|- Claim Outcome?
|- Get Customer
|- Customer Valid?
|- Map Downstream Order
|- Submit Downstream Order
|- Classify Downstream Response
|- Complete Order / Record Failure
+- Return HTTP Response
```

Meaningful names make references such as `#result[Get Customer]` understandable.

## 6.7 Initialize and normalize

Create variables:

| Variable | Initial value |
|---|---|
| `CorrelationId` | Valid incoming header or new GUID |
| `IdempotencyKey` | Required header |
| `RequestHash` | SHA-256 of normalized request |
| `AttemptCount` | `0` |
| `Outcome` | Empty structured object |
| `DownstreamPayload` | Empty object |

The API Trigger exposes the defined body/headers under `#trigger.data`. Use editor autocomplete because generated names and hyphenated headers may require bracket/dictionary syntax.

A Code Task can normalize and hash. Adapt trigger references to the actual generated model:

```csharp
var normalized = Newtonsoft.Json.Linq.JObject.FromObject(new
{
    orderId = ((string)#trigger.data.body.orderId)?.Trim(),
    customerId = ((string)#trigger.data.body.customerId)?.Trim(),
    amount = System.Convert.ToDecimal(#trigger.data.body.amount),
    currency = ((string)#trigger.data.body.currency)?.Trim().ToUpperInvariant(),
    requestedAt = System.DateTimeOffset.Parse(
        (string)#trigger.data.body.requestedAt,
        System.Globalization.CultureInfo.InvariantCulture)
        .ToUniversalTime()
        .ToString("O")
});

var bytes = System.Text.Encoding.UTF8.GetBytes(
    normalized.ToString(Newtonsoft.Json.Formatting.None));

var hash = System.Convert.ToHexString(
    System.Security.Cryptography.SHA256.HashData(bytes));

return new { Payload = normalized, RequestHash = hash };
```

Equivalent logical requests must produce the same hash. Do not include volatile values such as correlation ID or current time.

## 6.8 Validate

Collect validation errors rather than failing at the first field:

- Required and bounded idempotency key.
- Required order/customer identifiers.
- `amount > 0` and within supported range/scale.
- Supported currency.
- Valid offset timestamp.
- Allowed identifier characters.
- Acceptable body/collection size.

Use an Exclusive Decision:

```text
errors.Count == 0?
  Yes -> Claim Order
  No  -> Return 400 Problem response
```

Schema validation is useful, but Process validation remains defense in depth and implements business rules.

Promote only small safe values: `OrderId`, `CorrelationId`, `Outcome`, and possibly `AttemptCount`.

## 6.9 Atomically claim the idempotency key

Use a database Task named `Claim Order`:

- Connection: `#env.OrderDemo.SqlConnectionString`
- Parameters: idempotency key, order ID, request hash, correlation ID
- Retry: bounded only for known transient connection failures
- Logging: suppress connection string and complete payload

Conceptual atomic claim:

```sql
SET XACT_ABORT ON;
BEGIN TRANSACTION;

DECLARE @ExistingKey nvarchar(100);
SELECT @ExistingKey = IdempotencyKey
FROM dbo.IntegrationOrder WITH (UPDLOCK, HOLDLOCK)
WHERE IdempotencyKey = @IdempotencyKey OR OrderId = @OrderId;

IF @ExistingKey IS NULL
BEGIN
    INSERT dbo.IntegrationOrder
        (IdempotencyKey, OrderId, RequestHash, Status, CorrelationId)
    VALUES
        (@IdempotencyKey, @OrderId, @RequestHash, 'PROCESSING', @CorrelationId);
END;

SELECT * FROM dbo.IntegrationOrder
WHERE IdempotencyKey = COALESCE(@ExistingKey, @IdempotencyKey);

COMMIT TRANSACTION;
```

Branch:

| Outcome | Behavior |
|---|---|
| New row | Continue |
| Same key/hash, completed | Return stored response with `replayed: true` |
| Same key/hash, processing | Return `202` or status reference |
| Same key/order, different hash | Return `409` |
| Rejected | Return stored rejection |
| Retryable failure | Use controlled reprocessing policy |

Do not implement separate unprotected "check then insert." Unique constraints remain the final race defense.

Simulation fallback may use a Shared State Task/static object, but state clearly that it is not the durable production design.

## 6.10 Enrich the customer

Use a parameterized query:

```sql
SELECT ExternalCustomerId, IsActive
FROM dbo.Customer
WHERE CustomerId = @CustomerId;
```

| Result | Behavior |
|---|---|
| One active customer | Continue |
| No customer | `422 customer_not_found` |
| Inactive customer | `422 customer_inactive` |
| Multiple rows | Data-integrity failure and alert |
| Database unavailable | Retryable dependency failure, then `503` |

Simulation object:

```json
{
  "customerId": "CUS-101",
  "externalCustomerId": "EXT-CUS-8801",
  "isActive": true
}
```

## 6.11 Map the downstream contract

Use Assign Variable or a small Code Task:

```json
{
  "externalReference": "ORD-1001",
  "customer": { "id": "EXT-CUS-8801" },
  "total": { "amount": 249.95, "currency": "USD" },
  "submittedAt": "2026-07-13T14:30:00Z",
  "metadata": {
    "correlationId": "563885df-e152-4d31-a64d-4819d97b9997"
  }
}
```

Verify amount remains numeric, timestamp has UTC/offset semantics, internal fields do not leak, correlation is forwarded, and the idempotency key remains unchanged.

## 6.12 Obtain an OAuth token

Preferred choices:

- Approved reusable authentication Subprocess.
- Task/package capability accepting OAuth configuration/token.
- Direct token endpoint call when necessary.

```http
POST <TokenUrl>
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&
client_id=<client-id>&
client_secret=<secret>&
scope=<scope>
```

Do not put the secret/token into logged Process results. Production should cache/reuse a valid token until shortly before expiry. Obtaining once per Process is acceptable only as a time-boxed demonstration; explain the inefficiency.

## 6.13 Submit downstream

Configure `Submit Downstream Order`:

| Setting | Value |
|---|---|
| Method | `POST` |
| URL | `#env.OrderDemo.DownstreamBaseUrl + "/orders"` |
| Content type | `application/json` |
| Body | Mapped payload |
| Authorization | Bearer access token |
| Header | `Idempotency-Key: #var.IdempotencyKey` |
| Header | `X-Correlation-Id: #var.CorrelationId` |
| Timeout | `#env.OrderDemo.TimeoutSeconds` |
| Transport retries | Bounded and duplicate-safe |
| HTTP error throwing | Disable when manually classifying statuses |

Classify:

```text
2xx       -> parse and complete
400/422   -> permanent rejection; no retry
401/403   -> identity/scope failure; alert
409       -> inspect/query idempotent state
429       -> honor Retry-After; bounded delay
500-599   -> bounded retry when duplicate-safe
other     -> unexpected contract response
```

For the lab, implement transport retry and status classification. Describe a reusable Subprocess/bounded loop for precise `429`/`5xx` policy rather than duplicating a large group of shapes.

Attach Catch to the downstream Scope. In Catch:

1. Classify the exception.
2. Set a safe preinitialized `Outcome`.
3. Update durable state to retryable failure where appropriate.
4. Promote failure category/attempt count.
5. Return a safe `503` or rethrow after recording.

Do not access the failed Task's result from Catch; use Catch error context and variables initialized before the call.

## 6.14 Persist and return the outcome

Success update:

```sql
UPDATE dbo.IntegrationOrder
SET Status = 'COMPLETED',
    HttpStatus = 201,
    ResponseBody = @SafeResponseBody,
    ExternalOrderId = @ExternalOrderId,
    AttemptCount = @AttemptCount,
    LastError = NULL,
    UpdatedUtc = SYSUTCDATETIME()
WHERE IdempotencyKey = @IdempotencyKey;
```

Use analogous updates for `REJECTED` and `FAILED_RETRYABLE`. Store only safe bounded response/error data.

If downstream succeeds but this update fails:

- Do not create a new idempotency key.
- Record/alert an ambiguous partial-completion condition.
- Query downstream using order/key or replay the same key only if its contract guarantees idempotency.
- Repair local state through reconciliation.

Success response:

```json
{
  "orderId": "ORD-1001",
  "status": "submitted",
  "externalOrderId": "EXT-84721",
  "correlationId": "563885df-e152-4d31-a64d-4819d97b9997",
  "replayed": false
}
```

Duplicate replay has the same business result with `"replayed": true`.

Temporary failure:

```json
{
  "type": "https://example.internal/problems/dependency-unavailable",
  "title": "Order processing is temporarily unavailable",
  "status": 503,
  "code": "dependency_unavailable",
  "correlationId": "563885df-e152-4d31-a64d-4819d97b9997"
}
```

Return correlation ID in the response header and body.

## 6.15 Intentional failure tests

Run as many as possible and reason through the rest:

| Test | Expected behavior | Retry? | Evidence |
|---|---|---:|---|
| Missing `orderId` | `400`; downstream not called | No | Validation outcome |
| Amount `-1` | `400/422`; downstream not called | No | Field-safe error |
| Same request/key | Stored result replayed | No | One downstream submission |
| Same key, changed amount | `409` | No | Conflict metric/log |
| SQL unavailable before claim | `503`; no downstream call | Bounded | Database category |
| Downstream timeout | Same key on safe retry, then `503` | Bounded | Attempts/duration |
| Downstream `401` | Stop and alert identity owner | At most one token refresh | Auth category |
| Downstream `429` | Honor delay; `503` if exhausted | Yes | Throttle count |
| Downstream `500` | Bounded retry with same key | Yes | Attempts/status |
| Invalid downstream JSON | `502`; no blind repeat | Usually no | Contract category |
| Success then DB update failure | Reconciliation required | No new operation | Ambiguous state evidence |
| Customer missing | `422`; no downstream call | No | Business rejection |

For each test answer:

1. Caller, Frends, configuration, or dependency failure?
2. Could repeating create a duplicate?
3. What response should the caller receive?
4. What may be logged safely?
5. Is automatic or human recovery required?
6. How will support locate every affected order?

## 6.16 Production extensions

- Reusable OAuth-token Subprocess with safe caching.
- Retry Subprocess honoring `Retry-After` and jitter.
- Queue-based replay of `FAILED_RETRYABLE` work.
- Reconciliation Process for stale `PROCESSING` rows.
- Status endpoint for asynchronous orders.
- Contract tests against OpenAPI.
- Monitoring Rules for sustained failures and missing runs.
- Bounded batch reprocessing.
- Dashboard using promoted outcome/duration.
- Explicit log redaction and retention policy.

## 6.17 Two-minute lab explanation

Close the editor and deliver:

> The API Trigger is linked to an OpenAPI operation and protected by an API Policy. The Process normalizes and validates the order, establishes correlation, and hashes normalized content. It atomically claims the idempotency key in SQL so concurrent duplicates cannot both continue. A completed duplicate replays its result; changed content under the same key conflicts. It enriches the customer with parameterized SQL, maps a downstream contract, obtains a client-credentials token, and forwards correlation and idempotency headers. Only safe transient failures are retried within a deadline. The final response is stored for replay. If downstream succeeds but local completion fails, reconciliation uses the same key rather than creating another order. Promoted values and structured redacted logs let support trace and recover work.

## 6.18 Post-lab recall

Answer without opening the Process:

1. Where is the idempotency race prevented?
2. Which value remains unchanged across retries?
3. Why normalize before hashing?
4. Why finish the SQL transaction before HTTP?
5. Which failures are permanent?
6. How does `429` differ from `401`?
7. What happens when the same key carries a different amount?
8. How does support recover a stale `PROCESSING` row?
9. Which values are promoted?
10. Which values never appear in logs?
11. Why can Catch not assume a failed Task produced a result?
12. What changes across Development, Test, and Production?

### Answer key

1. Atomic database claim plus unique constraints.
2. The idempotency key for the same logical operation.
3. Semantically equivalent requests need the same stable hash.
4. Avoid long locks/connections around unbounded network latency.
5. Validation/business rejection, most `4xx`, permission/configuration/contract defects until corrected.
6. `429` requests delayed load reduction; `401` indicates missing/invalid authentication.
7. `409 Conflict`; never reinterpret the key.
8. Reconcile downstream by order/key, repair state, and replay only if confirmed safe.
9. Small non-sensitive order/correlation/outcome/attempt identifiers.
10. Secrets, tokens, auth headers, connection strings, private keys, unnecessary customer data.
11. The Task failed, so only Catch error context and preinitialized variables are reliable.
12. Endpoints, identities/secrets, Agent Groups, policies, capacity, log level, and monitoring values; Process logic/artifact should remain controlled.

---

# 7. Power Platform Essentials

## 7.1 Exact 30-minute routine

- **0-8:** Platform mental model and app types.
- **8-16:** Power Automate, connectors, Dataverse.
- **16-23:** Environments, solutions, DLP, ALM, limits.
- **23-30:** Comparison and closed-book questions.

```text
User -> Power App -> Connector/Connection -> Power Automate -> Dataverse/service
```

- **Power Apps:** Low-code user interfaces.
- **Power Automate:** Workflow orchestration.
- **Dataverse:** Structured business data, relationships, security, solution-aware metadata.
- **Connector:** Typed triggers/actions for a service.
- **Connection:** Authenticated instance/context for a connector.
- **Connection reference:** Solution component binding to the correct target-environment connection.
- **Environment:** Isolation boundary for apps, flows, connections, data, security, governance.
- **Solution:** Package for ALM and deployment.

## 7.2 Canvas versus model-driven apps

| Area | Canvas app | Model-driven app |
|---|---|---|
| Starts from | Screen/user experience | Dataverse model |
| Layout | Highly customizable | Generated from forms/views/tables/navigation |
| Data | Dataverse and connector sources | Dataverse |
| Best fit | Tailored task interface | Data-dense process application |
| Main risk | Complex formulas/design maintainability | Less precise layout control |
| Security | App sharing plus source permissions | Dataverse roles/record access |

## 7.3 Power Automate

Cloud flows can be automated/event-triggered, instant/user-triggered, or scheduled.

- Use expressions for small transformations.
- Use **Scopes** to group validation, processing, failure, and cleanup.
- Use **Configure run after** for try/catch/finally-style paths.
- Use **child flows** for cohesive reusable workflow behavior; parent/child should be solution-aware.
- Concurrency raises throughput but can break ordering, create races, and exceed downstream limits.
- Retry policies do not make writes safe; idempotency still matters.
- Filter with trigger conditions before starting unnecessary runs.

## 7.4 Dataverse

Prepare standard/custom tables, columns, choices, relationships, calculated/rollup fields, business rules, user/team/organization ownership, security roles/privileges, record sharing, column security, and auditing.

Effective access is composed from license, environment access, security role, table privilege/access depth, ownership, teams, sharing, and column security. Sharing the app does not automatically grant underlying data access.

## 7.5 Connectors and gateway

- A **custom connector** exposes a stable API, often from OpenAPI, when no suitable connector exists.
- The **on-premises data gateway** provides supported Power Platform cloud services with connectivity to on-premises sources.
- A gateway is not equivalent to a Frends Agent: the Agent executes Processes; the gateway mainly provides connectivity.
- Production gateway design needs ownership, patching, capacity, recovery, and clustering where required.

## 7.6 Environments, solutions, ALM, and DLP

Recommended lifecycle:

1. Develop inside an unmanaged solution in Development.
2. Include apps/flows/tables/connectors/connection references/environment variable definitions.
3. Deploy a versioned managed solution to Test.
4. Bind target connections and configuration values.
5. Run integration, security, and smoke tests.
6. Promote the same release artifact to Production.
7. Verify ownership, sharing, roles, connections, and monitoring.

**Unmanaged solution:** Editable source in Development.  
**Managed solution:** Controlled package normally installed downstream.

DLP/data policies classify/restrict connectors and combinations to reduce accidental data movement. They do not replace API authorization or source-system permissions.

Designs must account for premium licensing, connection ownership, expired identities, platform request allocation, connector throttling, Dataverse service-protection limits, and trigger/loop concurrency. `429` can come from a connector even when overall platform allocation remains.

## 7.7 Frends comparison

These are conceptual, not exact equivalences.

| Need | Frends | Power Platform |
|---|---|---|
| Workflow | Process | Power Automate flow |
| Reuse | Subprocess | Child flow |
| Packaged operation | Task | Connector action |
| Pro-code | Code/Custom Task/external service | Custom connector/plug-in/Function/API |
| Runtime | Agent in Agent Group | Microsoft cloud runtime |
| On-prem connectivity | Self Service Agent | On-premises gateway |
| Configuration | Environment Variable | Solution environment variable |
| API contract | OpenAPI-backed API/Tasks | Connector/custom connector |
| Execution history | Process Instances | Flow run history |
| Promotion | Process version to Agent Group | Solution through pipeline |

Choose **Frends** when enterprise/hybrid backend integration, files/APIs, and operationally managed orchestration dominate. Choose **Power Platform** for Microsoft 365/Dynamics, user-facing low-code apps, approvals, Dataverse, and citizen-development governance. A solution may use Power Apps for UI and Frends for durable backend integration.

## 7.8 Power Platform interview questions

### 1. Canvas versus model-driven app?

Canvas starts with a tailored user experience across Dataverse/connectors. Model-driven starts with Dataverse and generates a consistent data-dense interface from tables, forms, views, and relationships.

### 2. Connector, connection, and connection reference?

A connector defines service operations. A connection is an authenticated instance. A connection reference is solution metadata binding components to the appropriate target-environment connection.

### 3. When use a child flow?

For cohesive reusable workflow behavior with clear input/output contracts. Keep parent and child solution-aware and avoid creating a catch-all shared flow.

### 4. What does an on-premises gateway do?

It gives supported cloud services secure connectivity to on-premises sources. It still requires source authorization, ownership, patching, monitoring, capacity, and HA planning.

### 5. How do you promote a solution?

Build in an unmanaged Development solution and deploy a versioned managed artifact through Test to Production. Bind connection references/configuration per target and run checks, approvals, smoke tests, and monitoring.

### 6. What do DLP policies do?

They govern allowed connectors and which connector groups can be combined, reducing accidental data movement. They do not replace user/API/data-source authorization.

### 7. How do you handle Power Automate throttling?

Identify platform, connector, or Dataverse limits; reduce/filter calls, batch, cap concurrency, honor delays, and keep retries idempotent.

### 8. How does Dataverse security work?

Effective access combines environment/license, roles, table privileges/access depth, record ownership, teams/sharing, and optional column security. App sharing alone is insufficient.

### 9. When build a custom connector?

When a stable reusable API needs typed triggers/actions and no adequate connector exists. Start from OpenAPI, define authentication, solution-package it, classify it in DLP, and test deployment/errors/throttling.

### 10. Frends or Power Automate?

Decide from runtime location, systems, volume, support ownership, reliability, governance, licensing, and user interaction. Frends is commonly stronger for hybrid integration backends; Power Automate for Microsoft/user-centric automation.

## 7.9 Closed-book comparison

Give a two-minute comparison without the table. Include at least one case where both platforms belong in the same architecture and state why a Power Platform gateway is not a Frends Agent equivalent.

---

# 8. Security, SDLC, DevOps, and Production Support

## 8.1 Exact 65-minute routine

| Minutes | Activity |
|---:|---|
| 0-10 | Threat model and trust boundaries |
| 10-22 | Identity, secrets, network, input, logging |
| 22-34 | SDLC, YAML pipelines, tests, deployment |
| 34-45 | Observability and monitoring |
| 45-57 | Incident method and failure runbooks |
| 57-65 | Closed-book production drill |

## 8.2 Reference architecture and trust boundaries

```text
External caller
      |
      | HTTPS + authenticated request
      v
Frends API endpoint / policy boundary
      |
      | validated internal model
      v
Frends Process on Agent Group
      |                    |
      | parameterized SQL  | HTTPS + service identity
      v                    v
Customer database     Downstream order API
      |                    |
      +--------+-----------+
               |
               v
      logs, metrics, alerts,
      idempotency and reprocessing data
```

At every boundary ask:

1. Who calls?
2. How is identity verified?
3. What is it authorized to do?
4. Is transport encrypted?
5. Is input validated and bounded?
6. What timeout/rate limit applies?
7. What is safely logged?
8. How is failure detected and recovered?

Trust boundaries include caller-to-API, Process-to-database, Process-to-downstream API, Agent-to-control plane, execution-to-log store, operator-to-production, and Custom Task-to-package dependency.

## 8.3 Lightweight threat model

| Threat | Example | Controls |
|---|---|---|
| Spoofing | Stolen client credential | OAuth/certificate, short-lived token, rotation, least privilege |
| Broken authorization | Client submits for another tenant | Scope/tenant/ownership checks, deny by default |
| Replay | Same valid order repeated | Idempotency key, unique constraint |
| Tampering | Amount changed in transit | TLS, validation, authorization |
| Injection | Customer ID concatenated into SQL | Parameterization, allow-list, restricted DB account |
| Information disclosure | Token/customer payload logged | Allow-list logging, redaction, restricted retention/access |
| Repudiation | Untracked production configuration change | Named accounts, audit, approvals/change record |
| Denial of service | Excess calls exhaust capacity | Rate/body/concurrency limits, queues, scaling |
| Privilege escalation | Runtime account is DB owner | Separate identities and minimum permissions |
| Dependency compromise | Unsafe NuGet in Custom Task | Approved feeds, locked/scanned dependencies, review |
| Poison payload | Deterministic repeated failure | Validation, retry classification, quarantine |
| Egress abuse | Process sends data to unapproved host | Network allow-list/egress controls, reviewed config |
| Schema confusion | Changed response silently misread | Contract tests, versions, defensive parsing |
| Availability loss | One Agent stops all work | Health checks and justified HA design |

## 8.4 Identity and secrets

- Give each integration a named owner and non-personal service identity.
- Separate identities by environment and, where valuable, by integration.
- Grant only required API scopes, database rights, folders, and queues.
- Runtime Processes must not use administrator credentials.
- Define who may edit, deploy, activate, deactivate, and reprocess.
- Use secret Environment Variables or approved secret storage.
- Never hard-code secrets in Process logic, Code Tasks, source, payloads, or logs.
- Track credential owner, purpose, issue date, expiry, and rotation procedure.
- Overlap old/new credentials during rotation where supported; verify new before revoking old.
- Alert before expiry. If a secret appears in logs, treat it as compromised and rotate it.

## 8.5 Transport, input, and data protection

- Use TLS; validate certificate chain and host name. Never disable validation as an incident fix.
- Restrict Agent ingress/egress to required hosts/ports; document DNS/proxy/firewall/allow-list dependencies.
- Put internet ingress behind approved gateway/firewall/load-balancer controls.
- Set request/file/body/concurrency limits.
- Validate type, format, length, range, enum, cross-field rule, collection size, and content type.
- Treat downstream responses as untrusted input.
- Parameterize database commands and encode for the destination.
- Minimize sensitive data storage/logging and apply retention/deletion policy.
- Do not use personal data/secrets in URLs, correlation IDs, or idempotency keys.

## 8.6 Secure logging

Log an allow-listed operational summary:

```text
timestamp, environment, processName, processVersion,
processInstanceId, correlationId, non-sensitive businessKey,
sourceSystem, destinationSystem, operation, outcome,
durationMs, attemptNumber, httpStatus, errorCategory
```

Never intentionally log passwords, client secrets, tokens, private keys, full Authorization headers, connection strings, or unrestricted personal payloads.

## 8.7 SDLC for low-code integrations

**SDLC** means Software Development Life Cycle. Low-code changes still require engineering controls.

| Phase | Integration activities | Evidence/output |
|---|---|---|
| Discover | Business outcome, source/target owners, SLA, data classification | Problem statement, owners, NFRs |
| Analyze | Contracts, volume, latency, failure/recovery, licensing/network | Requirements and risk decisions |
| Design | Process diagram, schemas, security, idempotency, monitoring | Reviewed technical design/OpenAPI |
| Build | Process/Subprocess/Tasks/config and Custom Task code | Versioned artifacts/change history |
| Test | Unit, contract, integration, failure, security, reconciliation | Automated/manual test evidence |
| Release | Approval, dependencies, configuration, deployment, smoke test | Release record and known-good version |
| Operate | Logs, metrics, alerts, incidents, replay, capacity | Dashboards/runbooks/SLA reports |
| Improve/retire | Root-cause fixes, deprecation, data/archive/access cleanup | Change or retirement record |

Core principles:

- Develop, test, and operate as different environments/Agent Groups.
- Peer-review visual Process changes as seriously as code.
- Version OpenAPI, Process/Subprocess, Custom Task NuGet, and configuration requirements together.
- Treat configuration as controlled data, not an undocumented production edit.
- Separate duties where risk requires it: builder, reviewer, approver, operator.
- Maintain traceability from requirement to design, version, tests, deployment, and incident.

## 8.8 Source control and release inventory

Keep Custom Task source, tests, project files, dependency declarations, and pipeline YAML in Git. For Process/API artifacts, use Frends version history/diff and the organization's approved export/source-control automation.

A release inventory identifies:

- Process/Subprocess and API contract versions.
- Custom Task NuGet versions.
- Required Environment Variable keys.
- Database/downstream contract changes.
- Monitoring Rule changes.
- Test evidence and approval.
- Deployment/rollback instructions.
- Reprocessing/reconciliation implications.

## 8.9 YAML (`.yml`) CI example

YAML pipelines describe stages/jobs/steps as configuration. Syntax varies by CI product. This illustrative GitHub Actions pipeline builds/tests/packs a .NET Custom Task; adapt commands and approved Frends deployment automation to the organization.

```yaml
name: custom-task-ci

on:
  pull_request:
  push:
    branches: [main]
    tags: ['v*']

permissions:
  contents: read

jobs:
  build-test-pack:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'

      - name: Restore
        run: dotnet restore --locked-mode

      - name: Build
        run: dotnet build --configuration Release --no-restore

      - name: Test
        run: >-
          dotnet test --configuration Release --no-build
          --collect:"XPlat Code Coverage"

      - name: Pack
        if: startsWith(github.ref, 'refs/tags/v')
        run: dotnet pack --configuration Release --no-build --output artifacts

      - name: Upload package
        if: startsWith(github.ref, 'refs/tags/v')
        uses: actions/upload-artifact@v4
        with:
          name: nuget-package
          path: artifacts/*.nupkg
```

YAML rules:

- Spaces, not tabs; indentation defines hierarchy.
- Quote versions/patterns/ambiguous strings.
- Pin or deliberately govern third-party actions/templates.
- Give pipeline identities minimum permissions.
- Store secrets in CI secret storage, never YAML.
- Keep build/test/pack deterministic and fail on warnings according to team policy.
- Produce immutable artifacts once and promote the same artifact.
- Require approval for production, not a developer-local command.
- Add dependency/vulnerability scanning where supported.

## 8.10 Testing strategy

| Test | Purpose | Order example |
|---|---|---|
| Unit | Isolated C#/Custom Task logic | Normalize/hash/validate amount |
| Process/component | Branch behavior | `400` is not retried |
| Contract | Producer/consumer schema | OpenAPI response matches |
| Integration | Real test dependencies | Agent reaches test DB/API |
| Security | Auth, authorization, redaction | Token absent from logs |
| Failure | Recovery policy | `429` delay/limit works |
| Smoke | Deployed critical path | One test order completes |
| Reconciliation | No loss/duplicates | Source/destination totals agree |

Test happy path plus missing authentication, forbidden scope, invalid body, duplicate key, timeout, `429`, `500`, malformed response, database outage, redaction, rollback, and replay.

## 8.11 Deployment checklist

1. Identify exact Process, Subprocess, API, and Custom Task versions.
2. Confirm peer review and automated test results.
3. Verify OpenAPI/data-contract compatibility.
4. Verify target Environment Variable definitions.
5. Confirm secrets/certificates are valid without exposing values.
6. Deploy required Subprocess/Custom Task dependencies first.
7. Sequence database changes backward-compatibly.
8. Deploy to the Test Agent Group.
9. Run happy, validation, timeout, auth, throttling, duplicate, and replay tests.
10. Verify useful logs and redaction.
11. Verify Monitoring Rules and alert recipients.
12. Obtain production approval.
13. Record previous production version and recovery steps.
14. Deploy selected version to Production.
15. Keep Triggers inactive until prerequisites are verified when appropriate.
16. Run a controlled smoke test.
17. Activate Triggers deliberately.
18. Monitor initial executions, failure rate, latency, and downstream effects.
19. Reconcile expected/actual business outcomes.
20. Close the change only after acceptance checks pass.

## 8.12 Rollback versus roll-forward

Use **rollback** when the prior version is compatible, no irreversible migration blocks it, the fault is release-related, and restoration speed dominates.

Use **roll-forward** when external side effects or irreversible data changes make reversal unsafe, the old release is insecure/incompatible, or a controlled correction is safer.

> Rolling back a Process does not undo orders, payments, files, messages, or database changes already produced.

After either approach, identify affected records and reconcile/reprocess idempotently.

## 8.13 Observability: logs, metrics, traces

| Signal | Answers | Example |
|---|---|---|
| Logs | What happened in one execution? | Downstream `429` on attempt 2 |
| Metrics | How does behavior trend? | Failure rate, throughput, p95 duration |
| Correlation/trace | Which calls belong together? | API, SQL, downstream share one ID |

A Process Instance is the first Frends execution view. Inspect version, Agent/Group, first failing shape, timing, status, and safe promoted values.

Promote correlation ID, non-sensitive order ID, source/destination, business outcome, error category, and replay state. Do not promote secrets or raw payloads.

### Correlation-ID rules

1. Accept a valid bounded incoming ID or create one.
2. Return it to the caller.
3. Put it in every structured event.
4. Forward it in an agreed header/message property.
5. Store it with replay records.
6. Never derive it from a secret/personal value.
7. Keep business key separate so one item can have several attempts.

### Useful metrics

- Received, succeeded, failed, rejected, duplicate counts.
- Processing duration and dependency latency percentiles.
- Retry/throttle counts and status distribution.
- Queue depth, oldest-item age, replay backlog.
- Batch input/success/failure/control totals.
- Scheduled runs observed versus expected.
- Agent/runtime host health where team-managed.
- Certificate/credential days to expiry.

### Alert design

| Condition | Response |
|---|---|
| Authentication failures | Alert quickly; repeated ordinary retry rarely helps |
| Error-rate increase | Alert after meaningful sustained volume |
| Missing scheduled execution | Alert after expected window plus tolerance |
| Latency degradation | Alert on sustained percentile breach |
| Sustained `429` | Reduce pressure; investigate quota/traffic |
| Replay backlog age | Alert before business recovery target |
| No healthy Agent | Alert immediately for affected service |
| Certificate near expiry | Notify at planned rotation intervals |
| Sensitive data logged | Security incident |
| One invalid business record | Quarantine/report; normally do not page |

Thresholds reflect business impact, normal volume, and SLOs. Avoid alerting on every retry or invalid caller request.

## 8.14 Production incident method

Use this sequence in interviews and incidents:

1. **Assess impact:** Which integrations, customers, environments, and time range?
2. **Stabilize:** Stop unsafe retries, pause Trigger, reduce concurrency, or fail over.
3. **Identify:** Process/version, Agent Group, deployment time, correlation/business IDs.
4. **Classify:** Data, authentication, authorization, configuration, network, dependency, capacity, platform, or code.
5. **Inspect:** Process Instances and correlated dependency logs.
6. **Verify dependencies:** Agent, DNS, firewall, certificate, DB, queue, downstream API.
7. **Recover:** Rotate, correct configuration, roll back/forward, or restore dependency.
8. **Reprocess safely:** Reconcile first; apply idempotency to replay.
9. **Validate:** Controlled test plus actual business outcome.
10. **Communicate:** Impact, mitigation, backlog, owner, next update.
11. **Learn:** Root cause, contributing conditions, and preventive actions.

Capture start/detection time, Process/version, Agent Group/environment, recent changes, IDs, error/status, attempt timing, dependency health, affected/lost/delayed/duplicated/recovered counts, and exact recovery verification.

## 8.15 Failure runbooks

| Scenario | Diagnose | Immediate action | Recovery/prevention |
|---|---|---|---|
| Expired OAuth secret | Token error, `401/403`, configured identity/expiry | Stop repeated auth retry | Rotate in secret store, verify, resume/replay; add expiry owner/alert |
| Expired certificate | Expiry, chain, hostname, thumbprint, TLS error | Never disable validation | Install/register replacement, test overlap, revoke old, monitor expiry |
| Agent offline | Agent/service/host/CPU/memory/disk/connectivity | Fail over or pause ingress | Restore, verify Trigger coordination, use justified HA |
| DNS/firewall | Resolve host and test port/TLS from Agent network | Do not change Process logic blindly | Restore DNS/proxy/route/rule; synthetic check |
| Database unavailable | Health, login, locks, pool, network | Bounded retry; prevent storm | Restore, verify read/write, resume/drain; tune pool/availability |
| Downstream timeout | Determine if remote request completed | Do not blindly resubmit | Query by key/order; retry only if safe |
| Sustained `429` | `Retry-After`, concurrency, volume, quota | Reduce concurrency/queue | Delayed bounded retry; batch/cache/request capacity |
| Breaking schema | Compare redacted payload/contract/version | Quarantine incompatibles | Compatible mapping/version; contract tests |
| Wrong Environment Variable | Compare target prerequisites/audit | Restore known-good value | Smoke test; automate validation |
| Deployment regression | Correlate version/deployment/failure rise | Deactivate unsafe Trigger or rollback | Verify, reconcile effects, replay, add missing test |
| Duplicate processing | Check key registry and downstream state | Stop repeated replay | Select canonical result; unique/atomic controls |
| Sensitive data in logs | Identify type/access/retention/exposure | Restrict access and stop logging | Security response, rotate secrets, remove per policy, redaction tests |
| Scheduled Process stopped | Trigger, Agent, schedule/timezone, source | Define missed window before restore | Restore and backfill idempotently; missing-run alert |
| Remote success/local failure | Query by business/idempotency key | Do not resubmit until known | Reconcile local state or deliberate compensation |
| Poison record | Confirm deterministic same-input failure | Stop wasting retries | Quarantine, continue safe work, correct/audited replay |

## 8.16 Closed-book production drill

Scenario:

> A Process version was deployed at 09:00. At 09:12 failures increased, callers retried, and the downstream system contains more orders than Frends reports successful.

A strong answer:

1. Correlate failures with deployed version and affected interval.
2. Pause unsafe ingress/retries if duplicates continue.
3. Preserve evidence and identify business/idempotency keys.
4. Compare Process Instances to downstream records.
5. Check rollback compatibility; remember it does not undo side effects.
6. Do not blindly replay timed-out/local-failed executions.
7. Reconcile remote successes into local state.
8. Reprocess only confirmed missing orders through idempotent logic.
9. Monitor recovery/backlog and communicate impact.
10. Add the missing test, alert, or idempotency control.

## 8.17 Security and operations interview questions

### 1. How would you secure a Frends order API?

Require TLS, authenticate the client, authorize scope/tenant, validate/bound input, rate limit, and establish correlation. Call dependencies with separate least-privilege identities and log only safe operational identifiers.

### 2. Where should configuration and secrets live?

Endpoints/settings belong in environment configuration. Sensitive values use approved secret storage such as secret Environment Variables where appropriate. Never embed them in Process logic, source, payloads, or logs; assign owner/rotation.

### 3. How do you prevent log leakage?

Allow-list fields instead of logging whole payloads and attempting removal. Exclude/redact tokens, credentials, connection strings, and private customer fields; restrict access/retention and test redaction.

### 4. What is a good Frends deployment process?

Select exact versions, validate dependencies/configuration, deploy through Test, run functional/failure/security tests, approve Production, activate deliberately, smoke test, monitor, and reconcile. Record prior version and replay implications.

### 5. Rollback versus roll-forward?

Rollback when the prior version is compatible and fastest/safest. Roll forward when external side effects, irreversible migrations, insecurity, or incompatibility make reversal unsafe. Reconciliation remains separate.

### 6. What should be monitored?

Business throughput/outcome, failures, latency, retries, throttling, backlog age, missing schedules, Agent/dependency health, and credential expiry. Logs explain one execution; metrics show trends; correlation connects calls.

### 7. Why correlation IDs?

They connect inbound request, Process Instance, database, downstream call, and replay. Propagate them consistently, keep separate from business keys, and exclude sensitive values.

### 8. How detect a Process that did not run?

Monitor expected count/latest-success within a time window. Then inspect Trigger activation, Agent health, deployment, schedule/timezone, and source dependencies.

### 9. How investigate production failure?

Assess impact, identify version/IDs, inspect the first failed shape, classify the failure, verify Agent/dependency health, stabilize unsafe behavior, recover, replay idempotently, and confirm actual business state.

### 10. Should authentication failures be retried?

Usually not with ordinary rapid retries. A token endpoint can fail transiently, but invalid/expired credentials need intervention. Permit very limited refresh/retry only for a proven case and alert sustained `401/403`.

### 11. How do multiple Agents help availability?

Multiple Agents in an Agent Group can share execution in an HA design, with required shared state and traffic coordination. Monitor shared database/network/gateway dependencies because they can still fail centrally.

### 12. How prevent duplicates?

Use a stable key, atomically record status, enforce uniqueness, forward the key downstream, and query state after timeout. Apply the same protection to replay.

### 13. How manage a breaking schema change?

Identify consumers and prefer a backward-compatible or versioned contract. Run contract tests and plan producer/consumer deployment order. Quarantine incompatible input rather than retrying forever.

### 14. Which release tests matter most?

Happy path plus invalid data, missing/forbidden authorization, duplicate, timeout, `429`, `500`, malformed response, DB outage, redaction, rollback, and replay. Contract, smoke, and reconciliation tests catch different risks.

### 15. What do you do after downstream timeout?

Treat outcome as unknown. Query by idempotency/business key and retry only when duplicate-safe or confirmed absent; otherwise reconcile or deliberately compensate.

## 8.18 Final production checklist

```text
SECURITY
[ ] Authentication and authorization enforced
[ ] Least-privilege non-personal identities
[ ] Secrets outside logic/source/logs
[ ] TLS and certificate validation
[ ] Input/content/payload limits
[ ] Parameterized SQL
[ ] Sensitive logging reviewed

RELIABILITY
[ ] Explicit deadline/timeouts
[ ] Retryable failures classified
[ ] Bounded backoff and throttling response
[ ] Idempotency/duplicate detection
[ ] Quarantine and controlled replay
[ ] Unknown outcomes reconciled

SDLC / DEPLOYMENT
[ ] Exact versions and dependencies recorded
[ ] Peer review and tests passed
[ ] Contracts/configuration verified
[ ] Previous version and recovery plan known
[ ] Trigger activation deliberate
[ ] Smoke test and initial monitoring complete

OBSERVABILITY
[ ] Correlation propagated
[ ] Structured redacted logs
[ ] Business and technical metrics
[ ] Missing-execution alert
[ ] Agent/dependency health monitoring
[ ] Credential/certificate expiry alert

INCIDENT RESPONSE
[ ] Impact assessed and unsafe behavior stabilized
[ ] Failure classified with evidence preserved
[ ] Recovery verified through business state
[ ] Replay is idempotent
[ ] Root cause and preventive action recorded
```

---

# 9. Interview Question Bank and Mock Interview

## 9.1 One-minute introduction template

Use facts from your experience; do not memorize invented claims.

> I am a .NET developer with experience in [types of systems/domains]. My strongest areas are C#, APIs, data handling, and troubleshooting integrations across [systems]. In a recent example, I [problem], designed [solution], and achieved [measurable/relevant result]. Frends interests me because it combines visible BPMN orchestration with C#/.NET extensibility and hybrid execution. I would bring code-level engineering discipline to contracts, security, testing, deployment, monitoring, and support while keeping integrations understandable to the broader team.

Prepare two project stories:

- A successful integration from requirement to production.
- A production incident or difficult failure you diagnosed.

## 9.2 Mixed 45-minute drill

Shuffle these. Answer each in 90-120 seconds using Definition -> Example -> Risk -> Mitigation -> Monitoring.

1. Explain Frends to a nontechnical stakeholder.
2. Process versus Subprocess versus Custom Task?
3. How does an API Trigger reach an Agent-executed Process?
4. Design OAuth client-credentials for a downstream API.
5. `401` versus `403` versus `429`?
6. A `POST` times out. What next?
7. Design idempotency for order creation.
8. XML namespace, XSD, XPath, and XSLT roles?
9. SOAP envelope, WSDL, and Fault?
10. OpenAPI standards/rules you review?
11. `System.Text.Json` versus Newtonsoft.Json?
12. Process a CSV with one invalid record.
13. Handle 100,000 records without exhausting memory/API limits.
14. Detect a schedule that never ran.
15. Secure and monitor secrets/certificates.
16. Deploy and roll back safely.
17. Troubleshoot Agent-to-database connectivity.
18. Frends versus Power Automate?
19. Rollback versus roll-forward after side effects?
20. Describe your production-incident method.

Score each:

| Score | Meaning |
|---:|---|
| 0 | No answer or materially wrong |
| 1 | Correct definition only |
| 2 | Correct plus practical example |
| 3 | Adds tradeoff/failure handling |
| 4 | Adds security, testing, and operations |

Repeat every answer scoring 0-2. Do not spend time repeating 4s.

## 9.3 System-design method

When asked to design an integration:

1. Clarify functional goal, consumers, source/target ownership.
2. Quantify volume, payload size, latency, concurrency, schedule, and growth.
3. Clarify consistency, ordering, duplicate, and recovery requirements.
4. Draw systems and trust/network boundaries.
5. Choose sync, queue, event, polling, file, or batch deliberately.
6. Define contracts, schemas, validation, and versioning.
7. Define authentication/authorization and secrets.
8. Define timeout, retry, idempotency, quarantine, and reconciliation.
9. Define environment/deployment/rollback.
10. Define logs, metrics, alerts, SLO, ownership, and runbooks.

Do not begin with a tool. Begin with requirements and failure semantics, then map to Frends constructs.

## 9.4 System-design scenarios

### 1. On-premises SQL to SaaS API every five minutes

Use a Self Service Agent near SQL, Schedule Trigger, durable watermark/keyset query, bounded batches/concurrency, OAuth, idempotent destination calls, per-record outcomes, checkpoint after success boundary, missing-run/backlog alerts, and reconciliation.

### 2. Public order API with variable 30-second processing

Prefer authenticated API acceptance, persist/enqueue before returning `202`, expose status/callback, use durable idempotency, separate worker Process, deadline/retry policy, and backlog/age monitoring rather than holding a fragile request open.

### 3. Two-gigabyte nightly CSV

File Trigger, archive/control metadata, streaming parser, bounded batches, row number/error quarantine, controlled parallelism, checkpoint/restart, control totals, missing-file and excessive-duration monitoring. Never log the whole file.

### 4. Legacy SOAP service migration

Start from WSDL/XSD and binding/security requirements. Build a Frends REST-facing OpenAPI facade only if valuable; validate JSON, map via code/XSLT to namespaced SOAP envelope, parse Faults, preserve correlation, contract-test, and plan version/cutover compatibility.

### 5. Downstream permits 100 calls/minute

Rate-limit before sending, queue/batch, cap worker concurrency, honor `429/Retry-After`, cache reusable lookups/tokens, make consumers idempotent, and monitor throughput/backlog age against business SLA.

### 6. Same integration across three regions

Clarify data residency, latency, active-active versus active-passive, shared idempotency/state, routing, Agent Groups, dependency locality, failover consistency, config/secrets, and how replay avoids cross-region duplicates.

### 7. Power App initiates complex on-premises processing

Use Power App for UI, possibly a small Power Automate flow/custom connector for invocation, and Frends for governed hybrid backend orchestration near on-premises systems. Establish user/service authorization, async status, correlation, and ownership across platforms.

### 8. Partner changes XML schema without notice

Quarantine incompatible messages, preserve a safe sample, compare XSD/version/namespaces, avoid infinite retry, add compatible mapping or coordinated version, contract tests, partner change process, and schema-failure alert.

### 9. Payment API times out

Never blind retry with a new key. Query by idempotency/payment reference, reconcile outcome, use same key where provider guarantees it, avoid exposing internals, and provide an operational queue for unresolved states.

### 10. Schedule ran twice after failover

Treat schedules as at-least-once. Use a durable run/business key and atomic claim, HA shared state correctly, idempotent item handling, reconcile duplicates, and alert unusual run counts.

## 9.5 Behavioral answers with STAR

- **Situation:** One or two sentences of relevant context.
- **Task:** Your responsibility and success condition.
- **Action:** Specific decisions/actions you personally took.
- **Result:** Measurable outcome plus lesson/prevention.

Prepare these prompts:

1. Production incident under pressure.
2. Ambiguous requirement you clarified.
3. Disagreement in design/code review.
4. Technical debt you prioritized.
5. Mistake or failed deployment.
6. Performance/scalability improvement.
7. Security issue you identified.
8. Helping a less technical maker/developer.
9. Multiple urgent tasks and prioritization.
10. Learning a platform quickly.

Strong incident story shape:

> A release caused [observable impact]. I owned [responsibility]. I first stabilized [unsafe behavior], correlated [version/IDs], classified [root cause], and coordinated [teams]. We recovered through [rollback/fix/replay] and verified [business result]. I then added [test, alert, process change], which reduced recurrence/detection time by [truthful result].

Avoid blaming colleagues, claiming team work solely as yours, or giving a result with no verification.

## 9.6 Final 30-minute mock interview

Do not use notes during answers.

| Time | Prompt |
|---:|---|
| 0:00-2:00 | Introduction and relevant project |
| 2:00-4:00 | Explain Frends architecture |
| 4:00-6:00 | Process/Subprocess/Task/Custom Task choice |
| 6:00-9:00 | Design the order API and OpenAPI contract |
| 9:00-12:00 | Timeout/retry/idempotency scenario |
| 12:00-14:00 | SOAP/XML/XSLT or JSON-library comparison |
| 14:00-17:00 | Security and secret handling |
| 17:00-20:00 | Deploy, monitor, and roll back |
| 20:00-23:00 | Production incident scenario |
| 23:00-25:00 | Frends versus Power Platform |
| 25:00-28:00 | Behavioral STAR question |
| 28:00-30:00 | Candidate questions and final correction list |

### Mock scoring rubric

Score each category 0-4:

| Category | 0 | 2 | 4 |
|---|---|---|---|
| Correctness | Materially wrong | Core idea correct | Accurate with boundaries |
| Structure | Rambling/no answer | Understandable | Concise logical progression |
| Practicality | Pure definition | One example | Implementable design |
| Failure thinking | Ignores failure | Mentions error | Classifies/recovery/idempotency |
| Security | Ignores it | Generic mention | Identity, secrets, data/log controls |
| Operations | No support view | Logs only | Metrics, alerts, replay, ownership |

Target at least 18/24. Correct the lowest two categories only; do not restart the whole guide.

## 9.7 Questions to ask the interviewer

Choose three:

1. What integrations and source/target systems dominate the team's workload?
2. How are Frends Processes reviewed, tested, promoted, and monitored today?
3. How does the team choose between visual Process logic, Custom Tasks, and external .NET services?
4. What are the largest current reliability or governance challenges?
5. How are production incidents, replay, and reconciliation owned?
6. Which Frends Agent/runtime topology and environments does the team operate?
7. How much work uses SOAP/XML/files versus REST/events?
8. Where does Power Platform fit alongside Frends?
9. What would successful delivery in the first three months look like?

Avoid asking only about technology. At least one question should address outcomes, quality, or team operations.

## 9.8 Interview-day behavior

- Listen to the complete question; clarify ambiguity before designing.
- State assumptions and business constraints.
- Think aloud in a structured way, but avoid narrating every thought.
- If you do not know a Frends-specific setting, say how you would verify it and explain the underlying integration principle.
- Never invent platform behavior. Distinguish what you know, infer, and would confirm.
- For failure scenarios, assess impact and unknown outcomes before proposing replay.
- Keep initial answers under two minutes, then offer depth when asked.

---

# 10. Final Recall Sheet

Review this once tomorrow for 15-20 minutes. Then close it and reproduce the architecture and five answers aloud. Stop studying at least 30 minutes before the interview.

## 10.1 Frends in one page

```text
Tenant/Control Panel
  -> Environment (lifecycle/configuration)
  -> Agent Group (deployment/execution target)
  -> Agent(s) (runtime)

Trigger
  -> Process (end-to-end orchestration)
  -> Task / Code Task
  -> synchronous reusable Subprocess
  -> Return or Throw
  -> Process Instance + promoted values + monitoring
```

| Construct | Remember |
|---|---|
| Process | Triggered end-to-end BPMN/C# integration compiled for .NET |
| Subprocess | Reusable synchronous orchestration with Manual Trigger interface |
| Task | Packaged operation/connector action |
| Code Task | Small process-local C# |
| Custom Task | Tested reusable .NET 8 library packaged as NuGet |
| Environment | Development/Test/Production logic and configuration boundary |
| Agent Group | Where a selected version is deployed/executed |
| Agent | Actual runtime registering Triggers and running Processes |

References: `#trigger`, `#var`, `#env`, `#result`, `#process`, and Catch error context.

API lifecycle: OpenAPI `3.0.1` -> link operation to API Trigger Process -> API Policy -> deploy API/linked Processes together -> activate -> monitor API and Process Instances.

## 10.2 HTTP and API recall

```text
200 completed success
201 created
202 accepted, still processing
204 success, no body
400 invalid request
401 not authenticated
403 authenticated, not permitted
404 absent
409 state/idempotency conflict
415 wrong media type
422 semantic validation
429 throttled: honor Retry-After
500 internal failure
502 bad upstream response
503 temporarily unavailable
504 upstream timeout
```

OpenAPI review: supported version, title/version, stable `operationId`, methods/paths, request schema, required fields/constraints, every response, security scheme + enforcement, examples, reusable `$ref`, validation, compatibility, contract tests.

OAuth client credentials: client identity/secret or certificate -> token endpoint -> scoped short-lived access token -> Bearer API call. Cache safely; never log secrets/tokens; distinguish `401` from `403`.

## 10.3 Data/protocol recall

- YAML: spaces/indentation, mappings/sequences, quote ambiguity, validate, no secrets.
- RAML: separate YAML-based REST description language; not OpenAPI.
- RML: ambiguous; often RDF Mapping Language; ask which meaning.
- XML: well-formed, namespaces, XSD structure, XPath selection, XSLT transformation.
- SOAP: WSDL operation/binding, XML Envelope/Header/Body/Fault, version/content type, possible `SOAPAction`/WS-Security.
- JSON: `System.Text.Json` is modern .NET default; Newtonsoft.Json is mature/established. Defaults/DOM/converters differ; contract-test migrations.
- CSV: real parser, explicit dialect/encoding, row numbers, streaming/batching, quarantine.

## 10.4 Reliability recall

```text
Timeout != failure. It means outcome unknown.
Retry only transient + duplicate-safe + bounded + within deadline.
Idempotency key identifies logical operation.
Correlation ID connects telemetry.
Circuit breaker protects a failing dependency.
Quarantine stops poison-data retry waste.
Reconciliation verifies business state across systems.
```

Retry candidates: bounded network faults, `429`, selected `5xx`.  
Do not blindly retry: validation, permission, contract defects, unsafe writes.  
After timeout: query destination by same key/order before resubmission.

## 10.5 Security and operations recall

- TLS and authenticated/authorized least-privilege service identities.
- Secret Environment Variables/approved vault; ownership/rotation/expiry alerts.
- Validate and bound all untrusted input/output.
- Parameterized SQL.
- Allow-list structured logs; no secrets/tokens/full sensitive payloads.
- Deploy exact reviewed/tested version and dependencies/configuration.
- Smoke-test, activate deliberately, monitor, reconcile.
- Rollback does not undo external side effects.
- Logs explain one execution; metrics show trends; correlation links systems.
- Monitor failures, latency, retries/throttling, backlog, Agent/dependencies, missing schedules, credential expiry.

Incident sequence:

```text
Assess impact -> stabilize -> identify version/IDs -> classify -> inspect
-> verify dependencies -> recover -> reconcile/replay safely
-> validate business outcome -> communicate -> prevent recurrence
```

## 10.6 Five answers to rehearse tomorrow

1. Explain Frends Process-to-Agent execution and lifecycle.
2. Design the idempotent order integration.
3. Explain timeout, retry, `429`, and unknown outcome.
4. Explain secure deployment, monitoring, rollback, and replay.
5. Compare Frends, Power Automate, Custom Task, and external .NET service choices.

## 10.7 Sleep and interview morning

- Finish at least one hour before normal sleep.
- Do not trade normal sleep for passive rereading.
- Tomorrow, review only this section for 15-20 minutes.
- Close it; redraw the Frends/order architecture and answer three questions aloud.
- Stop studying at least 30 minutes before the interview.

## 10.8 Acronym glossary

| Acronym | Meaning |
|---|---|
| ALM | Application Lifecycle Management |
| API | Application Programming Interface |
| BPMN | Business Process Model and Notation |
| CI/CD | Continuous Integration / Continuous Delivery or Deployment |
| CSV | Comma-Separated Values |
| DLP | Data Loss Prevention/data policy governance |
| DLQ | Dead-Letter Queue |
| DTO | Data Transfer Object |
| HA | High Availability |
| HTTP | Hypertext Transfer Protocol |
| JWT | JSON Web Token |
| mTLS | Mutual Transport Layer Security |
| OAS | OpenAPI Specification |
| OAuth | Open Authorization framework |
| RAML | RESTful API Modeling Language |
| RDF | Resource Description Framework |
| RML | Often RDF Mapping Language; confirm project usage |
| REST | Representational State Transfer |
| SLA | Service-Level Agreement |
| SLI | Service-Level Indicator |
| SLO | Service-Level Objective |
| SDLC | Software Development Life Cycle |
| SOAP | XML messaging protocol name (originally an acronym) |
| TLS | Transport Layer Security |
| WSDL | Web Services Description Language |
| XML | Extensible Markup Language |
| XPath | XML Path Language |
| XSD | XML Schema Definition |
| XSLT | Extensible Stylesheet Language Transformations |
| YAML | YAML Ain't Markup Language |

---

# 11. Official References

Use the guide for tonight's preparation. Use these links to verify tenant/version-specific behavior, not as additional material to read end to end.

## Frends

- [Process](https://docs.frends.com/reference/process-development/process)
- [Subprocess](https://docs.frends.com/reference/process-development/subprocess)
- [Shapes](https://docs.frends.com/reference/shapes/shape)
- [Triggers](https://docs.frends.com/reference/shapes/event-shapes/trigger)
- [Task](https://docs.frends.com/reference/shapes/activity-shapes/task)
- [Code Task](https://docs.frends.com/reference/shapes/activity-shapes/code-task)
- [Reference values](https://docs.frends.com/reference/process-development/reference-values)
- [Creating Custom Tasks](https://docs.frends.com/guides/development/creating-custom-tasks)
- [Frends Runtime](https://docs.frends.com/hybrid-integration-architecture/frends-runtime)
- [Environments](https://docs.frends.com/management-and-operations/integration-lifecycle/environments)
- [High Availability](https://docs.frends.com/hybrid-integration-architecture/high-availability)
- [API Management](https://docs.frends.com/frends-development/api-management)
- [Create an API](https://docs.frends.com/guides/api-management/how-to-create-an-api-with-frends)
- [Link a Process to an API endpoint](https://docs.frends.com/guides/api-management/linking-a-process-to-api-endpoint)
- [API Policies](https://docs.frends.com/frends-development/api-management/api-policies)
- [Deploy an API](https://docs.frends.com/guides/api-management/deploying-an-api)
- [Deploy integrations](https://docs.frends.com/guides/integration-management/deploying-integrations)
- [Version Control](https://docs.frends.com/management-and-operations/integration-lifecycle/version-control)
- [Process Instances](https://docs.frends.com/management-and-operations/dashboard-and-monitoring/process-instances)
- [Process Log Settings](https://docs.frends.com/reference/administration/process-log-settings)
- [Error handling and monitoring](https://docs.frends.com/management-and-operations/dashboard-and-monitoring/error-handling-and-monitoring)
- [Test Processes and Tasks](https://docs.frends.com/guides/development/how-to-test-processes-and-tasks)
- [Official Tasks](https://tasks.frends.com/)

## Microsoft .NET and Power Platform

- [Asynchronous programming with async and await](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)
- [IHttpClientFactory](https://learn.microsoft.com/en-us/dotnet/core/extensions/httpclient-factory)
- [System.Text.Json overview](https://learn.microsoft.com/en-us/dotnet/standard/serialization/system-text-json/overview)
- [Newtonsoft.Json documentation](https://www.newtonsoft.com/json/help/html/Introduction.htm)
- [Power Platform ALM](https://learn.microsoft.com/en-us/power-platform/alm/)
- [Power Platform pipelines](https://learn.microsoft.com/en-us/power-platform/alm/pipelines)
- [Power Platform environment variables](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables)
- [Power Platform connectors](https://learn.microsoft.com/en-us/connectors/)
- [Manage on-premises data gateways](https://learn.microsoft.com/en-us/power-automate/gateway-manage)
- [Dataverse security](https://learn.microsoft.com/en-us/power-platform/admin/wp-security)
- [Power Platform data policies](https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention)
- [Power Automate limits and throttling](https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/understand-limits)
- [Create child flows](https://learn.microsoft.com/en-us/power-automate/create-child-flows)

## Standards

- [HTTP Semantics - RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)
- [OAuth 2.0 - RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [OpenAPI Specification](https://spec.openapis.org/oas/)
- [YAML Specification](https://yaml.org/spec/)
- [RAML Specification](https://raml.org/developers/raml-100-tutorial)
- [RML specification site](https://rml.io/specs/rml/)
- [W3C XML](https://www.w3.org/XML/)
- [W3C XSLT](https://www.w3.org/TR/xslt/)
- [W3C SOAP 1.2](https://www.w3.org/TR/soap12-part1/)

## Accuracy note

Frends capabilities and UI labels can differ by tenant/runtime version and installed Task packages. The guide deliberately emphasizes stable concepts. Use editor autocomplete and the tenant's Task documentation for exact input/result property names. Do not memorize version-specific log truncation sizes or assume a newer OpenAPI feature is supported without checking.

---

**End of guide. Protect sleep, retrieve rather than reread, and explain tradeoffs instead of listing features.**
