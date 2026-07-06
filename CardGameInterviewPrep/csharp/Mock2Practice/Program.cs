// ============================================================================
// MOCK 2 PRACTICE — "War", BASE VARIANT ONLY (no mutations yet).
//
// Part 1 (Ranks, Suits, Card, Deck, Player, Check) is given below, already
// working — that's drilled separately. Your job is ONLY the War-specific
// pieces: WarPlayer's shape is given (trivial), but every method in
// BaseWarGame currently throws NotImplementedException. Fill them in one at
// a time, rerunning after each — the checks in Main are already written and
// will go from a crash/FAIL to PASS as you complete each piece.
//
// THE STORY: Alice and Bob each hold half a shuffled deck, face down. Each
// round both flip their top card; the higher rank takes BOTH cards into a
// "won" pile. Equal rank: both cards go to a shared discard pile (no war —
// that's a Part 3 mutation, not built here). After N rounds (or a pile empties),
// whoever has more won cards wins; equal won-pile counts is a tie.
//
// Once every check says PASS, compare your BaseWarGame against the full
// reference (Game2_War.cs's FullWarGame in the Concepts project) — same
// method names, same shape, that one just has 4 more mutations layered on.
// ============================================================================

public static class Harness
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

public static class Ranks
{
    public static readonly string[] Order =
        { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "JOKER" };

    public static int Strength(string rank) => Array.IndexOf(Order, rank);
}

public static class Suits
{
    public static readonly string[] All = { "C", "D", "H", "S" };
    public static readonly string[] Strength = { "C", "D", "H", "S" };
    public static int Of(string suit) => Array.IndexOf(Strength, suit);
}

public sealed class Card
{
    public string Rank { get; }
    public string Suit { get; }              // null for jokers

    public Card(string rank, string suit) { Rank = rank; Suit = suit; }

    public bool IsJoker => Rank == "JOKER";
    public int Strength => Ranks.Strength(Rank);

    public override string ToString() => IsJoker ? "JOKER" : Rank + Suit;
}

public class Deck
{
    private readonly List<Card> _cards = new List<Card>();
    private readonly Random _rng;

    public Deck(bool includeJokers = false, int deckCount = 1, string[] stripRanks = null, int? seed = null)
    {
        _rng = seed.HasValue ? new Random(seed.Value) : new Random();
        var strip = new HashSet<string>(stripRanks ?? Array.Empty<string>());

        for (int d = 0; d < deckCount; d++)
        {
            foreach (var suit in Suits.All)
                foreach (var rank in Ranks.Order)
                    if (rank != "JOKER" && !strip.Contains(rank))
                        _cards.Add(new Card(rank, suit));

            if (includeJokers)
            {
                _cards.Add(new Card("JOKER", null));
                _cards.Add(new Card("JOKER", null));
            }
        }
    }

    public int Count => _cards.Count;

    public void Shuffle()
    {
        for (int i = _cards.Count - 1; i > 0; i--)
        {
            int j = _rng.Next(i + 1);
            (_cards[i], _cards[j]) = (_cards[j], _cards[i]);
        }
    }

    public Card Draw()
    {
        if (_cards.Count == 0)
            throw new InvalidOperationException("Cannot draw from an empty deck.");
        var top = _cards[_cards.Count - 1];
        _cards.RemoveAt(_cards.Count - 1);
        return top;
    }

    public List<Card> Draw(int n) => Enumerable.Range(0, n).Select(_ => Draw()).ToList();
}

public class Player
{
    public string Name { get; }
    public List<Card> Hand { get; } = new List<Card>();
    public Player(string name) { Name = name; }
    public string ShowHand() => string.Join(" ", Hand);
}


// ============================================================================
// YOUR TURN STARTS HERE — everything above this line is given and working.
// ============================================================================

// Given: War needs TWO piles per player (draw FROM, collect won cards INTO) —
// Core's Player (one Hand) doesn't fit. A Queue models "always take the TOP
// card" naturally: Dequeue() IS flipping the top card.
public sealed class WarPlayer
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

public sealed class BaseWarGame
{
    private int _totalCards;   // set by whichever constructor runs — the envelope check's expected total

    public WarPlayer A { get; private set; }
    public WarPlayer B { get; private set; }
    public List<Card> SharedDiscard { get; } = new List<Card>();

    // Real game: shuffle a fresh deck, split it evenly. _totalCards is captured

    // BEFORE drawing (deck.Count keeps shrinking as A and B draw from it).
    public BaseWarGame(string nameA, string nameB, int? seed = null)
    {
        var deck = new Deck(seed: seed);
        deck.Shuffle();
        _totalCards = deck.Count;
        int half = deck.Count / 2;
        A = new WarPlayer(nameA, deck.Draw(half));
        B = new WarPlayer(nameB, deck.Draw(deck.Count));   // whatever's left
    }

    // Test ctor: inject exact piles so checks are deterministic, not shuffle-dependent.
    public BaseWarGame(string nameA, IEnumerable<Card> pileA, string nameB, IEnumerable<Card> pileB)
    {
        A = new WarPlayer(nameA, pileA);
        B = new WarPlayer(nameB, pileB);
        _totalCards = A.DrawPile.Count + B.DrawPile.Count;
    }

    // The ONE place "who beats whom" lives. No suit tie-break, no war — those
    // are Part 3 mutations, not this base variant.
    private int CompareCards(Card a, Card b)
    {
        if (a.Strength != b.Strength) return a.Strength > b.Strength ? 1 : -1;
        return 0;
    }

    // One full action = one round.
    public void PlayRound(int roundNo)
    {
        if (A.DrawPile.Count == 0 || B.DrawPile.Count == 0) return;

        var ca = A.DrawPile.Dequeue();
        var cb = B.DrawPile.Dequeue();
        int r = CompareCards(ca, cb);
        string outcome;

        if (r > 0) { A.WonPile.Add(ca); A.WonPile.Add(cb); outcome = A.Name; }
        else if (r < 0) { B.WonPile.Add(ca); B.WonPile.Add(cb); outcome = B.Name; }
        else { SharedDiscard.Add(ca); SharedDiscard.Add(cb); outcome = "discard"; }

        Console.WriteLine($"  Round {roundNo}: {A.Name} {ca}  vs  {B.Name} {cb}  ->  {outcome}");
    }

    public void Play(int rounds)
    {
        for (int i = 1; i <= rounds && A.DrawPile.Count > 0 && B.DrawPile.Count > 0; i++)
            PlayRound(i);
    }

    public string Winner()
    {
        if (A.WonPile.Count == B.WonPile.Count) return "tie";
        return A.WonPile.Count > B.WonPile.Count ? A.Name : B.Name;
    }

    // THE STRONGEST CHECK: cards only ever move between piles, never vanish
    // or duplicate.
    public bool CardsBalance() =>
        A.DrawPile.Count + B.DrawPile.Count + A.WonPile.Count + B.WonPile.Count + SharedDiscard.Count == _totalCards;
}


public static class Program
{
    public static void Main()
    {
        Harness.Section("Base War: setup, comparator, one round, tie, envelope");

        // Setup: a real shuffled deck splits evenly.
        var setup = new BaseWarGame("A", "B", seed: 1);
        Harness.Check(setup.A.DrawPile.Count == 26 && setup.B.DrawPile.Count == 26,
                      "setup: a 52-card deck splits into two 26-card draw piles");

        // One round, no tie: the higher rank takes both cards.
        var oneRound = new BaseWarGame("A", new[] { new Card("K", "C") },
                                        "B", new[] { new Card("3", "D") });
        oneRound.PlayRound(1);
        Harness.Check(oneRound.A.WonPile.Count == 2 && oneRound.B.WonPile.Count == 0,
                      "one round, no tie: K beats 3, winner's WonPile gets both cards");

        // One round, a tie: both cards go to the shared discard, nobody wins them.
        var tieRound = new BaseWarGame("A", new[] { new Card("7", "H") },
                                        "B", new[] { new Card("7", "C") });
        tieRound.PlayRound(1);
        Harness.Check(tieRound.SharedDiscard.Count == 2 && tieRound.A.WonPile.Count == 0 && tieRound.B.WonPile.Count == 0,
                      "one round, a tie: equal ranks -> both cards discarded, nobody's WonPile changes");

        // No rounds played yet: 0-0 is still a real tie.
        var freshGame = new BaseWarGame("A", Array.Empty<Card>(), "B", Array.Empty<Card>());
        Harness.Check(freshGame.Winner() == "tie",
                      "Winner() before any rounds: 0 vs 0 is a tie, not a crash");

        // A full seeded run: confirm it plays to completion without crashing,
        // and the strongest invariant holds — no card vanishes or duplicates.
        var fullGame = new BaseWarGame("Alice", "Bob", seed: 42);
        fullGame.Play(10);
        Harness.Check(fullGame.CardsBalance(),
                      "envelope check: draw+won+discard piles still sum to the full 52-card deck");

        Console.WriteLine();
        Console.WriteLine(Harness.Failures == 0
            ? "ALL CHECKS PASSED — your BaseWarGame matches the Part 2 shape."
            : Harness.Failures + " CHECK(S) FAILED — implement the next TODO and rerun.");
    }
}
