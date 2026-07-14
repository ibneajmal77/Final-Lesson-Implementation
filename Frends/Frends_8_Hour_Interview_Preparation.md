# Frends Interview: Simple 8-Hour Study Guide

## Read This First

This guide uses simple English.

You do not need to memorize every line.

Study the parts marked **MUST KNOW**.

Use the parts marked **REFERENCE** only when you need more detail.

## Small Glossary

| Word | Simple meaning |
|---|---|
| Contract | Agreed input, output, and behavior |
| Schema | Rules for data shape |
| Mapping | How source fields become target fields |
| Authentication | Prove who is calling |
| Authorization | Check what the caller may do |
| Correlation ID | One ID used to trace a request |
| Timeout | Stop waiting after a time limit |
| Retry | Try the operation again |
| Idempotency | Duplicate protection |
| Rollback | Return code or settings to a safe version |
| Replay | Run failed work again |
| Reconciliation | Compare source and target records |

## Use This Answer Pattern

For most questions, use four steps:

1. **What:** Give a simple meaning.
2. **Why:** Explain why it is useful.
3. **How:** Give one example or a few steps.
4. **Safety:** Explain errors, security, or support.

Example:

> XSD is a rule file for XML. It checks the structure and data types. I use it before sending final XML to another system. If validation fails, I stop the message and record a safe error.

## The One Example Used in This Guide

```text
Order Portal
  -> REST API
  -> JSON request
  -> Frends
  -> XML transformation
  -> SOAP request
  -> Legacy ERP
```

Use this example in the interview. Change it to match your real work.

Do not say that you used a tool if you did not use it.

---

# 1. Exact 8-Hour Plan

This plan is exactly 480 minutes.

It is built for a 3:00 PM interview.

Start at 6:40 AM.

Finish studying at 2:40 PM.

Use 2:40 PM to 3:00 PM to prepare your room, water, camera, notes, and breathing.

| Time | Minutes | Study |
|---|---:|---|
| 06:40-06:55 | 15 | Quick test |
| 06:55-07:50 | 55 | SDLC and a new integration |
| 07:50-08:00 | 10 | Break |
| 08:00-09:10 | 70 | HTTP, security, OpenAPI, and JSON |
| 09:10-09:20 | 10 | Break |
| 09:20-10:10 | 50 | XML, XSD, XPath, XSLT, and SOAP |
| 10:10-10:25 | 15 | Food break |
| 10:25-11:30 | 65 | Frends and project story |
| 11:30-11:40 | 10 | Break |
| 11:40-12:30 | 50 | Errors, release, and production support |
| 12:30-12:40 | 10 | Break |
| 12:40-13:10 | 30 | .NET and Power Platform |
| 13:10-13:20 | 10 | Break |
| 13:20-13:55 | 35 | Top interview questions |
| 13:55-14:00 | 5 | Break |
| 14:00-14:40 | 40 | Mock interview |

If you start late, remove REFERENCE reading.

Do not remove sleep, breaks, the project answer, or the mock interview.

## What You Must Finish in Each Block

### 06:55-07:50

- Understand the SDLC diagram.
- Learn the new-integration steps.
- Speak the project answer once.

### 08:00-09:10

- Understand the HTTP request and response.
- Learn the API security layers.
- Read the OpenAPI tree.
- Explain the four JSON checks.

Use about:

- 10 minutes for HTTP.
- 20 minutes for security.
- 20 minutes for OpenAPI.
- 20 minutes for JSON.

### 09:20-10:10

- Learn the XML-family line.
- Follow one XML value through XPath and XSLT.
- Learn SOAP and WSDL.
- Speak the XML answer once.

### 10:25-11:30

- Learn the Frends platform diagram.
- Follow the Order Process diagram.
- Learn the release path.
- Speak the Frends project answer.

### 11:40-12:30

- Learn the retry decision.
- Learn the timeout example.
- Learn duplicate protection.
- Learn the incident steps.

### 12:40-13:10

- Compare the JSON libraries.
- Explain both meanings of middleware.
- Compare Frends and Power Platform.

### 13:20-13:55

- Answer the top 20 questions.
- Review only weak answers.

### 14:00-14:40

- Complete the mock interview.
- Stop reading new information.

## Quick Test

Give yourself a score for each question:

- `0`: I cannot answer.
- `1`: I know some words.
- `2`: I can explain it and give an example.

Questions:

1. How do you take a new integration to production?
2. What does middleware do?
3. How do you secure an API?
4. What is inside an OpenAPI file?
5. How do you validate required JSON fields?
6. What are XML, XSD, XPath, and XSLT?
7. What is inside a SOAP message?
8. What do you do after a timeout?

Study every `0` first. Then study every `1`.

After each topic, close the file and speak for one minute.

---

# 2. Whole Interview Map - MUST KNOW

Most integration questions follow this path:

```text
Understand the need
  -> agree the contract
  -> design the flow
  -> build it
  -> test it
  -> release it
  -> monitor it
  -> fix and improve it
```

Remember these short lines:

- **SDLC:** Plan -> Design -> Build -> Test -> Release -> Support.
- **Middleware:** Receive -> Check -> Change -> Send -> Track.
- **API security:** Connection -> Identity -> Permission -> Input -> Operations.
- **OpenAPI:** Info -> Servers -> Paths -> Models -> Security.
- **JSON checks:** Syntax -> Shape -> Business -> Outside data.
- **XML family:** XML has data. XSD checks. XPath finds. XSLT changes.
- **SOAP:** Envelope -> Header -> Body -> Fault.
- **Timeout:** The result may be unknown. Check before retry.

---

# 3. SDLC and a New Integration - MUST KNOW

## Simple Meaning

SDLC means Software Development Life Cycle.

It is the full life of a software change.

It starts with a need. It continues through support and improvement.

## SDLC Diagram

```text
Business need
     |
     v
Plan
Why do we need it?
     |
     v
Design
What must it do? How will it work?
     |
     v
Build
Create one complete path
     |
     v
Test
Check normal and failure cases
     |
     v
Release
Move it safely to production
     |
     v
Support
Monitor, recover, and improve
     |
     +--------------------+
                          |
                    feedback and change
                          |
                          v
                         Plan
```

SDLC is a loop.

Production learning can create a new requirement.

## The Six Main Stages

| Stage | Simple meaning | Main output |
|---|---|---|
| Plan | Understand the business need | Goal, owner, and scope |
| Design | Agree how it should work | Contract, mapping, and flow |
| Build | Create the integration | Reviewed Process and settings |
| Test | Prove normal and error cases | Test results and UAT approval |
| Release | Move it to production | Deployment and rollback plan |
| Support | Monitor, recover, and improve | Alerts, runbook, and fixes |

## SDLC Models

### Waterfall

Work moves through large stages in order.

It can fit stable or strongly controlled requirements.

### Agile

Work is delivered in small parts.

The team gets feedback often.

### DevOps

The team also owns release, automation, monitoring, and support.

### Simple Interview Answer

> Waterfall uses larger stages. Agile uses small deliveries and frequent feedback. DevOps adds automated release and operational ownership. Many teams use a mix of these models. The same SDLC work still needs to happen.

## Questions to Ask for a New Integration

### Business

- What problem are we solving?
- Who owns the source and target systems?
- What does success look like?
- Who will support it?

### Contract

- What starts the integration?
- Is there an OpenAPI, WSDL, XSD, or file format?
- Can I see real sample messages?
- What response and error should the caller receive?

### Data

- Which fields are required?
- What do null and empty values mean?
- Who owns each important field?
- How are dates, time zones, decimals, and currencies handled?
- Does the data contain personal or secret information?

### Scale

- How many messages arrive normally?
- What is the peak volume?
- How large is each message?
- How fast must the result be?

### Failure

- What happens if the target is down?
- Can a message be retried?
- How are duplicates prevented?
- How will failed work be replayed?
- How will we compare the source and target?

## A New Project Versus a Change

For a new project, create:

- Owners.
- Contracts.
- Environments.
- Security.
- Release rules.
- Monitoring and support.

For a change, also check:

- Existing users of the API.
- Backward compatibility.
- Old messages still waiting.
- API or schema version.
- Regression tests.
- Migration and deprecation.

Prefer adding an optional field.

Use a new version for a breaking change.

## From Request to Production

1. Understand the goal and owners.
2. Agree the contract and sample messages.
3. Write the field mapping.
4. Choose API, queue, file, database, or schedule.
5. Design security, timeout, retry, and duplicate handling.
6. Build one small end-to-end path.
7. Add validation and error handling.
8. Test normal, invalid, security, timeout, and duplicate cases.
9. Complete UAT.
10. Check production settings and secrets.
11. Deploy with a smoke test and rollback plan.
12. Monitor and compare the first real records.
13. Give support a runbook and replay process.

## Five Readiness Gates

These gates help you decide when to move forward.

```text
Gate 1: Ready to design?
Owners, goal, examples, volume, and security are clear.

        |
        v

Gate 2: Ready to build?
Contract, mapping, error rules, and test plan are agreed.

        |
        v

Gate 3: Ready for UAT?
Normal, invalid, security, duplicate, and timeout tests pass.

        |
        v

Gate 4: Ready for production?
UAT, settings, rollback, smoke test, alerts, and runbook are ready.

        |
        v

Gate 5: Is release complete?
The real target result is checked and the first records match.
```

## Detailed Order Example

The portal must send an order to an old ERP.

1. I confirm the business reason.
2. I find the owners of both systems.
3. I collect OpenAPI, WSDL, XSD, and sample messages.
4. I agree each field mapping.
5. I agree the volume and response-time goal.
6. I agree authentication and permission.
7. I agree invalid, duplicate, and timeout behavior.
8. I design REST and JSON into Frends.
9. I design Frends into SOAP and XML.
10. I build one valid order from start to finish.
11. I add validation, logs, and failure handling.
12. I test security, duplicates, timeout, and SOAP Faults.
13. I complete UAT.
14. I deploy with the right settings and versions.
15. I run a smoke test.
16. I check the real ERP order.
17. I monitor the first records.
18. I give support a runbook.

## Existing Feature Change Diagram

```text
Feature request
      |
      v
Find users and affected steps
      |
      v
Does the contract break old users?
      |
      +-- No --> Add optional behavior
      |             |
      |             v
      |        Regression test
      |
      +-- Yes -> New version or migration
                    |
                    v
              Test old and new users
                    |
                    v
                  UAT
                    |
                    v
           Controlled release and monitoring
```

## 60-Second Interview Answer

> I start by understanding the business goal, owners, source, target, and success rules. I agree the API or message contract, sample data, field mapping, security, volume, and error behavior. I design the flow, including timeout, retry, duplicate protection, logs, and monitoring. I build a small end-to-end path and test normal and failure cases. I release through the approved environments with a smoke test and rollback plan. After release, I monitor the first records, reconcile the result, and give support a runbook.

## If Requirements Change

> I confirm the reason and impact. I update the contract, mapping, tests, estimate, and acceptance rules. I tell all affected owners. I do not hide the change inside the Process.

## If UAT Finds a Defect

> I reproduce it with the same data. I check code, settings, data, permissions, and the requirement. I fix the cause and add a regression test. I deploy through the normal path and ask the user to test again.

## Definition of Done

The work is done when:

- The contract is approved.
- Security and validation work.
- Normal and failure tests pass.
- UAT is approved.
- Production settings are ready.
- Smoke test and rollback steps exist.
- Logs, alerts, replay, and reconciliation work.
- A support owner and runbook exist.

## Recall

1. Say the six SDLC stages.
2. Name five questions for a new integration.
3. What is different about changing an existing API?
4. What is needed before production?

---

# 4. Middleware and the Project Story - MUST KNOW

## Simple Meaning

Middleware sits between systems.

It helps systems communicate.

It can change protocol, format, security, or timing.

## What Middleware Does

Remember:

**Receive -> Check -> Change -> Send -> Track**

- Receive a request, file, or message.
- Check the caller and data.
- Change the data or protocol.
- Send it to the correct system.
- Track success, failure, and recovery.

## Project Picture

```text
Order Portal sends REST and JSON
  -> Frends checks security and data
  -> Frends maps the order
  -> Frends creates ERP XML
  -> Frends validates the final XML with XSD
  -> Frends sends a SOAP request
  -> ERP returns a result
  -> Frends logs and returns a safe response
```

## Detailed Middleware Diagram

```text
Order Portal
REST + JSON
     |
     v
+----------------------+
| Frends API Policy    |
| Check caller         |
| Check path and method|
| Apply traffic rules  |
+----------------------+
     |
     v
+----------------------+
| API Trigger          |
| Start one Process    |
+----------------------+
     |
     v
+-------------------------------+
| Order Process                 |
| 1. Keep correlation ID        |
| 2. Validate JSON              |
| 3. Check business rules       |
| 4. Check duplicate key        |
| 5. Map to an internal order   |
| 6. Create internal XML        |
| 7. Transform to ERP XML       |
| 8. Validate with ERP XSD      |
+-------------------------------+
     |
     v
Legacy ERP
SOAP + XML
     |
     v
Check HTTP status and SOAP Fault
     |
     v
Map the result to REST JSON
     |
     v
Log, monitor, store result, and reconcile
     |
     v
Order Portal
```

## Failure Paths

```text
Invalid data
   -> Return safe 400
   -> Do not call ERP

No or bad identity
   -> Return 401

Identity has no permission
   -> Return 403

Permanent SOAP Fault
   -> Record rejection
   -> Do not retry

Temporary target problem
   -> Limited retry
   -> Wait between attempts

Timeout after sending order
   -> Result is unknown
   -> Search ERP before retry

Same request again
   -> Use idempotency key
   -> Return known result
```

## Why Use Middleware?

- The portal does not need to understand SOAP.
- The ERP does not need to understand JSON.
- Security rules can be in one place.
- Mapping and error handling are easier to support.
- Logs can connect the full flow.
- One system can change with less effect on the other.

## 60-Second Project Answer

> One project connected an order portal to a legacy ERP. The portal used REST and JSON. The ERP used SOAP and XML. Frends checked the caller, validated the JSON, added a correlation ID, and prevented duplicate orders. It mapped the order, transformed it into the ERP XML format, and validated the final XML against the XSD. It then called the SOAP service and checked both the HTTP result and SOAP Fault. Temporary errors used limited retries only when duplicate handling was safe. Support could search by order ID and correlation ID.

## Explain Your Role

Use this sentence:

> I owned [requirements, mapping, Process design, testing, release, or support]. The team owned [other work]. My hardest decision was [decision]. I proved it with [test, log, metric, or result].

Use only real facts.

## Synchronous Versus Asynchronous

### Synchronous

The caller waits for the final result.

Use it when the work is fast and reliable.

### Asynchronous

The API accepts the work and finishes later.

It may return `202 Accepted`.

The caller needs a status URL, callback, or another result method.

Use it when the work is slow or the target is not always available.

## Recall

1. Say the five middleware actions.
2. Why use middleware?
3. Tell the order story in one minute.
4. When would you use `202 Accepted`?

# 5. HTTP and REST - MUST KNOW

## HTTP in Simple Words

HTTP is how many APIs send requests and responses.

An HTTP request has:

- A method.
- A URL.
- Headers.
- Sometimes a body.

An HTTP response has:

- A status code.
- Headers.
- Sometimes a body.

## Request and Response Diagram

```text
Client
  |
  |  HTTP request
  |  method + URL + headers + optional body
  v
API Policy or Gateway
  |
  v
Frends Process
  |
  v
Target system
  |
  |  HTTP response
  |  status + headers + optional body
  v
Client
```

## Example Request

```http
POST /orders HTTP/1.1
Authorization: Bearer <access-token>
Content-Type: application/json
Accept: application/json
X-Correlation-ID: abc-123
Idempotency-Key: ORD-1001

{
  "orderId": "ORD-1001",
  "amount": 125.50
}
```

Line by line:

- `POST` asks the API to create or start work.
- `/orders` is the resource path.
- `Authorization` carries the access token.
- `Content-Type` says the body is JSON.
- `X-Correlation-ID` connects logs.
- `Idempotency-Key` helps stop duplicate orders.
- The body contains the order data.

## Example Asynchronous Response

```http
HTTP/1.1 202 Accepted
Content-Type: application/json
Location: /operations/OP-9001
X-Correlation-ID: abc-123

{
  "operationId": "OP-9001",
  "status": "Pending"
}
```

`202` means the API accepted the work.

It does not mean the ERP finished the order.

The `Location` gives the caller a place to check.

## Common Methods

| Method | Simple use |
|---|---|
| `GET` | Read data |
| `POST` | Create data or start work |
| `PUT` | Replace a known resource |
| `PATCH` | Change part of a resource |
| `DELETE` | Remove a resource |

## Status Codes

Remember the groups:

- `2xx`: success.
- `4xx`: caller, access, or request problem.
- `5xx`: server or target problem.

| Code | Simple meaning |
|---|---|
| `200` | Success |
| `201` | Created; often return a `Location` |
| `202` | Accepted, but not finished |
| `204` | Success with no body |
| `400` | Bad request or invalid contract |
| `401` | Login or token is missing or invalid |
| `403` | Caller is known but not allowed |
| `404` | Route or resource not found |
| `405` | HTTP method is not allowed |
| `409` | Conflict, such as a duplicate ID |
| `415` | Body format is not supported |
| `422` | Business validation failed, if the API uses this rule |
| `429` | Too many requests |
| `500` | Unexpected server error |
| `502` | Gateway received a bad target response |
| `503` | Service is unavailable |
| `504` | Gateway waited too long |

First find which system returned the code.

Do not retry every error.

## Status Decision Diagram

```text
Response received
       |
       v
Which layer returned it?
Caller <- Gateway <- Frends <- Target
       |
       v
What type is it?
       |
       +-- 2xx
       |     -> Check the expected result
       |
       +-- Permanent 4xx
       |     -> Correct request, identity, or permission
       |
       +-- 429
       |     -> Follow Retry-After
       |     -> Retry only when safe
       |
       +-- Temporary connection or selected 5xx
       |     -> Limited retry
       |     -> Wait between attempts
       |
       +-- Timeout after a write
             -> Result is unknown
             -> Search by business ID
             -> Reconcile before retry
```

## Important Headers

### Request

- `Authorization`: access token or credential.
- `Content-Type`: format of the body.
- `Accept`: response format wanted by the caller.
- `X-Correlation-ID`: connects logs across systems.
- `Idempotency-Key`: helps prevent duplicate work.

### Response

- `Content-Type`: response format.
- `Location`: new resource or status URL.
- `Retry-After`: when the caller may try again.
- `Cache-Control: no-store`: do not store a sensitive response.

Never log a token, API key, password, or secret.

## REST Versus SOAP

### REST

- Uses HTTP methods and URLs.
- Often uses JSON.
- Usually uses an OpenAPI contract.

### SOAP

- Uses XML messages.
- Uses Envelope, Header, Body, and Fault.
- Usually uses WSDL and XSD.

Choose the style required by the systems and contract.

## 30-Second Answer

> An HTTP request has a method, URL, headers, and sometimes a body. The response has a status, headers, and sometimes a body. I use status codes to separate success, caller problems, and server problems. Before I retry, I find which system returned the error and whether the action is safe to repeat.

---

# 6. API Security - MUST KNOW

## Simple Memory Map

**Connection -> Identity -> Permission -> Input -> Operations**

## Security Layers Diagram

```text
Internet or private network
        |
        v
HTTPS or mTLS
Protect the connection
        |
        v
Authentication
Who is calling?
        |
        v
Authorization
What may this caller do?
        |
        v
Input checks
Method, size, fields, values
        |
        v
Traffic controls
Rate limit and timeout
        |
        v
Protected secrets and safe logs
        |
        v
Monitoring and alerts
```

## 1. Protect the Connection

- Use HTTPS.
- Use a trusted certificate.
- Use mTLS when both systems must show certificates.

mTLS proves certificate identity.

It does not replace business permission checks.

## 2. Check Identity

Authentication asks:

> Who is calling?

Common choices:

- OAuth access token.
- API key.
- Client certificate.

## 3. Check Permission

Authorization asks:

> Is this caller allowed to do this action on this record?

A valid token does not give access to every order.

Use least privilege.

This means giving only the access that is needed.

## 4. Check Input

Check:

- Method.
- Content type.
- Body size.
- Required fields.
- Data types and allowed values.
- Business rules.
- Resource ownership.

Treat every request as untrusted.

## 5. Protect Operations

- Use rate limits.
- Use timeouts.
- Store secrets outside the Process.
- Rotate secrets and certificates.
- Return safe errors.
- Mask sensitive log data.
- Monitor failed access.

## Authentication Versus Authorization

- Authentication means identity.
- Authorization means permission.

`401` normally means identity is missing or invalid.

`403` normally means the caller is known but not allowed.

## OAuth Client Credentials

This flow is common for one service calling another service.

1. The client sends its credential to the identity provider.
2. The identity provider returns a short-lived token.
3. The client sends the token to the API.
4. The API validates the token.
5. The API checks the required scope or role.

## OAuth Diagram

```text
Service client
      |
      | client ID + secret or certificate
      v
Identity provider
      |
      | short-lived access token
      v
Service client
      |
      | Authorization: Bearer <token>
      v
Frends API Policy or Gateway
      |
      | check token and route access
      v
Frends Process
      |
      | check business permission and input
      v
Target system
```

Important:

- The client secret goes to the identity provider.
- The client secret does not go to the Order API.
- The access token may be a JWT.
- Some access tokens are not JWTs.
- The API follows the identity provider's validation method.

The token is normally sent like this:

```text
Authorization: Bearer <token>
```

Cache the token until shortly before it expires.

Do not request a new token for every API call.

## Five JWT Questions

JWT is a common token format.

Ask:

1. Who signed it?
2. Who issued it?
3. Which API is it for?
4. Is it still valid now?
5. What may it do?

This means checking:

- Signature and allowed algorithm.
- Issuer.
- Audience.
- Expiry and not-before time.
- Scope or role.

Use a trusted token library.

Decoding a token is not the same as validating it.

## Frends API Policy

OpenAPI describes the security requirement.

The Frends API Policy helps enforce access at runtime.

The Process may also check business permission.

Tests prove that security works.

Do not assume that YAML alone secures the API.

## CORS

CORS is a browser rule.

It controls which websites may call an API from browser code.

CORS is not authentication.

## Security Tests

Test:

- No token.
- Invalid token.
- Expired token.
- Wrong audience.
- Missing scope or role.
- Access to another customer's record.
- Wrong content type.
- Large or invalid body.
- Too many requests.
- Safe error and safe logs.

## 60-Second Answer

> I secure an API in layers. I use HTTPS, authenticate the caller, and check permission for the exact action and record. I validate the method, content type, size, fields, and business rules. I use rate limits, timeouts, protected secrets, safe errors, and safe logs. OpenAPI describes security, while the Frends API Policy and Process enforce it. I also test missing, invalid, expired, and under-permissioned tokens.

---

# 7. OpenAPI, YAML, JSON, Swagger, and RAML - MUST KNOW

## Simple Meaning

OpenAPI is a contract for an HTTP API.

It tells people and tools:

- Which URLs exist.
- Which methods are allowed.
- What data can be sent.
- What responses can return.
- What security is needed.

## OpenAPI Tree Diagram

```text
openapi
|
+-- info
|   +-- title
|   +-- API version
|
+-- servers
|   +-- DEV, TEST, or PROD base URL
|
+-- paths
|   +-- /orders
|       +-- post
|           +-- parameters
|           +-- requestBody
|           +-- responses
|           +-- security
|
+-- components
|   +-- schemas
|   +-- parameters
|   +-- responses
|   +-- securitySchemes
|
+-- security
    +-- global default
```

Think of it like a folder tree.

The top tells you about the whole API.

Each path tells you about one URL.

Each method tells you about one action.

Swagger is the old specification name.

Swagger is also the name of API tools.

## Main OpenAPI Parts

Remember:

**Info -> Servers -> Paths -> Models -> Security**

| Part | Simple meaning |
|---|---|
| `openapi` | OpenAPI standard version |
| `info` | API title and API version |
| `servers` | Base URLs |
| `paths` | URLs and HTTP methods |
| `components` | Reusable models and security schemes |
| `security` | Default security requirement |

Inside an operation, look for:

- `summary`.
- `operationId`.
- `parameters`.
- `requestBody`.
- `responses`.
- `security`.

Inside a data model, look for:

- `type`.
- `properties`.
- `required`.
- `items` for arrays.
- `enum`.
- Length and number limits.
- `additionalProperties`.
- `$ref` for reuse.

## YAML Versus JSON

YAML and JSON can describe the same OpenAPI contract.

### YAML

- Uses indentation.
- Uses `key: value`.
- Uses `-` for a list.
- Uses spaces, not tabs.

### JSON

- Uses braces and brackets.
- Uses double quotes.
- Uses commas.

`.yml` and `.yaml` are both YAML file names.

RAML is another API description language.

RAML means RESTful API Modeling Language.

If the interviewer says RML, ask what they mean.

RML may mean RDF Mapping Language.

## Small OpenAPI Example

Read this example. Do not memorize it.

```yaml
openapi: 3.0.1
info:
  title: Order API
  version: 1.0.0

paths:
  /orders:
    post:
      operationId: createOrder
      security:
        - BearerAuth: []
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
          description: Invalid token

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Order:
      type: object
      required: [orderId, amount]
      properties:
        orderId:
          type: string
          minLength: 1
        amount:
          type: number
          minimum: 0.01
```

Frends commonly supports OpenAPI 3.0.1 and older Swagger 2.0.

Check the version supported by the real tenant.

## How to Read the Example

Start at `paths`.

Find `/orders`.

Then find `post`.

The operation says:

1. The caller needs bearer security.
2. The body is required.
3. The body uses the Order model.
4. `202` means accepted.
5. `400` means invalid input.
6. `401` means invalid identity.

Then go to `components`.

There you can find:

- How bearer security is described.
- Which Order fields exist.
- Which Order fields are required.
- Which limits apply.

## Where Headers Go

### Authentication Header

Put bearer, OAuth, or API-key rules in:

```text
components -> securitySchemes
```

Do not model `Authorization` as a normal parameter.

### Normal Request Header

Put a correlation header in operation `parameters`.

### Response Header

Put a response header under the response:

```yaml
'429':
  description: Too many requests
  headers:
    Retry-After:
      schema:
        type: integer
```

## Security Rules

- Global `security` applies to operations by default.
- An operation can override the global rule.
- Two security entries mean either one can be used.
- Two schemes in one entry mean both are needed.
- Runtime policy still decides real access.

## Good OpenAPI Rules

- Use a unique `operationId`.
- Make every path parameter required.
- Give every response a description.
- Quote YAML status codes such as `'200'`.
- Use reusable models with `$ref`.
- Define required fields at every object level.
- Add normal and error responses.
- Never put a real token or personal record in an example.
- Lint the file.
- Test the real API against the contract.
- Version a breaking change.

## 60-Second Answer

> OpenAPI is the contract for an HTTP API. I remember Info, Servers, Paths, Models, and Security. Operations describe parameters, request bodies, responses, and security. Models describe properties, required fields, types, and limits. YAML and JSON are only two ways to write the same OpenAPI model. The file helps documentation and testing, but the runtime still has to enforce validation and security.

---

# 8. JSON Validation - MUST KNOW

## Four Checks

Remember:

**Syntax -> Shape -> Business -> Outside data**

## Validation Flow Diagram

```text
JSON text
   |
   v
Can it be parsed?
   |
   +-- No --> Safe 400 error
   |
   v
Does the shape match?
required fields, types, limits
   |
   +-- No --> Safe field errors
   |
   v
Do business rules pass?
   |
   +-- No --> Safe business error
   |
   v
Do outside facts pass?
customer exists and caller is allowed
   |
   +-- No --> Safe not-found or permission error
   |
   v
Continue with the integration
```

## 1. Syntax

Ask:

- Is it valid JSON?
- Is the content type correct?
- Is the body size allowed?

## 2. Shape

Ask:

- Is the root the correct type?
- Are required fields present?
- Are nested required fields present?
- Are data types correct?
- Are values inside allowed limits?
- Are unknown fields allowed?

## 3. Business Rules

Examples:

- Amount must be greater than zero.
- End date cannot be before start date.
- Currency must be allowed.

## 4. Outside Data

Examples:

- Does the customer exist?
- Is the product active?
- May the caller submit for this customer?
- Was the order already completed?

## Required Fields Example

```yaml
type: object
required:
  - orderId
  - customer
properties:
  orderId:
    type: string
    minLength: 1
  customer:
    type: object
    required:
      - customerId
    properties:
      customerId:
        type: string
```

Important:

- `properties` describes possible fields.
- `required` makes selected fields mandatory.
- A nested object needs its own `required` list.
- Missing, null, and empty are different.
- Required means present. It does not always mean non-null.
- In OpenAPI 3.0, use `nullable: true` when null is allowed.
- `additionalProperties: false` rejects unknown fields.
- A strict unknown-field rule can reduce future compatibility.
- `format` may not be checked by every validator.
- `default` may not be added automatically.

## Four Similar Requests

### Valid

```json
{
  "orderId": "ORD-1001",
  "customer": {
    "customerId": "C-100"
  }
}
```

### Missing Field

```json
{
  "customer": {
    "customerId": "C-100"
  }
}
```

The `orderId` property is not present.

### Null Field

```json
{
  "orderId": null,
  "customer": {
    "customerId": "C-100"
  }
}
```

The property is present.

The value is null.

The schema must say whether null is allowed.

### Empty Field

```json
{
  "orderId": "",
  "customer": {
    "customerId": "C-100"
  }
}
```

The property is present.

The string is empty.

Use `minLength: 1` when empty text is not allowed.

## Example Error Result

```json
{
  "status": 400,
  "correlationId": "abc-123",
  "errors": [
    {
      "path": "$.orderId",
      "code": "required",
      "message": "orderId is required"
    }
  ]
}
```

This helps the caller fix the request.

It does not show internal code or secrets.

Parsing JSON is not full validation.

Creating a .NET object is not full validation.

## What to Test

For each important field, test:

- Missing.
- Null.
- Empty.
- Wrong type.
- Too small or too large.
- Unknown value.
- Extra field.
- Valid boundary.

## Safe Error

Return:

- HTTP status.
- Field path.
- Simple error code.
- Safe message.
- Correlation ID.

Do not return a stack trace or secret.

## 60-Second Answer

> I validate JSON in four steps. First, I check syntax, content type, and size. Second, I check the contract shape, including required fields, nested fields, types, limits, and unknown fields. Third, I check business rules. Finally, I check outside facts and permission. I test missing, null, empty, wrong-type, extra, and boundary values. I return a safe field-level error with a correlation ID.

## Recall

1. Say the five OpenAPI parts.
2. YAML versus JSON?
3. Where is bearer security defined?
4. What is the difference between `properties` and `required`?
5. Say the four JSON checks.

# 9. XML, XSD, XPath, XSLT, WSDL, and SOAP - MUST KNOW

## One-Line Meaning

| Name | Simple meaning |
|---|---|
| XML | Holds data |
| XSD | Defines XML rules |
| XPath | Finds XML values |
| XSLT | Changes XML |
| WSDL | Describes a SOAP service |
| SOAP | Carries an XML message |

Say this:

> XML has data. XSD checks it. XPath finds it. XSLT changes it. WSDL describes the service. SOAP carries the message.

## XML Family Diagram

```text
Source XML
   |
   +---- XSD checks it ------> valid or invalid
   |
   +---- XPath finds --------> one node or value
   |
   +---- XSLT changes -------> target XML
                                   |
                                   v
                               SOAP Body
                                   |
                                   v
                              SOAP service

WSDL describes the SOAP service.
It tells us the address, actions, messages, and XSD types.
```

## XML Parts

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ord:Order xmlns:ord="urn:orders" id="1001">
  <ord:Customer>A &amp; B Ltd</ord:Customer>
  <ord:Amount currency="USD">25.50</ord:Amount>
</ord:Order>
```

- The first line is the XML declaration.
- `ord:Order` is the root element.
- `ord:Customer` is a child element.
- `id` and `currency` are attributes.
- `25.50` is text.
- `xmlns:ord` defines a namespace.
- `&amp;` means `&`.

XML is case-sensitive.

An XML document must have one root element.

## Well-Formed Versus Valid

- **Well-formed:** XML syntax is correct.
- **Valid:** XML is well-formed and also follows its XSD.

## Namespace

A namespace separates XML vocabularies.

The namespace URI is the identity.

The prefix is only a short name.

These prefixes can mean the same namespace:

```xml
<a:Order xmlns:a="urn:orders"/>
<ord:Order xmlns:ord="urn:orders"/>
```

A wrong namespace is a common reason for an empty XPath result.

## Missing, Empty, and Nil

- Missing: there is no element.
- Empty: `<Name/>`.
- Nil: the element says there is no value.

Nil needs:

- The `xsi` namespace.
- `nillable="true"` in the XSD.

These three cases are not the same.

## XSD

XSD is the rule file for XML.

It can define:

- Elements and attributes.
- Data types.
- Child order.
- Required and optional values.
- Repeated values.
- Allowed values and limits.
- Namespace.

Important words:

| XSD word | Simple meaning |
|---|---|
| `element` | An XML element |
| `attribute` | An XML attribute |
| `simpleType` | A simple value |
| `complexType` | A value with children or attributes |
| `sequence` | Children appear in this order |
| `choice` | One option is allowed |
| `minOccurs` | Minimum count |
| `maxOccurs` | Maximum count |
| `restriction` | A value limit |

XSD checks structure and values.

It does not prove that a customer exists.

`targetNamespace` says which namespace the XSD defines.

## What XSD Checks in the Order

```text
Order
|
+-- id attribute
|   Must be present
|
+-- Customer
|   Must be present text
|
+-- Amount
    Must be a decimal
    currency attribute must be present
```

An XSD can also say:

- Currency must be USD, EUR, or GBP.
- One order can have many order lines.
- A note is optional.
- A date must use a valid date format.

XSD cannot check whether the customer exists in the ERP.

## XPath

XPath is an address for XML data.

```xpath
/ord:Order/ord:Customer
/ord:Order/@id
```

- `/` follows a path.
- `//` searches below the current node.
- `` selects an attribute.
- `[...]` adds a condition.

Bind the correct namespace before using the path.

## XPath Example Results

For the XML above:

| XPath | Result |
|---|---|
| `/ord:Order/@id` | `1001` |
| `/ord:Order/ord:Customer` | `A & B Ltd` |
| `/ord:Order/ord:Amount` | `25.50` |
| `/ord:Order/ord:Amount/@currency` | `USD` |

Common problem:

```text
The element is visible.
XPath returns nothing.
        |
        v
Check the namespace URI and prefix first.
```

## XSLT

XSLT changes XML into another format.

It uses XPath to find source values.

It uses templates to build the result.

Common parts are:

- `xsl:template`.
- `xsl:value-of`.
- `xsl:for-each`.
- `xsl:if`.
- `xsl:choose`.

For the order project:

1. Create a simple internal XML.
2. Use XSLT to create the ERP XML.
3. Validate the final ERP XML with the target XSD.

## XSLT Mapping Picture

```text
Source XML                         ERP XML
----------                         -------
Order/@id          ------------->  ErpOrder/OrderNumber
Order/Customer     ------------->  ErpOrder/BuyerName
Order/Amount       ------------->  ErpOrder/Total
Amount/@currency   ------------->  Total/@currency
```

Example target:

```xml
<ErpOrder>
  <OrderNumber>1001</OrderNumber>
  <BuyerName>A &amp; B Ltd</BuyerName>
  <Total currency="USD">25.50</Total>
</ErpOrder>
```

XPath finds the source values.

XSLT places them in the target structure.

Test namespaces, missing fields, repeated fields, dates, decimals, and encoding.

## XSD Versus XPath Versus XSLT

Use this answer:

> XSD asks, "Is this XML allowed?" XPath asks, "Where is the value?" XSLT asks, "What should this XML become?" XSD validates, XPath selects, and XSLT transforms.

## SOAP Message

Remember:

**Envelope -> Header -> Body -> Fault**

- Envelope is the outer SOAP message.
- Header has metadata or security.
- Body has the business request or response.
- Fault has the SOAP error.

## SOAP Shape

```text
Envelope
|
+-- Header
|   +-- security
|   +-- address
|   +-- correlation ID
|
+-- Body
    +-- business request or response
    |
    +-- Fault when SOAP processing fails
```

## SOAP Example

```xml
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <CorrelationId>abc-123</CorrelationId>
  </soap:Header>
  <soap:Body>
    <CreateOrder>
      <OrderNumber>1001</OrderNumber>
    </CreateOrder>
  </soap:Body>
</soap:Envelope>
```

The example is simplified.

The real business elements may also use namespaces.

A SOAP Header is inside the XML.

An HTTP header belongs to the network request.

They are different.

## WSDL

WSDL describes:

- Data types.
- Messages.
- Operations.
- Protocol binding.
- Service address.

WSDL describes the service.

XSD describes the XML data.

## WSDL Diagram

```text
WSDL
|
+-- Where?
|   Service address
|
+-- What action?
|   CreateOrder operation
|
+-- What input?
|   CreateOrderRequest message
|
+-- What output?
|   CreateOrderResponse message
|
+-- What error?
|   Declared Fault
|
+-- How?
|   SOAP binding and version
|
+-- What data?
    XSD types
```

When calling a SOAP service, check:

1. Service address.
2. SOAP version.
3. SOAP action.
4. Content type.
5. Header rules.
6. Input XML namespace.
7. Output and Fault messages.

## SOAP Details

- SOAP 1.1 often uses `text/xml`.
- SOAP 1.1 often uses the `SOAPAction` HTTP header.
- SOAP 1.2 often uses `application/soap+xml`.
- Follow the WSDL.
- Check the HTTP status and SOAP Fault.
- Use WS-Security only when the contract requires it.
- Disable unsafe external XML entities for untrusted XML.

## 60-Second Answer

> XML holds hierarchical data. XSD defines the allowed structure and values. XPath finds nodes, and XSLT changes XML into another structure. Namespaces are important because a wrong namespace can make XPath return nothing. SOAP has an Envelope, Header, Body, and Fault. WSDL describes the SOAP service, while XSD describes the XML data. I transform into the target XML and then validate it with the target XSD.

## Recall

1. Say the six XML-family meanings.
2. Well-formed versus valid?
3. XSD versus XPath versus XSLT?
4. Say the four SOAP parts.
5. WSDL versus XSD?

---

# 10. Frends - MUST KNOW

## Simple Meaning

Frends is a low-code integration platform.

It connects APIs, files, databases, messages, and systems.

Low-code makes the flow visual.

Good engineering is still needed.

## Four Groups

Remember:

**Define -> Deploy -> Run -> Observe**

## Frends Platform Diagram

```text
Tenant
|
+-- Environments
|   +-- DEV
|   +-- TEST
|   +-- UAT
|   +-- PROD
|
+-- Execution
|   +-- Agent Groups
|       +-- Agent 1
|       +-- Agent 2
|
+-- Integration design
|   +-- API definition
|   +-- API Policy
|   +-- Triggers
|   +-- Processes
|       +-- Tasks
|       +-- Decisions
|       +-- Loops
|       +-- Scopes and Catch
|       +-- Subprocesses
|
+-- Operations
    +-- Process Instances
    +-- Logs
    +-- Promoted values
    +-- Metrics and alerts
```

This is a learning picture.

Menu names can differ by Frends version.

## 1. Define the Flow

- A **Trigger** starts work.
- A **Process** is the full visual flow.
- A **Task** performs one action.
- A **Decision** chooses a path.
- A **Loop** repeats work.
- A **Scope and Catch** handle a group of errors.
- A **Subprocess** holds a smaller reusable flow.
- **Return** sends the result.
- **Throw** stops the flow with an error.

## 2. Deploy the Flow

- The hierarchy is Tenant -> Environments -> Agent Groups -> Agents.
- A **Tenant** is the main organization area.
- An **Environment** can be DEV, TEST, UAT, or PROD.
- Environment values hold URLs and other settings.
- Protected settings hold secrets and certificates.
- Versions move through approved environments.

## 3. Run the Flow

- An **Agent** runs the Process.
- An **Agent Group** contains one or more Agents.
- A Process may run on any Agent in the group.
- Shared state must use a shared and safe store.

Do not keep duplicate-control data only in one Agent's memory.

## 4. Observe the Flow

- A **Process Instance** is one Process run.
- Logs explain steps and errors.
- Promoted values make safe IDs searchable.
- Metrics show count, duration, and failures.
- Alerts tell support when action is needed.

Promoted values are logged.

Never promote a secret, token, or sensitive personal value.

## Frends API Flow

```text
API request
  -> API Policy
  -> API Trigger
  -> Process
  -> Tasks and Subprocesses
  -> Return
```

- OpenAPI describes the API.
- API Policy controls incoming access.
- API Trigger starts the linked Process.
- Process performs the business flow.

## The Order Process in Frends

1. API Policy checks the caller.
2. API Trigger starts the Process.
3. Process creates or keeps a correlation ID.
4. It validates JSON and business rules.
5. It checks the duplicate-protection key.
6. It maps the order.
7. It creates and transforms XML.
8. It validates the final XML with XSD.
9. It calls the SOAP ERP.
10. It checks HTTP status and SOAP Fault.
11. It returns a safe result.
12. It logs safe IDs and metrics.

## Process Decision Diagram

```text
API Policy
    |
    v
API Trigger
    |
    v
Create or keep correlation ID
    |
    v
Validate request
    |
    v
Is it valid?
    |
    +-- No
    |    |
    |    v
    |  Return safe field error
    |
    +-- Yes
         |
         v
    Check duplicate key
         |
         +-- Already complete
         |      |
         |      v
         |  Return saved result
         |
         +-- New
                |
                v
             Map order
                |
                v
          Create target XML
                |
                v
            Call ERP
          +-----+------+
          |            |
       Success       Failure
          |            |
          v            v
    Map response   Classify error
          |       Retry only if safe
          v            |
    Promote safe IDs   v
          |        Log and recover
          v
       Return
```

## Keep a Process Easy to Read

- Use business names, such as `Validate order`.
- Give each Process one clear job.
- Use a Subprocess for repeated flow.
- Keep expressions small.
- Keep URLs and secrets outside the Process.
- Catch errors where useful action is possible.
- Do not build one very large Process.

## Built-In Task Versus Custom .NET

Use a built-in Task when it solves the need.

Use a Subprocess for reusable visual flow.

Use custom .NET only when:

- A supported Task cannot solve the need clearly.
- The logic is reusable.
- The team can test and support it.

## Frends Error Points

- An HTTP `4xx` or `5xx` may need a status check.
- A Task may have an option to throw on an error status.
- Check the real Task behavior.
- An unhandled-error Subprocess cannot resume a failed Process.
- Keep the original error and add safe context.

## Release Path

```text
DEV -> TEST -> UAT -> PROD -> Smoke test -> Monitor
```

Before production, check:

- Correct Process and Subprocess versions.
- Environment values.
- Secret and certificate references.
- API Policy and Agent Group.
- Network access.
- Trigger state.
- Rollback steps.

## Deployment Diagram

```text
One reviewed integration version

DEV --------> TEST --------> UAT --------> PROD
 |              |              |             |
Developer       Integration    Business      Smoke test
checks          and failure    acceptance    Monitor
Review          tests          approval      Reconcile

Each environment has its own:
URL
identity
secret reference
certificate
Agent Group
permissions
```

The Process must not contain a production password.

The Process must not contain a hard-coded production URL.

## Create a Frends API from Start to Production

1. Create or import the supported OpenAPI file.
2. Review paths, methods, models, responses, and security.
3. Create the API Trigger.
4. Link the Trigger to the correct Process.
5. Apply the API Policy.
6. Select the correct Agent Group.
7. Add environment values.
8. Add protected secret and certificate references.
9. Test the Process directly.
10. Test through the real API path.
11. Deploy through DEV, TEST, UAT, and PROD.
12. Run a production smoke test.
13. Find the Process Instance.
14. Check the real target result.
15. Monitor the first requests.

## Inbound and Outbound Network Paths

```text
Inbound request
Caller
  -> DNS
  -> TLS
  -> Gateway or API Policy
  -> API Trigger
  -> Process

Outbound call
Process or Agent
  -> DNS
  -> Proxy or firewall
  -> TLS
  -> Target service
```

An API can accept inbound traffic and still fail outbound traffic.

Check both paths.

## 60-Second Answer

> In Frends, a Trigger starts a Process. Tasks perform steps, Decisions choose paths, and Subprocesses hold reusable flow. Agents run Processes in an environment. For an API, an API Policy controls access and an API Trigger starts the Process. I keep URLs and secrets outside the Process. I use correlation IDs, safe promoted values, error handling, tests, versioned deployment, logs, metrics, alerts, and a replay plan.

## Recall

1. What are Define, Deploy, Run, and Observe?
2. Trigger versus Process versus Task?
3. API Policy versus OpenAPI?
4. What must never be promoted?
5. What do you check before production?

# 11. Errors, Retry, Release, and Support - MUST KNOW

## Five Error Groups

Remember:

**Data -> Access -> Temporary -> Unknown -> Internal**

| Group | Example | Normal action |
|---|---|---|
| Data | Missing field or bad XML | Reject and correct |
| Access | Bad token or missing role | Fix identity or permission |
| Temporary | Connection reset or short outage | Retry only when safe |
| Unknown | Timeout after sending work | Check target before retry |
| Internal | Bad mapping, setting, or code | Investigate and fix |

## Retry

Retry only a temporary problem.

A good retry has:

- A small attempt limit.
- A longer wait each time.
- A small random delay.
- A timeout for each call.
- Duplicate protection.
- Logs and metrics.

For `429`, follow `Retry-After` when it is provided.

Do not retry:

- Bad input.
- Bad credentials.
- Missing permission.
- A permanent business rejection.
- A timed-out write when the result is unknown.

## Retry Decision Diagram

```text
Call target
    |
    v
What happened?
    |
    +-- Success
    |     -> Finish
    |
    +-- Bad input or business rejection
    |     -> Stop
    |     -> Correct the data
    |
    +-- Bad identity or permission
    |     -> Stop
    |     -> Fix access
    |
    +-- Temporary problem
    |     -> Is another call duplicate-safe?
    |          |
    |          +-- No  -> Stop and investigate
    |          |
    |          +-- Yes -> Wait and retry
    |
    +-- Timeout
          -> Result is unknown
          -> Check by business ID
```

## Retry Timeline Example

```text
Attempt 1
   |
   +-- temporary 503
   |
Wait 2 seconds
   |
Attempt 2
   |
   +-- temporary 503
   |
Wait 5 seconds
   |
Attempt 3
   |
   +-- still failing
   |
Stop retrying
Save safe failure details
Alert or move to recovery
```

The exact times depend on the system.

The important rule is a clear limit.

## Duplicate Protection

The technical word is **idempotency**.

Simple design:

1. The caller sends an idempotency key or business ID.
2. The integration stores the key and result.
3. The same key does not create the work again.
4. A repeated request returns the known result.

Use a shared and durable store.

The check and save must be atomic.

Atomic means two requests cannot both win at the same time.

## Duplicate Key Diagram

```text
Request with key ORD-1001
           |
           v
Check key in an atomic shared store
           |
           +-- New key
           |     -> Start work
           |     -> Save final result
           |
           +-- Work is running
           |     -> Return current status
           |
           +-- Work is complete
           |     -> Return saved result
           |
           +-- Same key, different body
                 -> Return conflict
```

The same key should represent the same request.

## Timeout

A timeout means:

> I did not receive the answer in time.

It does not prove that the target failed.

Do this:

1. Stop blind retries.
2. Search by order ID or idempotency key.
3. If the target completed the work, record success.
4. Retry only when duplicate work cannot happen.
5. Compare the source and target records.

Comparing source and target records is called **reconciliation**.

## Timeout Example

```text
Frends sends ORD-1001
        |
        v
ERP creates ORD-1001
        |
        v
ERP response is lost
        |
        v
Frends sees a timeout
        |
        v
Do not send the order again yet
        |
        v
Search ERP for ORD-1001
        |
        +-- Found
        |     -> Record success
        |
        +-- Not found
              -> Retry only with duplicate protection
```

## Queue and Dead-Letter Queue

Many queues can deliver the same message more than once.

The consumer must handle duplicates.

- Acknowledge after safe completion.
- Limit retry attempts.
- Move poison messages to a dead-letter queue.
- Record a safe reason.
- Fix the cause before replay.
- Replay slowly and verify the result.
- Keep order by business key only when required.

## Queue Diagram

```text
Caller
  |
  v
+------------------+
| Queue            |
| Holds work       |
+------------------+
  |
  v
Frends worker
  |
  +-- Success
  |     -> Mark complete
  |
  +-- Temporary problem
  |     -> Delayed retry
  |
  +-- Permanent problem
  |     -> Dead-letter queue
  |     -> Manual or controlled review
  |
  +-- Worker stops
        -> Message may appear again
```

A queue may send the same message again.

The worker still needs duplicate protection.

## Circuit Breaker

A circuit breaker stops calls to a failing target for a short time.

It protects both systems during a wider outage.

It does not replace duplicate protection.

## Logs

Useful logs contain:

- Correlation ID.
- Safe business ID.
- Process and version.
- Environment.
- Step and target.
- Status and duration.
- Retry attempt.
- Safe error type.

Do not log:

- Token.
- Password.
- API key.
- Connection string.
- Full sensitive message.

## Metrics and Alerts

Useful metrics include:

- Request count.
- Success and failure count.
- Duration.
- Retry and timeout count.
- Queue backlog.
- Missing expected runs.

A useful alert tells support what to check.

Do not alert on every small temporary problem.

## Release Checklist

Before production:

- Contract and mapping are approved.
- Tests and UAT pass.
- Versions are correct.
- Settings, secrets, certificates, and network access are ready.
- API Policy and permissions work.
- Smoke test is ready.
- Rollback steps are ready.
- Logs, alerts, replay, and support owner are ready.

After release:

1. Check the deployed version.
2. Run the smoke test.
3. Find the Process Instance.
4. Check the real target result.
5. Watch failures and duration.
6. Compare the first source and target records.

Rolling back code does not undo an order or payment.

Business correction may need a separate compensation step.

## Incident Steps

Remember:

**Impact -> Stop damage -> Find -> Fix -> Check -> Learn**

1. Find the affected users, records, and time.
2. Stop unsafe retries or pause the Trigger.
3. Trace one request with IDs and logs.
4. Make the smallest safe fix.
5. Test and compare the final records.
6. Add a test, alert, or runbook improvement.

## Incident Diagram

```text
Alert or user report
        |
        v
1. Impact
Who and what is affected?
        |
        v
2. Stop damage
Pause unsafe work
        |
        v
3. Find
Trace one correlation ID
        |
        v
4. Fix
Make the smallest safe change
        |
        v
5. Check
Smoke test and compare records
        |
        v
6. Learn
Add a test, alert, or runbook step
```

## Common Production Problems

### Request Never Reaches the Process

Check:

1. URL, method, DNS, and network.
2. TLS certificate.
3. Gateway and API Policy.
4. Path, method, Agent Group, and API Trigger.
5. Agent health.
6. Process Instances and logs.

### `401` or `403`

- `401`: check token, key, certificate, issuer, audience, and time.
- `403`: check scope, role, policy, and record ownership.

### `404`

Check environment, base URL, route, API version, method, deployment, and Trigger.

### `500`

Use the correlation ID.

Find the first internal error.

Check null data, mapping, settings, and component version.

### `502`, `503`, or `504`

- `502`: check the target response and network path.
- `503`: check health, load, or maintenance.
- `504`: check target time. Treat a write result as unknown.

### Postman Works but the App Fails

Compare the real:

- Method and URL.
- Headers.
- Body and encoding.
- Token.
- Certificate.
- Proxy, DNS, and timeout.

### DEV Works but UAT Fails

Compare:

- URL and route.
- Environment values.
- Secret and certificate.
- DNS, firewall, and proxy.
- Policy and permission.
- Process and Task versions.
- Data and time settings.

### XPath Returns Nothing

Check:

- Namespace.
- Root and full path.
- Case.
- Missing or empty element.
- SOAP Envelope.
- Encoding and schema change.

## More Production Cases

| Problem | Simple first checks |
|---|---|
| Slow but succeeds | Find slow step, target time, payload size, load, and timeout |
| Intermittent `502` | Find gateway, target response, load, DNS, and proxy pattern |
| Expired certificate | Find owner, renew safely, check trust chain, add expiry alert |
| Retry storm | Stop retries, protect target, add limit and wait, drain slowly |
| Target returns `429` | Follow `Retry-After`, reduce rate, keep retry limit |
| Poison message | Put in DLQ, record reason, fix cause, replay slowly |
| Wrong message order | Group by business key, check sequence or version |
| Partial success | Save completed step, retry failed step, compensate if needed |
| PROD database differs | Compare schema, migration, connection, permission, and data |
| Rollback after writes | Roll back code separately from business correction |

## 60-Second Answer

> I first classify the failure as data, access, temporary, unknown, or internal. I retry only temporary failures, with a limit, wait, timeout, logs, and duplicate protection. A timeout gives an unknown result, so I search the target before retrying a write. I keep correlation and business IDs, useful metrics, alerts, a runbook, controlled replay, and reconciliation. During an incident, I stop damage, trace one request, fix the cause, verify records, and learn from it.

---

# 12. Testing an Integration - MUST KNOW

Test more than the happy path.

| Test | What it checks |
|---|---|
| Contract | Request and response match OpenAPI, WSDL, or XSD |
| Mapping | Fields become the correct target values |
| Integration | Real systems communicate |
| Negative | Invalid input is rejected |
| Security | Wrong identity or permission is rejected |
| Performance | Volume and speed are acceptable |
| Recovery | Timeout, retry, replay, and duplicate handling work |
| Regression | Old behavior still works |
| UAT | Business users accept the result |
| Smoke | Production path is alive |

Tools may include:

- OpenAPI linter.
- Postman, Bruno, or curl for REST.
- SoapUI or another SOAP client.
- XSD and XSLT tools.
- Frends Process testing and Process Instances.

The test purpose is more important than the tool name.

## Testing Ladder

```text
1. Contract
OpenAPI, JSON, WSDL, and XSD are correct
        |
        v
2. Mapping
JSON, XML, XPath, and XSLT give correct values
        |
        v
3. Process
Tasks, Decisions, Catch, and Return work
        |
        v
4. System connection
Frends reaches the real test target
        |
        v
5. Failure and security
Bad data, bad access, timeout, and duplicate work
        |
        v
6. Volume and timing
Expected size, count, and speed
        |
        v
7. UAT
Business accepts the result
        |
        v
8. Production proof
Smoke test and real target record match
```

## Order Test Examples

| Test | Input or condition | Expected result |
|---|---|---|
| Valid order | Correct token and body | Expected response and one ERP order |
| Missing order ID | No `orderId` | Safe `400` and no ERP call |
| Empty customer | Empty `customerId` | Field error and no ERP call |
| Invalid token | Changed or expired token | `401` and no business work |
| Wrong permission | Missing scope or role | `403` and no ERP call |
| Duplicate request | Same key twice | One ERP order |
| SOAP business Fault | ERP rejects order | Safe mapped error and no blind retry |
| Temporary outage | Selected `503` | Limited retry and clear log |
| Timeout after send | No response | Search ERP before retry |
| Bad namespace | Changed XML namespace | Mapping test fails before release |
| Production smoke | Approved test order | Process Instance and ERP result match |

## Old API Versus New API Diagram

```text
Same method, headers, and body
            |
      +-----+-----+
      |           |
      v           v
   Old API     New API
      |           |
      +-----+-----+
            |
            v
Compare:
status
headers
body
validation
side effects
duration
logs
```

Use the same request.

Otherwise, the comparison is not fair.

## Compare a New API with an Old API

Send the same request.

Compare:

- Status.
- Headers and content type.
- Body.
- Validation and error format.
- Side effects.
- Duplicate behavior.
- Time.
- Logs and final target state.

## 30-Second Answer

> I test the contract, mapping, real system connection, invalid data, security, volume, timeout, retry, duplicate protection, and recovery. I complete regression testing and UAT before release. After release, I run a smoke test and check the real target result. I do not judge success only from the API response.

---

# 13. .NET for an Integration Interview - MUST KNOW

## Three Similar Names

- `System.Text` has text tools such as UTF-8 Encoding.
- `System.Text.Json` reads and writes JSON.
- `Newtonsoft.Json` is a separate JSON package.

Newtonsoft.Json is also called Json.NET.

## .NET Mental Map

```text
.NET platform
|
+-- C#
|   Programming language
|
+-- .NET runtime
|   Runs managed code
|
+-- Built-in libraries
|   +-- System.Text
|   |   Text and encoding
|   |
|   +-- System.Text.Json
|   |   JSON tools
|   |
|   +-- HTTP, files, dates, and logging
|
+-- NuGet packages
    +-- Newtonsoft.Json
        Separate JSON package
```

`System.Text` is a broad text namespace.

`System.Text.Json` is the JSON library.

## System.Text.Json Versus Newtonsoft.Json

| System.Text.Json | Newtonsoft.Json |
|---|---|
| Built into modern .NET | Separate package |
| Good first choice for new work | Common in older systems |
| Fast and well supported | Very flexible |
| Has `JsonDocument` and `JsonNode` | Has `JObject` and `JToken` |

Check contract differences:

- Property names and case.
- Missing and null fields.
- Enums.
- Dates and time zones.
- Unknown fields.
- Reference loops.
- Special object types.
- Custom converters.

Do not change libraries without contract tests.

Reading JSON into a .NET object is not full validation.

## JSON Processing Diagram

```text
JSON text
   |
   v
Parse JSON
Can the text be read?
   |
   v
Create a .NET object
Can values map to properties?
   |
   v
Validate the contract
Are required fields and types correct?
   |
   v
Validate business rules
Is the order allowed?
   |
   v
Validate permission
May this caller do it?
   |
   v
Use the safe result
```

Example:

```json
{
  "order_id": "ORD-1001",
  "amount": null,
  "extra": "unexpected"
}
```

Ask:

- Does `order_id` map to the expected property?
- Is null allowed for amount?
- What happens when amount is missing?
- Are extra fields allowed?
- How are dates and enums handled?
- Does a custom converter exist?

## 45-Second JSON Library Answer

> For new .NET work, I normally start with System.Text.Json because it is built in and well supported. I use Newtonsoft.Json when an existing solution needs it or when a special legacy contract is easier with it. I test casing, nulls, enums, dates, unknown fields, and converters. Deserialization does not replace required-field, business-rule, or authorization checks.

## Async and HTTP

Async/await helps while waiting for:

- HTTP.
- File.
- Database.
- Message operations.

It avoids blocking a worker.

It does not make the target faster.

Still use:

- Timeout.
- Cancellation when supported.
- Safe HTTP client reuse.
- Error checks.
- Safe retry rules.

Use `DateTimeOffset` or a clear UTC rule for timestamps.

Use `decimal` for money.

Use UTF-8 and stable machine formats at system boundaries.

## Two Meanings of Middleware

### Integration Middleware

Connects systems and changes messages.

Frends is used in this meaning.

### ASP.NET Core Middleware

Runs inside an ordered HTTP pipeline.

It can handle:

- Errors.
- Correlation and logging.
- Authentication.
- Authorization.
- Rate limits.
- Routing.

Keep business rules outside general HTTP middleware.

## ASP.NET Core Middleware Diagram

```text
HTTP request
     |
     v
Error handler
     |
     v
Correlation and request logging
     |
     v
Authentication
Who is calling?
     |
     v
Authorization
Is it allowed?
     |
     v
Rate limit and other checks
     |
     v
API endpoint
     |
     v
HTTP response
```

Order matters.

Each middleware step passes work to the next step.

## ASP.NET Middleware and Frends Together

```text
Caller
  |
  v
ASP.NET Core middleware
Inside one web application
  |
  v
API endpoint
  |
  v
Frends integration middleware
Between separate systems
  |
  v
ERP, file, database, or SOAP service
```

## When to Use Custom .NET in Frends

Use built-in Frends Tasks first.

Use custom .NET only when:

- No supported Task solves the need clearly.
- The logic is technical and reusable.
- It is tested and versioned.
- The team can support it.

---

# 14. Power Platform - MUST KNOW

## Main Parts

| Part | Simple use |
|---|---|
| Power Apps | Business user application |
| Power Automate | Workflow and approval automation |
| Dataverse | Managed business data |
| Connector | Connection to a service |
| Custom connector | Makes a custom API usable in Power Platform |
| Gateway | Connects supported on-premises data |
| Solution | Package for controlled deployment |
| DLP policy | Controls which connector groups can work together |

## Power Platform and Frends Diagram

```text
User
  |
  v
Power App
Form or business screen
  |
  v
Dataverse
Business data
  |
  v
Power Automate
Approval and notification
  |
  v
Custom connector or HTTP call
  |
  v
Frends API Policy
Identity and access
  |
  v
Frends Process
Validate, change, route, and recover
  |
  v
ERP, SOAP, files, database, or queue
```

## Frends Versus Power Platform

### Frends

Best known for:

- System integration.
- APIs.
- Files and databases.
- Data transformation.
- Technical monitoring and recovery.

### Power Platform

Best known for:

- Business apps.
- Forms.
- Approvals.
- Human workflow.
- Microsoft-connected automation.

They can work together.

Example:

1. Power App collects an order.
2. Power Automate gets approval.
3. Frends sends the order to the ERP.

## Full Approved-Order Example

1. A user enters an order in Power Apps.
2. Dataverse stores the request.
3. Power Automate sends an approval.
4. A manager approves it.
5. Power Automate calls a secured Frends API.
6. Frends checks the caller and request.
7. Frends checks the duplicate key.
8. Frends changes JSON into ERP XML.
9. Frends calls the SOAP ERP.
10. Frends returns or publishes the result.
11. Power Automate updates Dataverse.
12. The user receives a message.

## Choose the Platform Diagram

```text
Need a form or business screen?
        |
        +-- Yes -> Power Apps

Need an approval or human task?
        |
        +-- Yes -> Power Automate

Need managed business records?
        |
        +-- Yes -> Dataverse

Need complex system transformation?
        |
        +-- Yes -> Frends

Need REST-to-SOAP or file integration?
        |
        +-- Yes -> Frends

Need special independent service logic?
        |
        +-- Yes -> .NET

Need user workflow and system integration?
        |
        +-- Use Power Platform and Frends together
```

## Power Platform Release and Security

- Build in the correct DEV environment.
- Put work in a Solution.
- Use an unmanaged Solution in DEV.
- Use a managed Solution downstream when appropriate.
- Use environment variables.
- Use connection references.
- Map real connections in the target environment.
- Do not move secrets inside a Solution.
- Use Dataverse security roles.
- Remember that DLP is not user permission.
- Use source control and release pipelines where available.
- Check connector limits and licensing.
- Give flows a durable owner.
- Monitor runs and gateway health.
- Plan gateway ownership and high availability.

## Security Path

```text
User identity
     |
     v
Power Platform role
     |
     v
Dataverse permission
     |
     v
Connection reference or service identity
     |
     v
Frends API Policy
     |
     v
Frends Process
     |
     v
Target-system identity
```

## Combined Deployment Diagram

```text
Power Platform
DEV Solution -> TEST -> PROD
environment values + connection references

                must agree on
        API contract, URL, identity,
        deployment order, and smoke test

Frends
DEV Process -> TEST/UAT -> PROD
environment values + API Policy + version
```

## Find the Failed Step

```text
Did Power Apps save the request?
              |
              v
Did Power Automate run?
              |
              v
Did the connector call Frends?
              |
              v
Did the API Policy allow it?
              |
              v
Did the Frends Process start?
              |
              v
Did the target system accept it?
```

Use one correlation ID.

Find the first step that behaved differently.

## 45-Second Comparison Answer

> Frends is mainly an integration and middleware platform. Power Platform is strong for business apps, approvals, and human workflows. I choose based on the users, protocol, transformation, volume, recovery needs, connectors, security, licensing, and support team. They can work together. Power Platform can handle the user process, while Frends handles the system-to-system integration.

## Recall

1. What does a timeout mean?
2. What makes a retry safe?
3. System.Text versus System.Text.Json?
4. System.Text.Json versus Newtonsoft.Json?
5. Frends versus Power Platform?

# 15. Top 20 Interview Questions - MUST KNOW

Answer these without reading.

The earlier sections contain the full answers.

## Question and Memory Cues

| # | Question | Cues |
|---:|---|---|
| 1 | Tell me about yourself. | Role -> systems -> your work -> why this job |
| 2 | What is SDLC? | Plan -> Design -> Build -> Test -> Release -> Support |
| 3 | How do you handle a new integration? | Need -> contract -> flow -> test -> release -> support |
| 4 | How do you handle a changed requirement? | Impact -> contract -> tests -> approval -> communication |
| 5 | What information do you collect first? | Owners -> data -> security -> scale -> failure |
| 6 | Describe a middleware project. | REST/JSON -> Frends -> SOAP/XML -> ERP |
| 7 | How do you design a Frends Process? | Trigger -> clear Tasks -> errors -> settings -> logs |
| 8 | Frends, Power Platform, or custom .NET? | Systems -> people -> special code |
| 9 | What is in an HTTP request and response? | Method/URL/headers/body -> status/headers/body |
| 10 | How do you test an integration? | Contract -> negative -> security -> recovery -> UAT |
| 11 | REST versus SOAP? | HTTP/JSON/OpenAPI -> XML/WSDL/XSD |
| 12 | XML, XSD, XPath, and XSLT? | Data -> rules -> find -> change |
| 13 | Explain SOAP and WSDL. | Envelope -> Header -> Body -> Fault -> service contract |
| 14 | What is in OpenAPI? | Info -> Servers -> Paths -> Models -> Security |
| 15 | How do headers work in OpenAPI? | Security scheme -> request parameter -> response header |
| 16 | How do you validate JSON? | Syntax -> Shape -> Business -> Outside data |
| 17 | How do you secure an API? | HTTPS -> identity -> permission -> input -> operations |
| 18 | How do you handle retry and timeout? | Temporary only -> limit -> unknown result -> check target |
| 19 | DEV works but UAT fails. What do you do? | Same request -> compare settings/network/access/versions |
| 20 | System.Text.Json versus Newtonsoft.Json? | Built-in modern -> mature flexible -> contract tests |

## Common Mistakes

- Giving a long answer before giving the meaning.
- Talking only about the happy path.
- Saying HTTPS is full API security.
- Saying OpenAPI security protects the running API by itself.
- Retrying every timeout.
- Treating missing, null, and empty as the same.
- Ignoring XML namespaces.
- Saying deserialization is full validation.
- Saying deployment is complete without checking the target.
- Claiming work you did not personally perform.

---

# 16. Four Practice Scenarios - MUST KNOW

## Scenario 1: New REST-to-SOAP Integration

Question:

> A portal sends JSON. An ERP accepts SOAP XML. What do you do?

Answer order:

1. Confirm goal, owners, scale, and security.
2. Review OpenAPI, WSDL, XSD, and examples.
3. Agree mapping and acceptance rules.
4. Secure and validate the REST request.
5. Add correlation and duplicate protection.
6. Map, transform, and validate target XML.
7. Send SOAP and check HTTP status and Fault.
8. Test errors, release, monitor, replay, and reconcile.

## Scenario 2: ERP Timeout

Question:

> The ERP call timed out. Should you retry?

Answer:

> The result is unknown. I do not retry immediately. I search the ERP using the order ID or idempotency key. If the order exists, I record success. I retry only when I know duplicate work cannot happen. I then reconcile affected records.

## Scenario 3: DEV Works but UAT Gives `401`

Check:

1. Which system returned `401`?
2. Is the UAT URL correct?
3. Is the token endpoint correct?
4. Is the secret or certificate correct?
5. Are issuer, audience, time, scope, and role correct?
6. Can the UAT Agent reach the target?
7. Is the correct Process version deployed?

## Scenario 4: XPath Returns No Value

Check:

1. Namespace URI.
2. Root and full path.
3. Uppercase and lowercase letters.
4. SOAP Envelope around the data.
5. Missing, empty, or nil element.
6. Encoding.
7. New schema or message version.

Fix the path.

Add a regression test.

Replay only the affected records.

---

# 17. Your Real Project Story - MUST KNOW

Fill this with real information:

- Business problem: ______________________________________
- Source system: _________________________________________
- Target system: _________________________________________
- Trigger: _______________________________________________
- Input format: __________________________________________
- Output format: _________________________________________
- Security: ______________________________________________
- My personal work: ______________________________________
- Hardest problem: _______________________________________
- Error and retry design: _________________________________
- Duplicate protection: __________________________________
- Testing: _______________________________________________
- Release and rollback: __________________________________
- Logs and monitoring: ___________________________________
- Records per day: _______________________________________
- Normal response time: __________________________________
- Real result: ___________________________________________

## STAR Answer

- **Situation:** What was happening?
- **Task:** What did you need to do?
- **Action:** What did you personally do?
- **Result:** What happened?
- **Lesson:** What did you improve or learn?

Prepare three stories:

1. A new feature.
2. A production problem.
3. A changed requirement.

## Tell Me About Yourself

Use four short parts:

1. Your current role and experience.
2. Systems and integrations you know.
3. Your main relevant strengths.
4. Why this role fits your next step.

Example shape:

> I work in [role] and have experience with [systems]. I have worked on REST, SOAP, JSON, XML, and low-code workflows. My main work has included [your real work]. I am interested in this role because it combines integration design, Frends, support, and reliable delivery.

## Why Low-Code and Integration?

> I like solving problems between systems. I enjoy agreeing contracts, mapping data, handling errors, and making flows easy to support. Low-code makes the flow visible and speeds up common work. API and .NET knowledge help with the technical details.

## Questions to Ask the Interviewer

1. Which integrations would I work on first?
2. How does the team review and test Frends changes?
3. How are releases and rollbacks handled?
4. Who supports production integrations?
5. Which security and logging rules are required?
6. What does success in the first 90 days look like?

---

# 18. Final 40-Minute Mock Interview

Record your voice.

Do not read while answering.

## 00:00-00:05

- Tell me about yourself.
- Why integration and low-code?

## 00:05-00:15

- Explain SDLC.
- Explain a new integration.
- Describe your middleware project.

## 00:15-00:25

- Secure an API.
- Explain OpenAPI.
- Validate JSON.
- Explain the XML family.

## 00:25-00:35

Practice two scenarios from Section 16.

## 00:35-00:40

Score each area:

| Area | 0 | 1 | 2 |
|---|---|---|---|
| Clear order | No order | Some order | Very clear |
| Simple meaning | Wrong | Partly clear | Clear |
| Example | None | General | Real or specific |
| Failure and security | Missing | Small mention | Clear safe action |
| Your role | Unclear | Mostly team | Your work is clear |

Review only the answers that scored `0` or `1`.

## Speaking Rules

- Start with the direct answer.
- Use short sentences.
- Give one example.
- Mention one failure or safety point.
- Stop after 60 to 90 seconds.
- Do not invent experience.

---

# 19. Tomorrow Morning - One-Page Recall

Read only this section tomorrow morning.

## Answer

**What -> Why -> Example -> Failure and fix**

## Lifecycle

**Plan -> Design -> Build -> Test -> Release -> Support**

Know the need, contract, mapping, security, failure rules, tests, release, logs, replay, and owner.

## Middleware

**Receive -> Check -> Change -> Send -> Track**

Story: Portal REST/JSON -> Frends -> SOAP/XML ERP.

## Security

**Connection -> Identity -> Permission -> Input -> Operations**

OpenAPI describes security.

The Frends API Policy and Process enforce it.

## OpenAPI

**Info -> Servers -> Paths -> Models -> Security**

Authentication uses `securitySchemes`.

A normal request header uses `parameters`.

## JSON

**Syntax -> Shape -> Business -> Outside data**

`properties` describes fields.

`required` makes selected fields mandatory.

## XML

**XML data -> XSD rules -> XPath find -> XSLT change**

WSDL describes the SOAP service.

SOAP has Envelope, Header, Body, and Fault.

## Failure

Bad data: stop and correct.

Temporary problem: limited safe retry.

Timeout: check the target before retry.

## Frends

Trigger starts Process.

Tasks do work.

Agent runs it.

Process Instance and logs show what happened.

## Final Reminder

Use real experience.

Say what you did.

Give one safe example.

---

# 20. Small Reference - REFERENCE

## Integration Patterns

| Pattern | Use it when | Main risk |
|---|---|---|
| Synchronous API | Caller needs a quick final result | Timeout and strong coupling |
| Asynchronous API | Work is slow | Status and duplicate handling |
| Webhook | A system pushes an event | Signature and replay attack |
| Queue | Systems need buffering | Duplicate delivery and backlog |
| File/SFTP | Legacy batch exchange | Partial file and duplicate file |
| Database polling | No API or event exists | Missed or repeated rows |
| Schedule | Work runs at a known time | Overlapping runs and timezone |

## Safe File Flow

- Wait until writing is complete.
- Validate name, size, and encoding.
- Use a stable file ID or checksum.
- Archive completed files.
- Quarantine bad files.
- Handle partial success.

## Safe Database Flow

- Use a low-permission account.
- Use safe parameters.
- Store a durable checkpoint.
- Add a small safe overlap.
- Remove duplicates.
- Understand transaction limits.

## Useful Operational Words

| Word | Simple meaning |
|---|---|
| Backoff | Wait longer before each retry |
| Jitter | Add a small random wait |
| Circuit breaker | Stop calls to a failing target for a short time |
| Dead-letter queue | Holds messages that could not finish |
| RTO | Target time to restore service |
| RPO | Maximum acceptable data loss time |
| SLA | Agreed service level |
| Smoke test | Small check after release |
| Runbook | Support instructions |

## Official References

- [Frends documentation](https://docs.frends.com/)
- [Frends API Policies](https://docs.frends.com/guides/api-management/setting-up-api-policies)
- [Frends API Trigger](https://docs.frends.com/reference/triggers/api-trigger)
- [OpenAPI specification](https://spec.openapis.org/oas/latest.html)
- [JSON Schema object rules](https://json-schema.org/understanding-json-schema/reference/object)
- [OWASP REST security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [W3C XML](https://www.w3.org/TR/xml/)
- [W3C XSD](https://www.w3.org/TR/xmlschema11-1/)
- [W3C XSLT](https://www.w3.org/TR/xslt/)
- [W3C SOAP](https://www.w3.org/TR/soap12/)
- [System.Text.Json](https://learn.microsoft.com/dotnet/standard/serialization/system-text-json/overview)
- [Power Platform ALM](https://learn.microsoft.com/power-platform/alm/)

# Final Study Rule

Do not read a new topic after the eight hours.

Review the one-page recall.

Prepare your real story.

Sleep.
