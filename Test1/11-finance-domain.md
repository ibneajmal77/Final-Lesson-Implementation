# 11 — Capital Markets Domain Crash Course

> JD nice-to-haves: **Portfolio / Order / Execution Management Systems**, **financial mathematics**,
> **financial optimization**, columnar DBs. Industry tag: **BCM (Banking & Capital Markets)**.
>
> **Monday (Luxoft technical):** you need enough to show genuine interest and follow the conversation.
> **Stage 3 (client):** you need this file cold. Read it twice; it's the highest-leverage
> non-code file in the pack.

---

## 1. The 10-line map of the industry

- **Sell-side** = banks and brokers. They make markets, execute orders, provide research.
- **Buy-side** = asset managers, hedge funds, pension funds, **sovereign wealth funds** — they *own*
  the money and buy investments. **Abu Dhabi + portfolio management ⇒ almost certainly buy-side.**
- **Front office** = portfolio managers, traders, analysts (they make money).
  **Middle office** = risk, compliance, performance. **Back office** = settlement, accounting,
  reconciliation, reporting.
- Your app almost certainly sits **front-to-middle office**: a WPF desktop for PMs/traders, a Python
  analytics layer, and services keeping positions, orders and risk correct.
- **Custodian** = the bank that actually holds the assets. **Broker** = who executes your trade.
  **Prime broker** = broker + financing + custody for funds.
- The daily rhythm: **pre-trade** (idea, compliance check) → **trade** (order → execution) →
  **post-trade** (confirm, allocate, settle, reconcile) → **valuation & reporting** (NAV, P&L, risk).

---

## 2. Instruments — one line each (know these names)

| Asset class | What it is | Tech implication |
|---|---|---|
| **Equity** | Share of a company | Simple, high volume, corporate actions |
| **Fixed income / bonds** | A loan; pays coupons, has maturity | Price ↔ yield maths, accrued interest, day-count conventions |
| **FX** | Currency pairs, spot and forward | Multi-currency everything; base vs local currency |
| **Money market / cash** | Deposits, T-bills | |
| **Derivatives** — futures, options, swaps | Value *derived* from an underlying | Pricing models, Greeks, margin, notional ≠ market value |
| **Funds / ETFs** | Pooled vehicles | Look-through to holdings |
| **Private markets / real assets** | Illiquid, valued periodically | No live price → stale/manual valuation handling |

**Terms you must not blink at:** ticker/symbol, **ISIN / CUSIP / SEDOL / FIGI** (instrument
identifiers — the "primary key" problem of finance, and **instrument reference data / mastering is a
genuinely hard engineering problem** worth mentioning), bid/ask/mid, spread, last traded price,
volume, market cap, notional, par value, coupon, maturity, yield, duration, dividend, corporate
action (split, merger, dividend — these **retroactively change history**, which is a beautiful
data-engineering problem to raise).

---

## 3. The order lifecycle — learn this properly, it's the core

```
 Idea / model output
   → ORDER created (PM decides: buy 100,000 AAPL)
   → Pre-trade COMPLIANCE check (mandate limits, restricted list, concentration)
   → ORDER released to trader / OMS
   → ROUTED to a broker or venue  (this is where an EMS lives)
   → EXECUTION(S) come back — often many partial FILLS
   → ALLOCATION across funds/accounts (if a block order)
   → CONFIRMATION with the broker
   → SETTLEMENT (T+1 in the US since 2024; T+2 in much of the world)
   → POSITION and CASH updated; RECONCILED against custodian/broker records
```

**Order states (a state machine — see `08` §A3):**
`New → PendingNew → New(acked) → PartiallyFilled → Filled`
with side-branches `PendingCancel → Cancelled`, `PendingReplace → Replaced`, `Rejected`, `Expired`,
`DoneForDay`.

**Order types:** *market* (execute now, price uncertain), *limit* (price certain, execution
uncertain), *stop / stop-limit*, *market-on-close*, *iceberg*, *VWAP/TWAP/Implementation Shortfall*
(algorithmic execution). **Time in force:** DAY, GTC (good till cancelled), IOC (immediate or
cancel), FOK (fill or kill).

**Side:** Buy, Sell, Sell Short, Buy to Cover.

### 🔥 The engineering problems in this lifecycle (this is what you should talk about)
- **Partial fills**: an order of 100,000 may return 40 executions. Your position must be correct after
  every one, and they can arrive **out of order or duplicated**.
- **Cancel/replace race**: you send a cancel; a fill is already in flight. Who wins? The venue decides,
  and your system must handle "cancel rejected because already filled" gracefully.
- **Idempotency**: execution reports are re-sent on reconnect. **Dedupe on `ExecID`.** This is the
  purest real-world example of at-least-once delivery + idempotent consumers — *your* `08`/`09`
  material lands directly here.
- **Ordering**: sequence numbers per session; a gap means you must request a resend.
- **Audit**: every state transition must be reconstructable — *why did this order have this status at
  14:32:07.412?* **This is exactly why you used event sourcing at Calrom. Make that connection out
  loud; it's your single best domain bridge.**

---

## 4. OMS vs EMS vs PMS — get this distinction right

| System | Who uses it | Does |
|---|---|---|
| **PMS** (Portfolio Management System) | Portfolio manager | Holdings, cash, exposures, modelling, rebalancing, performance. *"What do I own and what should I own?"* |
| **OMS** (Order Management System) | PM + trader + compliance | Order creation, compliance checks, allocation, position keeping, lifecycle & audit. *"Manage the order end to end."* |
| **EMS** (Execution Management System) | Trader | Market connectivity, live market data, algos, smart order routing, low latency. *"Get it executed well."* |

Increasingly merged as **OEMS**. Vendor names to recognise: **Aladdin (BlackRock)**, Charles River,
SimCorp Dimension, Bloomberg AIM/EMSX/TOMS, Eze, Murex and Calypso (Luxoft has deep partnerships with
**Murex and Calypso** — worth knowing since Luxoft sells that expertise), FactSet, Enfusion.

> **If asked "what do you know about OMS?"**: *"An OMS is the system of record for the order lifecycle
> — creation, pre-trade compliance, routing, fills, allocation, and the audit trail — sitting between
> the portfolio manager's intent and the execution venue. The PMS answers 'what should the portfolio
> look like', the EMS is about getting the execution done well, and the OMS is the correctness and
> control layer in between. Engineering-wise it's a state machine over orders with strict
> idempotency, ordering and auditability requirements — which is the kind of system I've built, just
> in a different domain."*

---

## 5. FIX protocol — the lingua franca

**FIX (Financial Information eXchange)** is how orders and executions move between buy-side, brokers
and venues. Tag=value pairs separated by SOH (`\x01`), or FIXML/FAST/SBE binary variants.

```
8=FIX.4.4|9=176|35=D|49=BUYSIDE|56=BROKER|34=215|52=20260803-13:00:01.123|
11=ORD-000123|55=AAPL|54=1|38=100000|40=2|44=182.35|59=0|60=20260803-13:00:01.100|10=093|
```

| Tag | Meaning |
|---|---|
| 8 | BeginString (version) |
| 35 | **MsgType** — `D`=NewOrderSingle, `F`=OrderCancelRequest, `G`=CancelReplace, `8`=**ExecutionReport**, `9`=OrderCancelReject, `V`/`W`/`X`=market data request/snapshot/incremental |
| 34 | MsgSeqNum (gap detection → ResendRequest `2`) |
| 11 | ClOrdID (**your** order ID — the idempotency key) |
| 37 | OrderID (the broker's ID) |
| 17 / 150 / 39 | ExecID / ExecType / **OrdStatus** |
| 55 / 54 / 38 / 44 / 40 / 59 | Symbol / Side / OrderQty / Price / OrdType / TimeInForce |
| 14 / 151 / 6 | CumQty / LeavesQty / AvgPx |
| 10 | Checksum |

**Session vs application layer**: logon/logout, heartbeats (`0`), TestRequest (`1`), sequence numbers
and resend — that's the session layer, and it's where the reliability engineering lives. QuickFIX/n
is the common .NET library.

> **Great thing to say:** *"FIX sessions are essentially a reliable ordered messaging protocol with
> sequence numbers, gap fill and replay — conceptually the same problems as Kafka offsets and
> consumer-group replay, which I've worked with at scale. The domain-specific part is the message
> semantics and the venue quirks, and that's an anti-corruption layer job."*

**Other protocols/standards to recognise:** SWIFT (settlement/payments messaging, MT/MX ISO 20022),
ISO 20022 generally, SBE/ITCH/OUCH (low-latency exchange protocols), Bloomberg **BLPAPI** and
Refinitiv/LSEG **Eikon/RFA** for market data.

---

## 6. Positions, P&L and valuation — the numbers that must be right

- **Position** = quantity held of an instrument in an account. Long (+) / short (−).
- **Trade date vs settlement date** positions — both matter and they differ.
- **Market value** = quantity × price × FX rate (× contract multiplier for derivatives).
- **Average cost** vs **FIFO/LIFO** cost basis — affects realised P&L; the accounting method is a
  business rule, not a detail.
- **Realised P&L** (from closed trades) vs **unrealised P&L** (mark-to-market on open positions).
  ```
  Unrealised P&L = (current price − average cost) × quantity
  Realised P&L   = (sale price − cost of the sold lots) × quantity sold − fees
  ```
- **Mark-to-market**: revaluing at current market prices. Needs a *price source hierarchy* and a
  policy for stale/missing prices.
- **NAV (Net Asset Value)** = (assets − liabilities) / units. The number the whole back office exists
  to produce correctly, usually daily.
- **Accrued interest** on bonds; **day-count conventions** (ACT/360, ACT/365, 30/360) — a classic
  source of off-by-a-day bugs.
- **Multi-currency**: base currency vs local currency, FX translation, and FX P&L separated from
  security P&L.
- **Corporate actions** rewrite history (a 2-for-1 split doubles quantity and halves price
  retroactively) — hence **point-in-time / bitemporal data** (`07` §6).
- **T+1/T+2 settlement**, failed trades, and **reconciliation breaks** — the daily operational reality.

⚠️ **Money arithmetic:** `decimal` in C#, `Decimal` or integer minor units in Python, `DECIMAL/NUMERIC`
in SQL — **never `float`/`double` for money**. Rounding rules (half-even/banker's rounding) must be
explicit and consistent, and quantities/prices have instrument-specific precision (tick size, lot
size). If you say only one domain-technical thing all interview, say this one — it's the fastest way
to signal "I understand that in this domain, numbers are the product."

---

## 7. Risk & performance (middle office)

- **Exposure** — how much you'd lose if something goes to zero; gross vs net exposure.
- **VaR (Value at Risk)** — "95% confident we won't lose more than X over 1 day". Methods: historical
  simulation, variance-covariance, Monte Carlo. **Expected Shortfall / CVaR** = the average loss
  beyond VaR (regulators moved toward it because VaR ignores tail shape).
- **Volatility** — standard deviation of returns; annualised by ×√252. **Beta** — sensitivity to the
  market. **Sharpe ratio** = (return − risk-free) / volatility. **Tracking error** = std dev of
  active return vs benchmark. **Information ratio** = active return / tracking error.
- **Drawdown / max drawdown**; **attribution** (which decisions produced the return — allocation vs
  selection).
- **Greeks** (options): **delta** (Δ price sensitivity), **gamma** (Δ of delta), **vega** (volatility),
  **theta** (time decay), **rho** (rates). Know what they *are*, not how to derive them.
- **Stress testing / scenario analysis**; **limits and breaches** (pre-trade and post-trade).
- **Liquidity risk**, counterparty risk, concentration limits.

---

## 8. "Financial mathematics" and "financial optimization" — the honest depth you need

You are **not** being hired as a quant. You need to (a) not be lost, (b) be able to *implement* what a
quant specifies. Cover this much:

- **Time value of money**: present value / future value, discounting, `PV = CF / (1+r)^t`.
- **Compounding**, simple vs continuous (`e^{rt}`).
- **Returns**: simple vs log returns (log returns are additive over time — why quants prefer them),
  arithmetic vs geometric mean, **TWR (time-weighted)** vs **MWR/IRR (money-weighted)** returns —
  TWR judges the manager, MWR judges the investor's actual experience.
- **Bond maths**: price/yield inverse relationship, **duration** (price sensitivity to rates),
  convexity, YTM.
- **Options**: Black–Scholes exists and gives a fair value from spot, strike, time, rate and
  **implied volatility**; Monte Carlo and binomial trees for path-dependent products. You need the
  *vocabulary*, not the derivation.
- **Portfolio optimisation** ("financial optimization" in the JD): **Markowitz mean-variance** —
  maximise expected return for a given risk, producing the **efficient frontier**. In practice it's a
  **quadratic program**: minimise `wᵀΣw` subject to `Σw = 1` and constraints (long-only, sector caps,
  turnover limits, tracking-error budget). Solvers: `cvxpy`, `scipy.optimize`, OSQP, Gurobi/MOSEK.
  Practical issues: covariance matrix estimation error, instability of the weights, transaction costs,
  Black–Litterman as the standard fix. **Also: rebalancing** — moving the portfolio from current to
  target weights while minimising cost and respecting constraints.
- **Monte Carlo simulation** — for pricing, VaR and scenario generation. Embarrassingly parallel,
  which makes it a lovely *engineering* answer: *"that's CPU-bound and parallelisable — process pool
  or vectorised NumPy, and it's the kind of workload I'd push off the desktop onto a compute service
  and stream results back."*

> **Honest framing to use:** *"I'm an engineer, not a quant. I'd expect the models to come from the
> quant team, and my job is to implement them correctly and fast — get the numerics right, get the
> precision and rounding right, make it performant and testable, and make the results reproducible.
> The maths I'm comfortable with is present value, returns and volatility, and I understand
> mean-variance optimisation as a constrained quadratic program. I'd learn the specifics of your
> models."* — **This is a very strong answer.** Interviewers are wary of engineers who *think* they're
> quants; they love engineers who know exactly where the boundary is.

---

## 9. Regulation & compliance (say one or two of these, don't lecture)
MiFID II (Europe: best execution, transaction reporting, **RTS 25 clock synchronisation**), Dodd-Frank,
EMIR, Basel III/IV, SEC/FINRA rules, **UAE: SCA (Securities & Commodities Authority), ADGM's FSRA,
DFSA in Dubai**, plus AML/KYC and sanctions screening. What it means for engineering: **immutable
audit trails, data retention (often 7 years, WORM storage), timestamp accuracy, segregation of duties,
access control by entitlement, and change-control on anything touching trading.** That sentence is
what a technical interviewer wants; the acronyms are decoration.

---

## 10. The 15 things to be able to say without hesitation

1. Buy-side vs sell-side.
2. Front / middle / back office.
3. Order lifecycle: order → compliance → route → fills → allocate → settle → reconcile.
4. Partial fills, cancel/replace race, duplicate execution reports, dedupe on ExecID.
5. OMS vs EMS vs PMS.
6. FIX is tag=value over a sequenced session; 35=D new order, 35=8 execution report.
7. Long/short, market vs limit order, TIF (DAY/GTC/IOC/FOK).
8. Position = qty held; market value = qty × price × FX.
9. Realised vs unrealised P&L; mark-to-market.
10. NAV, T+1/T+2 settlement, reconciliation breaks.
11. **`decimal` for money, never float; explicit rounding; instrument-specific precision.**
12. VaR, volatility, Sharpe, beta, tracking error, drawdown.
13. Greeks: delta, gamma, vega, theta.
14. Mean-variance optimisation = constrained quadratic program; efficient frontier.
15. Audit trail and point-in-time correctness are non-negotiable — which is why event sourcing and
    bitemporal data matter here.

---

## 11. Two hours of extra credit (if you have the time before stage 3)
- Investopedia: "order types", "OMS", "NAV", "VaR", "duration".
- Skim the **FIX 4.4 message summary** (just MsgTypes and the tags in §5).
- Skim **QuickFIX/n** on GitHub — five minutes tells you what a FIX engine looks like in .NET.
- Read one page on **BlackRock Aladdin** to see how a buy-side platform is positioned.
- If you want one genuinely useful book chapter: the order-lifecycle chapter of any "trading systems"
  primer. Don't over-invest — **depth in engineering + honest curiosity beats shallow finance
  vocabulary**, and interviewers can tell the difference instantly.

---

## 12. How to use this on Monday (Luxoft technical round)

Don't perform domain expertise. Do this instead — **ask one good domain question and connect one
piece of your experience**:

> *"I've read that the role touches portfolio and order management. My background is logistics and
> airline reservations rather than capital markets, but the shape looks familiar — a state machine
> over an order, external counterparties you don't control, messages that can duplicate or arrive out
> of order, and an audit trail someone will interrogate later. At Calrom we used event sourcing on
> the reservation system precisely because we needed a replayable audit trail. Is that roughly the
> problem space here, or is it more the analytics and valuation side?"*

That single paragraph does four things: admits the gap, proves you did the reading, demonstrates
transferable depth, and asks a question that makes the interviewer talk about their system.
