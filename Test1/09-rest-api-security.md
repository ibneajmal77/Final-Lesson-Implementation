# 09 — REST APIs, Integration & Authentication Protocols

> JD must-have: **"REST APIs with authentication protocol experience"**. Plus "Windows development"
> → expect **Kerberos/Windows auth** alongside OAuth. This is one of your strongest areas — the goal
> is speed and precision, not learning.

---

## 1. REST fundamentals

**Constraints:** client-server · **stateless** (no server-side session; every request carries context)
· cacheable · uniform interface · layered system · code-on-demand (optional).

**Richardson Maturity Model:** L0 single endpoint (RPC-over-HTTP) → L1 resources → L2 HTTP verbs +
status codes → L3 HATEOAS. Most real APIs are L2, and that's a defensible choice — say so.

**Verbs & semantics** (the table they check):

| Verb | Safe | Idempotent | Use |
|---|---|---|---|
| GET | ✅ | ✅ | Read. **Never** mutate in a GET. |
| HEAD | ✅ | ✅ | Metadata only |
| PUT | ❌ | ✅ | Full replace at a known URI |
| DELETE | ❌ | ✅ | Remove (repeat → 404 or 204, still idempotent) |
| POST | ❌ | ❌ | Create / process. Make it idempotent with an **Idempotency-Key** header. |
| PATCH | ❌ | ❌ (usually) | Partial update (JSON Patch / JSON Merge Patch) |

**Status codes** — know these cold: 200/201 (+`Location`)/202/204 · 301/304 · **400** malformed ·
**401** unauthenticated · **403** authenticated but not allowed · **404** · **409** conflict ·
**412** precondition failed · **422** semantic validation · **429** rate limited (+`Retry-After`) ·
500 · **502/503/504** upstream/unavailable/timeout.

⚠️ Two distinctions interviewers use as a filter: **401 vs 403**, and **PUT vs PATCH vs POST
idempotency**.

**Design details worth naming:**
- Resource-noun URIs, plural, hierarchical: `/portfolios/{id}/positions`. Verbs live in the method.
- **Pagination**: offset (simple, degrades deep) vs **cursor/keyset** (stable, constant cost —
  the right answer for large or live-updating datasets).
- Filtering, sorting, sparse fieldsets: `?status=open&sort=-createdAt&fields=id,symbol`.
- **Versioning**: URI (`/v1/`), header, or media type. Say: *"URI versioning for external partners
  because it's obvious and cache-friendly; plus additive-only changes and a documented deprecation/
  sunset policy so we rarely need v2."*
- **Errors**: **RFC 7807 / 9457 Problem Details** — `type`, `title`, `status`, `detail`, `instance`,
  plus a correlation ID. ASP.NET Core has this built in.
- **Caching**: `Cache-Control`, `ETag` + `If-None-Match` (304), `Last-Modified`/`If-Modified-Since`.
  **`If-Match` for optimistic concurrency on writes → 412** — a great senior detail.
- **Contract-first**: OpenAPI 3.1, linting (Spectral), generated clients, **Pact consumer-driven
  contract tests** (you already do this — say it).
- **Bulk endpoints, long-running operations** (202 + status URL), **webhooks** (HMAC signature,
  timestamp, replay protection, retries with backoff, DLQ).

**REST vs gRPC vs GraphQL vs messaging — the decision answer:**
> *"REST for external/partner and CRUD-ish contracts; gRPC for high-frequency internal service calls
> where latency and payload size matter — binary protobuf, HTTP/2 multiplexing, streaming; GraphQL
> when many different clients need different shapes of the same graph and you want to avoid
> over-fetching; and asynchronous messaging whenever the caller doesn't need the answer now or the
> two sides must be decoupled in time. I've used all four on the same platform for different jobs."*
(That's literally true of your GAC and 7X work — say it with those examples.)

---

## 2. Authentication & authorisation

**Authentication** = who you are. **Authorisation** = what you may do. Say it in that order.

### OAuth 2.0 — the roles and the flows
Roles: resource owner (user), client (app), authorisation server, resource server (API).

| Flow | Use | Notes |
|---|---|---|
| **Authorization Code + PKCE** | Web apps, SPAs, **desktop/WPF apps** | The default today. PKCE (code verifier/challenge) stops interception on public clients. |
| **Client Credentials** | Service-to-service, daemons | No user; app identity only |
| Device Code | TVs, CLI, input-constrained | |
| Refresh Token | Renew without re-login | Rotate + revoke; detect reuse |
| ~~Implicit~~ / ~~ROPC~~ | **Deprecated** | Say this — it dates you correctly |

⚠️ **For a WPF desktop app**, the right answer is *Authorization Code with PKCE via the system browser
or WAM/MSAL, tokens stored in the OS secure store (DPAPI/credential manager), never a client secret in
the binary* — a desktop app is a **public client**. This is a very likely question given the JD.

### OIDC
An **identity** layer on top of OAuth 2.0 (which is only about *authorisation/delegated access*).
Adds the **ID token** (a JWT about the user), `/userinfo`, standard scopes (`openid`, `profile`,
`email`), and discovery (`/.well-known/openid-configuration`).
> **One-liner:** *"OAuth 2.0 gives an app permission to call an API; OIDC tells the app who the user
> is. Access token → API. ID token → client."* ⚠️ **Never use the ID token to call an API.**

### JWT
`header.payload.signature`, base64url. Claims: `iss`, `aud`, `sub`, `exp`, `nbf`, `iat`, `jti`, plus
roles/scopes.
**Validation checklist (say all of it):** verify signature against the **JWKS** from the issuer's
discovery endpoint (with key rotation/`kid`), check `iss`, `aud`, `exp`/`nbf` with small clock skew,
and **pin the expected algorithm** — reject `alg: none` and don't let the token choose (the classic
JWT vulnerabilities). Keep access tokens short-lived.
**JWT vs opaque reference tokens:** JWT = self-contained, no lookup, but **cannot be revoked before
expiry**. Opaque + introspection = revocable, but a network call per request. Trade-off answer:
short expiry + refresh rotation, or introspection for high-value operations.

### Other protocols to have one line on
- **SAML 2.0** — XML, enterprise SSO, still everywhere in banks (IdP-initiated flows, assertions).
- **Kerberos / Integrated Windows Auth** — the on-prem enterprise default: tickets from a KDC,
  SPNs, delegation/constrained delegation, the "double-hop" problem. **Very likely relevant here.**
- **mTLS** — both sides present certificates; standard for service-to-service in regulated
  environments and for broker/exchange connectivity. Certificate rotation is the operational pain.
- **API keys + HMAC signing** — partner/webhook auth; sign body+timestamp, reject stale timestamps to
  prevent replay.
- **Microsoft Entra ID** (your CV): managed identities and **workload identity federation** so there
  are no secrets at all — a great modern answer.

### Authorisation models
- **RBAC** (roles) vs **ABAC** (attributes/policies — user, resource, context) vs ReBAC.
- In ASP.NET Core: policy-based authorisation, `IAuthorizationRequirement` + handlers, claims
  transformation, resource-based authorisation (`IAuthorizationService.AuthorizeAsync(user, resource,
  policy)`) — **the right answer for "can this trader see this portfolio?"**, because the decision
  depends on the *instance*, not just the role.
- **Entitlements** in finance: users see only their desk's/fund's positions; this is usually
  **row-level** and enforced server-side, never by hiding UI. Say that.

---

## 3. API security checklist (OWASP API Top 10 — the ones that matter)

1. **BOLA / IDOR** (broken object-level authorisation) — the #1 API vulnerability. *"Every request must
   re-check that this user may access this specific object ID — never trust an ID from the client."*
2. Broken authentication — weak tokens, no expiry, no rotation.
3. Excessive data exposure — return DTOs, never entities; don't rely on the client to hide fields.
4. Lack of rate limiting → ASP.NET Core rate-limiting middleware, gateway quotas.
5. Broken function-level authorisation — admin endpoints reachable by non-admins.
6. Mass assignment — bind to explicit DTOs, not domain entities.
7. Injection — parameterised queries; validate and encode.
8. SSRF — validate outbound URLs.
9. Security misconfiguration — CORS wide open, verbose errors, debug endpoints in prod.
10. Insufficient logging/monitoring — **and in finance, immutable audit logs of who accessed what**.

Plus: TLS everywhere (TLS 1.2+), HSTS, secure headers/CSP, secrets in Key Vault (never config files),
input validation at the boundary (FluentValidation), output encoding, and **PII/data-residency** rules.

---

## 4. Integration patterns (your CV's strong suit — compress into soundbites)

- **API-led vs event-driven**: synchronous when the caller needs the answer and the coupling is
  acceptable; events when you need decoupling in time, fan-out, or replay.
- **Message reliability**: at-least-once + idempotent consumers; outbox for atomic publish; DLQ +
  replay; poison-message handling; **event versioning** (additive changes, tolerant reader).
- **Ordering**: partition by aggregate key (account/instrument) to keep per-entity order.
- **Anti-corruption layer** for every external/legacy system — you did exactly this against GDS/IATA
  NDC at Calrom and SAP/EDI at GAC. **In this role that becomes the broker/custodian/market-data
  vendor boundary. Say that explicitly — it maps your experience straight onto their problem.**
- **File/batch integration** — SFTP, fixed-width, CSV, EDI, and end-of-day cycles. ⚠️ Still enormous
  in finance (SWIFT messages, custodian files, NAV files). Don't sneer at batch; show you can do it
  reliably (checksums, control totals, idempotent reprocessing, late-file handling).
- **Reconciliation jobs** — compare systems, report breaks. Universal in finance.

---

## 5. Rapid-fire

1. Stateless vs stateful API → scale-out, any node serves any request.
2. CORS → browser-enforced; preflight `OPTIONS`; irrelevant to a desktop client.
3. CSRF → applies to cookie-based auth; mitigate with SameSite + anti-forgery tokens. Bearer-token
   APIs aren't vulnerable in the same way.
4. Access vs refresh token → short-lived API credential vs long-lived renewal credential.
5. Where do you store tokens in a desktop app? → OS secure storage (DPAPI / Windows Credential
   Manager) via MSAL's token cache — not plain files, not the registry.
6. Rate limiting algorithms → fixed window, sliding window, **token bucket** (allows bursts), leaky
   bucket.
7. Timeouts and retries → always set a timeout; retry only idempotent operations; exponential backoff
   **with jitter**; cap attempts; circuit-break.
8. Correlation ID → propagate through every hop and log it; W3C `traceparent` + OpenTelemetry.
9. Content negotiation → `Accept`/`Content-Type`.
10. gRPC streaming modes → unary, server-stream, client-stream, bidirectional — server-streaming is a
    natural fit for price updates to a service (though for browsers you'd need gRPC-Web).
11. Health checks → liveness vs readiness; don't fail liveness for a downstream dependency.
12. API gateway responsibilities → routing, authn, rate limits, quotas, transformation, observability
    (Azure APIM, YARP).
