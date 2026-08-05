# Angular vs React vs Vue: Production-Ready Master Matrix

This document compares Angular, React, and Vue from a production-readiness perspective. It is written as a practical completion checklist: what every production frontend app needs, how each framework usually handles it, what tools are commonly used, how to verify it, and what "done" means.

## Quick Summary

| Dimension | Angular | React | Vue | Practical conclusion |
|---|---|---|---|---|
| Framework type | Full application framework | UI library plus ecosystem/framework | Progressive framework | Angular gives the most structure; React gives the most flexibility; Vue balances structure and speed |
| Best fit | Enterprise apps, large teams, regulated environments, complex internal platforms | Product apps, full-stack apps, highly customized architecture, large ecosystem needs | Fast-moving apps, admin tools, SaaS products, teams wanting simpler DX |
| Built-in opinions | High | Low by itself; medium/high with Next.js or similar | Medium; high with Nuxt |
| Production burden | Lower architecture burden, more framework conventions | Higher decision burden unless using a full-stack React framework | Moderate burden, strong official ecosystem |
| Learning curve | Highest | Medium | Low to medium |
| Scaling model | CLI, DI, services, standalone components, strict patterns | Team-defined architecture, hooks, server-state tools, framework conventions | Composition API, composables, SFCs, Pinia, Nuxt when needed |
| Default app setup | Angular CLI | Recommended React framework or Vite | create-vue/Vite or Nuxt |
| Strongest advantage | Consistency at scale | Ecosystem depth and flexibility | Productivity and simplicity |
| Main risk | Complexity and verbosity | Fragmented choices and inconsistent architecture | Some ecosystem choices are smaller than React/Angular |

## Production-Ready Master Checklist

| Area | Production requirement | Angular | React | Vue | Must-have level | Verification method | Done criteria |
|---|---|---|---|---|---|---|---|
| Product scope | Clear user roles, user journeys, business rules, acceptance criteria | Document in feature modules/routes | Document in app routes/features | Document in routes/views/composables | Required | Product review, QA scenarios | Every critical flow has acceptance criteria |
| Architecture | Define feature boundaries, shared UI, API layer, auth layer, config layer | Feature folders, services, guards, interceptors | Framework routes/features, hooks, services, server-state layer | Views, composables, Pinia stores, services | Required | Architecture review | No unclear cross-feature dependencies |
| Microfrontend decision | Use microfrontends only when independent ownership/deployment is worth the added complexity | Angular shell/remotes, Module Federation, single-spa, web components | React shell/remotes, Module Federation, single-spa, web components | Vue/Nuxt shell/remotes, Vite federation, single-spa, web components | Conditional | Architecture decision record | MFE is justified by team, release, ownership, or migration needs |
| Microfrontend boundaries | Split by business domain, not by technical layer or component type | Domain remote apps and shared Angular libraries | Domain remote apps and shared packages | Domain remote apps, composables, shared packages | Required when MFE exists | Domain ownership review | Each remote has a clear owner, scope, SLA, and release path |
| Microfrontend contracts | Define runtime contracts, public APIs, events, routes, dependencies, browser support | Typed exposed modules, Angular library contracts | Typed exposed modules, package contracts, event contracts | Typed exposed modules, package/composable contracts | Required when MFE exists | Contract tests, integration tests | Host and remotes can evolve without accidental breaking changes |
| Microfrontend routing | Decide whether shell owns all routes or each remote owns a route subtree | Angular shell with lazy remote route config | React shell/router with remote route modules | Vue Router/Nuxt shell with remote route modules | Required when MFE exists | E2E route refresh tests | Direct links, refresh, redirects, 404, auth, and rollback work |
| Microfrontend communication | Prefer URL, backend APIs, typed events, or small shared stores; avoid hidden global coupling | RxJS/event bus only with strict contracts | Custom events, query cache boundaries, typed event bus | Custom events, Pinia only if intentionally shared | Required when MFE exists | Integration tests | Remotes communicate through documented, versioned mechanisms |
| Microfrontend shared dependencies | Decide which libraries are singletons, pinned, shared, isolated, or bundled per remote | Angular/framework packages usually singleton | React/react-dom usually singleton | Vue usually singleton inside same page runtime | Required when MFE exists | Bundle and runtime dependency audit | No duplicate incompatible framework/runtime copies unless intentionally isolated |
| Microfrontend deployment | Independent deploys, versioned remote entries, rollback, compatibility windows, manifest strategy | RemoteEntry or manifest per Angular remote | RemoteEntry/manifest per React remote | RemoteEntry/manifest per Vue remote | Required when MFE exists | Preview deploy and rollback test | Host can load compatible remote versions and survive failed remote deploys |
| Microfrontend failure isolation | Remote load failures, render errors, timeout, unavailable remote, bad version, partial outage | Error boundaries/shell fallbacks around remotes | Error Boundaries and loader fallbacks | Error handlers and shell fallbacks | Required when MFE exists | Failure injection | One broken remote does not break the whole shell |
| Microfrontend observability | Tag events/errors by shell version, remote name, remote version, route, user/session where allowed | Provider/interceptor metadata | Error boundary metadata | app error handler/router metadata | Required when MFE exists | Observability dashboard | Production issues identify the owning remote and release |
| Microfrontend security | Trust boundary, CSP, remote script policy, SRI/allowlists where feasible, dependency scanning per remote | Angular sanitization plus remote governance | React sanitization plus remote governance | Vue sanitization plus remote governance | Required when MFE exists | Security review | Remote code loading is controlled, reviewed, and monitored |
| Rendering model | Choose CSR, SSR, SSG, prerender, hybrid, or PWA | Angular SSR/prerender/hydration | Next.js/React Router/Remix-style framework or CSR Vite | Nuxt SSR/SSG or Vue SPA | Required | Lighthouse, SEO tests, deployment test | Rendering model matches SEO, performance, and hosting needs |
| Routing | Protected routes, nested layouts, 404, redirects, lazy routes, route metadata | Angular Router | React Router, Next.js App Router, TanStack Router | Vue Router or Nuxt routing | Required | E2E route tests | All routes work on refresh, direct link, and auth transitions |
| Layout system | Responsive shell, navigation, breadcrumbs, mobile nav, page templates | Components and CDK/Layout if needed | Component layout system, CSS framework/design system | SFC layouts, Nuxt layouts if used | Required | Visual QA, mobile screenshots | Layout works across target breakpoints |
| State model | Separate local UI state, URL state, server state, global client state, persisted state | Signals, services, NgRx when needed | Hooks, Context, Zustand, Redux Toolkit, TanStack Query/SWR | Pinia, composables, Vue reactivity, Vue Query | Required | State flow review, tests | State ownership is explicit and predictable |
| Server data | API fetching, caching, invalidation, retries, cancellation, loading and error states | HttpClient, RxJS, interceptors | TanStack Query, SWR, framework loaders/actions | Composables, Pinia, Vue Query, Nuxt useFetch | Required | Integration tests, network failure tests | API behavior is consistent and recoverable |
| API contracts | Typed request/response models, validation, versioning, error envelope | TypeScript interfaces, generated clients, Zod/io-ts if needed | OpenAPI clients, Zod, tRPC, GraphQL codegen | OpenAPI clients, Zod, GraphQL codegen | Required | Contract tests, schema checks | Frontend and backend contracts cannot drift silently |
| Authentication | Session/token strategy, refresh, logout, route protection, auth errors | Guards and Http interceptors | Middleware/loaders/hooks, route wrappers | Router guards/Nuxt middleware | Required | Auth E2E tests | Login, logout, expiry, refresh, denied access all work |
| Authorization | Role/permission checks, feature gates, UI hiding plus server enforcement | Guards/directives/services | Components/hooks/server checks | Directives/composables/router guards | Required | Permission matrix tests | UI and API permissions agree |
| Forms | Validation, touched states, async validation, error summary, accessibility | Reactive Forms | React Hook Form, Formik, Zod/Yup | VeeValidate, VueUse, custom composables | Required when forms exist | Component tests, accessibility tests | Forms are keyboard accessible and handle invalid/server errors |
| UX states | Loading, empty, error, partial failure, offline, retry, success states | Components and interceptors | Components, boundaries, server-state status | Components, composables, Suspense where appropriate | Required | Storybook/preview states, E2E | No blank or confusing states in critical flows |
| Design system | Tokens, typography, spacing, color, components, usage rules | Angular Material/CDK or custom | MUI, Radix, Chakra, shadcn, custom | Vuetify, Naive UI, Quasar, custom | Required for medium/large apps | Visual review, visual regression | Shared components cover repeated UI patterns |
| Accessibility | Semantic HTML, keyboard support, focus management, contrast, screen reader support | Angular CDK accessibility utilities help | Depends on team/component library | Depends on team/component library | Required | Axe, manual keyboard test, screen reader smoke test | WCAG target is met for critical flows |
| Internationalization | Translation, pluralization, dates, currency, RTL, locale routing | Angular i18n or Transloco | i18next, FormatJS, Lingui, next-intl | Vue I18n, Nuxt i18n | Required for multi-locale apps | Locale QA | UI works in longest target language and RTL if required |
| SEO | Metadata, canonical URLs, sitemap, robots, structured data, SSR/SSG for crawlers | Angular SSR/prerender | Next.js or equivalent React framework | Nuxt recommended | Required for public content | Search crawler tests, metadata tests | Important pages render indexable content |
| Performance budgets | JS/CSS/image budgets, LCP, INP, CLS, TTFB targets | Angular CLI budgets | Bundle analyzer, Lighthouse CI, framework analyzer | Vite/Rollup analyzer, Nuxt analyzer | Required | CI budget checks, Lighthouse CI | Builds fail or warn when budgets regress |
| Initial load performance | Reduce critical JS/CSS, lazy routes, optimize fonts/images, preload critical assets | Lazy routes, @defer, NgOptimizedImage, SSR | Dynamic imports, Suspense, framework image/font tools | Async components, route splitting, Nuxt image/font tools | Required | WebPageTest, Lighthouse, RUM | Core Web Vitals pass target percentile |
| Runtime performance | Avoid unnecessary renders/change detection, virtualize large lists, profile hot paths | Signals, OnPush, zoneless, Angular DevTools | Profiler, React Compiler, memo only where useful | v-memo, v-once, computed stability, virtual lists | Required | Browser profiling, framework devtools | Slow interactions are measured and fixed |
| Bundle hygiene | Tree shaking, ESM dependencies, avoid heavy libraries, analyze duplicates | Prefer ESM; avoid CommonJS warnings | Prefer ESM; check duplicate packages | Prefer ESM; Vite tree shaking | Required | Bundle analyzer | No avoidable heavy dependency in initial bundle |
| Images/media | Responsive sizes, modern formats, lazy loading, CDN, alt text | NgOptimizedImage | Next/Image or custom pipeline | Nuxt Image or Vite image tooling | Required when media exists | Lighthouse, visual QA | Images are optimized and accessible |
| Security basics | XSS, CSRF, CORS, secure cookies, no frontend secrets, dependency audit | Angular sanitization, avoid direct DOM APIs | Avoid unsafe HTML, sanitize explicitly | Never use untrusted templates, sanitize v-html | Required | Security review, SAST, dependency scan | No known high/critical vulnerabilities or obvious client-side leaks |
| CSP and browser security | Content-Security-Policy, Trusted Types where useful, SRI, frame policies | Strong Trusted Types story | Needs deliberate setup | Needs deliberate setup | Required for high-risk apps | Header tests, browser console checks | Security headers deployed and monitored |
| Dependency security | Lockfile, audit, license review, upgrade policy, supply-chain risk | npm/pnpm/yarn audit, Dependabot/Renovate | Same | Same | Required | CI audit, SBOM if needed | Vulnerabilities are tracked and remediated by policy |
| Secrets/config | Runtime config, environment separation, no secrets in JS bundle | Environment/config service | .env/framework runtime config | .env/Vite/Nuxt runtime config | Required | Build artifact inspection | No secret appears in frontend bundle |
| Error handling | Global error handler, boundary-level recovery, API error normalization | ErrorHandler and interceptors | Error Boundaries and reporting hooks | app.config.errorHandler and router/API hooks | Required | Failure injection | Errors are reported and user sees recoverable UI |
| Observability | Error tracking, RUM, analytics, tracing, release tags, alerts | Sentry/Bugsnag/etc. via providers/interceptors | Sentry/Bugsnag/etc. via app/framework | Sentry/Bugsnag/etc. via app handler | Required | Test error event, dashboard review | Production issues can be tied to release/user/session |
| Analytics | Product events, consent, privacy rules, event naming, funnel tracking | Service wrapper | Hook/service wrapper | Plugin/composable wrapper | Optional/required by product | Analytics QA | Events are documented and privacy-compliant |
| Testing strategy | Unit, component, integration, E2E, contract, accessibility, visual regression | Angular testing tools, Testing Library, Playwright/Cypress | Vitest/Jest, React Testing Library, Playwright/Cypress | Vitest, Vue Test Utils, Playwright/Cypress | Required | CI test pipeline | Critical paths fail CI on regression |
| Unit tests | Business logic, pure functions, composables/hooks/services | Services, pipes, utilities | Hooks/utilities/reducers | Composables/utilities/stores | Required | Test coverage review | Complex logic is covered |
| Component tests | Rendering, user interaction, accessibility states | Angular Testing Library | React Testing Library | Vue Test Utils | Required | Component test CI | Shared components and critical screens are covered |
| E2E tests | Real browser tests for critical flows | Playwright/Cypress | Playwright/Cypress | Playwright/Cypress | Required | CI and preview env tests | Critical user journeys pass on production build |
| Visual regression | Detect accidental UI changes | Storybook/Chromatic/Percy/etc. | Same | Same | Optional but valuable | Visual snapshots | Design system changes are reviewed intentionally |
| CI/CD | Install, lint, typecheck, test, build, scan, deploy preview, promote release | Angular CLI commands | Framework/Vite commands | Vite/Nuxt commands | Required | CI pipeline | Main branch is always releasable |
| Deployment | Static/CDN, Node SSR, edge runtime, container, rollback | Static or Angular SSR | Static, Node, edge depending stack | Static, Node/Nitro/Nuxt | Required | Smoke tests after deploy | Deployment is repeatable and reversible |
| Hosting and CDN | Cache headers, compression, TLS, HTTP/2/3, SPA fallback, SSR routing | Works well with CDN/static or Node SSR | Depends on chosen framework | Works with CDN/static or Nuxt server | Required | Header checks, direct route refresh | Assets cache long; HTML/cache policy is safe |
| Cache strategy | Asset hashing, API caching, service worker versioning, invalidation | Angular service worker if PWA | Workbox/framework PWA | Vite PWA/Nuxt PWA | Required for PWA/offline | Update/rollback tests | Users do not get broken mixed app versions |
| Reliability | Retry/backoff, idempotency, degraded mode, offline behavior | RxJS/interceptors/services | Query tools/framework actions | Composables/query tools | Required | Network throttling/failure tests | App handles bad networks gracefully |
| Browser/device support | Browserslist, mobile devices, low-end devices, assistive tech | Angular browser support policy | Team/framework-defined | Team/framework-defined | Required | Browser matrix QA | App works on committed support matrix |
| Compliance/privacy | GDPR, CCPA, HIPAA, PCI, SOC 2, consent, retention, PII minimization | App-specific | App-specific | App-specific | Required when applicable | Legal/security review | Data collection and consent are documented |
| Licensing | Open-source license review, commercial UI licenses, font/media rights | App-specific | App-specific | App-specific | Required | License scan | No incompatible license ships unnoticed |
| Documentation | README, setup, env vars, architecture, runbooks, ADRs | Angular workspace docs | Framework/app docs | Vue/Nuxt docs | Required | New-developer setup test | New engineer can run and understand app |
| Team process | Code ownership, review rules, branching, release process | Strong convention support | Must define carefully | Moderate convention support | Required | PR checklist, ownership map | Changes are reviewed by correct owners |
| Upgrade policy | Framework upgrades, dependency updates, deprecation tracking | ng update helps | More manual unless framework-managed | Vue/Nuxt upgrade guides | Required | Scheduled upgrade review | App is not trapped on unsupported versions |
| Cost | Hosting, CDN, monitoring, build minutes, third-party services | SSR can add server cost | Depends heavily on framework/hosting | Nuxt SSR can add server cost | Required | Cost dashboard | Cost is visible and acceptable |
| Supportability | Admin/debug tools, user issue reproduction, runbooks, feature flags | App-specific | App-specific | App-specific | Required for serious production apps | Support drill | Team can diagnose real user problems quickly |

## Framework-Specific Completion Matrix

| Topic | Angular production implementation | React production implementation | Vue production implementation |
|---|---|---|---|
| Recommended starting point | Angular CLI with current Angular version | Recommended React framework for production; Vite only when custom stack is intentional | create-vue/Vite for SPA; Nuxt for SSR/SSG/full-stack |
| Build command | `ng build` | Framework build command or `vite build` | `vite build` or `nuxt build` |
| Production output | `dist/<project>` or SSR output | Framework-specific output | `dist` for Vite SPA; `.output`/generated output for Nuxt |
| Microfrontend shell | Angular app shell with Angular Router, Module Federation/native federation, or single-spa root integration | React app shell through React Router/Next-style app shell, Module Federation, or single-spa root integration | Vue/Nuxt shell through Vue Router/Nuxt routing, Vite federation, Module Federation-compatible tooling, or single-spa |
| Microfrontend remote | Expose route modules, standalone components, Angular custom elements, or single-spa Angular app | Expose route modules/components, custom elements, or single-spa React app | Expose route modules/components, custom elements, or single-spa Vue app |
| Microfrontend isolation | Best with route-level domain remotes; web components or iframe when stronger isolation is needed | Best with route/domain remotes; web components or iframe for framework isolation | Best with route/domain remotes; web components or iframe for framework isolation |
| Microfrontend shared runtime | Share Angular/runtime dependencies only with strict version policy | Share `react` and `react-dom` as singletons when same React runtime is required | Share `vue` as singleton when same Vue runtime is required |
| Microfrontend design system | Shared Angular library or web-component design system | Shared package, design tokens, or web-component design system | Shared package, design tokens, or web-component design system |
| Microfrontend testing | Host-remote contract tests, integration E2E, remote standalone tests | Host-remote contract tests, integration E2E, remote standalone tests | Host-remote contract tests, integration E2E, remote standalone tests |
| Routing | Angular Router | React Router, Next.js routing, TanStack Router | Vue Router or Nuxt file routing |
| Lazy loading | Lazy routes, dynamic imports, `@defer` | Dynamic imports, route splitting, framework code splitting | Async components, dynamic imports, route splitting |
| State | Signals/services first; NgRx for large event-heavy state | Local state/hooks first; Context sparingly; Zustand/Redux Toolkit when needed; TanStack Query for server state | Vue reactivity/composables first; Pinia for shared state; Vue Query for server state |
| Forms | Reactive Forms for complex forms | React Hook Form plus schema validation | VeeValidate or composables plus schema validation |
| API layer | HttpClient, interceptors, typed services | Fetch/axios/client generator plus query library/framework loaders | Fetch/axios/client generator plus composables/query library |
| Error handling | Global `ErrorHandler`, route-level handling, HTTP interceptors | Error Boundaries, framework error routes, global reporting | `app.config.errorHandler`, route/API handling |
| Security model | Template binding escapes by default; sanitization for HTML/URLs; avoid unsafe DOM APIs | React escapes text by default; `dangerouslySetInnerHTML` must be sanitized | Vue escapes text by default; never compile untrusted templates; sanitize `v-html` |
| Performance tools | Angular DevTools, Chrome DevTools Angular track, budgets | React DevTools Profiler, browser profiler, bundle analyzer | Vue DevTools, browser profiler, Vite/Rollup analyzer |
| SSR/SSG | Angular SSR/prerender/hydration | Next.js or another React framework | Nuxt |
| PWA/offline | Angular service worker | Workbox/framework PWA support | Vite PWA/Nuxt PWA/community plugins |
| Testing | Angular testing utilities, Testing Library, Playwright/Cypress | React Testing Library, Vitest/Jest, Playwright/Cypress | Vue Test Utils, Vitest, Playwright/Cypress |
| UI libraries | Angular Material, CDK, PrimeNG, custom | MUI, Radix, Chakra, Ant Design, shadcn, custom | Vuetify, Naive UI, Quasar, Element Plus, custom |
| Best scaling pattern | Framework conventions, DI, typed services, clear feature boundaries | Strong team architecture rules plus framework conventions | Composables, Pinia, SFCs, Nuxt conventions |
| Main production risk | Over-complex abstractions, upgrade complexity, heavy bundles if careless | Too many ecosystem choices, inconsistent patterns, rerender/performance mistakes | Smaller ecosystem for some enterprise needs, misuse of reactivity, untrusted templates |

## Microfrontends Complete Matrix

Microfrontends are an organizational and deployment architecture first, not a UI feature. They are usually worth it only when multiple teams need independent ownership, independent release cycles, gradual migration, or strong domain separation. For most small and medium apps, a modular monolith frontend is simpler and cheaper.

| Microfrontend question | Production answer |
|---|---|
| When should you use it? | Use it when separate teams own separate product domains and need independent deployment, or when migrating a large legacy frontend incrementally |
| When should you avoid it? | Avoid it for small apps, simple dashboards, one-team products, or apps where shared state and shared UI change constantly together |
| What is the main benefit? | Independent ownership, independent releases, domain isolation, incremental migration, and technology flexibility |
| What is the main cost? | Runtime complexity, dependency/version conflicts, harder testing, harder observability, shared UX governance, and more deployment failure modes |
| Best split boundary | Business domain or route group, such as billing, checkout, account, admin, reporting |
| Bad split boundary | Button library, header only, technical layers, random pages, or components that change together every sprint |
| Preferred integration level | Route-level remotes first; component-level remotes only when there is a strong reason |
| Ownership model | Each remote has an owning team, code repository or package boundary, release pipeline, error budget, and support contact |
| Compatibility model | Host and remotes follow documented contracts and maintain compatibility for at least one deployment window |
| Rollback model | Host can pin, disable, or roll back a remote without redeploying every other remote |

### Microfrontend Architecture Patterns

| Pattern | How it works | Best for | Angular | React | Vue | Strengths | Risks |
|---|---|---|---|---|---|---|---|
| Route-level Module Federation | Shell loads remote route modules at runtime | Large apps with domain teams and independent deploys | Strong fit | Strong fit | Possible with Vite/webpack-compatible federation | Real independent builds and deployment | Shared dependency/version complexity |
| Component-level Module Federation | Shell loads remote widgets/components at runtime | Dashboards, plugin areas, independently owned widgets | Works, but use carefully | Works, common | Works with federation tooling | Fine-grained composition | Chatty contracts and runtime fragility |
| single-spa orchestration | Root config registers apps and mounts/unmounts them by active route | Mixed Angular/React/Vue migration or multi-framework apps | Strong fit | Strong fit | Strong fit | Explicit lifecycle management and framework mixing | More orchestration and routing complexity |
| Web components/custom elements | Each remote exports standards-based custom elements | Framework-neutral design systems, embedded widgets | Angular Elements or custom wrapper | React wrapper/build output | Vue custom element build/wrapper | Framework isolation and reusable HTML API | Styling, forms, events, SSR, and DX can be harder |
| Iframe composition | Remote app runs in an iframe | Untrusted or strongly isolated apps, third-party embeds | Framework independent | Framework independent | Framework independent | Strong isolation, independent runtime | Poorer UX integration, communication, routing, accessibility, and performance |
| Build-time packages | Domains publish versioned npm packages consumed by one app build | Shared libraries and slower release cadence | Strong fit | Strong fit | Strong fit | Simpler runtime and testing | Not independently deployed at runtime |
| Monorepo modular frontend | One deployable app with strict internal boundaries | Most teams before true MFE is needed | Strong fit | Strong fit | Strong fit | Lowest complexity while preserving modularity | No independent runtime deployment |

### Microfrontend Governance Checklist

| Governance area | Requirement | Done criteria |
|---|---|---|
| Domain ownership | Each remote maps to a product/domain owner | Every remote has an owner, escalation path, and roadmap |
| Contract ownership | Public exports, route contracts, event names, payload schemas, and shared dependency rules are versioned | Breaking changes require review and compatibility plan |
| Release ownership | Each remote has its own build, test, deploy, rollback, and monitoring | A remote can be shipped or rolled back independently |
| Shell ownership | Shell team owns global routing, auth handoff, layout shell, remote discovery, fallback behavior, and shared runtime policy | Shell changes do not require every remote team to coordinate unless contracts change |
| Design system ownership | Tokens, global layout, accessibility rules, and core components are owned centrally | Product pages feel like one app despite independent teams |
| Dependency ownership | Framework/runtime versions and shared package rules are reviewed centrally | No remote silently introduces incompatible shared runtime versions |
| Security ownership | Remote script sources, CSP, dependency scans, auth/session handling, and data boundaries are reviewed | Remote code loading is deliberate and controlled |
| Observability ownership | Error and RUM telemetry include shell and remote metadata | Incidents can be routed to the correct owning team |

### Microfrontend Technical Checklist

| Topic | What to decide | Production-ready rule |
|---|---|---|
| Shell responsibility | Routing, navigation, layout, auth bootstrap, remote discovery, fallback UI | Keep shell small and stable; do not put all business logic in the shell |
| Remote responsibility | Domain UI, domain data loading, domain validation, route subtree, remote-specific tests | Remote can run locally and in preview without the production shell |
| Shared state | URL, backend, events, query cache, or shared store | Prefer URL/backend/events; avoid one giant global client store across remotes |
| Shared UI | Design tokens, icons, base components, accessibility primitives | Version shared UI and test remotes against it |
| Shared dependencies | Framework runtime, router, state library, utility libraries | Share only when version compatibility is controlled; otherwise isolate |
| Events | Names, payload schema, ownership, lifecycle, failure behavior | Use typed events or schema validation for cross-remote communication |
| Auth | Session source, token refresh, permission checks, logout propagation | Shell initializes auth; remotes enforce UI behavior but backend remains source of truth |
| Routing | Route ownership, nested routes, params, redirects, direct links, 404s | Every remote route works on deep link, refresh, browser back, and auth change |
| CSS | Global reset, tokens, scoping, Shadow DOM decision, CSS module strategy | Remotes cannot accidentally break shell or other remotes with global CSS |
| Assets | Public path, CDN paths, hashed assets, remote asset loading | Each remote loads assets from its own versioned base path |
| SSR | Whether remotes render on server, client, or hybrid | Do not assume runtime federation automatically solves SSR; design SSR explicitly |
| Caching | Remote entry caching, asset caching, manifest caching, invalidation | Remote entry/manifest must update safely; immutable assets get long cache |
| Rollback | Host pinning, manifest versioning, kill switch, fallback remote | Bad remote deploy can be disabled or rolled back quickly |
| Local dev | Run shell and remotes together, mock missing remotes, stable ports | A developer can run one remote without starting the whole company frontend |
| Preview envs | Per-remote preview, shell plus remote preview, contract validation | PRs show realistic integrated behavior |
| Testing | Unit, remote component, remote standalone E2E, host integration E2E, contract tests | CI catches host-remote incompatibility before deploy |
| Observability | Error tags, RUM tags, remote version, shell version, route, dependency version | Dashboards can separate shell failures from remote failures |
| Performance | Remote load time, duplicate dependencies, waterfall requests, shared chunk behavior | MFE does not regress Core Web Vitals beyond budget |
| Accessibility | Focus transitions, route announcements, modal layering, keyboard behavior across remotes | Cross-remote navigation is accessible |
| Security | CSP, remote allowlist, dependency scans, secret scans, unsafe HTML review | Only approved remote origins and versions can execute in production |

### Microfrontend Deployment Matrix

| Deployment concern | Required production behavior |
|---|---|
| Independent build | Each remote builds from its own commit and produces immutable assets |
| Remote discovery | Shell knows remotes through static config, environment config, service discovery, or manifest |
| Versioning | Remote versions are identifiable by commit/build number and visible in telemetry |
| Compatibility window | Host supports current and previous remote contract where practical |
| Cache policy | Remote manifests/entries are short-cache or actively invalidated; hashed assets are long-cache immutable |
| Rollback | Remote can be rolled back without redeploying shell; shell can pin a known-good remote |
| Kill switch | Shell can hide or replace a broken remote with fallback UI |
| Canary | High-risk remotes can be exposed to a small user cohort first |
| Preview | PR preview validates shell plus changed remote before merge |
| Smoke test | Post-deploy smoke test verifies shell can load remote and critical route works |

### Microfrontend Testing Matrix

| Test type | What it catches | Required when MFE exists |
|---|---|---|
| Remote unit tests | Domain logic and utility regressions | Yes |
| Remote component tests | Remote UI behavior in isolation | Yes |
| Remote standalone E2E | Domain flow works without full shell complexity | Yes |
| Host integration E2E | Shell can load remote, route to it, pass auth/context, and show fallback | Yes |
| Contract tests | Exposed module, route, event, payload, and shared dependency compatibility | Yes |
| Visual regression | Cross-remote design-system drift | Recommended |
| Accessibility tests | Keyboard/focus behavior across shell and remote boundaries | Yes for critical flows |
| Performance tests | Remote load waterfall, duplicate shared dependencies, route LCP/INP | Yes for user-facing routes |
| Failure injection | Remote timeout, 404 remote entry, bad version, render crash | Yes |

### Microfrontend Anti-Patterns

| Anti-pattern | Why it fails |
|---|---|
| Splitting by framework instead of domain | Creates technical silos rather than product ownership |
| One shared global store for all remotes | Couples releases and makes independent deployment mostly fake |
| Sharing every dependency | Increases runtime negotiation risk and version conflicts |
| Sharing no dependencies without measuring | Can duplicate framework/runtime code and hurt performance |
| Shell owns all business logic | Remotes become thin views and cannot be independently owned |
| Remotes modify global CSS freely | One remote can break unrelated screens |
| No fallback for failed remote load | One failed remote can break the whole user session |
| No contract tests | Host and remote compatibility breaks only after deployment |
| No remote version in telemetry | Incidents become difficult to assign and debug |
| MFE for a one-team app | Adds complexity without solving an organizational problem |

## Decision Matrix

| Situation | Best choice | Why |
|---|---|---|
| Large enterprise team with strict standards | Angular | Strong conventions, CLI, DI, testing patterns, and built-in structure |
| Highly customized product architecture | React | Maximum ecosystem flexibility and many production framework choices |
| Team wants fast delivery with lower complexity | Vue | Excellent DX, clean SFC model, balanced official ecosystem |
| SEO-heavy marketing/content/product pages | React with Next.js or Vue with Nuxt | Mature SSR/SSG and metadata workflows |
| Regulated enterprise dashboard | Angular | Consistency, TypeScript-first workflow, strong architectural patterns |
| Complex interactive product with rich ecosystem needs | React | Broad ecosystem and community patterns |
| Admin dashboard/SaaS back office | Vue or Angular | Vue for speed; Angular for strict enterprise scale |
| Gradual adoption inside existing app | React or Vue | Both can be embedded incrementally |
| Long-lived app with rotating developers | Angular | Strong conventions reduce architecture drift |
| Small team with limited frontend specialization | Vue | Lower learning curve and productive defaults |
| Multiple teams need independent frontend releases | Microfrontends with Angular/React/Vue based on team ownership | MFE solves release ownership more than UI rendering |
| Migration from legacy AngularJS/Angular/React/Vue app | single-spa, route-level federation, or strangler-style shell | Lets old and new screens coexist during migration |
| Need third-party or untrusted app embedding | Iframe composition | Stronger isolation is more important than seamless integration |
| Need framework-neutral reusable widgets | Web components/custom elements | Works across Angular, React, Vue, and non-framework consumers |

## Must-Have vs Optional

| Capability | Required for every production app | Required only sometimes | Usually optional |
|---|---|---|---|
| TypeScript | Yes | No | No |
| Linting/formatting | Yes | No | No |
| Unit/component tests | Yes | No | No |
| E2E tests for critical flows | Yes | No | No |
| Error tracking | Yes | No | No |
| Responsive design | Yes | No | No |
| Accessibility baseline | Yes | No | No |
| Security headers | Yes | No | No |
| Dependency scanning | Yes | No | No |
| SSR/SSG | No | SEO/content/performance-sensitive apps | No |
| PWA/offline | No | Offline/field/mobile-like apps | No |
| Visual regression | No | Design-system-heavy apps | Small apps |
| Feature flags | No | Frequent releases, experiments, enterprise rollout | Static apps |
| Internationalization | No | Multi-region/multi-language apps | Single-locale apps |
| Advanced observability/tracing | No | Large apps, B2B/SaaS, revenue-critical flows | Small internal apps |
| Microfrontends | No | Large organizations, independent domain teams, gradual migration, plugin platforms | Most one-team apps |

## Complete Phase-by-Phase Production Plan

This is the execution plan for taking an Angular, React, Vue, or microfrontend frontend from idea to production and long-term operation. Treat every phase as a gate. If a phase is not applicable, mark it `N/A`, write the reason, and get explicit owner approval. Do not silently skip it.

### Perspective Coverage Map

| Perspective | What it must protect | Required outputs |
|---|---|---|
| Business | Value, cost, timeline, market fit, operational impact | Business case, success metrics, budget, release target, priority tradeoffs |
| Product | User outcomes, scope, acceptance criteria, workflow completeness | PRD, user journeys, requirements, feature map, acceptance criteria |
| User research | Real user needs, usability risks, accessibility expectations | Personas, jobs-to-be-done, research notes, usability findings |
| UX and content | Information architecture, flows, labels, empty/error states, user confidence | Wireframes, flows, copy deck, state inventory, navigation model |
| Visual design | Visual hierarchy, responsive layout, design quality, brand alignment | High-fidelity screens, responsive variants, token usage, visual QA notes |
| Design system | Consistency, reuse, accessibility primitives, component governance | Tokens, component inventory, usage rules, Storybook or equivalent |
| Frontend architecture | Framework fit, maintainability, routing, state, rendering, modularity | ADRs, folder conventions, state model, rendering decision, route map |
| Backend/API | Stable contracts, data semantics, latency, error behavior, versioning | OpenAPI/GraphQL/tRPC contracts, error envelope, mock server, test data |
| Security | XSS, CSRF, auth, session handling, supply chain, remote code risks | Threat model, security checklist, CSP plan, dependency scan, secret scan |
| Privacy/compliance | PII minimization, consent, retention, regional rules, auditability | Data map, consent plan, compliance review, retention rules |
| QA/testing | Regression prevention, coverage of critical flows, release confidence | Test strategy, test matrix, E2E suite, accessibility checks, defect policy |
| Performance | Core Web Vitals, bundle size, runtime responsiveness, network resilience | Performance budget, bundle report, Lighthouse/WebPageTest/RUM baseline |
| DevEx/tooling | Repeatable local setup, code quality, automation, fast feedback | README, package manager rules, lint/typecheck/test commands, generators |
| DevOps/platform | Environments, deploys, CDN, cache, rollback, infrastructure reliability | CI/CD pipeline, environment config, deployment runbook, rollback plan |
| SRE/operations | Observability, alerts, incident response, service health, error budgets | Dashboards, alerts, SLOs, incident runbook, ownership map |
| Data/analytics | Event quality, funnel visibility, privacy-safe measurement | Tracking plan, event schema, analytics QA, dashboard definitions |
| Support/customer success | Diagnosability, user issue handling, admin workflows, release awareness | Support runbook, known issues, debug metadata, escalation path |
| Legal/procurement | Licenses, vendor terms, accessibility/legal exposure, media rights | License scan, vendor review, DPA/SCC review if needed, asset rights |
| Management/governance | Ownership, staffing, decisions, risk control, communication | RACI, roadmap, risk register, decision log, launch sign-off |
| Finance | Hosting cost, monitoring cost, build minutes, vendor spend, TCO | Cost estimate, cost dashboard, budget guardrails, scale assumptions |

### Master Phase Overview

| Phase | Name | Primary question | Main outputs | Exit gate |
|---|---|---|---|---|
| 0 | Initiation and constraints | Why are we building this and what limits us? | Business case, stakeholders, constraints, initial risks | Sponsor agrees on goal, budget, timeline, and success metrics |
| 1 | Product discovery and scope | What exactly must users be able to do? | PRD, personas, journeys, MVP scope, acceptance criteria | Critical flows and non-goals are approved |
| 2 | Framework and architecture decision | Which frontend shape fits the product and team? | Framework ADR, rendering ADR, state/API/testing strategy | Architecture review accepts tradeoffs and operating model |
| 3 | Delivery governance and team setup | Who owns what and how will work move? | RACI, branching/review rules, delivery plan, risk register | Team can start implementation without unclear ownership |
| 4 | Repo, tooling, and local foundation | Can any developer run, test, and build the app consistently? | Project scaffold, TypeScript, lint, format, test runner, CI baseline | Clean install, lint, typecheck, test, and build pass |
| 5 | Design system and UX foundation | Can UI be built consistently and accessibly? | Tokens, core components, layout patterns, state inventory | Reusable UI primitives cover repeated patterns |
| 6 | App shell, routing, and navigation | Does the app skeleton behave like the final product? | Route map, layouts, guards, auth boundary, responsive shell | Direct links, refresh, 404, protected routes, mobile nav work |
| 7 | Data, API, auth, and state layer | Can frontend and backend integrate safely and predictably? | Typed client, auth flow, cache policy, error envelope, mocks | API contract tests and auth flows pass |
| 8 | Vertical-slice feature delivery | Are real workflows implemented end to end? | Feature slices, screens, data flows, tests, telemetry hooks | Each slice passes acceptance, QA, accessibility, and E2E checks |
| 9 | Forms, permissions, and edge states | Are complex user inputs and authorization handled correctly? | Validation, permission matrix, empty/loading/error/offline states | Invalid, denied, expired, slow, and failed cases are tested |
| 10 | Security, privacy, and compliance hardening | Can the app safely handle real users and real data? | Threat model closure, CSP, scans, data map, compliance sign-off | No blocking security/privacy findings remain |
| 11 | Accessibility and internationalization readiness | Can target users access and understand the app? | WCAG checklist, keyboard QA, screen reader smoke test, locale plan | Critical flows pass accessibility and locale stress checks |
| 12 | Performance and reliability engineering | Will the app feel fast and remain usable under poor conditions? | Budgets, bundle report, Core Web Vitals baseline, resilience tests | Performance budgets and network failure tests pass |
| 13 | Testing completion and release automation | Can regressions be caught before production? | Unit/component/E2E/contract/visual/a11y test suites in CI | Main branch is releasable from CI |
| 14 | Microfrontend readiness, if applicable | Can shell and remotes evolve independently without breaking users? | MFE contracts, manifest/versioning, fallback, rollback, remote telemetry | Host plus remotes pass compatibility and failure-injection tests |
| 15 | Observability, analytics, and supportability | Can production behavior be measured and diagnosed? | Dashboards, alerts, event schema, support runbook, release metadata | Test errors/events appear correctly in dashboards |
| 16 | Deployment, environments, and go-live | Can we deploy, validate, roll back, and operate production? | Environments, CDN/cache config, release checklist, rollback drill | Production smoke test and rollback drill pass |
| 17 | Post-launch stabilization | What did production reveal and what must be fixed first? | Launch report, defect triage, metric review, backlog update | Launch metrics meet thresholds or recovery plan is active |
| 18 | Long-term maintenance and evolution | Can the app stay healthy after launch? | Upgrade policy, dependency cadence, ownership map, roadmap | Maintenance process is scheduled and owned |

### Phase 0: Initiation and Constraints

| Area | Required actions |
|---|---|
| Goal | Define the business problem, target users, expected value, and reason a frontend change is needed. |
| Business | Confirm budget, deadline, revenue/customer impact, operational impact, and opportunity cost. |
| Product | Write the initial problem statement, target audience, top workflows, and non-goals. |
| Engineering | Identify technical constraints: existing backend, auth provider, hosting, browser support, legacy systems, data model, APIs, integrations, and team skills. |
| Security/compliance | Classify data sensitivity, regulatory exposure, vendor restrictions, audit requirements, and authentication constraints. |
| Operations | Identify release windows, support hours, incident expectations, uptime needs, and rollback expectations. |
| Deliverables | Project brief, stakeholder list, assumptions log, constraints list, initial risk register, success metric draft. |
| Verification | Stakeholders agree on why the project exists, what success means, what is out of scope, and what constraints cannot be broken. |
| Exit gate | No implementation starts until sponsor, product owner, engineering lead, design lead, QA lead, and security/compliance owner agree on the project frame. |

### Phase 1: Product Discovery and Scope

| Area | Required actions |
|---|---|
| Product | Define personas, roles, permissions, user journeys, core flows, edge flows, acceptance criteria, launch scope, and post-launch backlog. |
| UX | Map entry points, navigation paths, happy paths, failure paths, empty states, first-time use, repeat use, and recovery flows. |
| Business | Prioritize scope by impact, risk, legal need, customer commitment, and timeline. |
| Analytics | Define measurable outcomes: activation, completion rate, conversion, retention, task success, error rate, funnel drop-off. |
| QA | Convert requirements into testable scenarios and identify high-risk paths needing E2E coverage. |
| Support | Identify likely user confusion points, support macros, escalation triggers, and admin/debug needs. |
| Deliverables | PRD, user journey map, feature inventory, MVP/non-MVP split, role and permission matrix, acceptance criteria, analytics goals. |
| Verification | Every critical flow has an owner, acceptance criteria, expected states, error states, permissions, and analytics events. |
| Exit gate | Product, design, engineering, QA, analytics, and support agree that the scope is buildable, testable, and measurable. |

### Phase 2: Framework and Architecture Decision

| Area | Required actions |
|---|---|
| Framework choice | Choose Angular, React, Vue, or a microfrontend composition based on team skill, product complexity, release model, ecosystem needs, and long-term maintenance. |
| Rendering | Decide CSR, SSR, SSG, prerender, hybrid, edge rendering, or PWA based on SEO, performance, personalization, hosting, and compliance constraints. |
| Routing | Define route ownership, nested layouts, redirects, protected routes, deep links, 404 behavior, route metadata, and browser history rules. |
| State | Separate local UI state, URL state, server state, global client state, persisted state, and cross-tab state. |
| Data/API | Choose OpenAPI, GraphQL, tRPC, generated client, hand-written client, validation library, retry/cancel strategy, and error model. |
| Architecture | Define feature boundaries, shared components, dependency rules, import boundaries, service/composable/hook patterns, and folder structure. |
| Testing | Choose unit, component, E2E, contract, visual, accessibility, and performance testing tools. |
| Security | Decide secure cookie/token strategy, CSRF approach, CSP compatibility, secret handling, sanitization policy, and third-party script governance. |
| Performance | Define initial bundle budget, route-level budgets, image/font strategy, lazy loading strategy, and profiling approach. |
| Deliverables | Framework ADR, rendering ADR, routing map, state model, API strategy, testing strategy, security architecture notes, performance budget draft. |
| Verification | Architecture review compares tradeoffs, migration cost, team ability, performance impact, deployment impact, and failure modes. |
| Exit gate | Engineering lead, product owner, QA, security, DevOps, and design sign off before scaffolding production code. |

### Phase 3: Delivery Governance and Team Setup

| Area | Required actions |
|---|---|
| Ownership | Assign accountable owners for product, design, frontend, backend, QA, security, DevOps, analytics, support, and release management. |
| Process | Define branching, PR review rules, code ownership, Definition of Ready, Definition of Done, release cadence, and change approval flow. |
| Planning | Break work into milestones, vertical slices, integration points, and release candidates. |
| Risk | Maintain a risk register covering scope, API readiness, design readiness, performance, hiring/skills, dependencies, vendors, security, and compliance. |
| Communication | Set status reporting, decision logging, demo cadence, incident escalation, stakeholder review, and launch communication plan. |
| Deliverables | RACI, milestone plan, risk register, decision log, review checklist, delivery board, release calendar. |
| Verification | Every major deliverable and risk has a named owner and due date. |
| Exit gate | No phase depends on an unnamed person, hidden approval, or undefined review path. |

### Phase 4: Repo, Tooling, and Local Foundation

| Area | Required actions |
|---|---|
| Project setup | Scaffold the app using the chosen framework and official or team-approved tooling. |
| TypeScript | Enable strict TypeScript where possible and document any exceptions. |
| Package management | Pin package manager, lockfile policy, Node version, install command, dependency rules, and upgrade approach. |
| Code quality | Add linting, formatting, import rules, unused code checks, commit hooks if useful, and CI enforcement. |
| Testing baseline | Add unit/component test runner, E2E runner skeleton, coverage rules, test data strategy, and sample tests. |
| Build | Add production build, preview build, source maps policy, environment config, and artifact output rules. |
| Documentation | Write setup instructions, commands, env vars, architecture links, troubleshooting, and contribution rules. |
| Deliverables | Working repo, README, package scripts, baseline CI, sample component, sample route, sample API mock, initial tests. |
| Verification | Fresh checkout can install, run, lint, typecheck, test, build, and preview using documented commands. |
| Exit gate | A new developer can run the app without undocumented local knowledge. |

### Phase 5: Design System and UX Foundation

| Area | Required actions |
|---|---|
| Design tokens | Define color, typography, spacing, elevation, radius, motion, focus, z-index, breakpoints, and density rules. |
| Components | Build or adopt buttons, inputs, selects, dialogs, menus, tabs, tables, forms, alerts, toasts, skeletons, pagination, nav, and layout primitives. |
| States | Define loading, empty, error, disabled, hover, focus, selected, validation, permission denied, offline, and success states. |
| Responsive | Define mobile, tablet, desktop, and wide layouts for primary screens. |
| Accessibility | Establish focus styles, keyboard behavior, ARIA rules, contrast targets, reduced motion, and screen reader expectations. |
| Content | Define labels, helper text, empty state copy, error copy, confirmation copy, and destructive action language. |
| Governance | Define who can change tokens/components, how breaking visual changes are reviewed, and how examples are documented. |
| Deliverables | Token file, core components, state examples, responsive layouts, design QA checklist, Storybook or equivalent component preview. |
| Verification | Critical UI patterns are reusable, accessible, responsive, and visually consistent before feature work scales. |
| Exit gate | Feature teams can build screens without inventing one-off UI patterns for common controls. |

### Phase 6: App Shell, Routing, and Navigation

| Area | Required actions |
|---|---|
| Shell | Implement global layout, top nav, side nav, mobile nav, breadcrumbs, account menu, notifications area, skip link, and content outlet. |
| Routing | Implement public routes, protected routes, nested routes, dynamic params, redirects, 404, unauthorized, and route refresh behavior. |
| Auth boundary | Add auth bootstrap, session loading, route guards, logout handling, token/session expiry behavior, and permission loading. |
| Layout | Validate responsive behavior, scroll restoration, focus on route change, page title updates, and print behavior if needed. |
| Error boundaries | Add route-level and shell-level recovery UI for rendering failures and remote loading failures if applicable. |
| Deliverables | Usable app skeleton, route map, route tests, shell components, auth guard, navigation behavior tests. |
| Verification | Direct links, refresh, browser back/forward, mobile nav, 404, denied access, and session transitions work. |
| Exit gate | Users can move through the empty app shell in the same shape as the final product. |

### Phase 7: Data, API, Auth, and State Layer

| Area | Required actions |
|---|---|
| API contracts | Finalize typed request/response contracts, versioning, pagination, sorting, filtering, upload/download, and error envelope. |
| Client | Implement generated or typed API client, base URL config, auth headers, request IDs, retries, cancellation, timeouts, and error normalization. |
| Server state | Implement caching, invalidation, optimistic updates where appropriate, background refresh, stale state rules, and deduplication. |
| Auth | Implement login, logout, session refresh, expiry, denied access, multi-tab behavior, and secure storage/cookie strategy. |
| Authorization | Implement role/permission checks in UI while preserving backend as source of truth. |
| Mocking | Provide mock server, fixtures, contract tests, and local error simulation. |
| Deliverables | Typed API layer, auth integration, state conventions, mock data, contract tests, integration examples. |
| Verification | API mocks and real integration behave the same for success, validation error, auth error, server error, timeout, and retry cases. |
| Exit gate | Feature teams have one approved way to fetch, mutate, cache, validate, and display backend data. |

### Phase 8: Vertical-Slice Feature Delivery

| Area | Required actions |
|---|---|
| Build method | Deliver features as vertical slices: route, UI, data, state, permissions, analytics, errors, tests, and docs together. |
| Product | Validate each slice against acceptance criteria and priority. |
| UX/design | Review flow, copy, visual states, responsive behavior, keyboard behavior, and edge states. |
| Frontend | Keep code inside approved feature boundaries, reuse shared primitives, avoid hidden cross-feature coupling, and keep route chunks lazy when appropriate. |
| Backend | Confirm API readiness, latency, data quality, permissions, and failure behavior. |
| QA | Add automated tests for critical behavior and manual exploratory testing for high-risk flows. |
| Analytics | Add approved events with stable names, schemas, and privacy-safe payloads. |
| Support | Document user-visible behavior, known limitations, and debug signals. |
| Deliverables | Completed feature slices, tests, analytics events, UX sign-off, API sign-off, support notes. |
| Verification | Each slice passes acceptance, visual QA, accessibility smoke test, E2E flow, and error-state review. |
| Exit gate | A slice is not complete until success, failure, loading, empty, denied, and mobile states are handled. |

### Phase 9: Forms, Permissions, and Edge States

| Area | Required actions |
|---|---|
| Forms | Implement client validation, server validation, touched/dirty states, async validation, submit locking, unsaved-change prompts, and error summaries. |
| Permissions | Verify roles, feature flags, plan limits, ownership rules, read-only states, and unauthorized API responses. |
| Edge states | Cover loading, skeletons, empty, no results, partial data, offline, timeout, retry, rate limit, server error, conflict, stale data, deleted resource, and maintenance mode. |
| Destructive actions | Add confirmation, permission check, audit trail where needed, rollback/undo where appropriate, and clear success/error feedback. |
| QA | Test invalid input, malicious input, boundary values, slow network, duplicate submit, expired auth, denied access, and concurrent edits. |
| Deliverables | Form patterns, permission matrix tests, edge-state inventory, destructive action checklist, validation test suite. |
| Verification | Users never see blank screens or unrecoverable flows during common failure cases. |
| Exit gate | Every critical workflow is usable when data is missing, invalid, slow, denied, stale, or failed. |

### Phase 10: Security, Privacy, and Compliance Hardening

| Area | Required actions |
|---|---|
| Threat model | Review assets, actors, trust boundaries, entry points, abuse cases, dependency risks, third-party scripts, and remote code loading. |
| XSS | Audit unsafe HTML, template injection, markdown rendering, rich text, URL handling, DOM APIs, and third-party widgets. |
| Auth/session | Validate token/cookie security, CSRF protection, refresh flow, logout propagation, session timeout, and account switching. |
| Headers | Configure CSP, frame options, referrer policy, permissions policy, HSTS, content type options, and Trusted Types where appropriate. |
| Secrets | Confirm no secret, private key, privileged token, internal credential, or server-only config ships in frontend assets. |
| Dependencies | Run dependency audit, license review, SBOM if needed, lockfile review, and supply-chain policy checks. |
| Privacy | Map collected data, analytics payloads, consent requirements, retention, deletion rights, PII masking, and logging restrictions. |
| Compliance | Validate GDPR, CCPA/CPRA, HIPAA, PCI, SOC 2, accessibility law, industry rules, or customer contractual requirements as applicable. |
| Deliverables | Threat model, security checklist, privacy data map, scan reports, header tests, consent plan, compliance sign-off. |
| Verification | Security/privacy findings are triaged by severity and blocking issues are fixed or formally risk-accepted. |
| Exit gate | No high/critical known vulnerability, client-side secret leak, unapproved PII collection, or unresolved auth flaw remains. |

### Phase 11: Accessibility and Internationalization Readiness

| Area | Required actions |
|---|---|
| Accessibility standard | Set WCAG target, usually WCAG 2.2 AA for serious production apps unless a stricter standard applies. |
| Keyboard | Verify tab order, focus visibility, skip links, menus, dialogs, tables, forms, route changes, shortcuts, and traps. |
| Screen reader | Verify names, roles, landmarks, headings, live regions, form errors, route announcements, and status messages. |
| Visual access | Verify contrast, text resizing, zoom, reduced motion, color-independent meaning, focus states, and responsive reflow. |
| Internationalization | Plan translation keys, pluralization, dates, times, currency, numbers, sorting, locale routing, and timezone behavior. |
| RTL/long text | Stress test longest supported language, right-to-left layout if needed, and dynamic content overflow. |
| Deliverables | Accessibility test report, axe or equivalent results, manual keyboard checklist, screen reader smoke notes, i18n plan, locale test cases. |
| Verification | Critical flows are usable by keyboard and assistive technology, and text does not break layouts in target locales. |
| Exit gate | Accessibility and locale blockers are fixed before release candidate. |

### Phase 12: Performance and Reliability Engineering

| Area | Required actions |
|---|---|
| Budgets | Set route-level JS/CSS/image budgets, LCP, INP, CLS, TTFB, API latency, memory, and interaction targets. |
| Bundle | Analyze initial bundle, route chunks, duplicate dependencies, heavy libraries, polyfills, source maps, and CSS size. |
| Loading | Implement lazy routes, code splitting, prefetch/preload strategy, image optimization, font loading, critical CSS, and skeleton strategy. |
| Runtime | Profile render hot paths, large lists, expensive computed values, unnecessary rerenders/change detection, memory leaks, and animation cost. |
| Network | Test slow 3G/4G, offline, high latency, request timeout, API retry/backoff, cancellation, and partial outage behavior. |
| Reliability | Add idempotency support where relevant, conflict handling, optimistic update recovery, stale data handling, and degraded mode. |
| Deliverables | Performance budget, bundle analysis, profiling notes, Core Web Vitals baseline, network resilience test results, optimization backlog. |
| Verification | Production build passes budgets and critical flows remain usable under agreed low-end device/network conditions. |
| Exit gate | No performance regression blocks critical user workflows or violates agreed production budgets. |

### Phase 13: Testing Completion and Release Automation

| Area | Required actions |
|---|---|
| Unit | Cover pure logic, utilities, services, composables/hooks, reducers/stores, validators, formatters, and permission rules. |
| Component | Cover shared components, forms, tables, dialogs, menus, error states, keyboard behavior, and critical feature screens. |
| Integration | Cover API client, auth integration, route guards, state/data interactions, feature flags, and error normalization. |
| E2E | Cover login/logout, critical journeys, direct route refresh, permissions, CRUD flows, failed network, and mobile viewport smoke tests. |
| Contract | Validate frontend/backend schemas, generated clients, remote contracts, event payloads, and error envelopes. |
| Visual | Use visual regression for design-system-heavy apps, marketing surfaces, dashboards, and high-risk layouts. |
| Accessibility | Run automated checks in CI and keep manual keyboard/screen reader checks for critical flows. |
| CI | Enforce install, lint, typecheck, test, build, scan, preview deploy, smoke test, and artifact upload. |
| Deliverables | Test matrix, automated suites, CI pipeline, coverage report, flaky test policy, release candidate checklist. |
| Verification | CI catches a deliberately broken critical flow, type error, lint error, failed build, and failed E2E test. |
| Exit gate | Main branch can produce a production artifact at any time and release candidate builds are traceable. |

### Phase 14: Microfrontend Readiness, If Applicable

| Area | Required actions |
|---|---|
| Justification | Confirm microfrontends solve ownership, release independence, migration, or plugin needs that a modular monolith cannot solve more cheaply. |
| Boundaries | Split by business domain or route group, not by technical layer or arbitrary components. |
| Shell | Define shell responsibility: auth bootstrap, global routing, layout, remote discovery, fallback UI, shared runtime policy, and telemetry metadata. |
| Remotes | Define remote responsibility: domain routes, domain UI, domain data, domain tests, versioned public exports, and local standalone operation. |
| Contracts | Version exposed modules, route contracts, events, payload schemas, shared dependencies, CSS rules, and browser support. |
| Dependencies | Decide singleton, pinned, shared, isolated, or bundled dependencies with compatibility policy. |
| Deployment | Implement immutable remote assets, short-cache manifest/remote entry, version identifiers, preview deploys, canary, rollback, and kill switch. |
| Failure isolation | Test remote timeout, missing remote, bad version, render crash, auth mismatch, and shell fallback behavior. |
| Observability | Tag shell version, remote name, remote version, route, browser, release, user/session where allowed, and owning team. |
| Security | Review remote origins, CSP, script allowlist, dependency scans per remote, trust boundaries, and data sharing. |
| Deliverables | MFE ADR, ownership map, contract schemas, shared dependency policy, manifest/version plan, fallback UI, integration tests, rollback runbook. |
| Verification | Host and remotes can deploy independently without breaking compatible versions, and one broken remote does not break the whole app. |
| Exit gate | No remote ships without owner, contract, tests, telemetry, fallback, versioning, and rollback path. |

### Phase 15: Observability, Analytics, and Supportability

| Area | Required actions |
|---|---|
| Error tracking | Capture frontend errors, unhandled promise rejections, route errors, API failures, remote failures, release tags, and user/session context where allowed. |
| RUM | Track Core Web Vitals, route timings, API latency, device/browser class, slow interactions, and frontend health indicators. |
| Analytics | Implement event schema, naming conventions, funnel events, consent handling, QA validation, and dashboard ownership. |
| Logging | Add request IDs/correlation IDs, feature flag state, app version, route, environment, and remote version where applicable. |
| Alerts | Define alert thresholds for error rate, failed route loads, failed API calls, Core Web Vitals degradation, and deployment anomalies. |
| Support | Build issue reproduction steps, debug metadata, user/session lookup rules, admin tools if needed, known-issue process, and escalation path. |
| Deliverables | Observability dashboard, analytics dashboard, event catalog, alert rules, support runbook, release metadata policy. |
| Verification | Trigger a test error, failed API call, slow route, analytics event, and release marker; confirm all appear in the right dashboards. |
| Exit gate | Production issues can be assigned to an owner with enough context to reproduce or diagnose. |

### Phase 16: Deployment, Environments, and Go-Live

| Area | Required actions |
|---|---|
| Environments | Define local, test, preview, staging, production, and optional canary environments with clear config boundaries. |
| Config | Validate runtime config, build-time config, env vars, secrets separation, feature flags, API base URLs, and third-party keys. |
| Hosting | Configure static/CDN, SSR Node/edge/container hosting, TLS, HTTP/2/3, compression, SPA fallback, cache headers, and health checks. |
| CI/CD | Automate build, scan, test, artifact versioning, deployment, smoke test, release notes, and promotion. |
| Rollback | Test rollback, previous artifact promotion, cache invalidation, feature flag disable, remote pinning if MFE, and database/API compatibility assumptions. |
| Release | Prepare launch checklist, release owner, deployment window, stakeholder communication, support readiness, monitoring watch, and go/no-go criteria. |
| Deliverables | Deployment pipeline, environment matrix, production config, smoke tests, rollback runbook, launch checklist, release notes. |
| Verification | Staging deploy matches production behavior closely enough, production smoke tests pass, and rollback drill succeeds. |
| Exit gate | Go-live is approved only after product, engineering, QA, security, DevOps, support, and business sign-off. |

### Phase 17: Post-Launch Stabilization

| Area | Required actions |
|---|---|
| Monitoring | Watch errors, Core Web Vitals, traffic, API failures, conversion/task success, support tickets, and user feedback. |
| Triage | Prioritize defects by user impact, business impact, security risk, data loss risk, and workaround availability. |
| Product | Compare actual metrics against success criteria and identify adoption gaps or workflow confusion. |
| UX | Review session recordings or usability feedback if allowed, funnel drop-offs, confusing copy, and support complaints. |
| Engineering | Fix release blockers, performance regressions, flaky routes, integration bugs, and telemetry gaps. |
| Support | Update known issues, help docs, response templates, escalation rules, and customer messaging. |
| Deliverables | Launch report, defect triage board, metric review, support summary, stabilization backlog, follow-up release plan. |
| Verification | Blocking defects are fixed or mitigated, metrics are understood, and owners exist for remaining issues. |
| Exit gate | Project leaves hypercare only when operational metrics are stable and support volume is acceptable. |

### Phase 18: Long-Term Maintenance and Evolution

| Area | Required actions |
|---|---|
| Ownership | Keep code owners, feature owners, dashboard owners, dependency owners, and support owners current. |
| Upgrades | Schedule framework, TypeScript, build tool, browser support, dependency, and design-system upgrades. |
| Security | Continue dependency scans, threat-model refreshes, header reviews, secret scans, vendor reviews, and incident lessons learned. |
| Performance | Maintain budgets, review RUM trends, prevent bundle creep, and profile high-traffic workflows after major changes. |
| Testing | Prune flaky tests, add tests for escaped defects, review coverage around critical flows, and keep test data realistic. |
| Product | Revisit KPIs, backlog, user feedback, feature flags, A/B tests, and deprecation candidates. |
| Operations | Review SLOs, incident history, alert quality, runbooks, deployment frequency, rollback reliability, and cost. |
| Deliverables | Maintenance calendar, upgrade policy, deprecation policy, quarterly health report, cost report, roadmap refresh. |
| Verification | The app remains secure, fast, supportable, and releasable after the original launch team moves on. |
| Exit gate | Maintenance is considered active work with named owners, not an afterthought. |

### RACI by Phase

| Phase | Accountable | Responsible contributors | Consulted | Informed |
|---|---|---|---|---|
| 0. Initiation | Sponsor | Product, engineering lead | Security, finance, operations | All stakeholders |
| 1. Discovery | Product owner | UX, research, analytics, QA | Support, sales/customer success, legal | Engineering, leadership |
| 2. Architecture | Engineering lead | Frontend, backend, DevOps | Security, QA, design | Product, leadership |
| 3. Governance | Delivery lead | Product, engineering, QA | Security, support, management | Full team |
| 4. Tooling | Frontend lead | Frontend, DevOps, QA | Security | Engineering team |
| 5. Design system | Design lead | UX, frontend | Accessibility, product, QA | Full team |
| 6. App shell | Frontend lead | Frontend, UX, QA | Security, DevOps | Product |
| 7. Data/auth/state | Engineering lead | Frontend, backend | Security, QA, DevOps | Product |
| 8. Features | Product owner | Frontend, backend, design, QA | Analytics, support, security | Stakeholders |
| 9. Edge states | QA lead | Frontend, backend, UX | Product, security, support | Engineering |
| 10. Security/privacy | Security owner | Frontend, backend, DevOps | Legal, compliance, product | Leadership |
| 11. Accessibility/i18n | Design or accessibility owner | Frontend, QA, content | Legal, product | Full team |
| 12. Performance | Frontend lead | Frontend, DevOps, backend | Product, QA | Leadership |
| 13. Testing/CI | QA lead | Frontend, backend, DevOps | Product, security | Full team |
| 14. Microfrontends | Architecture owner | Shell team, remote teams, DevOps | Security, QA, design system owner | Product, leadership |
| 15. Observability/support | SRE or DevOps owner | Frontend, backend, analytics, support | Security, product | Full team |
| 16. Go-live | Release manager | DevOps, QA, engineering, product | Security, support, leadership | All stakeholders |
| 17. Stabilization | Product and engineering leads | QA, support, DevOps, analytics | Security, design | Leadership |
| 18. Maintenance | Engineering manager | Frontend, DevOps, QA, security | Product, support, finance | Leadership |

### Non-Negotiable Release Gates

| Gate | Required evidence |
|---|---|
| Product gate | PRD approved, acceptance criteria complete, critical flows mapped, non-goals documented. |
| Design gate | Responsive screens reviewed, reusable patterns defined, edge states and accessibility expectations documented. |
| Architecture gate | Framework/rendering/state/API/testing decisions documented with tradeoffs and owners. |
| Security gate | Threat model complete, dependency scan reviewed, no secrets in bundle, auth/session paths tested, CSP/security headers planned or deployed. |
| Privacy/compliance gate | Data collection reviewed, consent/retention requirements handled, analytics payloads approved. |
| Quality gate | Lint, typecheck, unit/component tests, E2E tests, contract tests, accessibility checks, and production build pass in CI. |
| Performance gate | Bundle budgets, Core Web Vitals targets, route timings, image/font optimization, and slow-network behavior meet target. |
| Observability gate | Error tracking, RUM, analytics, release tags, dashboards, and alerts are verified with test events. |
| Deployment gate | Staging deploy, production config, smoke test, rollback drill, cache policy, and release checklist are complete. |
| Support gate | Runbook, known issues, escalation path, debug metadata, and launch communication are ready. |

### Phase Artifact Index

| Artifact | Created in phase | Owner | Purpose |
|---|---|---|---|
| Project brief | 0 | Sponsor/product | Explain why the project exists and what success means. |
| Stakeholder map | 0 | Delivery lead | Prevent hidden approvers and unclear communication. |
| Risk register | 0-3, updated always | Delivery lead | Track and mitigate delivery, technical, security, product, and operational risks. |
| PRD | 1 | Product owner | Define scope, flows, requirements, acceptance criteria, and non-goals. |
| User journey map | 1 | UX/product | Show end-to-end user workflows and edge cases. |
| Permission matrix | 1, refined in 9 | Product/security | Define roles, access rules, and denied states. |
| Framework ADR | 2 | Engineering lead | Record Angular vs React vs Vue vs MFE decision and tradeoffs. |
| Rendering ADR | 2 | Engineering lead | Record CSR/SSR/SSG/prerender/PWA decision. |
| API contract | 2, finalized in 7 | Backend/API owner | Prevent frontend/backend drift. |
| Test strategy | 2, finalized in 13 | QA lead | Define what gets tested where and why. |
| RACI | 3 | Delivery lead | Assign accountable and responsible owners. |
| README/setup docs | 4 | Frontend lead | Make local development repeatable. |
| Design system docs | 5 | Design system owner | Keep UI consistent and accessible. |
| Route map | 6 | Frontend lead | Define navigation, auth, deep links, and layouts. |
| State model | 7 | Frontend lead | Clarify ownership of local, URL, server, global, and persisted state. |
| Threat model | 10 | Security owner | Identify and close frontend security risks. |
| Data/privacy map | 10 | Privacy/compliance owner | Document PII, consent, retention, and logging rules. |
| Accessibility report | 11 | Accessibility/QA owner | Prove critical flows are accessible. |
| Performance budget | 12 | Frontend lead | Prevent speed and bundle regressions. |
| CI/CD pipeline | 13, 16 | DevOps owner | Make builds, tests, scans, deploys, and rollbacks repeatable. |
| MFE contract pack | 14 | Architecture owner | Govern shell/remote compatibility if microfrontends exist. |
| Observability dashboard | 15 | SRE/DevOps owner | Diagnose production behavior by release, route, user/session where allowed. |
| Analytics tracking plan | 15 | Analytics owner | Measure product outcomes with privacy-safe events. |
| Deployment runbook | 16 | DevOps/release owner | Execute go-live consistently. |
| Rollback runbook | 16 | DevOps/release owner | Restore service quickly after a bad deploy. |
| Launch report | 17 | Product/engineering | Compare launch results with goals and capture follow-up work. |
| Maintenance calendar | 18 | Engineering manager | Keep dependencies, security, performance, and docs healthy. |

### Perspective-by-Perspective Final Validation

| Perspective | Final questions before production |
|---|---|
| Business | Does the release support the agreed goal, budget, timeline, and expected return? |
| Product | Can every target role complete every critical workflow with clear success and failure outcomes? |
| UX | Are navigation, copy, state transitions, and recovery paths understandable without explanation? |
| Design | Does the UI remain polished and responsive across supported breakpoints and content lengths? |
| Frontend | Are routes, state, API calls, feature boundaries, rendering, and error handling implemented consistently? |
| Backend/API | Are contracts stable, versioned, validated, performant, and tested against frontend expectations? |
| Security | Are XSS, CSRF, auth/session, CSP, dependency, secret, and third-party script risks controlled? |
| Privacy/compliance | Is collected data necessary, consented where required, protected, retained correctly, and audit-ready? |
| QA | Would CI fail if a critical user journey, permission rule, contract, build, or accessibility check regressed? |
| Performance | Are Core Web Vitals, bundle budgets, runtime interactions, and low-network conditions within target? |
| DevOps | Can the app be deployed, smoke-tested, monitored, rolled back, and configured without manual guesswork? |
| SRE/operations | Are alerts meaningful, dashboards actionable, ownership clear, and incident steps documented? |
| Analytics | Are product events complete, privacy-safe, stable, QA-tested, and mapped to business metrics? |
| Support | Can support identify release version, user path, known issues, escalation route, and workaround? |
| Legal/procurement | Are licenses, vendors, fonts, images, accessibility exposure, and data terms reviewed? |
| Finance | Are hosting, monitoring, third-party tools, build minutes, and scaling costs visible and acceptable? |
| Management | Are risks, owners, timeline, launch readiness, and post-launch obligations explicit? |

### Completion Roadmap Summary

| Stage | Phases | Output |
|---|---|---|
| Strategy | 0-3 | Business case, scope, architecture, governance, ownership, delivery plan |
| Foundation | 4-7 | Working app foundation, design system, shell, routing, API/auth/state layer |
| Product delivery | 8-9 | Complete feature slices with forms, permissions, edge states, and tests |
| Hardening | 10-13 | Security, privacy, accessibility, performance, reliability, and automated quality gates |
| Scale architecture | 14 | Microfrontend governance and runtime readiness when applicable |
| Production readiness | 15-16 | Observability, analytics, support, deployment, rollback, and go-live |
| Operations | 17-18 | Stabilization, learning, maintenance, upgrades, and long-term ownership |

## Done Criteria

| Area | Done means |
|---|---|
| Product | Critical flows are documented, tested, and approved |
| Architecture | A new developer can find where routes, API calls, state, and components belong |
| Security | No high/critical known vulnerabilities; no secrets in bundle; dangerous HTML paths reviewed |
| Performance | Core Web Vitals and bundle budgets have measured targets |
| Testing | CI blocks regressions in critical flows |
| Accessibility | Keyboard and screen-reader basics pass for critical workflows |
| Deployment | Production deploys are repeatable, observable, and reversible |
| Observability | Errors can be tied to release, route, browser, and user/session where privacy allows |
| Maintenance | Dependency upgrades and framework upgrades have an owner and cadence |
| Support | Real production user issues can be reproduced or diagnosed from logs/telemetry |
| Microfrontends | Shell and remotes have owners, contracts, compatibility tests, fallback behavior, versioned deploys, rollback, and remote-level telemetry |

## Source References

- Angular build docs: https://angular.dev/tools/cli/build
- Angular performance docs: https://angular.dev/best-practices/performance
- Angular security docs: https://angular.dev/best-practices/security
- Angular service worker devops docs: https://angular.dev/ecosystem/service-workers/devops
- React app creation docs: https://react.dev/learn/creating-a-react-app
- React installation docs: https://react.dev/learn/installation
- React Profiler docs: https://react.dev/reference/react/Profiler
- React Compiler docs: https://react.dev/learn/react-compiler/introduction
- Vue production deployment docs: https://vuejs.org/guide/best-practices/production-deployment.html
- Vue performance docs: https://vuejs.org/guide/best-practices/performance
- Vue security docs: https://vuejs.org/guide/best-practices/security
- Vue testing docs: https://vuejs.org/guide/scaling-up/testing.html
- webpack Module Federation concepts: https://webpack.js.org/concepts/module-federation/
- webpack ModuleFederationPlugin docs: https://webpack.js.org/plugins/module-federation-plugin/
- single-spa getting started docs: https://single-spa.js.org/docs/getting-started-overview/
- single-spa microfrontend types docs: https://single-spa.js.org/docs/module-types/
- MDN Web Components docs: https://developer.mozilla.org/en-US/docs/Web/API/Web_components
- MDN custom elements docs: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements
