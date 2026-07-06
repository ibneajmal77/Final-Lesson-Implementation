using System;
using System.Collections.Generic;
using System.Linq;

// #############################################################################
//  GAME SHAPE #3: BEST HAND  (classification / Mock 3 — the hardest)
//
//  Deal 5, classify (Three of a Kind > One Pair > High Card), compare category then
//  the defining rank. THE core trick: GroupBy(Rank) then look at group SIZES.
//
//  Category strength is kept as an ORDERED LADDER in data, so inserting "Two Pair"
//  later is renumbering one line, not rewriting comparisons.
//
//  "Jokers are wild" — the PEARLS MOVE: don't special-case the detection code. A
//  joker just changes what the rank groups LOOK like. So PRE-PROCESS the hand (joker
//  becomes a copy of your most frequent rank), then run the UNCHANGED classifier.
// #############################################################################
// #############################################################################
//  ★ SPOKEN SCRIPT — Best Hand ★
//
//  SAY (restate): "I classify each five-card hand — three of a kind beats a
//       pair beats high card — then compare category first, then the rank that
//       formed the category."
//  ASK: "If category AND that rank tie — shared win, or compare the next cards?"
//  ASK: "Ace low here as well?"
//  SAY (plan): "Plan: ONE Classify method built on GroupBy — group sizes reveal
//       pairs and trips — returning a comparable result. Printing stays separate."
// #############################################################################
sealed class HandResult
{
    public string Category;
    public int CategoryStrength;      // ladder position (higher = better)
    public int DefiningRank;          // strength of the rank forming the best group
    public int Kicker;                // highest leftover card, for same-category ties
    public List<int> TieBreakers;     // full compare path, highest priority first
}

static class BestHand
{
    // The category LADDER as data. Insert "Two Pair" here later = one edit.
    // index = strength.  0 High Card, 1 One Pair, 2 Three of a Kind.
    private static readonly string[] Ladder = { "High Card", "One Pair", "Three of a Kind" };

    // DRY RUN — Classify([7H, 7S, 7D, QC, 2H]):
    //   MakeJokersWild: no joker -> hand unchanged.
    //   GroupBy(Rank) -> { "7":3 cards, "Q":1, "2":1 }.
    //   Projected + sorted by size desc: [ {7,size3,str6}, {Q,size1,str11}, {2,size1,str1} ].
    //   groups[0].Size = 3 -> cat = 2 ("Three of a Kind").
    //   defining = groups[0].Str = 6 (the 7's strength).
    //   leftover groups are Q then 2, so kicker = 11 (Q).
    //   TieBreakers = [6,6,6,11,1]: first compare the trip rank, then the leftovers.
    //   -> HandResult{ "Three of a Kind", CatStrength 2, DefiningRank 6, Kicker 11 }.
    // SAY: "GroupBy rank, then look at group SIZES: a group of three is trips, a
    //       group of two is a pair. The category ladder is data, so inserting a
    //       new category later is one edit, not surgery."
    public static HandResult Classify(IEnumerable<Card> handIn)
    {
        // PEARLS MOVE: replace jokers with a copy of the most frequent real rank first.
        var hand = MakeJokersWild(handIn.ToList());

        var groups = hand.GroupBy(c => c.Rank)                       // GroupBy = pairs/trips in ONE call
                         .Select(g => new { Rank = g.Key, Size = g.Count(), Str = Ranks.Strength(g.Key) })
                         .OrderByDescending(g => g.Size).ThenByDescending(g => g.Str)
                         .ToList();

        int cat = groups[0].Size >= 3 ? 2 : (groups[0].Size == 2 ? 1 : 0);
        int defining = groups[0].Str;

        // TieBreakers is the full "compare recipe" after category.
        // Written as rank labels, the order is:
        //   Pair of 7s with Q,9,2 -> [7,7,Q,9,2].
        //   Pair of 7s with 9,5,2 -> [7,7,9,5,2].
        // In the list itself those labels are stored as numeric rank strengths.
        // The pair ranks tie, then Q beats 9. This prevents the common bug where
        // same-category hands compare only one card and miss the next kicker.
        var tieBreakers = groups.SelectMany(g => Enumerable.Repeat(g.Str, g.Size)).ToList();
        int kicker = tieBreakers.Skip(groups[0].Size).DefaultIfEmpty(defining).First();

        return new HandResult
        {
            Category = Ladder[cat],
            CategoryStrength = cat,
            DefiningRank = defining,
            Kicker = kicker,
            TieBreakers = tieBreakers
        };
    }

    // DRY RUN — MakeJokersWild([7H, 7S, JOKER, QD, 2C]):
    //   real ranks: 7,7,Q,2 -> most frequent = "7". Joker becomes new Card("7","*").
    //   returned hand groups as 7:3 -> the UNCHANGED classifier then reports Three of a Kind.
    // SAY: "For wild jokers I preprocess the HAND — the joker becomes a copy of
    //       my most frequent rank — and the classifier itself stays untouched.
    //       A full optimizer would try every rank; I'll note that trade-off and
    //       move on."
    private static List<Card> MakeJokersWild(List<Card> hand)
    {
        if (!hand.Any(c => c.IsJoker)) return hand;
        var real = hand.Where(c => !c.IsJoker).ToList();
        if (real.Count == 0) return hand;
        // most frequent real rank (ties -> strongest)
        string best = real.GroupBy(c => c.Rank)
                          .OrderByDescending(g => g.Count()).ThenByDescending(g => Ranks.Strength(g.Key))
                          .First().Key;
        return hand.Select(c => c.IsJoker ? new Card(best, "*") : c).ToList();
    }

    // Comparing COMPOSITE results: category, then defining rank, then kicker.
    public static int Compare(HandResult x, HandResult y)
    {
        if (x.CategoryStrength != y.CategoryStrength) return x.CategoryStrength.CompareTo(y.CategoryStrength);
        if (x.DefiningRank != y.DefiningRank) return x.DefiningRank.CompareTo(y.DefiningRank);

        // Walk every tie-break card in order. Return as soon as one differs.
        // If all tie-breakers match, the hands are truly tied.
        int n = Math.Min(x.TieBreakers.Count, y.TieBreakers.Count);
        for (int i = 0; i < n; i++)
            if (x.TieBreakers[i] != y.TieBreakers[i])
                return x.TieBreakers[i].CompareTo(y.TieBreakers[i]);

        return x.TieBreakers.Count.CompareTo(y.TieBreakers.Count);
    }
}


// ---- SELF-CHECKS for this game (run from Program.Main) -----------------------
static class BestHandDemo
{
    public static void RunChecks()
    {
        Harness.Section("Best Hand: classify via GroupBy, compare composite, jokers wild");
        var trips = BestHand.Classify(new[] { new Card("7","H"), new Card("7","S"), new Card("7","D"),
                                              new Card("Q","C"), new Card("2","H") });
        Harness.Check(trips.Category == "Three of a Kind" && trips.DefiningRank == Ranks.Strength("7"),
                      "classify: three 7s -> Three of a Kind, defining rank 7");

        var pair = BestHand.Classify(new[] { new Card("7","H"), new Card("7","S"), new Card("Q","D"),
                                             new Card("2","C"), new Card("9","H") });
        Harness.Check(BestHand.Compare(trips, pair) > 0, "composite compare: trips beat a pair");

        var weakerPair = BestHand.Classify(new[] { new Card("7","C"), new Card("7","D"), new Card("9","D"),
                                                   new Card("5","C"), new Card("2","H") });
        Harness.Check(BestHand.Compare(pair, weakerPair) > 0,
                      "edge case: same pair rank -> compare kickers in order (Q beats 9)");

        // Joker wild: a joker + two 7s should classify as Three of a Kind (Pearls preprocessing).
        var wild = BestHand.Classify(new[] { new Card("7","H"), new Card("7","S"), new Card("JOKER",null),
                                             new Card("Q","D"), new Card("2","C") });
        Harness.Check(wild.Category == "Three of a Kind",
                      "MUTATION 'jokers wild' = preprocess hand, run UNCHANGED classifier");
    }
}


// #############################################################################
//  ★ YOUR BUILD MISSION 2 — GROW BEST HAND INTO THE FULL MOCK 3 GAME ★
//
//  Your TieBreakers fix already solved the hardest part (same-category compare).
//  Three things remain: two new categories, and the game wrapper around it all.
//
//  MICRO-CLEANUPS FIRST (2 minutes, from Claude's review):
//    - In Compare(): the DefiningRank comparison is now redundant — it always
//      equals TieBreakers[0]. Either delete it or add a comment saying you know.
//    - The final `Count.CompareTo(Count)` line can simply be `return 0;`
//      (hands in one game always have equal size).
//
//  STEP 1 — [M1] TWO PAIR (between One Pair and Three of a Kind).
//    Detection: after the GroupBy sort, a Two Pair is simply
//        groups[0].Size == 2 && groups[1].Size == 2
//    Insert "Two Pair" into the Ladder array, THEN make the category lookup
//    survive future insertions: build the category NAME first, and derive the
//    number from the data instead of hard-coding 2/1/0:
//        string name = ...decide by group sizes...;
//        int cat = Array.IndexOf(Ladder, name);
//    CHECKS (write them first, watch them fail):
//        K K 4 4 2  -> "Two Pair"
//        Two Pair beats One Pair; Three of a Kind beats Two Pair
//        K K 4 4 x  vs  K K 3 3 x  -> first wins (TieBreakers already handles
//        it: [12,12,3,3,..] vs [12,12,2,2,..] — say WHY out loud).
//
//  STEP 2 — [M2] FLUSH (all 5 same suit) — beats everything.
//    Detection is one LINQ line on the ORIGINAL hand:
//        hand.All(c => c.Suit == hand[0].Suit)
//    Put "Flush" at the TOP of the Ladder. Check: 5 hearts -> Flush; Flush
//    beats Three of a Kind.
//    TRAP (say this aloud in the interview): the joker-wild replacement card
//    was created with suit "*", and a real joker has NO suit — so decide the
//    simplification: "a joker never helps a flush" is the safe default; state
//    it as an assumption and move on. A check should pin your choice down:
//        7H 8H 9H JH JOKER -> NOT a Flush (under the stated assumption).
//
//  STEP 3 — the game wrapper (the actual Part 2 deliverable!).
//        class FullBestHandGame { Players; Deck; Deal(5); Winners() }
//    Winners() = classify every player's hand, keep everyone whose result
//    compares equal to the best (ties share the win — reuse BestHand.Compare).
//    Print each player like the mock demands:
//        Bob:  7H 7S 7D QC 2H  ->  Three of a Kind (7)
//    (Display the defining rank as its LABEL — Ranks.Order[defining] — not the
//    number 6. Display bugs are the most common silent point-loss.)
//    CHECK with forced hands (inject into Hand like HighScoreDemo does):
//    trips beat two-pair beats pair beats high card, and a forced exact tie
//    returns BOTH players.
//
//  DONE = static class FullBestHandDemo { public static void RunChecks() },
//  uncomment its call in Program.Main, all green, then ask Claude for review.
// #############################################################################
