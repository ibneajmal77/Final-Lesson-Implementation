using System;
using System.Collections.Generic;
using System.Linq;

// #############################################################################
//  GAME SHAPE #2: WAR / BATTLE  (round loop + comparator / Mock 2)
//
//  Two players split the deck; each round both flip the top card; the stronger rank
//  takes both. Most cards won wins. Stresses: the comparator + the round loop + pile
//  bookkeeping (a Queue models a pile naturally: Dequeue the top).
//
//  Mutation routing: aces high -> Ranks.Order; suit breaks tie -> CompareCards;
//  jokers beat all -> Ranks.Order (already last). We show a tie-break via SUIT here.
// #############################################################################
// #############################################################################
//  ★ SPOKEN SCRIPT — War ★
//
//  SAY (restate): "Both players flip their top card each round; the higher rank
//       takes both cards; after the rounds, the bigger pile of won cards wins."
//  ASK: "On equal ranks — do the cards go to a discard, or is there a 'war'?"
//  ASK: "Exactly 10 rounds, or play until a pile is empty?"
//  SAY (plan): "Plan: ONE comparator method for 'who beats whom', a PlayRound
//       method for one flip-flip-compare, then a loop. Piles are Queues —
//       Dequeue IS flipping the top card."
// #############################################################################
class WarGame
{
    private readonly Queue<Card> _a;
    private readonly Queue<Card> _b;
    private readonly bool _suitBreaksTies;   // a mutation flag, kept in ONE place
    public int WonA { get; private set; }
    public int WonB { get; private set; }

    public WarGame(IEnumerable<Card> pileA, IEnumerable<Card> pileB, bool suitBreaksTies = false)
    {
        _a = new Queue<Card>(pileA);
        _b = new Queue<Card>(pileB);
        _suitBreaksTies = suitBreaksTies;
    }

    // The comparator = the ONE place "who beats whom" lives for this game.
    // Returns +1 if a wins, -1 if b wins, 0 if tied.
    // DRY RUN — CompareCards(QH, 9D):  Q strength 11 vs 9 strength 8. 11 != 8 -> 11>8 -> return +1 (a wins).
    // DRY RUN — CompareCards(5S, 5C) with _suitBreaksTies=true:
    //   strengths equal (both 4) -> fall through. Suits.Of("S")=3 > Suits.Of("C")=0 -> return +1 (a wins).
    //   Without the flag, that same tie returns 0.
    // EDGE CASE — CompareCards(5S, 5S) with _suitBreaksTies=true:
    //   ranks tie AND suits tie -> return 0. Tie-breakers must not invent a winner.
    // SAY: "Every 'who beats whom' decision goes through this ONE comparator —
    //       when the tie rule changes later, only this method changes."
    public int CompareCards(Card a, Card b)
    {
        if (a.Strength != b.Strength) return a.Strength > b.Strength ? 1 : -1;
        if (_suitBreaksTies)
        {
            int suitA = Suits.Of(a.Suit);
            int suitB = Suits.Of(b.Suit);
            if (suitA != suitB) return suitA > suitB ? 1 : -1;  // added compare level
        }
        return 0;
    }

    // One full action = one round.
    // SAY: "One round is one method. My safety net: cards must never vanish —
    //       all piles together must always sum back to the full deck."
    public void PlayRound()
    {
        if (_a.Count == 0 || _b.Count == 0) return;
        var ca = _a.Dequeue();
        var cb = _b.Dequeue();
        int r = CompareCards(ca, cb);
        if (r > 0) WonA += 2;
        else if (r < 0) WonB += 2;
        // (a real tie policy would carry a pot; omitted for a minimal, correct demo)
    }

    public void Play(int rounds) { for (int i = 0; i < rounds && _a.Count > 0 && _b.Count > 0; i++) PlayRound(); }
    public string Winner() => WonA == WonB ? "tie" : (WonA > WonB ? "A" : "B");
}


// ---- SELF-CHECKS for this game (run from Program.Main) -----------------------
static class WarDemo
{
    public static void RunChecks()
    {
        Harness.Section("War: comparator, round loop, suit tie-break");
        int cmp = new WarGame(new Card[0], new Card[0]).CompareCards(new Card("Q", "H"), new Card("9", "D"));
        Harness.Check(cmp > 0, "comparator: Q beats 9");

        var warSuit = new WarGame(new Card[0], new Card[0], suitBreaksTies: true);
        Harness.Check(warSuit.CompareCards(new Card("5", "S"), new Card("5", "C")) > 0,
                      "MUTATION 'suits break ties': 5S beats 5C via Suits.Strength");
        Harness.Check(warSuit.CompareCards(new Card("5", "S"), new Card("5", "S")) == 0,
                      "edge case: same rank AND same suit is still a tie");
          
        var war = new WarGame(new[] { new Card("K", "C"), new Card("2", "C") },
                              new[] { new Card("3", "D"), new Card("A", "D") });
        war.Play(2);
        Harness.Check(war.Winner() == "A", "war round loop: K,2 vs 3,A -> A wins 2 rounds to 0 (ace low!)");
    }
}


// #############################################################################
//  FULL WAR — the real Mock 2 Part 2 + all four Part 3 mutations, cumulative.
//
//  THE STORY: Alice and Bob each hold half a shuffled deck, face down. Each
//  round both flip their top card; higher rank takes BOTH cards into a "won"
//  pile. After N rounds (or until a pile empties), the bigger won pile wins.
//
//  WHY A SEPARATE WarPlayer CLASS: this game needs TWO piles per player (a
//  draw pile you flip FROM, a won pile you collect INTO) — Core's Player (one
//  Hand) doesn't fit. A Queue models "always take the TOP card" naturally:
//  Dequeue() IS flipping the top card.
//
//  WHY THREE TIE POLICIES LIVE IN ONE ENUM, NOT THREE BOOLS: Discard / War /
//  SuitBreaksTies are mutually EXCLUSIVE — a round is never "war AND suit
//  break" at once. Two independent bools would let you (accidentally) set
//  both; one enum makes the invalid combination unrepresentable. (M2 and M3
//  are shown here as TWO SWITCHABLE POLICIES so you can test and compare both
//  — in the real interview, M3 REPLACES M2: you'd delete the War case
//  entirely, not keep it around as a permanent option. Say that out loud.)
// #############################################################################
enum TieRule { Discard, War, SuitBreaksTies }

sealed class WarPlayer
{
    public string Name { get; }
    public Queue<Card> DrawPile { get; }
    public List<Card> WonPile { get; } = new List<Card>();

    public WarPlayer(string name, IEnumerable<Card> startingPile)
    {
        Name = name;
        DrawPile = new Queue<Card>(startingPile);
    }
}

sealed class FullWarGame
{
    // [M1] "Aces are high." ROUTE: ordering data — but NOT the global Ranks.Order
    // (Core's checks assert ace-low; editing the shared array would break them).
    // Instead: this game keeps its OWN rank array field, swappable per instance.
    // SAY: "Ordering is swappable DATA — I'm not touching the shared Ranks.Order,
    //      because two different game instances need two different orderings
    //      alive at the same time. A local field, not a global edit."
    private static readonly string[] AceHighOrder =
        { "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "JOKER" };

    private readonly string[] _rankOrder;
    private readonly TieRule _tieRule;
    private readonly int _totalCards;   // the envelope check's expected total

    public WarPlayer A { get; }
    public WarPlayer B { get; }
    public List<Card> SharedDiscard { get; } = new List<Card>();
    public bool GameOver { get; private set; }     // [M2] set only by a war a player can't cover
    public string Loser { get; private set; }

    // Real game: shuffle a fresh deck, split it evenly.
    // DRY RUN — new FullWarGame("Alice","Bob", seed:1): Deck.Count=52, half=26.
    //   A.DrawPile gets the first 26 draws, B gets the remaining 26.
    public FullWarGame(string nameA, string nameB, int? seed = null,
                        bool acesHigh = false, TieRule tieRule = TieRule.Discard,
                        bool includeJokers = false)
    {
        _rankOrder = acesHigh ? AceHighOrder : Ranks.Order;
        _tieRule = tieRule;

        var deck = new Deck(includeJokers: includeJokers, seed: seed);
        deck.Shuffle();
        _totalCards = deck.Count;
        int half = deck.Count / 2;
        A = new WarPlayer(nameA, deck.Draw(half));
        B = new WarPlayer(nameB, deck.Draw(deck.Count));   // whatever's left
    }

    // Test ctor: inject exact piles so mutation checks are deterministic —
    // same reason every other game file in this project has one of these.
    public FullWarGame(string nameA, IEnumerable<Card> pileA,
                        string nameB, IEnumerable<Card> pileB,
                        bool acesHigh = false, TieRule tieRule = TieRule.Discard)
    {
        _rankOrder = acesHigh ? AceHighOrder : Ranks.Order;
        _tieRule = tieRule;
        A = new WarPlayer(nameA, pileA);
        B = new WarPlayer(nameB, pileB);
        _totalCards = A.DrawPile.Count + B.DrawPile.Count;
    }

    private int Strength(Card c) => Array.IndexOf(_rankOrder, c.Rank);

    // The ONE place "who beats whom" lives. Suit tie-break folds in here so a
    // 0 return means "genuinely still tied" no matter which policy is active.
    // DRY RUN — CompareCards(5S,5C) with SuitBreaksTies: ranks equal -> suits
    //   compared: Of("S")=3 > Of("C")=0 -> +1 (a wins), no war needed at all.
    // DRY RUN — CompareCards(JOKER,JOKER) with SuitBreaksTies: ranks equal ->
    //   Suits.Of(null)=-1 for BOTH (jokers have no suit) -> still equal -> 0.
    //   [M4] "two jokers collide -> discard both" falls straight out of this;
    //   no joker-specific code needed because Suits.Of is already null-safe.
    private int CompareCards(Card a, Card b)
    {
        int sa = Strength(a), sb = Strength(b);
        if (sa != sb) return sa > sb ? 1 : -1;
        if (_tieRule == TieRule.SuitBreaksTies)
        {
            int suitA = Suits.Of(a.Suit), suitB = Suits.Of(b.Suit);
            if (suitA != suitB) return suitA > suitB ? 1 : -1;
        }
        return 0;
    }

    // One full action = one round. Prints exactly like the mock's own example.
    // SAY: "One round is one method — whatever the tie policy is, this is the
    //      only place that dispatches to it."
    public void PlayRound(int roundNo)
    {
        if (GameOver || A.DrawPile.Count == 0 || B.DrawPile.Count == 0) return;

        var ca = A.DrawPile.Dequeue();
        var cb = B.DrawPile.Dequeue();
        int r = CompareCards(ca, cb);
        string outcome;

        if (r > 0) { A.WonPile.Add(ca); A.WonPile.Add(cb); outcome = A.Name; }
        else if (r < 0) { B.WonPile.Add(ca); B.WonPile.Add(cb); outcome = B.Name; }
        else if (_tieRule == TieRule.War) outcome = ResolveWar(ca, cb);
        else { SharedDiscard.Add(ca); SharedDiscard.Add(cb); outcome = "discard"; }   // Discard, or the SuitBreaksTies joker-collision edge case

        Console.WriteLine($"  Round {roundNo}: {A.Name} {ca}  vs  {B.Name} {cb}  ->  {outcome}");
    }

    // [M2] "Real war on a tie." ROUTE: only this method — CompareCards, Play,
    // and Winner don't know war exists.
    // DRY RUN — tie on 7C/7D, A has [2D,KH] left, B has [3D,2C] left:
    //   pot=[7C,7D]. Both piles have >=2 -> proceed. Facedown: 2D,3D added.
    //   Flip: KH vs 2C -> K beats 2 -> A takes the whole pot (6 cards).
    // TRAP, dry run — tie on 7C/7D, A has ONLY [KH] left (1 card):
    //   A.DrawPile.Count(1) < 2 -> GameOver=true, Loser="A" — the war never
    //   even starts; running out of cards to COVER a war is an instant loss.
    private string ResolveWar(Card firstA, Card firstB)
    {
        var pot = new List<Card> { firstA, firstB };
        while (true)
        {
            if (A.DrawPile.Count < 2) { GameOver = true; Loser = A.Name; return $"WAR -> {A.Name} can't cover it, game over"; }
            if (B.DrawPile.Count < 2) { GameOver = true; Loser = B.Name; return $"WAR -> {B.Name} can't cover it, game over"; }

            pot.Add(A.DrawPile.Dequeue());          // face down
            pot.Add(B.DrawPile.Dequeue());
            var flipA = A.DrawPile.Dequeue();       // the deciding flip
            var flipB = B.DrawPile.Dequeue();
            pot.Add(flipA);
            pot.Add(flipB);

            int r = CompareCards(flipA, flipB);
            if (r > 0) { A.WonPile.AddRange(pot); return $"WAR -> {A.Name} takes {pot.Count}"; }
            if (r < 0) { B.WonPile.AddRange(pot); return $"WAR -> {B.Name} takes {pot.Count}"; }
            // still tied -> loop again; the pot keeps growing until someone wins it
        }
    }

    public void Play(int rounds)
    {
        for (int i = 1; i <= rounds && !GameOver && A.DrawPile.Count > 0 && B.DrawPile.Count > 0; i++)
            PlayRound(i);
    }

    // [M4] "Play until a pile is empty" — the loop condition, nothing else.
    // SAY: "This always terminates: every round removes cards from a strictly
    //      finite pool and never returns them, and a doomed war ends the game
    //      early — but a defensive round cap costs one line, so I'll keep it."
    public void PlayUntilEmpty()
    {
        int round = 1;
        while (!GameOver && A.DrawPile.Count > 0 && B.DrawPile.Count > 0 && round <= 1000)
        {
            PlayRound(round);
            round++;
        }
    }

    // A war-loss ends the game immediately for the OTHER player, regardless
    // of won-pile counts at that moment.
    public string Winner()
    {
        if (GameOver) return Loser == A.Name ? B.Name : A.Name;
        if (A.WonPile.Count == B.WonPile.Count) return "tie";
        return A.WonPile.Count > B.WonPile.Count ? A.Name : B.Name;
    }

    // THE STRONGEST WAR CHECK: cards can only move between piles, never vanish
    // or duplicate. Call this after any round, any mutation — it should always
    // be true.
    public bool CardsBalance() =>
        A.DrawPile.Count + B.DrawPile.Count + A.WonPile.Count + B.WonPile.Count + SharedDiscard.Count == _totalCards;
}


// ---- SELF-CHECKS for Full War (run from Program.Main) -------------------------
static class FullWarDemo
{
    public static void RunChecks()
    {
        Harness.Section("Full War: setup, tie policies, war, aces-high, envelope");

        // Setup: a real shuffled deck splits evenly.
        var setup = new FullWarGame("Alice", "Bob", seed: 1);
        Harness.Check(setup.A.DrawPile.Count == 26 && setup.B.DrawPile.Count == 26,
                      "setup: a 52-card deck splits into two 26-card draw piles");

        // Default policy (Discard): a tie sends both cards to SharedDiscard,
        // nobody's won-pile changes.
        var discard = new FullWarGame("A", new[] { new Card("7", "H") },
                                       "B", new[] { new Card("7", "C") });
        discard.PlayRound(1);
        Harness.Check(discard.SharedDiscard.Count == 2 && discard.A.WonPile.Count == 0,
                      "default tie policy: equal ranks -> both cards discarded, no war");

        // [M1] Aces high: a local rank array, global Ranks.Order untouched.
        var aceHigh = new FullWarGame("A", new[] { new Card("A", "C") },
                                       "B", new[] { new Card("K", "D") }, acesHigh: true);
        aceHigh.PlayRound(1);
        Harness.Check(aceHigh.A.WonPile.Count == 2,
                      "MUTATION 'aces high': A's ace now beats B's king (local data, Ranks.Order untouched)");

        // [M2] War: a tie triggers face-down+flip; the flip decides; winner
        // takes the whole pot (2 tied + 2 facedown + 2 flip = 6 cards).
        var war = new FullWarGame("A", new[] { new Card("7", "C"), new Card("2", "D"), new Card("K", "H") },
                                   "B", new[] { new Card("7", "D"), new Card("3", "D"), new Card("2", "C") },
                                   tieRule: TieRule.War);
        war.PlayRound(1);
        Harness.Check(war.A.WonPile.Count == 6 && war.B.DrawPile.Count == 0,
                      "MUTATION 'war on tie': flips decide, winner takes all 6 pot cards");

        // [M2] TRAP: a player who can't cover the war (fewer than 2 cards left
        // to place face-down + flip) loses the whole game immediately.
        var warLoss = new FullWarGame("A", new[] { new Card("7", "C"), new Card("K", "H") },
                                       "B", new[] { new Card("7", "D"), new Card("2", "C"), new Card("9", "S") },
                                       tieRule: TieRule.War);
        warLoss.PlayRound(1);
        Harness.Check(warLoss.GameOver && warLoss.Loser == "A" && warLoss.Winner() == "B",
                      "TRAP: a player who can't cover a war loses the game immediately");

        // [M3] REPLACES M2 — suits break ties outright now, no war at all.
        var suitTie = new FullWarGame("A", new[] { new Card("5", "S") },
                                       "B", new[] { new Card("5", "C") }, tieRule: TieRule.SuitBreaksTies);
        suitTie.PlayRound(1);
        Harness.Check(suitTie.A.WonPile.Count == 2,
                      "MUTATION 'suit breaks ties' (replaces war): 5S beats 5C outright, no war triggered");

        // [M4] Two jokers collide under SuitBreaksTies: both suits are null ->
        // Suits.Of gives -1 for both -> still a genuine tie -> discard both.
        var jokerCollide = new FullWarGame("A", new[] { new Card("JOKER", null) },
                                            "B", new[] { new Card("JOKER", null) }, tieRule: TieRule.SuitBreaksTies);
        jokerCollide.PlayRound(1);
        Harness.Check(jokerCollide.SharedDiscard.Count == 2,
                      "MUTATION 'jokers, two collide': suit compare can't apply -> both discarded, no crash");

        // [M4] Play until a pile empties, with jokers in the deck. Confirm the
        // strongest invariant: every card is accounted for at the end.
        var untilEmpty = new FullWarGame("Alice", "Bob", seed: 7, includeJokers: true);
        untilEmpty.PlayUntilEmpty();
        Harness.Check(untilEmpty.A.DrawPile.Count == 0 && untilEmpty.B.DrawPile.Count == 0,
                      "MUTATION 'play until empty': both draw piles fully consumed");
        Harness.Check(untilEmpty.CardsBalance(),
                      "envelope check: draw+won+discard piles still sum to the full 54-card deck");

        // A short printed demo, matching the mock's own output format.
        Harness.Section("Demo: a few rounds of Full War");
        var demo = new FullWarGame("Alice", "Bob", seed: 42);
        demo.Play(5);
        Console.WriteLine($"  Alice won: {demo.A.WonPile.Count}   Bob won: {demo.B.WonPile.Count}   discard: {demo.SharedDiscard.Count}");
        Console.WriteLine("  Cards balance: " + demo.CardsBalance());
    }
}
