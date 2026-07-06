using System;
using System.Collections.Generic;
using System.Linq;

// #############################################################################
//  CORE.cs — the shared building blocks every game reuses:
//     Harness · Ranks · RanksAceHigh · Suits · Card · Deck · Player
//  Plus CoreConcepts.RunChecks() for the domain / deck / LINQ sections that
//  aren't tied to any single game.
// #############################################################################

// #############################################################################
//  ★ PART 1 SPOKEN SCRIPT — Part 1 is 100% guaranteed, so this script always runs ★
//
//  SAY (restate): "I need a Card with a rank and a suit, a 52-card deck,
//       shuffle, draw one and draw n, and a small demo proving it works."
//  ASK: "Jokers stay OUT of the deck for now, right?"
//  ASK: "Is letter display fine — QD, 10H — instead of the suit symbols?"
//  ASK: "Ace is LOW, as the intro doc says?"
//  SAY (plan): "My plan: rank order as a data array, then Card, then Deck with
//       shuffle and draw, then a tiny check helper so you see PASS lines as I go."
//
//  Then type — reading every // SAY: below out loud as you write that piece.
// #############################################################################


// #############################################################################
//  THE TEST HARNESS (Testing is the cheapest points in the exam)
//
//  Three lines, no framework. Visible PASS/FAIL on every run IS the whole
//  "Testing & unblocking" grading axis, made cheap. In a real interview you start
//  this by ~minute 5 and, on every rule change, you update the check FIRST (watch
//  it go red), then fix the code (watch it go green). That red->green loop,
//  narrated out loud, is the strongest signal you can send.
// #############################################################################
// SAY: "First a three-line check helper — every run prints PASS or FAIL, so we
//       both see the code staying correct while the rules keep changing."
static class Harness
{
    public static int Failures = 0;

    public static void Check(bool ok, string label)
    {
        Console.WriteLine((ok ? "  PASS  " : "  FAIL  ") + label);
        if (!ok) Failures++;
    }

    public static void Section(string title)
    {
        Console.WriteLine();
        Console.WriteLine("=== " + title + " ".PadRight(70 - title.Length, '='));
    }
}


// #############################################################################
//  RANK ORDER AS DATA  (Programming Pearls, Column 3)
//
//  A card carries THREE ideas people mix up:
//     1. Rank ORDER    = how strong a card is (Q beats 7).   -> lives HERE, one array.
//     2. POINTS        = how much a card scores.             -> lives in Game.PointsOf.
//     3. SUIT          = C/D/H/S, normally unordered.        -> lives in Suits.
//
//  "Which card beats which" is ORDERING. We keep it as one ordered array instead
//  of a pile of if-statements. Position in the array = strength. That means the
//  classic mutation "aces are high now" is a ONE-LINE data move, not a code hunt.
//
//  TRAP baked in from their PDF: ACE IS LOW. Order is A 2 .. 10 J Q K JOKER.
// #############################################################################
// SAY: "Rank order is one data array — a card's strength is its position in it.
//       If a rule later makes aces high, I move one string; no logic changes."
static class Ranks
{
    // LOW -> HIGH. Ace low. JOKER sits above K (the deck builder skips it unless asked).
    public static readonly string[] Order =
        { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "JOKER" };

    // Strength = the card's POSITION in the order array. One source of truth.
    //
    // DRY RUN — Strength("Q"):
    //   Order = [A,2,3,4,5,6,7,8,9,10,J,Q,K,JOKER]
    //           index 0 1 2 3 4 5 6 7 8  9 10 11 12  13
    //   Array.IndexOf finds "Q" at index 11 -> returns 11.
    //   Strength("7") -> index 6.  11 > 6, so Q outranks 7. Done, no if-statements.
    public static int Strength(string rank) => Array.IndexOf(Order, rank);
}

// MUTATION "aces are high" demonstrated as pure data: move "A" to just before JOKER.
// Notice: no comparison code changed anywhere — only the array. That is the point.
static class RanksAceHigh
{
    public static readonly string[] Order =
        { "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "JOKER" };

    public static int Strength(string rank) => Array.IndexOf(Order, rank);
}


// #############################################################################
//  SUITS (unordered until a rule says otherwise)
//
//  The doc says suits are UNORDERED, so there is deliberately no Strength() here.
//  Under-engineering trap avoided: we do NOT build suit ordering before it's asked.
//  When a mutation like "suits break ties: C < D < H < S" arrives, we add ONE array
//  (same pattern as Ranks) and one compare step.
// #############################################################################
// SAY: "The doc says suits are UNORDERED, so I deliberately don't build suit
//       comparison yet — I'll add it the moment a tie-break rule asks for it."
static class Suits
{
    public static readonly string[] All = { "C", "D", "H", "S" }; // ♣ ♦ ♥ ♠

    // Added ONLY when a tie-break rule demands it. Mirrors the Ranks pattern.
    public static readonly string[] Strength = { "C", "D", "H", "S" }; // C weakest, S strongest
    public static int Of(string suit) => Array.IndexOf(Strength, suit);
}


// #############################################################################
//  CARD (a card is a FACT, not a score)
//
//  A Card only knows its rank and suit — two immutable facts. It deliberately does
//  NOT know its point value, because the SAME card is worth different points in
//  different games (QD = 12 here, 10 after a mutation, and in War it's not "points"
//  at all — just a rank comparison). "What a card is worth" is a GAME rule, so it
//  lives in the game, not the card. (This is where we diverge from CtCI 7.1's
//  BlackjackCard subclass — be ready to say why.)
//
//  JOKER trap: a joker has a rank but NO suit (null). Special-cased in ToString.
// #############################################################################
// SAY: "A card is two read-only facts: rank and suit. What a card is WORTH is a
//       game rule, so points will live in the game class — not in the card."
// SAY (at ToString): "Jokers have no suit, so display is special-cased —
//       otherwise I'd print 'JOKERnull'."
sealed class Card
{
    public string Rank { get; }
    public string Suit { get; }              // null for jokers

    public Card(string rank, string suit) { Rank = rank; Suit = suit; }

    public bool IsJoker => Rank == "JOKER";
    public int Strength => Ranks.Strength(Rank);

    // Display rule = the VIEW. A joker prints without a suit, else rank+suit (QD, 10H).
    public override string ToString() => IsJoker ? "JOKER" : Rank + Suit;
}


// #############################################################################
//  DECK (contents are DATA -> constructor params, never subclasses)
//
//  Encapsulation: _cards is private; the only doors are Shuffle/Draw. Outside code
//  can't reorder or corrupt the deck.
//
//  Composition-over-inheritance: "with jokers", "two decks", "remove all 2s" are
//  all DECK CONTENTS. A JokerDeck : Deck subclass would be a smell. Instead they are
//  constructor PARAMETERS. One class, many decks.
//
//  Shuffle = Fisher-Yates: O(n), every ordering equally likely, 4 lines. A seed makes
//  runs reproducible while debugging (say aloud you'd remove it for real play).
//
//  Draw() throws on empty = "fail loud". A clear crash beats silent wrong answers.
//  Deck exhaustion has 3 policies (throw / reshuffle discards / end game); we default
//  to throw and show reshuffle as an opt-in method — decide the policy only when asked.
// #############################################################################
class Deck
{
    private readonly List<Card> _cards = new List<Card>();
    private readonly Random _rng;

    // DRY RUN — new Deck(): includeJokers=false, deckCount=1, stripRanks=null.
    //   strip = empty set. Outer d-loop runs once.
    //   For each of 4 suits, loop 14 ranks but skip "JOKER" -> 13 suited cards per suit.
    //   4 suits x 13 = 52 cards. includeJokers false -> no jokers added. Count = 52.
    //   new Deck(includeJokers:true) -> +2 jokers = 54.
    //   new Deck(deckCount:2)        -> the whole build runs twice = 104.
    //   new Deck(stripRanks:["2"])   -> "2" skipped -> 12 per suit x 4 = 48.
    // SAY: "Deck contents are constructor PARAMETERS — jokers, multiple decks,
    //       stripped ranks are all data, so I never need a subclass per deck."
    // SAY: "I'm seeding Random while building so bugs reproduce exactly; I'd
    //       remove the seed for real play."
    public Deck(bool includeJokers = false, int deckCount = 1, string[] stripRanks = null, int? seed = null)
    {
        // ONE Random instance. new Random() inside a loop => identical time seeds
        // => identical "shuffles". Seed it for reproducible debugging.
        _rng = seed.HasValue ? new Random(seed.Value) : new Random();

        var strip = new HashSet<string>(stripRanks ?? Array.Empty<string>());

        // Built FROM Ranks.Order — one source of truth for what ranks exist.
        // deckCount lets us stack multiple decks; stripRanks drops ranks ("remove all 2s").
        for (int d = 0; d < deckCount; d++)
        {
            foreach (var suit in Suits.All)
                foreach (var rank in Ranks.Order)
                    if (rank != "JOKER" && !strip.Contains(rank))
                        _cards.Add(new Card(rank, suit));

            if (includeJokers)
            {
                _cards.Add(new Card("JOKER", null));
                _cards.Add(new Card("JOKER", null));   // the intro PDF pictures exactly 2
            }
        }
    }

    public int Count => _cards.Count;

    // DRY RUN — Shuffle() on a tiny 4-card deck [A,B,C,D] with a fixed RNG:
    //   i=3: j=Next(4)=1 -> swap idx3,idx1 -> [A,D,C,B]
    //   i=2: j=Next(3)=2 -> swap idx2,idx2 -> [A,D,C,B]   (swapping with itself is fine)
    //   i=1: j=Next(2)=0 -> swap idx1,idx0 -> [D,A,C,B]
    //   loop stops at i=1>0 false. Result: [D,A,C,B]. Every ordering is equally likely.
    //   Each card is "placed" exactly once, back-to-front -> O(n), no bias.
    // SAY: "Shuffle is Fisher–Yates — one pass, O(n), every ordering equally
    //       likely. I loop from the END down to 1, swapping with a random spot."
    public void Shuffle()
    {
        for (int i = _cards.Count - 1; i > 0; i--)
        {
            int j = _rng.Next(i + 1);
            (_cards[i], _cards[j]) = (_cards[j], _cards[i]);   // tuple swap = the clean 1-liner
        }
    }

    // SAY: "I draw from the END of the list so it's O(1). An empty deck THROWS —
    //       failing loudly beats returning silent wrong data."
    public Card Draw()
    {
        if (_cards.Count == 0)
            throw new InvalidOperationException("Cannot draw from an empty deck.");
        var top = _cards[_cards.Count - 1];   // draw from the END: O(1). RemoveAt(0) would be O(n).
        _cards.RemoveAt(_cards.Count - 1);
        return top;
    }

    public List<Card> Draw(int n) => Enumerable.Range(0, n).Select(_ => Draw()).ToList();

    // Exhaustion policy #2 (opt-in): reshuffle a discard pile back into the deck.
    public void Reshuffle(IEnumerable<Card> discards)
    {
        _cards.AddRange(discards);
        Shuffle();
    }
}


// #############################################################################
//  PLAYER (has-a hand; a noun that sticks around -> a field)
// #############################################################################
// SAY: "A player is a name plus a hand. Nouns that stick around become fields;
//       verbs that happen become methods."
class Player
{
    public string Name { get; }
    public List<Card> Hand { get; } = new List<Card>();
    public int Score { get; set; }                         // used by trick-taking
    public Player(string name) { Name = name; }
    public string ShowHand() => string.Join(" ", Hand);
}


// #############################################################################
//  CORE CONCEPT CHECKS — domain, deck, and LINQ/collections (game-agnostic)
// #############################################################################
static class CoreConcepts
{
    public static void RunChecks()
    {
        // ---- the domain (rank / points / suit are different) ------------------
        Harness.Section("Domain: rank order, ace-low, joker, display");
        Harness.Check(Ranks.Strength("Q") > Ranks.Strength("7"), "rank order: Q beats 7");
        Harness.Check(Ranks.Strength("A") < Ranks.Strength("2"), "ace is LOW by default (a PDF trap)");
        Harness.Check(Ranks.Strength("JOKER") > Ranks.Strength("K"), "joker outranks king");
        Harness.Check(new Card("Q", "D").ToString() == "QD", "display rule: rank+suit -> QD");
        Harness.Check(new Card("JOKER", null).ToString() == "JOKER", "joker displays WITHOUT a suit");

        // Mutation 'aces high' is pure DATA — a different array, zero code changes.
        Harness.Check(RanksAceHigh.Strength("A") > RanksAceHigh.Strength("K"),
                      "MUTATION 'aces high' = a one-line data move (RanksAceHigh)");

        // ---- deck composition is constructor params, not subclasses -----------
        Harness.Section("Deck: composition via constructor parameters");
        Harness.Check(new Deck().Count == 52, "standard deck = 52");
        Harness.Check(new Deck(includeJokers: true).Count == 54, "with jokers = 54 (flag, not a subclass)");
        Harness.Check(new Deck(deckCount: 2).Count == 104, "two decks = 104 (param, not a subclass)");
        Harness.Check(new Deck(stripRanks: new[] { "2" }).Count == 48, "stripped 'remove all 2s' = 48");

        // Shuffle is reproducible with a seed; draw is O(1) from the end; empty throws.
        var deck = new Deck(seed: 42);
        deck.Shuffle();
        var five = deck.Draw(5);
        Harness.Check(five.Count == 5 && deck.Count == 47, "envelope check: draw 5 leaves 47 (52-5)");

        bool threw = false;
        try { new Deck(stripRanks: Ranks.Order).Draw(); } catch (InvalidOperationException) { threw = true; }
        Harness.Check(threw, "empty deck FAILS LOUD (throws) — a clear crash beats silent wrong data");

        // ---- LINQ / collections the interview actually uses -------------------
        Harness.Section("LINQ & collections you actually use");
        var demoHand = new List<Card> { new Card("7","H"), new Card("7","S"), new Card("Q","D"),
                                        new Card("2","C"), new Card("9","H") };
        Harness.Check(demoHand.Sum(c => c.Strength + 1) == (7+7+12+2+9), "Sum over a hand");
        Harness.Check(demoHand.Count(c => c.Suit == "H") == 2, "Count(predicate): 2 hearts");
        Harness.Check(demoHand.All(c => c.Suit == "H") == false, "All (flush check) = false here");
        Harness.Check(demoHand.GroupBy(c => c.Rank).Any(g => g.Count() == 2), "GroupBy finds the pair of 7s");
        Harness.Check(string.Join(" ", demoHand.OrderBy(c => c.Strength).Select(c => c.Rank))
                            == "2 7 7 9 Q", "OrderBy is for DISPLAY — the hand itself is untouched");
    }
}
