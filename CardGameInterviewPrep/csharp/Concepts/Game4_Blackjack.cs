using System;
using System.Collections.Generic;
using System.Linq;

// #############################################################################
//  GAME SHAPE #4: BLACKJACK LITE  (soft ace / Mock 4)
//
//  Get close to a target (21) without going over. The one tricky rule is the SOFT
//  ACE: an ace is 1 OR 11. Put that logic in ONE method, BestTotal(hand): count all
//  aces as 11, then drop 10 per ace while you're busting. Target is a FIELD, never a
//  magic number, so "target becomes 24" is a one-line change.
// #############################################################################
// #############################################################################
//  ★ SPOKEN SCRIPT — Blackjack ★
//
//  SAY (restate): "Get as close to 21 as possible without going over; an ace
//       counts 1 or 11, whichever is better; both sides draw until at least 17."
//  ASK: "Does the dealer stand on exactly 17?"
//  ASK: "If both bust — nobody wins?"
//  SAY (plan): "Plan: BasePoints for one card, BestTotal owning ALL the ace
//       logic, and the target as a named field — never a magic number."
// #############################################################################
class Blackjack
{
    public int Target { get; }
    public Blackjack(int target = 21) { Target = target; }

    // Base value: number = face value; J/Q/K = 10; A counted as 11 up front; JOKER = 0.
    // SAY: "I handle the NAMED ranks before int.Parse, so a JOKER or a face card
    //       can never reach the parser and crash."
    public int BasePoints(Card c)
    {
        if (c.IsJoker) return 0;
        if (c.Rank == "A") return 11;
        if (c.Rank == "J" || c.Rank == "Q" || c.Rank == "K") return 10;
        return int.Parse(c.Rank);
    }

    // The soft-ace rule, isolated in ONE method.
    // DRY RUN — BestTotal([AH, 6D]), Target 21:
    //   BasePoints: A=11, 6=6 -> total = 17. aces = 1.
    //   while (17 > 21)? no -> loop skipped. return 17.  (The ace stayed "soft" at 11.)
    //
    // DRY RUN — BestTotal([AH, AS, 9D]), Target 21:
    //   BasePoints: 11 + 11 + 9 = 31. aces = 2.
    //   while (31 > 21 && aces>0): total=21, aces=1  -> now (21 > 21)? no -> stop. return 21.
    //   One ace counts as 11, the other dropped to 1. Exactly the "soft ace" behaviour.
    // SAY: "The soft-ace rule, isolated in ONE method: count every ace as 11
    //       first, then drop 10 per ace while I'm still over the target."
    public int BestTotal(IEnumerable<Card> hand)
    {
        var cards = hand.ToList();
        int total = cards.Sum(BasePoints);
        int aces = cards.Count(c => c.Rank == "A");
        while (total > Target && aces > 0) { total -= 10; aces--; }  // 11 -> 1 as needed
        return total;
    }

    public bool IsBust(IEnumerable<Card> hand) => BestTotal(hand) > Target;
}


// ---- SELF-CHECKS for this game (run from Program.Main) -----------------------
static class BlackjackDemo
{
    public static void RunChecks()
    {
        Harness.Section("Blackjack: soft-ace logic isolated in BestTotal");
        var bj = new Blackjack();
        Harness.Check(bj.BestTotal(new[] { new Card("A","H"), new Card("6","D") }) == 17, "A+6 = 17 (ace as 11)");
        Harness.Check(bj.BestTotal(new[] { new Card("A","H"), new Card("K","D") }) == 21, "A+K = 21 (blackjack)");
        Harness.Check(bj.BestTotal(new[] { new Card("A","H"), new Card("A","S"), new Card("9","D") }) == 21,
                      "A+A+9 = 21 (one ace 11, one ace 1)");
        Harness.Check(bj.IsBust(new[] { new Card("K","H"), new Card("Q","D"), new Card("5","C") }),
                      "K+Q+5 = 25 -> bust");
        Harness.Check(new Blackjack(target: 24).Target == 24, "MUTATION 'target 24' = a FIELD, not a magic number");
    }
}


// #############################################################################
//  ★ YOUR BUILD MISSION 3 — FULL BLACKJACK ROUND (the real Mock 4 Part 2) ★
//
//  BestTotal above is the brain. Mock 4 wants a whole ROUND around it: deal,
//  two hit loops, and a winner ruling. Keep the Blackjack class untouched;
//  build the round machine next to it and let it USE bj.BestTotal(...).
//
//  THE STORY:
//    Player and Dealer each get 2 cards (alternating, one at a time).
//    Player draws until their best total reaches at least 17. Dealer the same.
//    Bust = total over 21. Both bust: nobody wins. One busts: the other wins.
//    Neither busts: higher total wins; equal totals tie.
//
//  STEP 1 — the round class.
//        class BlackjackRound
//        {
//            Blackjack Rules;              // has-a: Target lives in ONE place
//            List<Card> PlayerHand; List<Card> DealerHand;
//            Deck Deck;
//            BlackjackRound(int? seed = null, int target = 21)
//        }
//    Deal 2 each, alternating: player, dealer, player, dealer.
//    CHECK: both hands have 2 cards; deck has 48 left.
//
//  STEP 2 — the hit policy, as its own tiny method (rule home!):
//        bool ShouldHit(List<Card> hand) => Rules.BestTotal(hand) < 17;
//        void PlayOut(List<Card> hand) { while (ShouldHit(hand)) hand.Add(Deck.Draw()); }
//    Keep 17 as a named field (StandAt) — you already know why (M4 below).
//    CHECK with forced hands (test ctor or public hands): a hand of 10,6 draws
//    at least once; a hand of 10,7 stands.
//
//  STEP 3 — the ruling, in ONE method:
//        string Winner()
//    Order of the rules MATTERS — write them top-down:
//        both bust -> "nobody"; player bust -> "Dealer"; dealer bust -> "Player";
//        higher BestTotal wins; equal -> "tie".
//    CHECK all five branches with forced hands. Five checks, one minute each.
//
//  PART 3 MUTATIONS (routes only — you write the edits):
//    [M1] Dealer hits on SOFT 17. Soft = the total is 17 AND at least one ace
//         is currently counted as 11. Detect it with arithmetic, no new state:
//         the LOWEST possible total counts every ace as 1, i.e.
//             int lowest = cards.Sum(BasePoints) - 10 * aceCount;
//         If BestTotal(hand) != lowest, an ace is still being counted as 11,
//         so the hand is SOFT. Add IsSoft(hand) to the Blackjack class (it owns
//         all ace logic), then only the DEALER's hit rule changes:
//             total < 17 || (total == 17 && IsSoft(hand))
//         CHECK: A+6 (soft 17) -> dealer hits; 10+7 (hard 17) -> dealer stands.
//    [M2] 5-CARD CHARLIE: any non-busted hand with 5+ cards wins immediately.
//         Route: Winner() ONLY — new rule at the TOP of the ruling order (after
//         the bust checks — a busted 5-card hand is still busted; ask if unsure,
//         then type your assumption as a comment).
//         CHECK: 5 small cards (e.g. 2,2,3,4,5 = 16) beats a dealer 21.
//    [M3] Jokers in the deck, worth 0, never soft. BasePoints already returns 0
//         for jokers (look at it!) and IsSoft counts ACES, not jokers — so the
//         route is: Deck flag only. Add the check: JOKER+A+6 is still 17, soft.
//    [M4] Target 24, dealer still stands hard 17 / hits soft 17. If Target and
//         StandAt are fields, this is ONE constructor argument. If it takes more
//         than 2 edits, a constant leaked — hunt it, say so, fix it.
//
//  TRAPS:
//    - Deck can empty during a hit loop -> Draw() throws. Decide the policy out
//      loud (stop hitting is fine for the mock), guard with Deck.Count > 0.
//    - Never compute totals inline anywhere — every total goes through
//      BestTotal, or M1/M4 will make you hunt duplicates.
//
//  DONE = static class BlackjackRoundDemo { public static void RunChecks() },
//  uncomment in Program.Main, all green, ask Claude for the review.
// #############################################################################
