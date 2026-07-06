using System;
using System.Collections.Generic;
using System.Linq;

// ============================================================================
// MOCK 1 — "HIGH SCORE" — FINAL STATE after all Part 3 mutations.
//
// Tags show WHEN each line arrived (read NOTES.md for the evolution story):
//   [P1] Part 1: Card + Deck            [P2] Part 2: deal, score, winner
//   [M1] J/Q/K worth 10                 [M2] diamonds count double
//   [M3] jokers in deck, worth 20       [M4] tie -> one extra card each
//
// The lesson is not the code — it's that every mutation landed in ONE place.
// ============================================================================

public static class Ranks                                             // [P1]
{
    public static readonly string[] Order =
        { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "JOKER" };

    public static int Strength(string rank) => Array.IndexOf(Order, rank);
}

public static class Suits                                             // [P1]
{
    public static readonly string[] All = { "C", "D", "H", "S" };
}

public sealed class Card                                              // [P1]
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

public class Deck                                                     // [P1]
{
    private readonly List<Card> _cards = new List<Card>();
    private readonly Random _rng;

    public Deck(bool includeJokers = false, int? seed = null)
    {
        _rng = seed.HasValue ? new Random(seed.Value) : new Random();

        foreach (var suit in Suits.All)
            foreach (var rank in Ranks.Order)
                if (rank != "JOKER")
                    _cards.Add(new Card(rank, suit));

        if (includeJokers)                                            // used from [M3]
        {
            _cards.Add(new Card("JOKER", null));
            _cards.Add(new Card("JOKER", null));
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

public class Player                                                   // [P1]
{
    public string Name { get; }
    public List<Card> Hand { get; } = new List<Card>();

    public Player(string name) { Name = name; }

    public string ShowHand() => string.Join(" ", Hand);
}

public class HighScoreGame                                            // [P2]
{
    public List<Player> Players { get; }
    public Deck Deck { get; }

    public HighScoreGame(IEnumerable<string> names, bool includeJokers = false, int? seed = null)
    {
        Players = names.Select(n => new Player(n)).ToList();
        Deck = new Deck(includeJokers, seed);
        Deck.Shuffle();
    }

    public void Deal(int cardsEach)                                   // [P2]
    {
        for (int round = 0; round < cardsEach; round++)
            foreach (var p in Players)
                p.Hand.Add(Deck.Draw());
    }

    // The ONLY place that knows what a card is worth. Public on purpose —
    // say aloud: "keeping it public so I can spot-check values in my checks".
    public int PointsOf(Card card)
    {
        if (card.IsJoker) return 20;                                  // [M3] joker = 20

        int points;
        switch (card.Rank)
        {
            case "A": points = 1; break;                              // [P2]
            case "J":
            case "Q":
            case "K": points = 10; break;                             // [M1] was J=11 Q=12 K=13
            default: points = int.Parse(card.Rank); break;            // [P2] safe: specials handled above
        }

        if (card.Suit == "D") points *= 2;                            // [M2] diamonds double
        return points;                                                //      (joker has no suit -> unaffected)
    }

    public int ScoreHand(Player p) => p.Hand.Sum(PointsOf);           // [P2]

    private List<Player> WinnersAmong(List<Player> pool)              // [P2], generalized in [M4]
    {
        int best = pool.Max(ScoreHand);
        return pool.Where(p => ScoreHand(p) == best).ToList();
    }

    public List<Player> ResolveWinners()                              // [M4]
    {
        var contenders = WinnersAmong(Players);
        while (contenders.Count > 1 && Deck.Count >= contenders.Count)
        {
            Console.WriteLine("Tie between " + string.Join(", ", contenders.Select(p => p.Name))
                              + " — dealing one extra card each.");
            foreach (var p in contenders)
                p.Hand.Add(Deck.Draw());
            contenders = WinnersAmong(contenders);
        }
        return contenders;   // >1 left means the deck ran out -> they share the win
    }

    public void PrintStandings()                                      // [P2]
    {
        foreach (var p in Players)
            Console.WriteLine($"{p.Name,-6} score {ScoreHand(p),3}   {p.ShowHand()}");
    }
}

public static class Program
{
    private static int _failures = 0;

    private static void Check(bool ok, string label)
    {
        Console.WriteLine((ok ? "PASS  " : "FAIL  ") + label);
        if (!ok) _failures++;
    }

    public static void Main()
    {
        // Probe game: exercises the scoring policy directly, one card at a time.
        // Dry run after all mutations: QD is 20 (queen=10, diamond doubles),
        // 5D is 10, JOKER is 20, and non-diamonds keep their base points.
        var probe = new HighScoreGame(new[] { "T" });
        Check(probe.PointsOf(new Card("7", "H")) == 7, "7H = 7");
        Check(probe.PointsOf(new Card("A", "S")) == 1, "ace = 1");
        Check(probe.PointsOf(new Card("Q", "C")) == 10, "face card = 10          [M1]");
        Check(probe.PointsOf(new Card("5", "D")) == 10, "diamond doubles         [M2]");
        Check(probe.PointsOf(new Card("Q", "D")) == 20, "diamond face card = 20  [M1+M2]");
        Check(probe.PointsOf(new Card("JOKER", null)) == 20, "joker = 20         [M3]");
        Check(new Deck(includeJokers: true).Count == 54, "deck now holds 54       [M3]");

        // Forced tie so the [M4] path runs deterministically. (The injected cards
        // also still sit in the deck — fine for a points-level test; mention that
        // trade-off aloud if you do this live.)
        var tie = new HighScoreGame(new[] { "X", "Y" }, seed: 7);
        tie.Players[0].Hand.Add(new Card("5", "H"));
        tie.Players[1].Hand.Add(new Card("5", "S"));
        var resolved = tie.ResolveWinners();
        Check(resolved.Count == 1, "tie resolved by extra cards               [M4]");

        Console.WriteLine();

        // ---- demo run ---------------------------------------------------------
        var game = new HighScoreGame(new[] { "Alice", "Bob", "Cara" },
                                     includeJokers: true, seed: 42);
        game.Deal(5);
        game.PrintStandings();
        var winners = game.ResolveWinners();
        Console.WriteLine("Winner(s): " + string.Join(", ", winners.Select(w => w.Name)));

        Console.WriteLine();
        Console.WriteLine(_failures == 0 ? "ALL CHECKS PASSED" : _failures + " CHECK(S) FAILED");
    }
}
