using System;
using System.Collections.Generic;
using System.Linq;

// #############################################################################
//  GAME SHAPE #6: TRICK TAKING LITE  (follow-suit + trump / Mock 6)
//
//  Leader plays a card; its suit is the LED suit. Others must FOLLOW SUIT if they can.
//  Highest card of the led suit wins — unless a TRUMP suit was set, which beats the led
//  suit. Legality lives in LegalCards; resolution lives in WinnerOfTrick.
// #############################################################################
sealed class Play { public Player Player; public Card Card; }

// #############################################################################
//  ★ SPOKEN SCRIPT — Trick Taking ★
//
//  SAY (restate): "The leader's card sets the led suit; everyone must follow
//       that suit if they can; the highest card of the led suit takes the
//       trick — unless a trump card was played."
//  ASK: "Does the trick winner lead the next trick?"
//  ASK: "Is a deterministic choice fine — always the lowest legal card?"
//  SAY (plan): "Plan: LegalCards owns follow-suit legality, WinnerOfTrick owns
//       resolution. Legality and resolution stay two separate methods."
// #############################################################################
static class TrickTaking
{
    // Follow-suit rule: if you HAVE the led suit you must play it; otherwise anything.
    // SAY: "If you hold the led suit you MUST play it — that legality rule lives
    //       here and nowhere else."
    public static List<Card> LegalCards(List<Card> hand, string ledSuit)
    {
        var following = hand.Where(c => c.Suit == ledSuit).ToList();
        return following.Count > 0 ? following : hand;
    }

    // Resolution: trump beats led; within the same "tier", highest strength wins.
    //
    // DRY RUN — WinnerOfTrick([Alice:7H, Dan:KH], ledSuit "H", trump null):
    //   tier(7H): not trump, suit==led "H" -> 1.   tier(KH): 1.  Both tier 1.
    //   OrderByDescending(tier) keeps both, ThenByDescending(strength): KH(str12) > 7H(str6).
    //   First() -> Dan's KH. Dan wins.
    // DRY RUN — same plays with trump "S": neither is a spade, tiers still 1 vs 1 -> KH still wins.
    //   But if Dan had played 2S instead: tier(2S)=2 > tier(7H)=1 -> the 2 of trump beats the 7 of led.
    // SAY: "Resolution works in TIERS: trump above led suit above everything
    //       else; within a tier the highest strength wins. Adding trump later
    //       touches only this method."
    public static Player WinnerOfTrick(List<Play> plays, string ledSuit, string trump)
    {
        // rank each play: trump = tier 2, led suit = tier 1, everything else = tier 0.
        // trump != null matters: without it, a joker's null suit would accidentally
        // match "no trump" and become tier 2.
        Func<Card, int> tier = c => trump != null && c.Suit == trump ? 2 : (c.Suit == ledSuit ? 1 : 0);
        return plays.OrderByDescending(p => tier(p.Card))
                    .ThenByDescending(p => p.Card.Strength)
                    .First().Player;
    }
}


// ---- SELF-CHECKS for this game (run from Program.Main) -----------------------
static class TrickTakingDemo
{
    public static void RunChecks()
    {
        Harness.Section("Trick taking: follow-suit legality + trump resolution");
        var hand = new List<Card> { new Card("2","H"), new Card("Q","S"), new Card("K","C") };
        Harness.Check(TrickTaking.LegalCards(hand, "H").Single().ToString() == "2H",
                      "follow suit: holding a heart, only the heart is legal");
        Harness.Check(TrickTaking.LegalCards(new List<Card>{ new Card("Q","S") }, "H").Count == 1,
                      "no led suit in hand -> anything is legal");

        var alice = new Player("Alice"); var dan = new Player("Dan");
        var plays = new List<Play> {
            new Play{ Player=alice, Card=new Card("7","H") },
            new Play{ Player=dan,   Card=new Card("K","H") },
        };
        Harness.Check(TrickTaking.WinnerOfTrick(plays, "H", null).Name == "Dan",
                      "no trump: highest of led suit (KH) wins the trick");

        var trumpPlays = new List<Play> {
            new Play{ Player=alice, Card=new Card("7","H") },
            new Play{ Player=dan,   Card=new Card("2","S") },
        };
        Harness.Check(TrickTaking.WinnerOfTrick(trumpPlays, "H", "S").Name == "Dan",
                      "MUTATION 'spades trump': 2S beats 7H because trump tier wins");
    }
}


// #############################################################################
//  ★ YOUR BUILD MISSION 5 — FULL TRICK-TAKING GAME (the real Mock 6 Part 2) ★
//
//  LegalCards and WinnerOfTrick above are the two rule homes — both finished
//  (you fixed the null-trump trap yourself). The mission is the game around
//  them: leading, following, scoring, rotating the leader.
//
//  THE STORY:
//    4 players, 5 cards each, 5 tricks. Player 0 leads trick 1. The first card
//    played sets the LED suit; everyone else must follow it if they can.
//    Highest card of the led suit takes the trick, scores 1 point, and LEADS
//    the next trick. After 5 tricks, most points wins (ties share).
//
//  STEP 1 — the strategy method (deterministic, per the mock):
//        Card ChooseCard(Player p, string ledSuit)
//    = the LOWEST legal card: LegalCards(...).OrderBy(c => c.Strength).First(),
//    then p.Hand.Remove(it) — find first, THEN remove (never inside a foreach).
//    For the LEADER ledSuit is null — decide: leader plays lowest card overall.
//    CHECK: hand [KH 2H QS], led H -> plays 2H (lowest legal, not KH, not QS).
//
//  STEP 2 — one trick = one method:
//        Player PlayTrick(int trickNo)
//    Leader plays first -> ledSuit = that card's suit. The other 3 follow in
//    seat order (AdvanceTurn-style wrap around the table). Collect the plays in
//    List<Play>, resolve with WinnerOfTrick, winner.Score++, print the trick,
//    return the winner (= next leader).
//    CHECK with forced 1-card hands: Alice 7H leads, Bob 2H, Cara QS, Dan KH
//    -> Dan wins (KH highest of led suit; QS is not led and not trump).
//
//  STEP 3 — the game:
//        class TrickGame { Players(4); Deck; Deal(5); int LeaderIndex;
//                          PlayAll() -> 5 tricks; Winners() by Score (a LIST) }
//    CHECK: after 5 tricks the four scores sum to exactly 5 (no trick vanished
//    or double-counted — the envelope check of this game).
//
//  PART 3 MUTATIONS:
//    [M1] Spades are trump -> pass "S" as trump. ALREADY WORKS — the check
//         above proves it (2S beats 7H). Legality does NOT change: you must
//         still follow the led suit if you can. Zero-edit mutation if your
//         PlayTrick takes trump as a parameter — design for that now.
//    [M2] Trump rotates per trick: C, D, H, S, repeat. Route: ONE helper,
//             string TrumpFor(int trickNo) => Suits.All[trickNo % 4];
//         and PlayTrick uses it. Never hard-code "S" in more than one place.
//         CHECK: trick 0 trump C, trick 3 trump S, trick 4 trump C again.
//    [M3] Aces HIGH for trick resolution. Same lesson as War M1: do NOT edit
//         the global Ranks.Order (Core checks break). Make the strength used by
//         WinnerOfTrick swappable data (a rank array the game owns, or a
//         Func<Card,int> strength parameter). One data move, zero logic edits.
//    [M4] Jokers: may ALWAYS be played (even when you could follow suit), count
//         as the HIGHEST trump; two jokers in one trick -> the FIRST one played
//         wins. Three routes, one edit each:
//           LegalCards     -> legal = following suit ? following + your jokers
//                             : whole hand  (a joker's Suit is null, so it is
//                             never inside `following` by accident — check it!)
//           WinnerOfTrick  -> jokers get a tier ABOVE trump (tier 3).
//           First-joker-wins -> comes FREE: OrderByDescending is a STABLE sort,
//                             equal keys keep play order. KNOW that word and
//                             say it — or add ThenBy(play order) explicitly.
//         CHECK: joker beats the ace of trump; two jokers -> first player wins.
//
//  TRAPS:
//    - The led suit is the suit of the FIRST CARD PLAYED, not the leader's
//      favorite suit, and (M4) a led JOKER means... ask! (Sane default: next
//      real card's suit leads; type your assumption as a comment.)
//    - Seat order around the table keeps going clockwise from the leader —
//      the leader CHANGES each trick, the seat order never does.
//
//  DONE = static class TrickGameDemo { public static void RunChecks() },
//  uncomment in Program.Main, all green, ask Claude for the review.
// #############################################################################
