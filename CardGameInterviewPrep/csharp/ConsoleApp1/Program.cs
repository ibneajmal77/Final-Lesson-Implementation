using System.Runtime.CompilerServices;

static class Ranks
{
    public static readonly string[] Order = { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "JOKER" };
    public static int Strength(string rank) => Array.IndexOf(Order, rank);
}

static class Suits
{
    public static readonly string[] All = { "C", "H", "D", "S" };
    public static readonly string[] Strength = { "C", "H", "D", "S" };
    public static int Of(string suit) => Array.IndexOf(Strength, suit);
}

sealed class Card
{
    public string Rank { get; }
    public string Suit { get; }

    public Card(string rank, string suit)
    {
        Rank = rank;
        Suit = suit;
    }

    public int Strength => Ranks.Strength(Rank);

    public bool IsJoker => Rank == "JOKER";

    public override string ToString() => IsJoker ? "JOKER" : Rank + Suit;
}

sealed class Deck
{
    private List<Card> _cards = new List<Card>();
    Random _rng;

    public Deck(bool includeJokers = false, int deckCount = 1, string[] stripSuits = null, string[] stripRanks = null, int? seed = null)
    {
        _rng = seed != null ? new Random(seed.Value) : new Random();
        for (int i = 0; i < deckCount; i++)
        {
            foreach (var suit in Suits.All)
            {
                if (stripSuits == null || !stripSuits.Contains(suit))
                {
                    foreach (var rank in Ranks.Order)
                    {
                        if (rank != "JOKER" && (stripRanks == null || !stripRanks.Contains(rank)))
                        {
                            _cards.Add(new Card(rank, suit));
                        }
                    }
                }
            }

            if (includeJokers)
            {
                _cards.Add(new Card("JOKER", null));
                _cards.Add(new Card("JOKER", null));
            }
        }
    }

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
        {
            throw new InvalidOperationException("Don't have any card available");
        }

        var top = _cards[_cards.Count - 1];
        _cards.RemoveAt(_cards.Count - 1);
        return top;
    }

    public List<Card> Draw(int n) => Enumerable.Range(0, n).Select(x => Draw()).ToList();

    public int Count => _cards.Count;
}

sealed class Player
{
    public string Name { get; }

    public Player(string name)
    {
        Name = name;
    }

    public int Score { get; set; }

    public string ShowHand() => string.Join(" ", Hand);

    public List<Card> Hand = new List<Card>();
}

class HighScoreGame
{
    public List<Player> Players { get; }
    public Deck Deck { get; }
    public HighScoreGame(string[] names, bool includeJokers = false, int? seed = null)
    {
        Players = names.Select(x => new Player(x)).ToList();
        Deck = new Deck(includeJokers: includeJokers, seed: seed);
        Deck.Shuffle();
    }

    public void Deal(int cardsEachPlayer)
    {
        for (int i = 0; i < cardsEachPlayer; i++)
        {
            foreach (var item in Players)
            {
                item.Hand.Add(Deck.Draw());
            }
        }
    }

    public int PointsOf(Card card) => card.Strength + 1;

    public int ScoreHands(Player player) => player.Hand.Sum(PointsOf);

    public List<Player> BestMeasure(List<Player> players)
    {
        int best = players.Max(ScoreHands);
        return players.Where(x => ScoreHands(x) == best).ToList();
    }

    public List<Player> Winner()
    {
        var contenders = BestMeasure(Players);

        while (contenders.Count > 1 && Deck.Count > contenders.Count)
        {
            // This was the missing piece: without dealing a new card to each
            // contender, calling BestMeasure(contenders) again just re-checks
            // the SAME unchanged hands and returns the SAME result forever.
            foreach (var p in contenders)
                p.Hand.Add(Deck.Draw());
            contenders = BestMeasure(contenders);
        }

        return contenders;
    }
}

sealed class WarPlayer
{
    public string Name { get; }
    public Queue<Card> DrawPile { get; }

    public List<Card> WonPile { get; set; } = new List<Card>();

    public WarPlayer(string name, List<Card> cards)
    {
        Name = name;
        DrawPile = new Queue<Card>(cards);
    }
}

class WarGame
{
    public WarPlayer A { get; }
    public WarPlayer B { get; }

    public List<Card> DiscardPile { get; set; } = new List<Card>();

    public int _totalCount { get; set; }
    public Deck Deck { get; set; }

    public WarGame(string nameOfA, string nameOfB, int? seed = null)
    {
        Deck = new Deck(seed: seed);
        Deck.Shuffle();
        int half = Deck.Count / 2;
        A = new WarPlayer(nameOfA, Deck.Draw(half));
        B = new WarPlayer(nameOfB, Deck.Draw(Deck.Count));
    }

    public int CompareCards(Card a, Card b)
    {
        if (a.Strength != b.Strength)
        {
            return a.Strength > b.Strength ? 1 : -1;
        }
        return 0;
    }

    public void PlayRounds(int rounds)
    {
        if (A.DrawPile.Count == 0 || B.DrawPile.Count == 0) return;
        var ac = A.DrawPile.Dequeue();
        var bc = B.DrawPile.Dequeue();

        var r = CompareCards(ac, bc);

        string outcome;
        if (r > 0)
        {
            A.WonPile.Add(ac);
            A.WonPile.Add(bc);

            outcome = A.Name;
        }

        else if (r < 0)
        {
            B.WonPile.Add(ac);
            B.WonPile.Add(bc);

            outcome = B.Name;
        }
        else
        {
            DiscardPile.Add(ac);
            DiscardPile.Add(bc);

            outcome = "discard";
        }

        Console.WriteLine($"{A.Name} {ac}  vs  {B.Name} {bc}  ->  {outcome}");
    }

    public void Play(int rounds)
    {
        for (int i = 0; i < rounds && A.DrawPile.Count > 0 && B.DrawPile.Count > 0; i++)
        {
            PlayRounds(rounds);
        }
    }

    public string Winner()
    {
        if (A.WonPile.Count == B.WonPile.Count)
        {
            return "Tie";
        }

        return A.WonPile.Count > B.WonPile.Count ? A.Name : B.Name;
    }
}
