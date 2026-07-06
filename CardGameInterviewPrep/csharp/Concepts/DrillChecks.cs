using System;
using System.Linq;
using System.Reflection;

// #############################################################################
//  DRILL CHECKS — a test harness pointed at YOUR OWN practice files.
//
//     Program2.cs (namespace Concepts.Ace) = your attempt 2 (logic right, style gaps)
//
//  Program1.cs was retired 2026-07-05 (deleted — you moved on to Program3.cs /
//  Program4.cs). Ask for a fresh CheckProgram3()/CheckProgram4() section once
//  one of those is finished, if you want the same OK/TO-FIX treatment on it.
//
//  HOW THIS WORKS (coach mode):
//    Every line prints OK or TO-FIX. A TO-FIX line names ONE defect in YOUR file,
//    and the comment above it tells you the exact fix. You edit Program2.cs
//    (never this file), rerun `dotnet run`, and watch lines flip to OK one by
//    one. That red -> green loop is the exact habit the interview grades.
//    These lines do NOT count into the reference tally in Main.
//
//    Some checks use REFLECTION (inspecting your types by name). That is only so
//    this file keeps compiling while methods are still missing from your files.
//    You will never need reflection in the interview itself.
// #############################################################################
static class DrillChecks
{
    private static int _toFix;

    private static void Fix(bool ok, string label)
    {
        Console.WriteLine((ok ? "  OK      " : "  TO-FIX  ") + label);
        if (!ok) _toFix++;
    }

    public static void RunChecks()
    {
        _toFix = 0;
        // CheckProgram1() retired 2026-07-05 — Program1.cs no longer exists in this
        // project (you moved on to Program3.cs / Program4.cs). Ask if you want a
        // fresh CheckProgram3() / CheckProgram4() pointed at whichever is current.
        CheckProgram2();
        Console.WriteLine();
        Console.WriteLine(_toFix == 0
            ? "  DRILL DONE — Program2.cs matches the reference quality bar."
            : "  " + _toFix + " TO-FIX target(s) left in Program2.cs — your personal bug list.");
    }

    // ---- Attempt 2: Program2.cs ---------------------------------------------
    private static void CheckProgram2()
    {
        Harness.Section("DRILL Program2.cs (attempt 2) — logic is right, close the style gaps");

        // These pass already — your attempt-2 logic is correct. KEEP them green.
        Fix(new Concepts.Ace.Deck(false, 1).Count == 52, "P2: standard deck = 52");
        Fix(new Concepts.Ace.Deck(true, 1).Count == 54, "P2: jokers flag -> 54");
        Fix(new Concepts.Ace.Deck(false, 1, new[] { "2" }).Count == 48,
            "P2: skipRanks works (yours is the correct version!)");

        bool threw = false;
        try { new Concepts.Ace.Deck(false, 0).Draw(); }
        catch (InvalidOperationException) { threw = true; }
        Fix(threw, "P2: empty deck fails loud (throws)");

        var d1 = new Concepts.Ace.Deck(false, 1, null, null, 7);
        var d2 = new Concepts.Ace.Deck(false, 1, null, null, 7);
        d1.Shuffle(); d2.Shuffle();
        Fix(string.Join(" ", d1.Draw(5)) == string.Join(" ", d2.Draw(5)),
            "P2: same seed -> same shuffle (reproducible debugging)");

        // GAP: `new Deck()` must work — it is the standard call in every game ctor.
        // FIX: give the first two parameters defaults:
        //      Deck(bool isJokerIncluded = false, int deckCount = 1, ...)
        Fix(typeof(Concepts.Ace.Deck).GetConstructors()[0].GetParameters().All(p => p.IsOptional),
            "P2: every ctor parameter optional -> `new Deck()` compiles");

        // GAP: every game compares cards; your Card cannot say how strong it is.
        // FIX: `public int Strength => Ranks.Strength(Rank);`  (your Concepts.Ace.Ranks)
        Fix(typeof(Concepts.Ace.Card).GetProperty("Strength") != null,
            "P2: Card.Strength exists");

        // GAP: Rank/Suit have public setters — a card must be an immutable fact.
        // FIX: `{ get; }` only, on both.
        Fix(!typeof(Concepts.Ace.Card).GetProperty("Rank").CanWrite,
            "P2: Card.Rank is get-only");

        // GAP: _cards and _rng are public fields.
        // FIX: `private readonly` for both (List<Card> and Random).
        Fix(typeof(Concepts.Ace.Deck).GetField("_cards", BindingFlags.Public | BindingFlags.Instance) == null
            && typeof(Concepts.Ace.Deck).GetField("_rng", BindingFlags.Public | BindingFlags.Instance) == null,
            "P2: _cards and _rng are private");

        // GAP: Person.Hand has a public setter — anyone could swap the whole list.
        // FIX: `public List<Card> Hand { get; } = new List<Card>();`
        Fix(!typeof(Concepts.Ace.Person).GetProperty("Hand").CanWrite,
            "P2: Person.Hand is get-only");
    }
}
