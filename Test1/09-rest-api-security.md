# 09 — REST APIs & SECURITY, IN PLAIN ENGLISH

> Must-have: **"REST APIs with authentication protocol experience"**. And because "Windows
> development" is listed, expect **Kerberos/Windows auth** alongside OAuth.
>
> **This is one of your strongest areas.** The goal here is **speed and precision**, not learning.
> Answer in 30 seconds and stop.

---

# EASY MEMORY NOTES

Read this first. Start with the short phrase. Say the simple line. Add the last column only if they
ask for more.

| Remember | Say it simply | If they ask more |
|---|---|---|
| **401 who, 403 allowed** | 401 means not logged in. 403 means logged in but not allowed. | Authentication first, authorisation second. |
| **Safe retries** | A retry must not create the same thing twice. | Use idempotency keys for POST actions. |
| **PKCE for desktop** | Desktop apps cannot safely store secrets. | Use Authorization Code with PKCE. |
| **OAuth vs OIDC** | OAuth lets an app call an API. OIDC tells who the user is. | Access token goes to the API; ID token stays with the client. |
| **Check JWT properly** | Do not trust a token just because it looks valid. | Check signature, issuer, audience, expiry, and algorithm. |
| **JWT cannot be pulled back easily** | A JWT normally works until it expires. | Use short expiry and refresh-token rotation. |
| **Check object access** | Always check if this user can access this object. | This prevents IDOR/BOLA bugs. |
| **ETag protects edits** | Only update if the version has not changed. | Use `If-Match`; return 412 on conflict. |
| **Cursor pages** | Use cursor paging for large lists. | Offset gets slower and less stable at deep pages. |
| **Same error shape** | API errors should look consistent. | Use Problem Details with a correlation ID. |

---

# PART 0 — THE 10 API ANSWERS THAT WIN

| # | The question | Simple answer |
|---|---|---|
| 1 | **401 vs 403** | "401 means not logged in. 403 means logged in but not allowed." |
| 2 | **Which verbs are idempotent?** | "GET, PUT, and DELETE are safe to retry. For POST, add an idempotency key." |
| 3 | **OAuth for a desktop app** | "Use Authorization Code with PKCE because a desktop app cannot keep a secret." |
| 4 | **OAuth vs OIDC** | "OAuth gives API access. OIDC tells the app who the user is." |
| 5 | **Validating a JWT** | "Check signature, issuer, audience, expiry, and algorithm." |
| 6 | **Can you revoke a JWT?** | "Not easily before it expires. Use short expiry and refresh-token rotation." |
| 7 | **The #1 API vulnerability** | "Always check if this user can access this object." |
| 8 | **Optimistic concurrency over HTTP** | "Use `ETag` and `If-Match`; return 412 if the version changed." |
| 9 | **Pagination at scale** | "Use cursor or keyset paging for big lists." |
| 10 | **Error format** | "Use Problem Details and include a correlation ID." |

---

# PART 1 — REST FUNDAMENTALS

## 1.1 What REST actually requires

**Say:** *"Client-server, **stateless** — no server-side session, every request carries its own
context — cacheable, a uniform interface, and layered. Stateless is the one that matters
practically, because it's what lets any node serve any request."*

**Richardson Maturity Model:** Level 0 is RPC over HTTP → Level 1 is resources → Level 2 is proper
verbs and status codes → Level 3 is HATEOAS.
**Say:** *"Most real APIs are Level 2, and that's a defensible choice — HATEOAS rarely pays for
itself."*

## 1.2 The verb table they check

| Verb | Safe | Idempotent | Use |
|---|---|---|---|
| `GET` | ✅ | ✅ | Read. **Never mutate in a GET** |
| `PUT` | ❌ | ✅ | Full replace at a known URI |
| `DELETE` | ❌ | ✅ | Remove. Repeating gives 404 or 204 — still idempotent |
| `POST` | ❌ | ❌ | Create or process. Make it idempotent with an **`Idempotency-Key`** header |
| `PATCH` | ❌ | usually ❌ | Partial update |

**Say what idempotent means, simply:** *"Doing it twice has the same effect as doing it once. That
matters because networks retry, and the client often can't tell whether the first attempt landed."*

## 1.3 Status codes — know these cold

| Code | Means |
|---|---|
| **200 / 201 / 202 / 204** | OK / Created (with `Location`) / Accepted (async) / No content |
| **304** | Not modified — the cache is still valid |
| **400** | Malformed request |
| **401** | **Not authenticated** — I don't know who you are |
| **403** | **Not authorised** — I know you, you can't do this |
| **404** | Not found |
| **409** | Conflict |
| **412** | Precondition failed — used with `If-Match` |
| **422** | Well-formed but semantically invalid |
| **429** | Rate limited — send `Retry-After` |
| **502 / 503 / 504** | Bad upstream / unavailable / upstream timeout |

## 1.4 Design details worth naming

- **Resource nouns, plural, hierarchical:** `/portfolios/{id}/positions`. The verb lives in the method.
- **Pagination:** *"Offset is simple but degrades at depth and is unstable while rows are being
  inserted. **Cursor or keyset** paging is stable and constant cost — the right answer for large or
  live-updating datasets."*
- **Versioning:** *"URI versioning for external partners, because it's obvious and cache-friendly.
  Plus additive-only changes and a documented deprecation and sunset policy, so we rarely need a v2
  at all."*
- **Errors:** **RFC 7807 / 9457 Problem Details**, with a correlation ID.
- **Caching:** `Cache-Control`, `ETag` + `If-None-Match` → 304.
  ⚠️ **The senior detail:** *"`If-Match` is a version check over HTTP. If someone changed the row
  first, return 412. It is the same idea as checking a row version in the database."*
- **Contract-first:** OpenAPI 3.1, linting, generated clients, and **Pact consumer-driven contract
  tests** — *you already do this, so say it.*
- **Long-running operations:** 202 plus a status URL.
- **Webhooks:** HMAC signature over body plus timestamp, replay protection, retries with backoff, DLQ.

## 1.5 REST vs gRPC vs GraphQL vs messaging — the decision answer

**Say:**
> *"REST for external and partner contracts and anything CRUD-ish. **gRPC** for high-frequency internal
> calls where latency and payload size matter — binary protobuf, HTTP/2 multiplexing, and streaming.
> **GraphQL** when many different clients need different shapes of the same graph and you want to stop
> over-fetching. And **asynchronous messaging** whenever the caller doesn't need the answer now, or
> the two sides need to be decoupled in time.*
>
> *I've used all four on the same platform, for different jobs."*

That last line is literally true of your work — say it with the examples.

---

# PART 2 — AUTHENTICATION AND AUTHORISATION

**Say them in this order:** *"**Authentication** is who you are. **Authorisation** is what you're
allowed to do."*

## 2.1 OAuth 2.0 — the flows

**The four roles:** the **resource owner** (the user), the **client** (the app), the **authorisation
server**, and the **resource server** (the API).

| Flow | Use it for | Note |
|---|---|---|
| **Authorization Code + PKCE** | Web apps, SPAs, **and desktop apps** | **The default today.** PKCE stops interception on public clients |
| **Client Credentials** | Service to service, daemons | No user — app identity only |
| Device Code | TVs, CLIs, anything hard to type on | |
| Refresh Token | Renew without re-login | Rotate and revoke; detect reuse |
| ~~Implicit~~ / ~~Password~~ | **Deprecated** | **Saying this dates you correctly** |

⚠️ **The very likely question, given the job description:**

**Q: How would you authenticate a WPF desktop app?**
**Say:** *"**Authorization Code with PKCE**, through the system browser or WAM via MSAL. A desktop app
is a **public client** — there is no safe place to put a secret in a binary that ships to users. PKCE
is what protects the code exchange. Tokens go in the OS secure store — DPAPI or the Windows Credential
Manager, which MSAL's token cache handles — never a plain file, never the registry."*

## 2.2 OIDC

**Say:** *"OIDC is an **identity** layer on top of OAuth 2.0, because OAuth on its own is only about
delegated access. It adds the **ID token**, which is a JWT about the user, plus a `/userinfo`
endpoint, standard scopes, and discovery."*

**The one-liner:** *"OAuth gives an app permission to call an API. OIDC tells the app who the user is.
**Access token goes to the API. ID token stays with the client.**"*
⚠️ **Never use the ID token to call an API.**

## 2.3 JWT

Structure: `header.payload.signature`, base64url encoded.
Claims: `iss` (issuer), `aud` (audience), `sub` (subject), `exp`, `nbf`, `iat`, `jti`, plus roles and
scopes.

**Say the whole validation checklist — it's a filter question:**
> *"Verify the signature against the **JWKS** from the issuer's discovery endpoint, handling key
> rotation via `kid`. Check `iss` and `aud`. Check `exp` and `nbf` with a small clock skew allowance.
> And **pin the expected algorithm** — reject `alg: none` and never let the token tell you how to
> verify it. Those last two are the classic JWT vulnerabilities."*

**Q: JWT or opaque tokens?**
**Say:** *"A JWT is self-contained, so there's no lookup per request — but **you can't revoke it before
it expires**. An opaque token plus introspection is revocable, but costs a network call every request.
The usual answer is short-lived access tokens with refresh rotation, and introspection only for
high-value operations."*

## 2.4 The other protocols — one line each

- **Kerberos / Integrated Windows Auth** — *"The on-prem enterprise default. Tickets from a KDC, SPNs,
  constrained delegation, and the double-hop problem."* ⚠️ **Very likely relevant in a bank.**
- **mTLS** — *"Both sides present certificates. Standard for service-to-service in regulated
  environments and for broker or exchange connectivity. Certificate rotation is the operational
  pain."*
- **SAML 2.0** — *"XML-based enterprise SSO. Still everywhere in banks."*
- **API keys plus HMAC signing** — *"For partner and webhook auth. Sign the body plus a timestamp, and
  reject stale timestamps to prevent replay."*
- **Entra ID with workload identity federation** — *"So there are no secrets at all."* A great modern
  answer.

## 2.5 Authorisation models

**RBAC** (roles) vs **ABAC** (attributes and policies — user, resource, context).

⚠️ **The answer that matters for this domain:**
**Q: "Can this trader see this portfolio?"**
**Say:** *"That's **resource-based** authorisation, not role-based — the decision depends on the
specific instance, not just the role. In ASP.NET Core that's
`IAuthorizationService.AuthorizeAsync(user, resource, policy)` with a requirement and a handler.*

*And in finance, entitlements are usually **row-level**: a user sees only their desk's or their fund's
positions. **That has to be enforced server-side — never by hiding it in the UI.**"*

**That last sentence is the one they're listening for.**

---

# PART 3 — API SECURITY (the OWASP items that matter)

1. ⚠️ **BOLA / IDOR — broken object-level authorisation. The number one API vulnerability.**
   **Say:** *"Every request must re-check that this user may access this specific object ID. Never
   trust an ID that came from the client."*
2. **Broken authentication** — weak tokens, no expiry, no rotation.
3. **Excessive data exposure** — *"Return DTOs, never entities. Don't rely on the client to hide
   fields — the data is still on the wire."*
4. **No rate limiting** — ASP.NET Core rate-limiting middleware, or gateway quotas.
5. **Broken function-level authorisation** — admin endpoints reachable by non-admins.
6. **Mass assignment** — bind to explicit DTOs, not domain entities.
7. **Injection** — parameterised queries always.
8. **Security misconfiguration** — CORS wide open, verbose errors, debug endpoints in production.
9. **Insufficient logging** — ⚠️ *"and in finance, **immutable audit logs of who accessed what**."*

**Plus:** TLS 1.2 or higher everywhere, HSTS, secrets in Key Vault and never in config files,
validation at the boundary, and data-residency rules.

---

# PART 4 — INTEGRATION PATTERNS (your strong suit — compress into soundbites)

- **Synchronous or events?** *"Synchronous when the caller needs the answer now and the coupling is
  acceptable. Events when you need decoupling in time, fan-out, or replay."*
- **Message reliability** — *"At-least-once delivery plus idempotent consumers. Outbox for atomic
  publish. Dead-letter queue with replay. And tolerant-reader event versioning — additive changes
  only."*
- **Ordering** — *"Partition by aggregate key — account or instrument — to keep per-entity order."*
- ⚠️ **Anti-corruption layer** — *"I did exactly this against GDS at Calrom and SAP/EDI at GAC. **In
  this role that becomes the broker, custodian and market-data vendor boundary.**"*
  **Say that mapping explicitly — it puts your experience straight onto their problem.**
- ⚠️ **File and batch integration** — *"SFTP, fixed-width files, CSV, EDI, end-of-day cycles. This is
  still enormous in finance — SWIFT messages, custodian files, NAV files. I wouldn't sneer at batch;
  I'd do it reliably: checksums, control totals, idempotent reprocessing, and explicit late-file
  handling."*
  **Saying this shows you know what a bank actually runs on.**
- **Reconciliation jobs** — compare systems, report breaks. Universal in finance.

---

# PART 5 — RAPID-FIRE: 35 QUESTIONS

| # | Q | A |
|---|---|---|
| 1 | REST's key constraint | **Stateless** — any node can serve any request |
| 2 | Richardson level of most APIs | Level 2 — proper verbs and status codes |
| 3 | Which verbs are idempotent? | GET, PUT, DELETE. **Not POST** |
| 4 | Make POST idempotent | An `Idempotency-Key` header plus a dedupe store |
| 5 | PUT vs PATCH | Full replace vs partial update |
| 6 | 401 vs 403 | Don't know you vs know you and you can't |
| 7 | 409 vs 412 | General conflict vs a failed `If-Match` precondition |
| 8 | 429 | Rate limited — include `Retry-After` |
| 9 | 202 | Accepted — long-running, here's a status URL |
| 10 | ETag | A version tag for a resource; `If-None-Match` → 304 |
| 11 | Optimistic concurrency over HTTP | `If-Match` on write, 412 on conflict |
| 12 | Problem Details | **RFC 7807** — the standard error body |
| 13 | Pagination at scale | Cursor / keyset, not offset |
| 14 | Versioning strategy | URI for partners, plus additive-only changes |
| 15 | REST vs gRPC | External and CRUD vs internal, low latency, streaming |
| 16 | When GraphQL? | Many clients, many shapes of one graph, over-fetching problem |
| 17 | OAuth roles | Resource owner, client, authorisation server, resource server |
| 18 | Flow for a desktop app | **Authorization Code + PKCE**, public client |
| 19 | Why PKCE? | Stops interception of the code on a public client |
| 20 | Flow for service to service | Client Credentials |
| 21 | Deprecated flows | Implicit and Resource Owner Password |
| 22 | OAuth vs OIDC | Delegated access vs identity |
| 23 | ID token vs access token | To the client vs to the API. Never mix them |
| 24 | JWT parts | Header, payload, signature |
| 25 | JWT validation | JWKS signature, `iss`, `aud`, `exp`, and **pin the algorithm** |
| 26 | Can you revoke a JWT? | Not before expiry. Keep them short-lived |
| 27 | Where do desktop tokens go? | OS secure store — DPAPI / Credential Manager, via MSAL |
| 28 | Access vs refresh token | Short-lived API credential vs long-lived renewal credential |
| 29 | Kerberos | On-prem Windows auth: KDC tickets, SPNs, the double-hop problem |
| 30 | mTLS | Both sides present certificates. Rotation is the pain |
| 31 | RBAC vs ABAC | Roles vs attributes and context |
| 32 | "Can this trader see this portfolio?" | **Resource-based** authorisation, enforced server-side |
| 33 | #1 API vulnerability | **BOLA / IDOR** — re-check object-level access every request |
| 34 | Rate limiting algorithms | Fixed window, sliding window, **token bucket** (allows bursts), leaky bucket |
| 35 | Retries | Only for idempotent operations. Exponential backoff **with jitter**, capped, plus a circuit breaker |
