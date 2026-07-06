using System;
using System.Collections.Generic;
using System.Linq;

// #############################################################################
//  GAME SHAPE #5: CRAZY EIGHTS LITE  (legality predicate / Mock 5)
//
//  Play a card matching the top card's RANK or SUIT, else draw. The whole game hinges
//  on ONE predicate: IsPlayable(card, top, currentSuit). Wild 8s and jokers are just
//  branches at the TOP of that predicate. Turn rotation (index + direction) lives in
//  ONE place so "reverse direction" is a one-line change.
//
//  C# TRAP shown: never remove from a List you're foreach-ing. Find, then remove.
// #############################################################################
// #############################################################################
//  ★ SPOKEN SCRIPT — Crazy Eights ★
//
//  SAY (restate): "On your turn, play a card matching the top card's rank or
//       suit; if you can't, draw one card; first empty hand wins."
//  ASK: "If the drawn card is playable, do I play it immediately?"
//  ASK: "What happens when the draw pile runs out?"
//  SAY (plan): "Plan: ONE IsPlayable predicate owns all matching; TakeTurn owns
//       one player's action; turn movement lives in one AdvanceTurn helper."
// #############################################################################
static class CrazyEights
{
    // currentSuit = the effective suit (differs from top.Suit only after a wild 8 chose one).
    // SAY: "The whole game hangs on this one predicate — wild 8s and jokers are
    //       just branches at the TOP of it, not scattered if-statements."
    public static bool IsPlayable(Card card, Card top, string currentSuit)
    {
        if (card.Rank == "8") return true;                 // wild: branch at the top
        if (card.IsJoker) return true;                     // treat joker as always playable
        return card.Rank == top.Rank || card.Suit == currentSuit;
    }

    // SAY: "I FIND the card first and remove it after — never remove from a list
    //       you are still iterating; that's a classic C# runtime crash."
    public static Card ChooseFirstLegal(IEnumerable<Card> hand, Card top, string currentSuit)
        => hand.FirstOrDefault(c => IsPlayable(c, top, currentSuit));   // may be null -> then draw

    // Turn rotation in ONE place. direction is +1 or -1; "reverse" just flips its sign.
    //
    // DRY RUN — AdvanceTurn(2, 3, +1):  (2+1)=3; 3%3=0; (0+3)=3; 3%3=0 -> 0. Player 2 -> player 0 (wraps).
    // DRY RUN — AdvanceTurn(0, 3, -1):  (0-1)=-1; -1%3=-1; (-1+3)=2; 2%3=2 -> 2. Player 0 -> player 2.
    //   The double-mod ( %count + count )%count is what makes -1 wrap correctly instead of going negative.
    // SAY: "Turn movement lives in ONE helper. The double-mod keeps -1 wrapping
    //       correctly, so 'reverse direction' later is just flipping a sign."
    public static int AdvanceTurn(int index, int count, int direction)
        => ((index + direction) % count + count) % count;   // wraps safely for -1 too
}


// ---- SELF-CHECKS for this game (run from Program.Main) -----------------------
static class CrazyEightsDemo
{
    public static void RunChecks()
    {
        Harness.Section("Crazy Eights: IsPlayable predicate + turn rotation");
        var top = new Card("9", "H");
        Harness.Check(CrazyEights.IsPlayable(new Card("5","H"), top, "H"), "5H playable on 9H (matches SUIT)");
        Harness.Check(CrazyEights.IsPlayable(new Card("9","D"), top, "H"), "9D playable on 9H (matches RANK)");
        Harness.Check(!CrazyEights.IsPlayable(new Card("2","C"), top, "H"), "2C NOT playable on 9H");
        Harness.Check(CrazyEights.IsPlayable(new Card("8","C"), top, "H"), "MUTATION '8s wild' = a branch at the top");
        Harness.Check(CrazyEights.AdvanceTurn(2, 3, 1) == 0, "turn rotation wraps 2 -> 0 of 3");
        Harness.Check(CrazyEights.AdvanceTurn(0, 3, -1) == 2, "MUTATION 'reverse' = flip direction sign, one place");
    }
}


// #############################################################################
//  ★ YOUR BUILD MISSION 4 — FULL CRAZY EIGHTS (the real Mock 5 Part 2) ★
//
//  This is the BIGGEST build of the five: a real turn machine. IsPlayable and
//  AdvanceTurn above are your two finished parts — the mission is the machine
//  around them. Budget a full 60-minute session for this one.
//
//  THE STORY:
//    3 players, 5 cards each. One card is flipped to start the discard pile.
//    On your turn: play one card matching the top's rank or suit. If you have
//    several, play the FIRST in your hand. If none: draw ONE card — if it is
//    playable, play it immediately, otherwise keep it. First empty hand wins.
//    Safety stop after 30 turns: fewest cards wins (ties possible).
//
//  STEP 1 — the state (this game is 90% state discipline):
//        class CrazyEightsGame
//        {
//            List<Player> Players; Deck Deck;
//            List<Card> Discard;           // top = Discard[Discard.Count - 1]
//            string CurrentSuit;           // usually top.Suit; differs after a wild 8
//            int Current; int Direction;   // whose turn + which way (+1/-1)
//            int PendingDraw; bool PendingSkip;   // penalties waiting for next player
//        }
//    Setup: deal 3x5, flip one starter card, CurrentSuit = starter.Suit.
//    CHECK: everyone has 5, discard has 1, deck has 52-15-1 = 36.
//
//  STEP 2 — one turn = ONE method, and this exact order inside it:
//        void TakeTurn()
//          1. serve penalties FIRST (if PendingSkip: clear it, advance, return;
//             if PendingDraw > 0: draw that many, clear it, advance, return)
//          2. find the card: hand.FirstOrDefault(c => IsPlayable(c, Top, CurrentSuit))
//             C# TRAP the mock names: NEVER remove inside a foreach over the
//             hand. FirstOrDefault first, THEN hand.Remove(card).
//          3. if found: remove from hand, add to Discard, update CurrentSuit
//          4. else: if Deck.Count > 0 draw one; if THAT card is playable, play
//             it (same path as 3), else keep it
//          5. print the turn line, then Current = AdvanceTurn(Current, n, Direction)
//    CHECK with forced hands: top 9H, hand [2C 5H QS 9D] -> plays 5H (first
//    match), hand count drops to 3, discard top is now 5H.
//
//  STEP 3 — the loop + winner:
//        while nobody's hand is empty && turns < 30 -> TakeTurn()
//        Winner(s): empty hand, else fewest cards — return a LIST (ties!).
//
//  PART 3 MUTATIONS (each is small IF steps 1-2 are clean):
//    [M1] 8s are WILD (IsPlayable already allows them — look!). What is missing
//         is CHOOSING the suit after playing an 8: pick the suit you hold most
//         of; tie -> C, then D, then H, then S. Route: one ChooseSuit(hand)
//         method + the CurrentSuit update in step 3 of TakeTurn.
//         CHECK: hand [8C 5H 7H] plays 8 -> CurrentSuit becomes "H".
//         TRAP: ties must follow Suits.All order — GroupBy + OrderBy count desc,
//         then by Array.IndexOf(Suits.All, suit) asc.
//    [M2] Jokers: always playable (already true — look again!), and the next
//         player SKIPS. Route: Deck flag + set PendingSkip when a joker lands.
//         TRAP: the joker has NO suit — do not assign CurrentSuit = null; keep
//         the previous CurrentSuit (decide + say it + type the comment).
//    [M3] A played 2 forces next player: draw two, lose turn. Route: PendingDraw
//         += 2 — you already built the pending mechanism in step 2.1, so this
//         mutation is ONE line. That is the payoff of penalties-as-state.
//    [M4] A played Q reverses direction. Route: Direction = -Direction. Your
//         AdvanceTurn already wraps negative — the check exists above.
//
//  TRAPS THAT COST POINTS:
//    - Deck runs empty: stop drawing, players who cannot play just pass.
//      State the policy out loud; guard Deck.Count.
//    - The starter flip could be an 8: mock says accept it, no special rule.
//    - Penalties apply to the NEXT player only, once — clear them after serving.
//
//  DONE = static class CrazyEightsGameDemo { public static void RunChecks() }
//  with forced-hand checks + one full printed 3-player demo (seeded). Uncomment
//  in Program.Main, all green, ask Claude for the review.
// #############################################################################
