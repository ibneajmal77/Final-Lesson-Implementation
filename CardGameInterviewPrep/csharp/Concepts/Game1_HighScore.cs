using System;
using System.Collections.Generic;
using System.Linq;

// #############################################################################
//  GAME SHAPE #1: HIGH SCORE  (the base game / Mock 1)
//
//  Deal K cards to N players, sum each hand, highest total wins.
//
//  This class shows the POLICY METHODS where every scoring rule lives:
//     PointsOf(card)  -> what ONE card scores          (virtual: mutations override it)
//     ScoreHand(p)    -> Sum(PointsOf) over the hand
//     Winners()       -> returns a LIST, because ties are real
//
//  Abstraction: Main calls Deal/Winners and never learns Fisher-Yates exists.
//  Dependency inversion: ScoreHand depends on the PointsOf ABSTRACTION, not on values
//  inlined at call sites — that indirection is exactly what makes mutations one-liners.
// #############################################################################
// #############################################################################
//  ★ PART 2 SPOKEN SCRIPT — High Score (the most likely Part 2) ★
//
//  SAY (restate): "Three players, five cards each; every card maps to points;
//       a hand's score is the sum; the highest hand wins, ties share the win."
//  ASK: "Face cards are 11, 12, 13 — or all worth 10?"
//  ASK: "If players tie for the best score, they all win — confirmed?"
//  SAY (plan): "Plan: Deal, then PointsOf for ONE card, ScoreHand as the sum,
//       and Winners returning a LIST because ties are real."
// #############################################################################
class HighScoreGame
{
    public List<Player> Players { get; }
    public Deck Deck { get; }

    public HighScoreGame(IEnumerable<string> names, bool includeJokers = false, int? seed = null)
    {
        Players = names.Select(n => new Player(n)).ToList();
        Deck = new Deck(includeJokers: includeJokers, seed: seed);
        Deck.Shuffle();
    }

    public void Deal(int cardsEach)
    {
        // Round-robin, like a real dealer. After a fair shuffle, block dealing is
        // statistically identical — worth saying aloud, then moving on.
        for (int round = 0; round < cardsEach; round++)
            foreach (var p in Players)
                p.Hand.Add(Deck.Draw());
    }

    // ---- THE RULE HOMES. Mutations land HERE, nowhere else. -------------------
    // NOTE the split: Strength answers "who outranks whom"; PointsOf answers "what
    // is this worth". Different kinds of rules -> different homes. Default A=1..K=13.
    // DRY RUN — PointsOf(QD): card.Strength = 11 (Q's index) -> 11 + 1 = 12.
    //           PointsOf(AD): strength 0 -> 1.   PointsOf(5D): strength 4 -> 5.
    // SAY: "Every point value lives in THIS one method. In these exercises the
    //       values always change — when they do, I edit here and nowhere else."
    public virtual int PointsOf(Card card) => card.Strength + 1;

    // DRY RUN — ScoreHand for a hand [AD, QD, 5H]:
    //   Sum(PointsOf) calls PointsOf on each card and adds:  1 + 12 + 5 = 18.
    public virtual int ScoreHand(Player p) => p.Hand.Sum(PointsOf);

    // Winners returns ALL tied players. Under-engineering trap avoided: never assume
    // exactly one winner. "Lowest wins" is a one-word change (Max -> Min) in a subclass.
    // DRY RUN — Winners() with Alice=11, Bob=15, Cara=11:
    //   best = Max(ScoreHand) = 15.
    //   Where(score == 15) keeps only Bob -> [Bob].
    //   If Alice AND Cara both had 15, BOTH would be returned -> ties stay visible.
    // SAY: "Winners returns EVERY player tied at the best score — I never assume
    //       exactly one winner; ties are a real case in card games."
    public virtual List<Player> Winners()
    {
        int best = Players.Max(ScoreHand);
        return Players.Where(p => ScoreHand(p) == best).ToList();
    }
}

// ---- MUTATIONS OF HIGH SCORE, each showing WHERE the change lands -------------

// "J, Q, K are each worth 10."  ROUTE: PointsOf only. (Rule of two: FIRST variant
// could just edit the method in place; we subclass here to keep both visible at once.)
// SAY (when this rule arrives): "That's a SCORING rule, so it lands in PointsOf
//      only. First I change my check to expect Q = 10 and watch it FAIL — then
//      I change the method and watch it go green."
class FaceCardsAreTenGame : HighScoreGame
{
    public FaceCardsAreTenGame(IEnumerable<string> names, int? seed = null) : base(names, seed: seed) { }

    // DRY RUN — PointsOf(QD): first if matches (Q) -> return 10. (Was 12 in the base game.)
    // DRY RUN — PointsOf(5D): not J/Q/K, not A, not JOKER -> int.Parse("5") -> 5.
    //   Order matters: JOKER is handled BEFORE int.Parse, so "JOKER" never reaches Parse and throws.
    public override int PointsOf(Card card)
    {
        if (card.Rank == "J" || card.Rank == "Q" || card.Rank == "K") return 10;  // the whole change
        if (card.Rank == "A") return 1;
        if (card.Rank == "JOKER") return 0;
        return int.Parse(card.Rank);   // only reached AFTER the named ranks -> "JOKER" never parses
    }
}

// "Diamonds count double."  ROUTE: PointsOf only — one multiplier line. Nothing about
// dealing, display, or winners knows or cares.
// SAY: "Still a scoring rule, still PointsOf: I reuse the base value and add ONE
//      modifier line. Dealing, display and winners stay untouched."
class DoubleDiamondsGame : HighScoreGame
{
    public DoubleDiamondsGame(IEnumerable<string> names, int? seed = null) : base(names, seed: seed) { }

    public override int PointsOf(Card card)
    {
        int points = base.PointsOf(card);                 // reuse the base rule...
        if (card.Suit == "D") points *= 2;                // ...then one modifier line
        return points;
    }
}

// "Lowest score wins."  ROUTE: Winners only — Max becomes Min.
// SAY: "That's a WINNER rule, not a scoring rule: Max becomes Min inside
//      Winners. One word changes."
class LowestWinsGame : HighScoreGame
{
    public LowestWinsGame(IEnumerable<string> names, int? seed = null) : base(names, seed: seed) { }

    public override List<Player> Winners()
    {
        int best = Players.Min(ScoreHand);                // Max -> Min, that's it
        return Players.Where(p => ScoreHand(p) == best).ToList();
    }
}

// "Ties are no longer shared: each tied player draws ONE extra card and scores are
// compared again. Repeat until one winner remains. If the deck runs out, the
// remaining tied players share the win."  (Mock 1, M4)
//
// ROUTE: still Winners() — but unlike M1-M3, this is not a one-line value swap.
// Winners() must gain a NEW CAPABILITY: re-ask "who's best" on a SHRINKING pool,
// not just once on the full player list. Nothing else moves — PointsOf, ScoreHand,
// Deal, and Deck all stay exactly as they are; a redraw just calls Deck.Draw()
// the same way Deal() already does.
//
// SAY (routing, before you type a line): "This isn't a scoring rule, so PointsOf
//      doesn't change. It's a winner rule, so it's Winners() — but the SHAPE has
//      to change: I need to re-check 'who's tied' again after dealing extra
//      cards, and only among the players still in the race."
//
// Why NOT the StrategyScoredGame delegate trick? That pattern is for when TWO
// rules must COEXIST (old scoring + new scoring, swappable). Here the OLD
// "ties just share" behavior is fully RETIRED by this rule, not kept alongside
// the new one — so a plain override is the correct (smaller) move.
class TieBreakDrawGame : HighScoreGame
{
    public TieBreakDrawGame(IEnumerable<string> names, int? seed = null) : base(names, seed: seed) { }

    // SAY: "This is the exact same 'who's best' question Winners() already
    //      asks — I've just parameterized it on a POOL instead of always
    //      reading the full Players list. That's what lets me re-run the same
    //      check on a shrinking group of contenders."
    private List<Player> BestAmong(List<Player> pool)
    {
        int best = pool.Max(ScoreHand);
        return pool.Where(p => ScoreHand(p) == best).ToList();
    }

    // DRY RUN — 2-way tie, deck has plenty of cards left:
    //   contenders = [Alice, Bob], both scored 13. Deck.Count(50) >= 2 -> enter loop.
    //   Alice draws a 3, Bob draws a 9 -> BestAmong re-scores -> only Bob is best now.
    //   contenders = [Bob], Count == 1 -> loop stops. Return [Bob]. One clean winner.
    //
    // DRY RUN — 3-way tie, only 1 card left in the deck:
    //   contenders.Count(3) > Deck.Count(1) -> "Deck.Count >= contenders.Count" is
    //   1 >= 3 -> FALSE. The loop body never runs at all.
    //   Return all 3, still tied -> they SHARE the win (the deck ran out).
    public override List<Player> Winners()
    {
        var contenders = BestAmong(Players);

        // SAY: "While more than one player is tied AND the deck can serve every
        //      one of them a card, deal one each and re-check just this pool.
        //      If the deck can't serve them all, I stop and they share the win —
        //      that's the exact rule, so I check Deck.Count BEFORE dealing,
        //      never after (dealing to only SOME of them would be unfair)."
        while (contenders.Count > 1 && Deck.Count >= contenders.Count)
        {
            foreach (var p in contenders)
                p.Hand.Add(Deck.Draw());          // extra card joins the hand permanently
            contenders = BestAmong(contenders);    // re-check ONLY the players still in the race
        }

        return contenders;   // 1 left = a real winner; >1 left = deck ran out, they share
    }
}

// THE RULE OF TWO, in code: when TWO scoring rules must coexist (not just replace one
// another), THAT is when you extract. Here scoring becomes a swappable delegate — one
// line to swap old vs new. Saying "I'd lift PointsOf into a strategy" earns credit even
// before you type it. Don't build this on the FIRST variant; build it on the SECOND.
// SAY: "Two scoring rules now need to coexist — that's my 'rule of two' moment:
//      I lift scoring into a swappable function instead of copy-pasting classes."
class StrategyScoredGame : HighScoreGame
{
    private readonly Func<Card, int> _score;
    public StrategyScoredGame(IEnumerable<string> names, Func<Card, int> score, int? seed = null)
        : base(names, seed: seed) { _score = score; }

    public override int PointsOf(Card card) => _score(card);   // the call site never changes
}


// ---- SELF-CHECKS for this game (run from Program.Main) -----------------------
static class HighScoreDemo
{
    public static void RunChecks()
    {
        Harness.Section("High Score game + mutations (each change in ONE place)");
        var q = new Card("Q", "D");
        var five5 = new Card("5", "D");
        var five5h = new Card("5", "H");

        var baseGame = new HighScoreGame(new[] { "A" });
        Harness.Check(baseGame.PointsOf(q) == 12, "default points: Q = 12 (strength+1)");

        var faces = new FaceCardsAreTenGame(new[] { "A" });
        Harness.Check(faces.PointsOf(q) == 10, "MUTATION 'J/Q/K=10' lands in PointsOf only");

        var dd = new DoubleDiamondsGame(new[] { "A" });
        Harness.Check(dd.PointsOf(five5) == 10 && dd.PointsOf(five5h) == 5,
                      "MUTATION 'diamonds double': 5D=10, 5H=5 — PointsOf only, display untouched");

        // Winners always returns a LIST (ties are real). Force a tie and prove two winners.
        var tieGame = new HighScoreGame(new[] { "X", "Y" });
        tieGame.Players[0].Hand.Add(new Card("K", "C"));   // 13
        tieGame.Players[1].Hand.Add(new Card("K", "D"));   // 13
        Harness.Check(tieGame.Winners().Count == 2, "ties are real: Winners() returns BOTH tied players");

        // 'Lowest wins' = Max->Min in Winners only.
        var low = new LowestWinsGame(new[] { "Lo", "Hi" });
        low.Players[0].Hand.Add(new Card("2", "C"));       // 2
        low.Players[1].Hand.Add(new Card("K", "C"));       // 13
        Harness.Check(low.Winners().Single().Name == "Lo", "MUTATION 'lowest wins' = Max->Min in Winners only");

        // MUTATION 'ties redraw' (M4): 2-way tie, deck has 50 cards left (plenty) ->
        // resolves to exactly one winner. We don't assert HOW MANY rounds it took
        // (that depends on the shuffle) — only the final invariant: one winner left.
        var tieBreak = new TieBreakDrawGame(new[] { "Alice", "Bob" }, seed: 5);
        tieBreak.Players[0].Hand.Add(new Card("K", "C"));   // 13
        tieBreak.Players[1].Hand.Add(new Card("K", "D"));   // 13 -> forced tie
        Harness.Check(tieBreak.Winners().Count == 1,
                      "MUTATION 'ties redraw': tie resolves to exactly one winner");

        // No tie at all -> the override still behaves like the base case: zero
        // draws, one winner, immediately. Proves the loop guard short-circuits.
        var noTie = new TieBreakDrawGame(new[] { "Win", "Lose" }, seed: 3);
        noTie.Players[0].Hand.Add(new Card("K", "C"));      // 13
        noTie.Players[1].Hand.Add(new Card("2", "C"));      // 2
        Harness.Check(noTie.Winners().Single().Name == "Win",
                      "MUTATION 'ties redraw': no tie -> resolves immediately, zero draws");

        // Deck EXHAUSTION path: drain the deck down to 1 card, then force a
        // 3-way tie. Deck.Count(1) < contenders.Count(3) -> the loop condition
        // is false before it ever runs -> they SHARE the win, exactly per the rule.
        var runsOut = new TieBreakDrawGame(new[] { "A", "B", "C" }, seed: 9);
        runsOut.Deck.Draw(51);                              // leaves exactly 1 card
        runsOut.Players[0].Hand.Add(new Card("K", "C"));    // 13
        runsOut.Players[1].Hand.Add(new Card("K", "D"));    // 13
        runsOut.Players[2].Hand.Add(new Card("K", "H"));    // 13 -> 3-way tie
        Harness.Check(runsOut.Winners().Count == 3,
                      "MUTATION 'ties redraw': deck can't serve everyone -> they SHARE the win");

        // Rule of two: two scorings coexist behind ONE call site via a delegate.
        var strat = new StrategyScoredGame(new[] { "A" }, c => c.IsJoker ? 20 : c.Strength + 1);
        Harness.Check(strat.PointsOf(new Card("JOKER", null)) == 20,
                      "RULE OF TWO: swap scoring via a delegate (extract on the SECOND variant)");

        // A full demo round — what Part 2 output actually looks like (seed 42 = deterministic).
        Harness.Section("Demo: a full High Score round");
        var game = new HighScoreGame(new[] { "Alice", "Bob", "Cara" }, seed: 42);
        game.Deal(5);
        foreach (var p in game.Players)
            Console.WriteLine($"  {p.Name,-6} score {game.ScoreHand(p),3}   {p.ShowHand()}");
        Console.WriteLine("  Winner(s): " + string.Join(", ", game.Winners().Select(w => w.Name)));
    }
}
