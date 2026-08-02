# 11 — CAPITAL MARKETS, IN PLAIN ENGLISH

> Nice-to-haves in the job spec: **Portfolio / Order / Execution Management Systems**, **financial
> mathematics**, **financial optimization**. Industry tag: **BCM — Banking & Capital Markets**.
>
> **For the technical round:** you need enough to show genuine interest and follow the conversation.
> **For the client round:** you need this file cold.
>
> ⚠️ **Don't perform expertise.** The interviewer is the domain expert. What wins is
> **engineering depth plus honest curiosity** — and they can tell the difference instantly.

---

# PART 0 — THE 10 DOMAIN LINES THAT WIN

| # | The question | The answer, in one breath |
|---|---|---|
| 1 | **Buy-side vs sell-side** | "Buy-side **owns** the money — asset managers, pension funds, sovereign wealth funds. Sell-side are the banks and brokers who make markets and execute. **Abu Dhabi plus portfolio management means almost certainly buy-side.**" |
| 2 | **The order lifecycle** | "Order → pre-trade compliance → route → **partial fills** → allocate → settle → reconcile." |
| 3 | **OMS vs EMS vs PMS** | "**PMS** — what should I own. **OMS** — manage the order and the audit trail. **EMS** — execute it well." |
| 4 | **What is FIX?** | "Tag-equals-value messages over a sequenced session. `35=D` is a new order, `35=8` is an execution report, `11=ClOrdID` is your order ID." |
| 5 | **Money** | "`decimal` in C#, `Decimal` in Python, `DECIMAL` in SQL. **Never float.** Explicit rounding, instrument-specific precision." |
| 6 | **Realised vs unrealised P&L** | "Realised is from closed trades. Unrealised is mark-to-market on what you still hold." |
| 7 | **The hard engineering problem** | "**Execution reports duplicate and arrive out of order.** You dedupe on `ExecID` and sequence on `MsgSeqNum`. It's at-least-once delivery plus idempotent consumers — exactly what I've built at scale." |
| 8 | **Why audit matters** | "A regulator doesn't just want to know what the number is. They want to know **why it was that number at 14:32:07**. That's why event sourcing and point-in-time data matter here." |
| 9 | **Financial optimisation** | "Mean-variance — Markowitz. It's a **constrained quadratic program**: minimise portfolio variance subject to weights summing to one, plus constraints. The output is the efficient frontier." |
| 10 | **Your honest frame** | "**I'm an engineer, not a quant.** My job is to implement the models correctly, precisely and fast." |

---

# PART 1 — THE MAP OF THE INDUSTRY

**Say it simply:**

- **Sell-side** = banks and brokers. They make markets, execute orders, publish research.
- **Buy-side** = asset managers, hedge funds, pension funds, **sovereign wealth funds**. They *own* the
  money and buy investments.
  ⚠️ **Abu Dhabi plus portfolio management means almost certainly buy-side.**

**The three offices:**
- **Front office** — portfolio managers, traders, analysts. *They make the money.*
- **Middle office** — risk, compliance, performance. *They check the money.*
- **Back office** — settlement, accounting, reconciliation. *They move and record the money.*

**Your app almost certainly sits front-to-middle office:** a WPF desktop for PMs and traders, a Python
analytics layer, and services keeping positions, orders and risk correct.

**Two more words:**
- **Custodian** — the bank that actually holds the assets.
- **Broker** — who executes your trade.

**The daily rhythm:** pre-trade (idea, compliance check) → trade (order, execution) → post-trade
(confirm, allocate, settle, reconcile) → valuation and reporting (NAV, P&L, risk).

---

# PART 2 — INSTRUMENTS (one line each)

| Asset class | What it is | What it means for the code |
|---|---|---|
| **Equity** | A share of a company | Simple, high volume, corporate actions |
| **Fixed income / bonds** | A loan that pays coupons and matures | Price-to-yield maths, accrued interest, **day-count conventions** |
| **FX** | Currency pairs | **Multi-currency everything** — base vs local currency |
| **Derivatives** (futures, options, swaps) | Value *derived* from something else | Pricing models, Greeks, margin. **Notional ≠ market value** |
| **Funds / ETFs** | Pooled vehicles | Look-through to the underlying holdings |
| **Private / real assets** | Illiquid, valued periodically | **No live price** — you need stale and manual valuation handling |

## Terms not to blink at

Ticker · bid / ask / mid · spread · last traded price · volume · notional · coupon · maturity · yield ·
duration · dividend.

⚠️ **Two of these are genuinely good engineering conversations — raise them:**

**1. Instrument identifiers — ISIN, CUSIP, SEDOL, FIGI.**
**Say:** *"That's the primary-key problem of finance. The same instrument has different identifiers in
different systems and different regions, and **instrument reference data mastering is a genuinely hard
engineering problem** — it's a golden-record and matching problem, not a lookup table."*

**2. Corporate actions.**
**Say:** *"A two-for-one split doubles the quantity and halves the price **retroactively**. So a
corporate action rewrites history — which means your data model needs to be point-in-time or
bitemporal, or every historical report silently changes. That's a beautiful data-engineering
problem."*

**Both of those make you sound like an engineer who has thought about the domain, rather than someone
who memorised vocabulary.**

---

# PART 3 — THE ORDER LIFECYCLE (learn this properly — it's the core)

```
 Idea / model output
   → ORDER created            (PM decides: buy 100,000 AAPL)
   → PRE-TRADE COMPLIANCE     (mandate limits, restricted list, concentration)
   → released to the trader / OMS
   → ROUTED to a broker or venue        (this is where an EMS lives)
   → EXECUTIONS come back — often MANY PARTIAL FILLS
   → ALLOCATION across funds / accounts (if it was a block order)
   → CONFIRMATION with the broker
   → SETTLEMENT               (T+1 in the US since 2024; T+2 in much of the world)
   → POSITION and CASH updated, then RECONCILED against the custodian
```

**Order states — it's a state machine:**
`New → PendingNew → New (acknowledged) → PartiallyFilled → Filled`
with branches to `PendingCancel → Cancelled`, `PendingReplace → Replaced`, `Rejected`, `Expired`.

**Order types:** *market* (execute now, price uncertain) · *limit* (price certain, execution
uncertain) · *stop* · *VWAP / TWAP* (algorithmic execution).
**Time in force:** DAY · GTC (good till cancelled) · IOC (immediate or cancel) · FOK (fill or kill).

## 🔥 The engineering problems in this lifecycle — **this is what you should actually talk about**

**1. Partial fills.**
*"An order for 100,000 might come back as forty separate executions. The position has to be correct
after every single one — and they can arrive **out of order or duplicated**."*

**2. The cancel/replace race.**
*"You send a cancel; a fill is already in flight. Who wins? The venue decides, and your system has to
handle 'cancel rejected, already filled' gracefully. **That's the classic OMS race condition.**"*

**3. Idempotency.**
*"Execution reports get re-sent on reconnect. **You dedupe on `ExecID`.** This is the purest
real-world example of at-least-once delivery plus idempotent consumers that I know of."*

**4. Audit.**
⚠️ *"Every state transition has to be reconstructable. **Why did this order have this status at
14:32:07.412?** That's exactly why we used event sourcing at Calrom — we needed a replayable audit
trail."*

**Make that Calrom connection out loud. It's your single best domain bridge.**

---

# PART 4 — OMS vs EMS vs PMS (get this right)

| System | Who uses it | What it does |
|---|---|---|
| **PMS** — Portfolio Management System | Portfolio manager | Holdings, cash, exposures, modelling, rebalancing. *"What do I own, and what **should** I own?"* |
| **OMS** — Order Management System | PM, trader, compliance | Order creation, compliance, allocation, positions, **lifecycle and audit**. *"Manage the order end to end."* |
| **EMS** — Execution Management System | Trader | Market connectivity, live data, algos, smart routing, low latency. *"Get it executed **well**."* |

Increasingly merged as **OEMS**.

**Vendor names to recognise:** **Aladdin (BlackRock)**, Charles River, SimCorp, Bloomberg AIM/EMSX,
Eze, Enfusion — and ⚠️ **Murex and Calypso**, because *Luxoft has deep partnerships in both and sells
that expertise*. Knowing those two names specifically is worth something in a Luxoft interview.

## The full answer if they ask "what do you know about an OMS?"

> *"An OMS is the **system of record for the order lifecycle** — creation, pre-trade compliance,
> routing, fills, allocation, and the audit trail. It sits between the portfolio manager's intent and
> the execution venue.*
>
> *The PMS answers 'what should the portfolio look like'. The EMS is about getting the execution done
> well. The OMS is the **correctness and control layer** in between.*
>
> *Engineering-wise it's a **state machine over orders** with strict idempotency, ordering and
> auditability requirements — which is the kind of system I've built, just in a different domain."*

**That's a complete, honest, senior answer. Learn its shape.**

---

# PART 5 — FIX PROTOCOL

**Say what it is, simply:** *"FIX is how orders and executions move between the buy-side, brokers and
venues. It's tag-equals-value pairs separated by a control character, over a **sequenced session**."*

```
8=FIX.4.4|35=D|49=BUYSIDE|56=BROKER|34=215|52=20260803-13:00:01.123|
11=ORD-000123|55=AAPL|54=1|38=100000|40=2|44=182.35|59=0|10=093|
```

| Tag | Meaning |
|---|---|
| **35** | **MsgType** — `D` = new order, `F` = cancel, `G` = cancel/replace, **`8` = execution report** |
| **11** | **ClOrdID** — *your* order ID. **This is the idempotency key** |
| **37** | OrderID — the broker's ID |
| **17 / 150 / 39** | ExecID / ExecType / **OrdStatus** |
| **34** | MsgSeqNum — a gap means you send a resend request |
| 55 / 54 / 38 / 44 | Symbol / Side / Quantity / Price |
| 14 / 151 / 6 | CumQty / LeavesQty / AvgPx |

**Session layer vs application layer:** *"Logon, heartbeats, sequence numbers and resend are the
**session** layer — and that's where the reliability engineering lives. QuickFIX/n is the common .NET
library."*

## ⚠️ The best thing you can say about FIX

> *"A FIX session is essentially a **reliable, ordered messaging protocol with sequence numbers, gap
> fill and replay** — conceptually the same problems as Kafka offsets and consumer-group replay, which
> I've worked with at scale. The domain-specific part is the message semantics and the venue quirks,
> and **that's an anti-corruption layer job**."*

**That single paragraph converts your distributed-systems experience into domain credibility.**

**Others to recognise:** SWIFT and **ISO 20022** (settlement and payments), ITCH/OUCH (low-latency
exchange protocols), **Bloomberg BLPAPI** and **Refinitiv/LSEG** for market data.

---

# PART 6 — POSITIONS, P&L AND VALUATION

**The numbers that have to be right. This is what the whole system exists for.**

- **Position** = how much of an instrument you hold in an account. Long (+) or short (−).
- **Market value** = quantity × price × FX rate (× contract multiplier for derivatives).
- **Realised P&L** — from **closed** trades. **Unrealised P&L** — mark-to-market on what you still
  hold.
  ```
  Unrealised = (current price − average cost) × quantity
  Realised   = (sale price − cost of the lots sold) × quantity sold − fees
  ```
- **Cost basis** — average cost vs FIFO vs LIFO. ⚠️ *"That's a business rule, not a detail — it changes
  the realised P&L number."*
- **Mark-to-market** — revaluing at current prices. Needs a **price source hierarchy** and an explicit
  policy for stale or missing prices.
- **NAV** = (assets − liabilities) ÷ units. *"The number the entire back office exists to produce
  correctly, usually daily."*
- **Accrued interest** and **day-count conventions** (ACT/360, ACT/365, 30/360) — *"a classic source of
  off-by-one-day bugs."*
- **Multi-currency** — base vs local currency, and **FX P&L separated from security P&L**.
- **T+1 / T+2 settlement**, failed trades, and **reconciliation breaks** — the daily operational
  reality.

## ⚠️ THE ONE THING TO SAY IF YOU SAY NOTHING ELSE

> *"Money is `decimal` in C#, `Decimal` or integer minor units in Python, and `DECIMAL` in SQL —
> **never float or double**. Rounding has to be explicit and consistent — usually banker's rounding —
> and quantities and prices have instrument-specific precision: tick size and lot size.*
>
> *In this domain the numbers **are** the product."*

**This is the fastest possible way to signal that you understand what matters here. Say it early.**

---

# PART 7 — RISK AND PERFORMANCE (middle office)

**One line each. Know what they *are*, not how to derive them.**

- **Exposure** — how much you'd lose if something went to zero. Gross vs net.
- **VaR (Value at Risk)** — *"95% confident we won't lose more than X over one day."* Methods:
  historical simulation, variance-covariance, Monte Carlo.
- **Expected Shortfall / CVaR** — the average loss *beyond* VaR. *"Regulators moved toward it because
  VaR tells you nothing about the shape of the tail."*
- **Volatility** — standard deviation of returns, **annualised by × √252**.
- **Beta** — sensitivity to the market.
- **Sharpe ratio** = (return − risk-free) ÷ volatility.
- **Tracking error** — how far you drift from the benchmark. **Information ratio** = active return ÷
  tracking error.
- **Drawdown** — peak-to-trough loss.
- **Attribution** — which decisions produced the return: allocation versus selection.
- **The Greeks** (options): **delta** (price sensitivity) · **gamma** (change in delta) · **vega**
  (volatility) · **theta** (time decay) · **rho** (rates).

---

# PART 8 — FINANCIAL MATHS AND OPTIMISATION (the honest depth you need)

**You are not being hired as a quant.** You need to (a) not be lost, and (b) be able to **implement**
what a quant specifies. That's it.

**Cover this much:**

- **Time value of money** — present value, discounting: `PV = CF / (1+r)^t`.
- **Returns** — simple vs **log returns** (*"log returns are additive over time, which is why quants
  prefer them"*). And **TWR vs MWR**: *"time-weighted judges the manager, money-weighted judges the
  investor's actual experience."*
- **Bond maths** — price and yield move inversely; **duration** is price sensitivity to rates;
  convexity is the second-order effect.
- **Options** — *"Black-Scholes gives a fair value from spot, strike, time, rate and **implied
  volatility**. Monte Carlo or binomial trees for path-dependent products."* You need the vocabulary,
  not the derivation.
- **Portfolio optimisation** — *this is the "financial optimization" in the job spec:*
  > *"Markowitz **mean-variance**: maximise expected return for a given level of risk, which produces
  > the **efficient frontier**. In practice it's a **constrained quadratic program** — minimise wᵀΣw
  > subject to the weights summing to one, plus real-world constraints like long-only, sector caps and
  > turnover limits. Solvers are cvxpy, scipy, OSQP or a commercial one like Gurobi.*
  >
  > *The practical problems are covariance estimation error and the instability of the weights —
  > Black-Litterman is the standard fix."*
- **Monte Carlo** — ⚠️ **and here's the engineering answer that makes you sound useful:**
  *"Monte Carlo is embarrassingly parallel. That's CPU-bound work, so in Python it's a process pool or
  vectorised NumPy — and it's exactly the kind of workload I'd push **off the desktop** onto a compute
  service and stream the results back."*

## ⚠️ THE HONEST FRAMING — use it, it's genuinely strong

> *"I'm an engineer, not a quant. I'd expect the models to come from the quant team, and my job is to
> implement them correctly and fast — get the numerics right, get the precision and rounding right,
> make it performant and testable, and make the results **reproducible**.*
>
> *The maths I'm comfortable with is present value, returns and volatility, and I understand
> mean-variance optimisation as a constrained quadratic program. I'd learn the specifics of your
> models."*

**Why this works:** interviewers are wary of engineers who *think* they're quants. They love engineers
who know exactly where the boundary is.

---

# PART 9 — REGULATION (say one or two, don't lecture)

**Names:** MiFID II (Europe — best execution, transaction reporting, **RTS 25 clock
synchronisation**), Basel III, SEC/FINRA. **In the UAE: the SCA, ADGM's FSRA, and the DFSA in Dubai.**
Plus AML and KYC.

⚠️ **But the acronyms are decoration. This sentence is what a technical interviewer actually wants:**

> *"What regulation means for engineering is: **immutable audit trails, data retention — often seven
> years on WORM storage — timestamp accuracy, segregation of duties, access control by entitlement,
> and change control on anything that touches trading.**"*

---

# PART 10 — THE 15 THINGS TO SAY WITHOUT HESITATION

1. Buy-side owns the money; sell-side executes.
2. Front office makes it, middle office checks it, back office records it.
3. Order → compliance → route → fills → allocate → settle → reconcile.
4. Partial fills, the cancel/replace race, duplicate execution reports, **dedupe on ExecID**.
5. PMS = what should I own. OMS = manage it and audit it. EMS = execute it well.
6. FIX is tag=value over a sequenced session. `35=D` new order, `35=8` execution report.
7. Market vs limit order; DAY / GTC / IOC / FOK.
8. Market value = quantity × price × FX.
9. Realised vs unrealised P&L; mark-to-market.
10. NAV, T+1/T+2 settlement, reconciliation breaks.
11. **`decimal` for money, never float. Explicit rounding. Instrument-specific precision.**
12. VaR, volatility × √252, Sharpe, beta, tracking error, drawdown.
13. Greeks: delta, gamma, vega, theta.
14. Mean-variance optimisation is a constrained quadratic program; the output is the efficient
    frontier.
15. **Audit trail and point-in-time correctness are non-negotiable** — which is why event sourcing and
    bitemporal data matter here.

---

# PART 11 — HOW TO USE THIS IN THE INTERVIEW

⚠️ **Don't perform domain expertise.** Do this instead — **ask one good question and connect one piece
of your experience:**

> *"I've read that the role touches portfolio and order management. My background is logistics and
> airline reservations rather than capital markets — but the **shape** looks familiar: a state machine
> over an order, external counterparties you don't control, messages that can duplicate or arrive out
> of order, and an audit trail someone will interrogate later.*
>
> *At Calrom we used event sourcing on the reservation system precisely because we needed a replayable
> audit trail.*
>
> *Is that roughly the problem space here — or is it more the analytics and valuation side?"*

**That single paragraph does four things:**
1. Admits the gap honestly.
2. Proves you did the reading.
3. Demonstrates transferable depth.
4. Ends with a question that makes the interviewer talk about their system — which is the best
   possible outcome.

---

# PART 12 — EXTRA CREDIT, IF YOU HAVE AN HOUR

- Investopedia: *order types*, *OMS*, *NAV*, *VaR*, *duration*.
- Skim the **FIX 4.4 message summary** — just the MsgTypes and the tags in Part 5.
- Skim **QuickFIX/n** on GitHub. Five minutes tells you what a FIX engine looks like in .NET.
- Read one page on **BlackRock Aladdin** to see how a buy-side platform is positioned.

⚠️ **Don't over-invest here.** Depth in engineering plus honest curiosity beats shallow finance
vocabulary — and an interviewer who works in the domain can tell the difference in one question.
