# 06a — FASTAPI, FROM ZERO

> **Read `06-python.md` first.** This file assumes you know decorators, async, and type hints.
>
> Same format throughout:
> **What** → **Code** → **Why** → **Say** → **Hook** → ⚠️ **Trap**
>
> **Your angle in this interview:** FastAPI is **ASP.NET Core Minimal API**. Say that early.
> It makes every answer land with a .NET interviewer.

**30 minutes?** Part 0 → Part 3 → Part 12.

---

# 📑 MAP

| Part | Topic |
|---|---|
| 0 | The 12 answers that win |
| 1 | What FastAPI is |
| 2 | Your first API |
| 3 | Where data comes from: path, query, body, header |
| 4 | Pydantic — the heart of it |
| 5 | Response models and status codes |
| 6 | Dependency injection |
| 7 | Errors |
| 8 | Async vs sync — **the one that gets you caught** |
| 9 | Middleware, CORS, lifespan |
| 10 | Auth: JWT and OAuth2 |
| 11 | Databases |
| 12 | Background work, WebSockets, streaming |
| 13 | Testing |
| 14 | Structure, config, deployment |
| 15 | Performance |
| 16 | FastAPI vs Django vs Flask vs ASP.NET |
| 17 | 80 rapid-fire questions |

---

# EASY MEMORY NOTES

Read this first. Start with the short phrase. Say the simple line. Add the last column only if they
ask for more.

| Remember | Say it simply | If they ask more |
|---|---|---|
| **Python Minimal API** | FastAPI is like ASP.NET Core Minimal API in Python. | It uses Starlette for web and Pydantic for data. |
| **Types make docs** | Type hints become validation and API docs. | FastAPI creates OpenAPI and Swagger automatically. |
| **Do not block async** | An `async def` route must not call blocking code. | Use true async libraries or make the route plain `def`. |
| **Depends = DI** | `Depends()` gives a route what it needs. | Use it for DB sessions, settings, and current user. |
| **Response model protects output** | The response model decides what leaves the API. | It stops fields like password hashes leaking. |
| **Auth as dependency** | Check the token before the route runs. | Decode JWT, check expiry and issuer, then load the user. |
| **Stream big output** | Do not build huge files in memory. | Return a stream/generator instead. |
| **Use workers** | Run several server processes in production. | One process per core is common because of the GIL. |

---

# PART 0 — THE 12 ANSWERS THAT WIN

| # | Question | Full answer in simple words |
|---|---|---|
| 1 | **What is FastAPI?** | "FastAPI is a Python framework for building APIs. It feels close to ASP.NET Core Minimal API: routes are functions, type hints describe inputs, and the framework handles validation and docs." |
| 2 | **Why is it fast?** | "FastAPI sits on async web plumbing, so it handles many waiting requests well. Pydantic validation is also fast. It is fast for Python, but ASP.NET Core is still faster for raw throughput." |
| 3 | **What does Pydantic do?** | "Pydantic checks incoming data, converts it where safe, and gives me a typed Python object. It is like model binding plus validation." |
| 4 | **The biggest trap?** | "Do not put blocking code inside an `async def` route. One blocking database or HTTP call can freeze the event loop. Use true async libraries or make the route plain `def`." |
| 5 | **`def` vs `async def` route?** | "`async def` runs on the event loop, so everything inside should be awaitable. Plain `def` runs in a thread pool, which is safer for blocking libraries." |
| 6 | **Dependency injection?** | "`Depends()` gives routes the things they need: DB sessions, settings, current user, permissions. It is also easy to override in tests." |
| 7 | **Docs?** | "FastAPI creates OpenAPI automatically from routes and type hints. `/docs` gives Swagger UI, and `/openapi.json` gives the contract." |
| 8 | **Auth?** | "I usually check auth in a dependency. It reads the bearer token, validates the JWT, checks expiry and issuer, and loads the current user before the route body runs." |
| 9 | **How do you run it?** | "In production I run multiple Uvicorn workers, usually behind Nginx or another reverse proxy. Multiple processes matter because Python has the GIL." |
| 10 | **Response model?** | "The response model is the output contract. It filters what leaves the API, so fields like password hashes do not leak from ORM objects." |
| 11 | **Background jobs?** | "`BackgroundTasks` is fine for small after-response work, like sending a simple email. For important work that must survive restarts, use a real queue like Celery, RQ, or ARQ." |
| 12 | **vs Django?** | "FastAPI is best for focused APIs and async services. Django is best when I want a full product stack: ORM, admin, auth, migrations, forms, and templates." |

---

# PART 1 — WHAT FASTAPI IS

## 1.1 The stack under it

```
Your code
   ↓
FastAPI       ← routing, validation, DI, OpenAPI
   ↓
Starlette     ← the actual ASGI web framework: routing, middleware, WebSockets
   ↓
Uvicorn       ← the ASGI server (built on uvloop + httptools)
   ↓
ASGI          ← the async protocol between server and app
```

Plus **Pydantic** for validation, which isn't in the chain — it's used at the edges.

**Say:** *"FastAPI is a thin, opinionated layer over Starlette for the web parts and Pydantic for the data parts. That's why it's small: it composes two mature libraries rather than reimplementing them."*

---

## 1.2 WSGI vs ASGI — know this

| | WSGI | ASGI |
|---|---|---|
| Style | synchronous | **asynchronous** |
| One worker handles | one request at a time | thousands concurrently |
| WebSockets | no | yes |
| Used by | Flask, Django (classic) | FastAPI, Starlette, Django (modern) |
| Servers | Gunicorn, uWSGI | **Uvicorn**, Hypercorn, Daphne |

**Say:** *"WSGI is one request per worker thread — the whole model is blocking. ASGI is an async protocol, so one process handles thousands of concurrent connections while they wait on I/O, and it supports WebSockets and long-lived connections."*

**Hook:** **WSGI = blocking. ASGI = async + WebSockets.**

---

## 1.3 Why it's fast — three reasons

1. **ASGI + uvloop.** Async I/O all the way down. uvloop is libuv, the same event loop as Node.
2. **Pydantic v2 core is Rust.** Validation is 5–50× faster than v1.
3. **No ORM, no template engine, no admin.** Nothing you don't ask for.

⚠️ **Be honest about "fast":** *"It's fast for a Python framework — comparable to Node. ASP.NET Core is still meaningfully faster on raw throughput. What FastAPI buys you is developer speed and the Python data ecosystem."*

That honesty scores points in a .NET room.

---

# PART 2 — YOUR FIRST API

```python
from fastapi import FastAPI

app = FastAPI(title="Trading API", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}
```

```bash
uvicorn main:app --reload        # main = the file, app = the variable
```

Now open:
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs` ← **interactive Swagger UI, free**
- `http://127.0.0.1:8000/openapi.json`

**Line by line:**
- `@app.get("/health")` — a decorator registering a route. Same as `[HttpGet("/health")]`.
- returning a dict — FastAPI serialises it to JSON automatically.
- `--reload` — dev only. Never in production.

**Say:** *"Routes are decorators, the return value is serialised automatically, and OpenAPI docs come from the type hints with no annotations or XML comments. That last part is the real difference from ASP.NET."*

---

# PART 3 — WHERE DATA COMES FROM

**The rule FastAPI uses to decide.** Given a parameter, it asks:

| Condition | It's read from |
|---|---|
| The name appears in the path string | **the path** |
| It's a simple type (int, str, bool, float) and not in the path | **the query string** |
| It's a Pydantic model | **the JSON body** |
| It's declared `Header()`, `Cookie()`, `Form()`, `File()` | that source |
| It's declared `Depends()` | dependency injection |

```python
from fastapi import FastAPI, Query, Path, Header, Body
from pydantic import BaseModel

class OrderIn(BaseModel):
    symbol: str
    qty: int
    price: float

@app.post("/accounts/{account_id}/orders")
def create_order(
    account_id: int = Path(..., gt=0),                  # from the PATH
    dry_run: bool = Query(False),                       # from the QUERY string
    order: OrderIn = Body(...),                         # from the JSON BODY
    x_request_id: str | None = Header(None),            # from a HEADER
):
    ...
```

⚠️ `x_request_id` maps to the header `X-Request-ID`. Underscores become hyphens automatically.

**Validation in the declaration:**
```python
q: str = Query(..., min_length=3, max_length=50, pattern="^[A-Z]+$")
page: int = Query(1, ge=1, le=1000, description="Page number")
```
`...` (Ellipsis) means **required**. Anything else is the default.

**Say:** *"FastAPI infers the source from the type. Simple types are query params, Pydantic models are the body, and path names match the route. The constraints live in the signature, so the validation and the documentation can't drift apart."*

**Hook:** **Simple type → query. Model → body. Named in path → path.**

**Modern style (3.9+), preferred:**
```python
from typing import Annotated
def f(q: Annotated[str, Query(min_length=3)] = "x"): ...
```

---

# PART 4 — PYDANTIC ⭐

**This is the heart of FastAPI. Most FastAPI questions are really Pydantic questions.**

## 4.1 A model

```python
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from decimal import Decimal
from datetime import datetime

class OrderIn(BaseModel):
    model_config = ConfigDict(extra="forbid")      # ⭐ reject unknown fields

    symbol: str = Field(..., min_length=1, max_length=6)
    qty: int = Field(..., gt=0, description="Number of shares")
    price: Decimal = Field(..., gt=0, decimal_places=4)
    side: Literal["BUY", "SELL"]
    placed_at: datetime | None = None

    @field_validator("symbol")
    @classmethod
    def upper(cls, v: str) -> str:
        return v.upper()

    @model_validator(mode="after")
    def check_notional(self):
        if self.qty * self.price > 10_000_000:
            raise ValueError("notional exceeds limit")
        return self
```

**What you get for free:**
- Wrong type → 422 with a precise error path.
- `"10"` → `10` for an int field (coercion).
- Unknown field → rejected, because of `extra="forbid"`.
- The whole thing documented in OpenAPI.

**Say:** *"Pydantic parses and validates at the boundary, and gives me a typed object inside. Unlike plain type hints — which are erased — Pydantic actually enforces them at runtime, because it reads the same annotations and builds a validator from them."*

**Hook:** **Hints are erased. Pydantic enforces.**

---

## 4.2 v1 vs v2 — worth one sentence

| | v1 | v2 |
|---|---|---|
| Core | Python | **Rust (`pydantic-core`)** |
| Speed | baseline | **5–50× faster** |
| `@validator` | old | `@field_validator` |
| `.dict()` / `.json()` | old | `.model_dump()` / `.model_dump_json()` |
| `class Config` | old | `model_config = ConfigDict(...)` |
| `orm_mode` | old | `from_attributes=True` |

**Say:** *"v2 moved the validation core to Rust — same API shape, order-of-magnitude faster. The migration is mostly renames: `validator` to `field_validator`, `.dict()` to `.model_dump()`."*

---

## 4.3 Settings from the environment

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    log_level: str = "INFO"
    model_config = ConfigDict(env_file=".env")

settings = Settings()      # reads env vars, validates, fails fast at startup
```

**Say:** *"Config is a validated Pydantic model, so a missing or malformed environment variable kills the process at startup instead of at 3am on a code path nobody tested."*

**Hook:** **Fail fast at boot, not at runtime.**

---

# PART 5 — RESPONSE MODELS AND STATUS CODES

```python
from fastapi import status

class OrderOut(BaseModel):
    id: int
    symbol: str
    status: str
    # note: no internal fields, no user_id, no audit columns

@app.post("/orders",
          response_model=OrderOut,
          status_code=status.HTTP_201_CREATED)
def create(order: OrderIn) -> OrderOut:
    saved = repo.save(order)     # this may have 30 fields
    return saved                 # only OrderOut fields go out ⭐
```

**Why it matters — say this exactly:**
> *"The response model is a filter, not just documentation. If I return the ORM object directly, every column leaks — password hashes, internal flags, other tenants' identifiers. Separate `In` and `Out` models mean the API contract is explicit and a new database column can't accidentally become a public field."*

**Hook:** **Separate In and Out models. Columns aren't a contract.**

**Useful options:**
```python
response_model_exclude_none=True
response_model_exclude={"internal_id"}
```

**Status codes to know:**

| Code | Meaning |
|---|---|
| 200 | OK |
| 201 | Created — return the resource + `Location` |
| 202 | Accepted — queued, not done |
| 204 | No Content — for DELETE |
| 400 | Bad request (your explicit business rejection) |
| 401 | Not authenticated |
| 403 | Authenticated but not allowed |
| 404 | Not found |
| 409 | Conflict — duplicate, or optimistic-concurrency failure |
| 422 | **Validation failed** ← FastAPI's default for bad input |
| 429 | Rate limited |
| 500 | Your bug |
| 503 | Dependency down |

⚠️ **Trap: "Why 422 and not 400?"** → *"422 Unprocessable Entity means the syntax was valid JSON but the semantics failed validation. FastAPI uses it for Pydantic failures so you can distinguish malformed requests from rejected ones. You can override the handler to return 400 if your API standard requires it."*

---

# PART 6 — DEPENDENCY INJECTION ⭐

## 6.1 The idea

**What.** A function that FastAPI calls for you, injecting the result into your route.

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db              # ⭐ everything after yield runs AFTER the response
    finally:
        db.close()

@app.get("/orders")
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()
```

**Say:** *"`Depends` is dependency injection at the parameter level. A generator dependency gives me setup and teardown — the code after `yield` runs when the request finishes, so sessions and transactions always close. It's the same role as scoped services in ASP.NET Core DI."*

**Hook:** **`yield` = setup, then teardown after the response.**

---

## 6.2 Dependencies chain

```python
def get_token(authorization: str = Header(...)) -> str: ...
def get_current_user(token: str = Depends(get_token),
                     db: Session = Depends(get_db)) -> User: ...
def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(403, "admin only")
    return user

@app.delete("/orders/{id}")
def cancel(id: int, admin: User = Depends(require_admin)): ...
```

**Caching:** within one request, each dependency runs **once**, even if requested five times.
Turn it off with `Depends(f, use_cache=False)`.

**Router-level and app-level:**
```python
router = APIRouter(dependencies=[Depends(require_admin)])   # applies to every route
app = FastAPI(dependencies=[Depends(verify_api_key)])       # applies globally
```
Use the list form when you want the side effect (a check) but not the value.

---

## 6.3 Why interviewers love this: testing

```python
app.dependency_overrides[get_db] = lambda: test_session
```

**Say:** *"Dependency overrides are why the DI matters. In tests I swap the real database session or the auth dependency for a fake with one line, and no production code changes. That's the whole argument for DI, made concrete."*

**Hook:** **Override in tests. One line.**

---

# PART 7 — ERRORS

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Order not found")
raise HTTPException(404, "Not found", headers={"X-Error": "missing"})
```

**A global handler for your domain exceptions — this is the senior answer:**
```python
class InsufficientMargin(Exception):
    def __init__(self, required, available):
        self.required, self.available = required, available

@app.exception_handler(InsufficientMargin)
async def margin_handler(request: Request, exc: InsufficientMargin):
    return JSONResponse(
        status_code=409,
        content={"error": "insufficient_margin",
                 "required": str(exc.required),
                 "available": str(exc.available)},
    )
```

**Say:** *"Domain code raises domain exceptions and knows nothing about HTTP. A handler at the edge maps them to status codes. That keeps the business layer transport-agnostic — the same rule works whether it's called by HTTP, a queue consumer or a batch job."*

**Hook:** **Domain raises. The edge maps to HTTP.**

⚠️ Mention **RFC 7807 / RFC 9457 Problem Details** — a standard JSON error shape
(`type`, `title`, `status`, `detail`, `instance`). ASP.NET Core does this by default, so
naming it lands well.

---

# PART 8 — ASYNC VS SYNC ⭐⭐ THE ONE THAT CATCHES PEOPLE

## 8.1 The rule

| You write | FastAPI does |
|---|---|
| `async def` | runs it **on the event loop** |
| `def` | runs it **in a threadpool** (40 threads by default) |

**So:**
- `async def` + blocking call → **the whole server stalls**. Every request. ❌
- `def` + blocking call → fine. It's on a worker thread. ✅
- `async def` + all-await → best throughput. ✅

```python
@app.get("/bad")
async def bad():
    time.sleep(5)                 # ❌ freezes EVERY request for 5 seconds
    requests.get(url)             # ❌ same
    db.query(...)                 # ❌ sync SQLAlchemy — same

@app.get("/ok")
def ok():
    time.sleep(5)                 # ✅ threadpool. Only this request waits

@app.get("/best")
async def best():
    await asyncio.sleep(5)        # ✅
    await httpx_client.get(url)   # ✅
    await session.execute(stmt)   # ✅ async SQLAlchemy
```

**Say this whole thing — it's the money answer:**
> *"FastAPI runs `async def` routes on the event loop and plain `def` routes in a threadpool. So the dangerous combination is `async def` with blocking code inside — one slow call blocks every concurrent request, because it's a single thread. My rule: if everything in the handler is awaitable, use `async def`. If I'm calling a blocking driver, either declare the route `def` and let the threadpool handle it, or wrap the call in `asyncio.to_thread`. And I don't mix — a sync database driver inside an async route is the most common production incident I've seen in this stack."*

**Hook:** **Async route = everything must be awaitable. Otherwise use `def`.**

---

## 8.2 The async library swap

| Blocking | Async |
|---|---|
| `requests` | **`httpx`** (or `aiohttp`) |
| `psycopg2` | **`asyncpg`** |
| SQLAlchemy sync | `AsyncSession` + `create_async_engine` |
| `redis-py` sync | `redis.asyncio` |
| `open()` | `aiofiles` |
| `time.sleep` | `asyncio.sleep` |
| pymongo | `motor` |

---

# PART 9 — MIDDLEWARE, CORS, LIFESPAN

## 9.1 Middleware

Runs on every request, wrapping the whole pipeline.

```python
@app.middleware("http")
async def add_timing(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}"
    response.headers["X-Request-ID"] = request_id
    return response
```

**Use it for:** correlation IDs, timing, structured access logs, security headers, rate limits.
**Don't use it for:** anything needing route-specific knowledge — that's a dependency.

**Say:** *"Middleware is the ASP.NET Core request pipeline — same shape, `call_next` instead of `next(context)`. I use it for cross-cutting infrastructure: correlation ID, timing, logging. Anything route-specific goes in a dependency instead."*

---

## 9.2 CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],   # ⚠️ never ["*"] with credentials
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Say:** *"CORS is a browser rule, not a server security control. It stops another site's JavaScript reading my responses. It does nothing against a direct HTTP call — so it's never a substitute for authentication."*

**Hook:** **CORS protects the browser, not the server.**

---

## 9.3 Lifespan — startup and shutdown

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(dsn)     # startup
    app.state.http = httpx.AsyncClient()
    yield
    await app.state.pool.close()                        # shutdown
    await app.state.http.aclose()

app = FastAPI(lifespan=lifespan)
```

**Say:** *"Lifespan replaces the old `@app.on_event` hooks. Connection pools and HTTP clients get created once at startup and closed cleanly on shutdown. Creating an `httpx.AsyncClient` per request is a classic performance bug — you lose connection pooling and eventually exhaust sockets."*

**Hook:** **One pool, one client, per process.**

---

# PART 10 — AUTH

## 10.1 JWT, end to end

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form.username)
    if not user or not pwd.verify(form.password, user.hashed_password):
        raise HTTPException(401, "Bad credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    token = jwt.encode(
        {"sub": str(user.id), "scopes": user.scopes,
         "exp": datetime.now(timezone.utc) + timedelta(minutes=15)},
        SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

def current_user(token: str = Depends(oauth2)) -> User:
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(401, "Invalid token")
    return load_user(payload["sub"])

@app.get("/me")
def me(user: User = Depends(current_user)):
    return user
```

## 10.2 The points to make

| Point | Say |
|---|---|
| **Hashing** | "bcrypt or argon2 with a per-user salt. Never a plain SHA — it's too fast to brute-force" |
| **Token lifetime** | "Access token 15 minutes, refresh token days, rotated on use" |
| **Revocation** | ⭐ "JWTs are stateless, so they can't be revoked. That's the real trade-off. I keep them short-lived and hold a `jti` denylist in Redis for forced logout" |
| **Storage** | "httpOnly, Secure, SameSite cookie beats localStorage — localStorage is readable by any XSS" |
| **Algorithm** | "Pin the algorithm on decode. Accepting `alg` from the token header is the classic `alg: none` attack" |
| **Asymmetric** | "RS256 when several services verify but only one issues — they get the public key, not the secret" |
| **Scopes** | "FastAPI has `SecurityScopes` for per-endpoint scope checks" |

**Say:** *"The honest trade-off with JWT is revocation. It's stateless, so a valid token stays valid until it expires. I mitigate with short lifetimes, refresh rotation, and a `jti` denylist in Redis for forced logout — which reintroduces some state, but only on the revocation path."*

**Hook:** **JWT's cost is revocation. Short life + denylist.**

⚠️ **Trap: "Session cookie or JWT?"** → *"Sessions if it's one server-rendered app — revocation is free and the server holds the state. JWT when several services must verify without a shared session store. I wouldn't use JWT just because it's fashionable."*

---

# PART 11 — DATABASES

## 11.1 The async pattern

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(DSN, pool_size=20, max_overflow=10, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/orders")
async def list_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.active))
    return result.scalars().all()
```

**Full ORM detail is in `06c-orm-databases.md`.** Here, know these four:

| Setting | Why |
|---|---|
| `pool_pre_ping=True` | tests the connection before use — survives DB restarts and idle timeouts |
| `expire_on_commit=False` | ⭐ otherwise attributes reload after commit and lazy-load outside the session |
| `pool_size` | must fit `workers × pool_size` under the DB's max connections |
| `selectinload` / `joinedload` | avoids the N+1 query |

⚠️ **Trap: "Async DB in FastAPI — anything to watch?"** → *"Two things. The session is not concurrency-safe, so one session per request, never shared between tasks. And connection maths: with four Uvicorn workers and a pool of twenty, that's eighty connections before overflow — that has to fit Postgres's limit, or you need PgBouncer."*

---

# PART 12 — BACKGROUND WORK, WEBSOCKETS, STREAMING

## 12.1 BackgroundTasks

```python
from fastapi import BackgroundTasks

@app.post("/orders")
def create(order: OrderIn, bg: BackgroundTasks):
    saved = repo.save(order)
    bg.add_task(send_confirmation_email, saved.id)    # runs AFTER the response
    return saved
```

⚠️ **Say the limit:** *"`BackgroundTasks` runs in the same process, after the response. If the process dies, the task is gone. It's for cheap best-effort work — sending an email, writing an audit line. Anything that must not be lost goes on a real queue: Celery, ARQ, or a broker like RabbitMQ."*

**Hook:** **BackgroundTasks = best effort. Celery = guaranteed.**

## 12.2 WebSockets — the real-time answer

```python
@app.websocket("/ws/prices")
async def prices(ws: WebSocket):
    await ws.accept()
    try:
        async for tick in market_feed():
            await ws.send_json({"symbol": tick.symbol, "price": str(tick.price)})
    except WebSocketDisconnect:
        cleanup()
```

**Say:** *"For a live prices feed I'd use WebSockets, and at scale I'd put Redis pub/sub behind them so any worker can fan out to any connected client. Server-Sent Events are the simpler option if it's one-directional — they're plain HTTP and reconnect automatically."*

**Hook:** **WebSocket = two-way. SSE = one-way and simpler.**

⚠️ **Say the backpressure point — it separates seniors:** *"With a fast feed and a slow client you have to decide: buffer, drop, or conflate. For prices I conflate — keep only the latest tick per symbol and send on a timer. An unbounded queue per client is how you run out of memory."*

## 12.3 Streaming a large response

```python
from fastapi.responses import StreamingResponse

@app.get("/export")
def export():
    def rows():
        for r in query_millions():
            yield f"{r.id},{r.symbol}\n"
    return StreamingResponse(rows(), media_type="text/csv")
```

**Say:** *"Streaming keeps memory constant on a large export — the generator from Part 7 of the Python file, applied to HTTP."*

---

# PART 13 — TESTING

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_order():
    r = client.post("/orders", json={"symbol": "VOD", "qty": 10, "price": 1.5})
    assert r.status_code == 201
    assert r.json()["symbol"] == "VOD"

def test_validation():
    r = client.post("/orders", json={"symbol": "VOD", "qty": -1, "price": 1.5})
    assert r.status_code == 422

# async version
import pytest, httpx
@pytest.mark.asyncio
async def test_async():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://t") as c:
        r = await c.get("/health")
    assert r.status_code == 200

# swap the database
app.dependency_overrides[get_db] = lambda: test_session
```

**Say:** *"`TestClient` exercises the real app in-process — no network, no server. Dependency overrides swap the database and the auth. I use testcontainers for a real Postgres in integration tests, because SQLite hides constraint and type differences that then fail in production."*

**Hook:** **TestClient + dependency_overrides. Real DB in integration.**

---

# PART 14 — STRUCTURE, CONFIG, DEPLOYMENT

## 14.1 Project layout

```
app/
  main.py              # FastAPI(), routers, middleware, lifespan
  core/
    config.py          # Pydantic Settings
    security.py        # hashing, JWT
  api/
    deps.py            # shared dependencies
    v1/
      orders.py        # APIRouter
      accounts.py
  models/              # ORM tables
  schemas/             # Pydantic In/Out models
  services/            # ⭐ business logic. No FastAPI imports here
  repositories/        # data access
  tests/
```

**Say:** *"Routers per resource, versioned under `/api/v1`. The important rule is that `services/` imports nothing from FastAPI — the business logic doesn't know it's behind HTTP. That's what makes it testable and reusable from a queue consumer or a batch job."*

**Hook:** **Services know nothing about HTTP.**

```python
from fastapi import APIRouter
router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/")
def list_orders(): ...

app.include_router(router, prefix="/api/v1")
```

## 14.2 Deployment

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "app.main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-w", "4", "-b", "0.0.0.0:8000"]
```

**The production checklist — rattle this off:**

| Item | Answer |
|---|---|
| Workers | `2 × cores + 1`, one process per core. GIL means processes, not threads |
| Reverse proxy | Nginx or a cloud LB. TLS, compression, static files |
| Health | `/health` liveness, `/ready` readiness (checks DB + broker) |
| Logging | JSON to stdout, correlation ID, no PII |
| Metrics | `prometheus-fastapi-instrumentator`; OpenTelemetry for traces |
| Secrets | env vars or Key Vault. Never in the image |
| Migrations | Alembic, run as a job **before** the rollout, never at startup |
| `--reload` | dev only |
| Docs | disable `/docs` in production if the API is internal |

**Say:** *"Uvicorn workers under Gunicorn, one per core, behind Nginx. Migrations run as a separate job before the deployment, not on app startup — otherwise four workers race to migrate the same database."*

**Hook:** **Migrate before the rollout, not at startup.**

---

# PART 15 — PERFORMANCE

| Problem | Fix |
|---|---|
| Blocking call in `async def` | ⭐ the number one cause. Make it async or use `def` |
| `httpx.AsyncClient()` per request | create once in lifespan |
| N+1 queries | `selectinload` / `joinedload` |
| Serialising huge payloads | paginate; `orjson` via `ORJSONResponse` |
| Repeated identical reads | Redis, or `functools.cache` for static data |
| Slow validation | Pydantic v2; avoid deep nested models on hot paths |
| CPU work in a route | push to a process pool or a queue |
| One worker | more workers — one per core |

```python
from fastapi.responses import ORJSONResponse
app = FastAPI(default_response_class=ORJSONResponse)     # faster JSON
```

**Say:** *"I'd profile before guessing, but in FastAPI the first thing I check is whether a blocking call is sitting inside an `async def` route. That single mistake accounts for most 'FastAPI is slow' reports."*

---

# PART 16 — FASTAPI vs DJANGO vs FLASK vs ASP.NET

| | **FastAPI** | **Django** | **Flask** | **ASP.NET Core** |
|---|---|---|---|---|
| Style | async API framework | many features included | minimal | many features included |
| Protocol | ASGI | WSGI + ASGI | WSGI | Kestrel |
| ORM | none (bring SQLAlchemy) | **built in** | none | EF Core |
| Admin UI | no | **yes** ⭐ | no | no |
| Auth | build it | **built in** | extension | Identity |
| Migrations | Alembic | **built in** | Alembic | EF Migrations |
| Validation | **Pydantic** ⭐ | forms/serializers | manual | DataAnnotations |
| Docs | **automatic** ⭐ | DRF add-on | extension | Swashbuckle |
| Async DB | yes | improving | no | yes |
| Best for | microservices, ML serving, real-time | full products with a back office | small services | enterprise .NET |

**The answer to "which would you pick?":**
> *"It's about how much of the product is not the API. If I need an admin back office, user management, a CMS and migrations on day one, Django saves months. If it's a service exposing an API — especially one serving models or handling real-time streams — FastAPI, because it's async-first and the validation and docs come from the same type hints. For this kind of stack I'd put the transactional core in .NET and use FastAPI for the Python analytics services, behind a versioned contract."*

**Hook:** **API only → FastAPI. Whole product → Django.**

---

# PART 17 — RAPID-FIRE: 80 QUESTIONS

| # | Q | A |
|---|---|---|
| 1 | What is FastAPI? | Async Python API framework on Starlette + Pydantic |
| 2 | Built on? | Starlette (web) + Pydantic (data) |
| 3 | Server? | Uvicorn (ASGI) |
| 4 | WSGI vs ASGI? | Blocking vs async + WebSockets |
| 5 | Why fast? | ASGI, uvloop, Rust Pydantic core |
| 6 | Docs URL? | `/docs`, `/redoc`, `/openapi.json` |
| 7 | Docs generated from? | Type hints |
| 8 | .NET equivalent? | ASP.NET Core Minimal API |
| 9 | Define a route? | `@app.get("/path")` |
| 10 | Query param? | Simple type not in the path |
| 11 | Path param? | Name matches the route |
| 12 | Body? | A Pydantic model parameter |
| 13 | Header param? | `Header(None)` |
| 14 | Required marker? | `...` (Ellipsis) |
| 15 | Underscores in headers? | Become hyphens |
| 16 | Validation failure code? | 422 |
| 17 | Why 422 not 400? | Valid syntax, failed semantics |
| 18 | What does Pydantic do? | Parse, validate, coerce at runtime |
| 19 | Are type hints enforced? | Not by Python. Pydantic enforces |
| 20 | Reject unknown fields? | `extra="forbid"` |
| 21 | Field constraints? | `Field(gt=0, max_length=6)` |
| 22 | Custom field check? | `@field_validator` |
| 23 | Cross-field check? | `@model_validator(mode="after")` |
| 24 | Pydantic v2 change? | Rust core, 5–50× faster |
| 25 | v1 `.dict()` → v2? | `.model_dump()` |
| 26 | v1 `@validator` → v2? | `@field_validator` |
| 27 | Config from env? | `BaseSettings` |
| 28 | Why validate config? | Fail fast at startup |
| 29 | `response_model` does? | Filters the output |
| 30 | Why separate In/Out models? | Stops internal fields leaking |
| 31 | 201 means? | Created |
| 32 | 204? | No content |
| 33 | 401 vs 403? | Not authenticated vs not allowed |
| 34 | 409? | Conflict / duplicate |
| 35 | DI keyword? | `Depends()` |
| 36 | Dependency with teardown? | `yield` |
| 37 | When does teardown run? | After the response |
| 38 | Cached per request? | Yes |
| 39 | Disable caching? | `use_cache=False` |
| 40 | Apply DI to all routes? | Router/app `dependencies=[...]` |
| 41 | Swap a dependency in tests? | `app.dependency_overrides` |
| 42 | Raise an HTTP error? | `HTTPException(404, "...")` |
| 43 | Map a domain error? | `@app.exception_handler` |
| 44 | Standard error format? | RFC 9457 Problem Details |
| 45 | `async def` route runs where? | The event loop |
| 46 | `def` route runs where? | A threadpool |
| 47 | Worst mistake? | Blocking call inside `async def` |
| 48 | Effect? | Freezes every concurrent request |
| 49 | Fix? | Async library, `def` route, or `to_thread` |
| 50 | `requests` replacement? | `httpx` |
| 51 | `psycopg2` replacement? | `asyncpg` |
| 52 | `time.sleep` replacement? | `asyncio.sleep` |
| 53 | Middleware for? | Correlation ID, timing, logging |
| 54 | Middleware signature? | `(request, call_next)` |
| 55 | CORS protects? | The browser, not the server |
| 56 | `allow_origins=["*"]` risk? | Illegal with credentials |
| 57 | Startup/shutdown hook? | `lifespan` |
| 58 | Create the HTTP client where? | Lifespan, once |
| 59 | Per-request client cost? | No pooling, socket exhaustion |
| 60 | Auth scheme? | OAuth2 password flow + JWT bearer |
| 61 | Hash passwords with? | bcrypt or argon2 |
| 62 | JWT weakness? | Can't be revoked |
| 63 | Mitigation? | Short expiry + `jti` denylist |
| 64 | Access token life? | ~15 minutes |
| 65 | `alg: none` attack? | Always pin the algorithm on decode |
| 66 | RS256 when? | Many verifiers, one issuer |
| 67 | Token storage? | httpOnly Secure SameSite cookie |
| 68 | Session vs JWT? | One app vs many services |
| 69 | Background work? | `BackgroundTasks` |
| 70 | Its limitation? | Lost if the process dies |
| 71 | Guaranteed jobs? | Celery / ARQ |
| 72 | Real-time push? | WebSockets, or SSE one-way |
| 73 | Fan out across workers? | Redis pub/sub |
| 74 | Slow client on a fast feed? | Conflate — latest value per symbol |
| 75 | Huge export? | `StreamingResponse` + generator |
| 76 | Test tool? | `TestClient` |
| 77 | Group routes? | `APIRouter` |
| 78 | Worker count? | ~one per core |
| 79 | Run migrations when? | A job before rollout |
| 80 | FastAPI vs Django? | API-only vs whole product |

---

## ✅ Before you close this file

- [ ] Say the **Part 0** table, all 12
- [ ] Say the **Part 8** async/sync answer word for word — it's the one they probe
- [ ] Explain **`response_model`** and why In/Out models are separate
- [ ] Explain **JWT revocation** and your mitigation
- [ ] Run the **Part 17** rapid-fire, target 65/80

**Then go to `06b-django.md`.**
