# 10 - Mind Map: Play the Game in Your Head, Then Write Code

Use this file when the other files feel too abstract. The goal is simple:

1. See the game like a small movie.
2. Name the moving pieces.
3. Turn those pieces into classes, fields, and methods.
4. Add checks that prove the movie is happening correctly.

Do not start by thinking "What code do I write?" Start with "What is happening on the table?"

## Plain English version

Before writing code, imagine the table.

Ask:

1. Who are the players?
2. Where are the cards?
3. Whose turn is it?
4. What is one player allowed to do?
5. How do we know who won?

Then turn the answers into code:

- People become `Player`.
- Cards become `Card`.
- The pile of remaining cards becomes `Deck`.
- The rules become methods like `PointsOf`, `IsPlayable`, or `WinnerOfTrick`.

If you can explain the game in your head, the code becomes much easier.

---

## The universal card-game mind map

Every prompt becomes this map:

```text
Game
|
+-- Setup
|   +-- What deck exists?
|   +-- How many players?
|   +-- How many cards does each player get?
|
+-- State
|   +-- Player hands
|   +-- Deck count
|   +-- Optional piles: discard, won pile, draw pile
|   +-- Optional turn index / leader / direction
|
+-- One action
|   +-- Deal one card?
|   +-- Draw one card?
|   +-- Play one card?
|   +-- Compare one card?
|   +-- Score one hand?
|
+-- Rule homes
|   +-- Card points: PointsOf
|   +-- Rank comparison: Ranks.Order
|   +-- Legal play: IsPlayable or LegalCards
|   +-- Winner: Winners, ResolveWinners, or WinnerOfTrick
|   +-- Turn movement: AdvanceTurn
|
+-- End
    +-- Fixed number of rounds?
    +-- Empty hand?
    +-- Empty deck?
    +-- Highest score?
```

If you can fill this map, you can write the code.

---

## The universal code map

Write code in this order:

```text
1. Card
   - Rank
   - Suit
   - IsJoker
   - Strength
   - ToString()

2. Deck
   - List<Card> _cards
   - Shuffle()
   - Draw()
   - Draw(n)

3. Player
   - Name
   - Hand
   - Optional: Score, WonPile, DrawPile

4. Game class
   - Players
   - Deck
   - Setup/deal method
   - One rule method at a time

5. Main
   - Checks
   - Demo run
```

Mental rule: if a noun stays around, it is probably a field or class. If a verb happens, it is probably a method.

Examples:
- "Player has a hand" -> `Player.Hand`.
- "Deck can draw" -> `Deck.Draw()`.
- "Card can score differently per game" -> `Game.PointsOf(Card)`.
- "Player may play only matching card" -> `IsPlayable(Card, top)`.

---

## Mock 1 mind map: High Score

Mental movie:

```text
Shuffle deck.
Deal 5 cards to Alice, Bob, Cara.
Look at Alice's whole hand and add points.
Look at Bob's whole hand and add points.
Look at Cara's whole hand and add points.
Highest total wins.
```

State:

```text
Player
+-- Name
+-- Hand: List<Card>
```

Code homes:

```text
Deal(cardsEach)      -> gives cards to players
PointsOf(card)       -> single card value
ScoreHand(player)    -> sum of PointsOf for the hand
Winners()            -> max score, return all tied players
```

Think through example:

```text
Alice: AH 10D
Bob:   KS 2C

If K=13:
Alice = 1 + 10 = 11
Bob   = 13 + 2 = 15
Bob wins.

If J/Q/K become 10:
Bob = 10 + 2 = 12
Bob still wins, but only PointsOf changed.
```

Code you should imagine:

```csharp
public int PointsOf(Card card) { ... }
public int ScoreHand(Player p) => p.Hand.Sum(PointsOf);
public List<Player> Winners() { ... }
```

---

## Mock 2 mind map: Battle / War

Mental movie:

```text
Split deck into two draw piles.
Round starts.
Alice flips top card.
Bob flips top card.
Compare ranks.
Winner takes both cards into won pile.
Repeat for 10 rounds.
Most won cards wins.
```

State:

```text
BattlePlayer
+-- Name
+-- DrawPile
+-- WonPile

Game
+-- DiscardPile for tied rounds
```

Code homes:

```text
CompareCards(a, b)   -> rank comparison, later suit comparison
PlayRound()          -> draw two cards, compare, award
PlayGame()           -> loop rounds
Winner()             -> compare won pile counts
```

Think through example:

```text
Alice flips 9H.
Bob flips QD.
Q strength > 9 strength.
Bob.WonPile gets 9H and QD.
```

Mutation route:

```text
Aces high        -> Ranks.Order
War on tie       -> tie branch in Compare/PlayRound
Suit breaks tie  -> CompareCards
Jokers           -> Ranks.Order plus joker edge case
```

---

## Mock 3 mind map: Best Hand

Mental movie:

```text
Deal 5 cards to each player.
For each hand, group cards by rank.
A group of 3 means Three of a Kind.
A group of 2 means One Pair.
Otherwise High Card.
Compare category first, then defining rank.
```

State:

```text
HandResult
+-- CategoryName
+-- CategoryStrength
+-- DefiningRankStrength
+-- Optional kicker
```

Code homes:

```text
ClassifyHand(hand)   -> returns HandResult
CompareResults(a,b)  -> category, rank, kicker
Winners()            -> best result among players
```

Think through example:

```text
Alice: 7H 7S 7D QC 2H
Groups:
7 -> 3 cards
Q -> 1 card
2 -> 1 card

Result: Three of a Kind, defining rank 7.
```

Mutation route:

```text
Two Pair        -> ClassifyHand category ladder
Flush           -> ClassifyHand
Joker wild      -> preprocessing inside ClassifyHand
Kicker          -> HandResult gets another comparison field
```

---

## Mock 4 mind map: Blackjack Lite

Mental movie:

```text
Deal 2 cards to player and dealer.
Player keeps drawing until total >= 17.
Dealer keeps drawing until total >= 17.
Aces can be 1 or 11.
Best total is the highest total <= target.
Bust is over target.
Winner is whoever is closest without busting.
```

State:

```text
Player
+-- Name
+-- Hand

Game
+-- Target = 21
+-- StandAt = 17
```

Code homes:

```text
BasePoints(card)     -> number/face/joker value
BestTotal(hand)      -> ace logic
IsBust(hand)         -> BestTotal > Target
ShouldHitDealer()    -> dealer policy
Winner()             -> bust/charlie/total comparison
```

Think through example:

```text
Hand: AH 6D
Ace as 1  -> total 7
Ace as 11 -> total 17
Best total <= 21 is 17.
```

Mutation route:

```text
Dealer hits soft 17 -> ShouldHitDealer / IsSoftTotal
5-card charlie      -> Winner
Joker = 0           -> BasePoints
Target 24           -> Target field, not magic number
```

---

## Mock 5 mind map: Crazy Eights Lite

Mental movie:

```text
There is a discard top card.
Current player looks at hand.
If a card matches rank or suit, play it.
If not, draw one card.
If drawn card matches, play it; otherwise keep it.
Move to next player.
First empty hand wins.
```

State:

```text
Game
+-- Players
+-- Deck
+-- DiscardPile
+-- CurrentPlayerIndex
+-- Direction
+-- PendingSkip or PendingDraw
+-- CurrentSuit if wild 8 was played
```

Code homes:

```text
IsPlayable(card, top)  -> rank/suit/wild matching
ChooseCard(player)     -> first legal card
TakeTurn(player)       -> play or draw
AdvanceTurn()          -> index and direction
ApplyCardEffect(card)  -> skip, draw two, reverse
```

Think through example:

```text
Top: 9H
Alice hand: 2C 5H QS 9D

5H matches suit H.
9D matches rank 9.
First playable card is 5H, so Alice plays 5H.
New top is 5H.
```

Mutation route:

```text
8 wild       -> IsPlayable plus CurrentSuit
Joker skip   -> IsPlayable plus ApplyCardEffect
2 draw two   -> ApplyCardEffect
Queen reverse-> AdvanceTurn / Direction
```

---

## Mock 6 mind map: Trick Taking Lite

Mental movie:

```text
Leader plays one card.
That card's suit becomes led suit.
Other players must follow led suit if they can.
After everyone plays one card, choose trick winner.
Winner gets 1 point and leads next trick.
```

State:

```text
Player
+-- Name
+-- Hand
+-- Score

Play
+-- Player
+-- Card

Game
+-- LeaderIndex
+-- TrickNumber
+-- TrumpSuit optional
```

Code homes:

```text
LegalCards(player, ledSuit) -> follow-suit rule
ChooseCard(player, ledSuit) -> lowest legal card
WinnerOfTrick(plays)        -> led suit / trump comparison
PlayTrick()                 -> one complete trick
```

Think through example:

```text
Alice leads 7H.
Led suit is H.
Bob has 2H QS, so Bob must play 2H.
Cara has no hearts, so Cara may play anything.
Dan has KH 3C, so Dan must play KH.

Without trump, highest heart wins: KH.
Dan wins the trick.
```

Mutation route:

```text
Spades trump       -> WinnerOfTrick
Changing trump     -> TrumpSuitForTrick
Aces high          -> Ranks.Order
Joker always legal -> LegalCards plus WinnerOfTrick
```

---

## How to write the code in your mind

Before typing, say this checklist:

1. "What are my objects?"
   - Almost always `Card`, `Deck`, `Player`, `Game`.
2. "What state changes?"
   - Hand grows/shrinks, deck count drops, piles change, turn index changes, scores change.
3. "What is one full action?"
   - One deal, one round, one turn, one trick, one hand classification.
4. "Where does each rule live?"
   - Points, ordering, legal play, winner, turn movement.
5. "What tiny check proves this?"
   - One known hand, one known comparison, one known winner.

Then type the smallest version that makes that mental movie run.

---

## If you feel lost

Use this emergency simplification:

```text
1. Ignore mutations for now.
2. Make one example work.
3. Print state after each step.
4. Put every rule in a named method.
5. Only then handle the next mutation.
```

Example:

```text
I do not understand Crazy Eights yet.
So I test only this:
Top card = 9H.
Hand = 2C 5H QS 9D.
IsPlayable should return true for 5H and 9D only.
```

Once that works, the bigger game becomes easier because the rule has a home.
