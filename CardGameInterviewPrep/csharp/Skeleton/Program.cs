using System;
using System.Collections.Generic;
using System.Linq;

// ============================================================================
// CARD GAME SKELETON — the "muscle memory zone".
// Goal: type everything down to the Check helper from a BLANK file in <10 min.
//
// Design rule (see 03-design-playbook.md): every game rule lives in ONE place.
//   who outranks whom   -> Ranks.Order (one array)
//   what a card scores  -> Game.PointsOf (one method)
//   how a hand scores   -> Game.ScoreHand (one method)
//   who wins            -> Game.Winners (one method; returns a LIST — ties are real)
//   what's in the deck  -> Deck constructor (parameters, never subclasses)
//
// ★ SPEAK WHILE YOU TYPE THIS (practice out loud in every cold start): ★
//   Restate: "A Card is rank + suit; I need a 52-card deck, shuffle, draw."
//   ASK: jokers out for now? letter display (QD) okay? ace LOW per the doc?
//   Then narrate each piece:
//     Ranks : "Rank order is one data array — position IS strength; if aces go
//              high later, I move one string."
//     Suits : "Suits are unordered per the doc — no comparison until asked."
//     Card  : "Two read-only facts; a card's VALUE is a game rule, lives in Game."
//     Deck  : "Contents are constructor parameters; seeded Random while testing."
//     Shuffle: "Fisher–Yates, O(n), every ordering equally likely."
//     Draw  : "From the END so it's O(1); empty deck throws — fail loud."
//     Check : "Three-line harness so every run PROVES the code still works."
//   Close: "Part 1 done and demonstrated — ready for Part 2."
// ============================================================================

public static class Ranks
{
    // Comparison order, LOW -> HIGH. Ace is LOW per the intro doc — confirm on the day.
    // JOKER sits above K; the deck builder skips it unless jokers are requested.
    public static readonly string[] Order =
        { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "JOKER" };

    public static int Strength(string rank) => Array.IndexOf(Order, rank);
}

public static class Suits
{
    // Unordered per the intro doc — so no Strength() here. If a rule ever orders
    // suits, add one (same pattern as Ranks) and you're done.
    public static readonly string[] All = { "C", "D", "H", "S" }; // ♣ ♦ ♥ ♠
}

public sealed class Card
{
    public string Rank { get; }
    public string Suit { get; }                       // null for jokers

    public Card(string rank, string suit)
    {
        Rank = rank;
        Suit = suit;
    }

    public bool IsJoker => Rank == "JOKER";
    public int Strength => Ranks.Strength(Rank);

    public override string ToString() => IsJoker ? "JOKER" : Rank + Suit;
}

public class Deck
{
    private readonly List<Card> _cards = new List<Card>();
    private readonly Random _rng;

    public Deck(bool includeJokers = false, int? seed = null)
    {
        // Seed while practicing/debugging -> reproducible runs. Unseeded for real play.
        _rng = seed.HasValue ? new Random(seed.Value) : new Random();

        // Built FROM Ranks.Order — one source of truth for what ranks exist.
        foreach (var suit in Suits.All)
            foreach (var rank in Ranks.Order)
                if (rank != "JOKER")
                    _cards.Add(new Card(rank, suit));

        if (includeJokers)
        {
            _cards.Add(new Card("JOKER", null));
            _cards.Add(new Card("JOKER", null));      // the intro PDF pictures exactly 2
        }
    }

    public int Count => _cards.Count;

    public void Shuffle()
    {
        // Fisher–Yates: in place, O(n), every permutation equally likely.
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
        var top = _cards[_cards.Count - 1];           // take from the end: O(1)
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

public class Game
{
    public List<Player> Players { get; }
    public Deck Deck { get; }

    public Game(IEnumerable<string> names, bool includeJokers = false, int? seed = null)
    {
        Players = names.Select(n => new Player(n)).ToList();
        Deck = new Deck(includeJokers, seed);
        Deck.Shuffle();
    }

    public void Deal(int cardsEach)
    {
        // Round-robin like a real dealer. (After a fair shuffle, block dealing is
        // statistically identical — worth saying aloud, then moving on.)
        for (int round = 0; round < cardsEach; round++)
            foreach (var p in Players)
                p.Hand.Add(Deck.Draw());
    }

    // ---- policy methods: rule changes land HERE, nowhere else ---------------

    // NOTE the split: Strength = who outranks whom; PointsOf = what a card scores.
    // Different kinds of rules -> different homes. Default: A=1 ... K=13, JOKER=14.
    public virtual int PointsOf(Card card) => card.Strength + 1;

    public virtual int ScoreHand(Player p) => p.Hand.Sum(PointsOf);

    public List<Player> Winners()
    {
        int best = Players.Max(ScoreHand);
        return Players.Where(p => ScoreHand(p) == best).ToList();
    }
}

public static class Program
{
    private static int _failures = 0;

    // Three-line test harness. Visible PASS/FAIL on every run is the entire
    // "Testing & Optimizing" grading axis, made cheap. Start it by minute ~5.
    private static void Check(bool ok, string label)
    {
        Console.WriteLine((ok ? "PASS  " : "FAIL  ") + label);
        if (!ok) _failures++;
    }

    public static void Main()
    {
        // ---- micro-checks: cheap proof each layer works ----------------------
        Check(new Deck().Count == 52, "standard deck has 52 cards");
        Check(new Deck(includeJokers: true).Count == 54, "joker deck has 54 cards");
        Check(new Card("Q", "D").ToString() == "QD", "card displays rank + suit");
        Check(new Card("JOKER", null).ToString() == "JOKER", "joker displays without suit");
        Check(Ranks.Strength("A") < Ranks.Strength("2"), "ace is LOW");
        Check(Ranks.Strength("JOKER") > Ranks.Strength("K"), "joker outranks king");

        var deck = new Deck(seed: 42);
        deck.Shuffle();
        var five = deck.Draw(5);
        Check(five.Count == 5 && deck.Count == 47, "drawing 5 leaves 47");

        // ---- demo game --------------------------------------------------------
        // Dry run: Deal(5) gives each player 5 cards. ScoreHand sums PointsOf for
        // each card in that player's hand. Winners returns every player whose
        // score equals the best score, so ties stay visible instead of disappearing.
        var game = new Game(new[] { "Alice", "Bob", "Cara" }, seed: 42);
        game.Deal(5);
        foreach (var p in game.Players)
            Console.WriteLine($"{p.Name,-6} score {game.ScoreHand(p),3}   {p.ShowHand()}");
        Console.WriteLine("Winner(s): " + string.Join(", ", game.Winners().Select(w => w.Name)));

        Console.WriteLine(_failures == 0 ? "ALL CHECKS PASSED" : _failures + " CHECK(S) FAILED");
    }
}
