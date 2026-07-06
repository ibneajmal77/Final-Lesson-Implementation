using System;

// =============================================================================
//  THE COMPLETE GUIDE — EXPLAINED IN CODE   (orchestrator)
//
//  The concepts are split across files so you can study ONE game at a time — the
//  same "banner-comment-as-a-file" habit you'd use in the real single-file exam:
//
//     Core.cs             — Harness, Ranks, Suits, Card, Deck, Player + domain/deck/LINQ checks
//     Game1_HighScore.cs  — HighScoreGame + its mutations + a demo round
//     Game2_War.cs        — WarGame (comparator + round loop)
//     Game3_BestHand.cs   — classification via GroupBy + jokers-wild
//     Game4_Blackjack.cs  — soft-ace BestTotal
//     Game5_CrazyEights.cs— IsPlayable predicate + turn rotation
//     Game6_TrickTaking.cs— follow-suit legality + trump resolution
//     Program.cs          — THIS file: runs every game's own checks in order
//
//  Run it:   cd csharp/Concepts   &&   dotnet run
//
//  THE ONE IDEA everything serves:
//    You build a card game while rules keep changing. You win by putting EACH RULE
//    IN EXACTLY ONE PLACE, so every change is a one-line edit — not a rewrite.
//
//  ─────────────────────────────────────────────────────────────────────────────
//  ★ THE SPOKEN SCRIPT — how to use the // SAY: and // ASK: markers ★
//
//  Every file now carries the words to SPEAK while typing that code:
//     // ASK:  a clarifying question — ask these BEFORE coding that part.
//     // SAY:  narration — speak it right before/while typing the code below it.
//  Practice rule for today: in every drill, read the SAY lines OUT LOUD as you
//  type. By tomorrow they come out of your mouth on their own.
//
//  OPENING (first 60 seconds — do not spend longer):
//    SAY: "Hi, I'm <name>, I build .NET services. I'm ready — can I see Part 1?"
//
//  EVERY PART, the same 6 moves, spoken:
//    1. SAY: "Let me restate it: <one sentence>. Did I get that right?"
//    2. ASK: at most 3 questions that change what you build (see each file).
//    3. SAY: "My plan: <the 2-4 methods you will write>. Starting now."
//    4. Type — narrating with the SAY lines — and RUN every 2-3 minutes.
//    5. SAY: "Let me prove it." -> add a Check, run it, point at the PASS line.
//    6. SAY: "Done. With more time I'd <one improvement>. Next part?"
//
//  EVERY RULE CHANGE in Part 3 — the R5 ritual, spoken:
//    SAY: "So the rule is now: <restate it>."
//    SAY: "That's a <scoring / ordering / winner / legality / turn> rule,
//          so it lives in <method> — nothing else should change."
//    SAY: "First I update the check so it FAILS under the new rule..."  (run: red)
//    SAY: "...now the small fix..."                                     (type)
//    SAY: "...and we're green again."                                   (run: PASS)
//
//  IF STUCK (never be silent for 2 minutes):
//    SAY: "I don't remember the exact API — 30 seconds on learn.microsoft.com."
//         (documentation and Google are ALLOWED — using them fast is GRADED WELL)
//    SAY: "I'll write the simple version first and improve it if time allows."
//  ─────────────────────────────────────────────────────────────────────────────
//
//  HOW TO BUILD ANY CARD GAME LOGIC IN THE INTERVIEW:
//
//    1. Name the state first.
//       Ask: what objects must survive between actions?
//       Usually: Deck, Player list, each player's Hand, discard pile, current top card,
//       current turn index, direction, scores, trump suit, or target score.
//
//    2. Name ONE action.
//       Do not try to solve the whole game at once. Pick the smallest repeated move:
//       Deal one card, play one card, compare two cards, resolve one trick, or finish
//       one round. Then loop that action.
//
//    3. Put every rule in a small "rule home" method.
//       Scoring rule       -> PointsOf / ScoreHand / BestTotal
//       Can I play this?   -> IsPlayable / LegalCards
//       Who wins this?     -> CompareCards / Winners / WinnerOfTrick
//       Card order         -> Ranks.Order / Suits.Strength
//       Turn movement      -> AdvanceTurn
//
//    4. Handle Part 2 and Part 3 by routing the change, not rewriting.
//       "Aces high"             -> change rank order data.
//       "Faces are 10"          -> change PointsOf.
//       "Lowest score wins"     -> change Winners.
//       "8s are wild"           -> add one branch in IsPlayable.
//       "Spades are trump"      -> add one tier in WinnerOfTrick.
//       "Same pair, compare next card" -> add ordered tie-breakers in BestHand.
//
//    5. Test every rule with tiny forced hands.
//       Do not wait for random shuffles to prove logic. Create the exact cards that
//       hit the case: tie, empty deck, same pair with different kickers, trump beating
//       led suit, reverse turn wrapping from 0 to the last player.
//
//    6. Say this out loud while coding:
//       "I am going to put this rule in one method, prove it with a small check, then
//       reuse it from the larger game loop." That is the clean-code signal they want.
// =============================================================================


// =============================================================================
//  ★★★  COMPLETE PROGRAM DRY RUN  ★★★   (read this first — it traces the WHOLE run)
//
//  This is what happens, step by step, when you type `dotnet run`. Follow the values.
//  Every line below is proven by a matching PASS in the real output.
//
//  Main() prints the title, then calls each *.RunChecks() in order:
//
//  CoreConcepts.RunChecks()
//   1) DOMAIN
//      Ranks.Strength("Q") -> IndexOf in [A,2,..,K,JOKER] -> 11. Strength("7") -> 6.
//          11 > 6  => "Q beats 7"  ............................... PASS
//      Strength("A")=0 < Strength("2")=1 => ace is LOW ........... PASS
//      Strength("JOKER")=13 > Strength("K")=12 .................. PASS
//      Card("Q","D").ToString(): not joker -> "Q"+"D" = "QD" .... PASS
//      Card("JOKER",null).ToString(): IsJoker -> "JOKER" ....... PASS
//      RanksAceHigh.Strength("A")=12 > "K"=11 (a DIFFERENT array) PASS
//   2) DECK
//      new Deck().Count = 4x13 = 52; +jokers 54; deckCount 2 ->104; strip "2" ->48  PASS
//      deck(seed 42).Draw(5): 52 -> 47 (draw from END) ......... PASS
//      empty deck Draw() THROWS -> caught -> threw=true ........ PASS
//   9) LINQ on [7H,7S,QD,2C,9H]
//      Sum(strength+1)=37; Count(H)=2; All(H)=false; GroupBy finds a size-2 group;
//      OrderBy(strength) -> "2 7 7 9 Q" (a view; the hand is untouched) ......... PASS
//
//  HighScoreDemo.RunChecks()
//      baseGame.PointsOf(QD)=12; faces->10; diamonds double 5D->10, 5H->5;
//      forced K/K tie -> Winners() returns 2; lowest-wins picks "Lo";
//      MUTATION 'ties redraw' (M4): forced tie -> resolves to 1 winner; no tie ->
//      resolves immediately; deck drained to 1 card + 3-way tie -> all 3 SHARE;
//      delegate scoring: PointsOf(JOKER)=20. Then prints a full dealt round. ..... PASS
//
//  WarDemo.RunChecks()
//      CompareCards(QH,9D) -> +1; suit tie-break 5S>5C -> +1; 5S vs 5S -> 0
//      (rank AND suit equal stays a tie — tie-breakers must not invent a winner);
//      war [K,2] vs [3,A]: round1 K>3, round2 2>A (ace LOW!) -> "A" wins ......... PASS
//
//  FullWarDemo.RunChecks()  (Mission 1 — the full Mock 2 game, all 4 mutations)
//      setup: 52 cards -> 26/26 draw piles; default tie -> both discarded;
//      MUTATION aces-high: A's ace beats B's king (local rank data only);
//      MUTATION war: tied flips -> facedown+flip -> winner takes all 6;
//      TRAP: a player who can't cover a war (<2 cards) loses instantly;
//      MUTATION suit-breaks-ties (replaces war): 5S beats 5C, no war triggered;
//      two jokers collide under suit-tie-break -> both discarded, no crash;
//      play-until-empty + jokers: piles drain to 0, envelope check holds ........ PASS
//
//  BestHandDemo.RunChecks()
//      Classify(7,7,7,Q,2) -> Three of a Kind, defining 7; trips beat a pair;
//      pair 7s + Q,9,2 beats pair 7s + 9,5,2 (TieBreakers walk: Q > 9 kicker);
//      Classify(7,7,JOKER,Q,2): joker becomes a 7 -> Three of a Kind ............ PASS
//
//  BlackjackDemo.RunChecks()
//      BestTotal(A,6)=17; A,K=21; A,A,9 -> 31 drops one ace -> 21; K,Q,5 busts;
//      Blackjack(24).Target==24 (a field, not a magic number) .................. PASS
//
//  CrazyEightsDemo.RunChecks()
//      IsPlayable: 5H(suit)✓ 9D(rank)✓ 2C✗ 8C(wild)✓;
//      AdvanceTurn(2,3,+1)=0 wrap; AdvanceTurn(0,3,-1)=2 reverse-wrap ........... PASS
//
//  TrickTakingDemo.RunChecks()
//      LegalCards: holding a heart -> only the heart legal; no heart -> anything;
//      WinnerOfTrick(7H,KH led H) -> Dan (KH highest);
//      trump "S": 2S out-tiers 7H (a 2 of trump beats a K of led suit) ......... PASS
//
//  Finally Main prints the tally. Harness.Failures stayed 0 -> "ALL CHECKS PASSED".
//
//  AFTER the tally: DrillChecks.RunChecks() targets YOUR OWN Program1/Program2
//  files and prints OK / TO-FIX per defect, with the exact fix in a comment above
//  each check (DrillChecks.cs). Goal before mock day: every line says OK.
//
//  THE THROUGH-LINE: every "MUTATION ..." line touched exactly ONE method or ONE
//  array. That is the entire skill this interview tests.
// =============================================================================
static class Program
{
    static void Main()
    {
        Console.WriteLine("THE COMPLETE GUIDE, EXPLAINED IN CODE — running all concept checks\n");

        // Each call lives in its own file and proves that game's concepts.
        CoreConcepts.RunChecks();        // domain · deck · LINQ  (Core.cs)
        HighScoreDemo.RunChecks();       // Game shape #1         (Game1_HighScore.cs)
        WarDemo.RunChecks();             // Game shape #2         (Game2_War.cs)
        BestHandDemo.RunChecks();        // Game shape #3         (Game3_BestHand.cs)
        BlackjackDemo.RunChecks();       // Game shape #4         (Game4_Blackjack.cs)
        CrazyEightsDemo.RunChecks();     // Game shape #5         (Game5_CrazyEights.cs)
        TrickTakingDemo.RunChecks();     // Game shape #6         (Game6_TrickTaking.cs)
        FullWarDemo.RunChecks();         // Mission 1, DONE       (Game2_War.cs)

        // ---- REMAINING MISSIONS --------------------------------------------------
        // Each Game file ends with a "YOUR BUILD MISSION" plan: YOU write the full
        // game (state, loop, mutations) under the fragment, following the plan.
        // Uncomment each demo call as you finish its mission. Recommended order:
        // FullBestHandDemo.RunChecks();     // Mission 2 — Game3_BestHand.cs
        // BlackjackRoundDemo.RunChecks();   // Mission 3 — Game4_Blackjack.cs
        // CrazyEightsGameDemo.RunChecks();  // Mission 4 — Game5_CrazyEights.cs
        // TrickGameDemo.RunChecks();        // Mission 5 — Game6_TrickTaking.cs

        // ---- Final tally (reference + finished missions) ------------------------
        Console.WriteLine();
        Console.WriteLine(Harness.Failures == 0
            ? "ALL CHECKS PASSED — every concept behaves as the guide describes."
            : Harness.Failures + " CHECK(S) FAILED — reread the section each failing line names.");

        // ---- YOUR DRILL ZONE (deliberately after the tally) ----------------------
        // Checks pointed at YOUR practice files, Program1.cs and Program2.cs.
        // TO-FIX lines are your personal bug list: fix the file, rerun, watch each
        // line flip to OK. Separate counter — never touches the tally above.
        DrillChecks.RunChecks();
    }
}
