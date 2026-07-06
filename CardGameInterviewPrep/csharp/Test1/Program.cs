
namespace Test1
{
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

    static class Ranks
    {
        public static readonly string[] Order = { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "JOKER" };
        public static int Strength(string rank) => Array.IndexOf(Order, rank);
    }
    static class Suits
    {
        public static readonly string[] ALL = { "C", "D", "H", "S" };
        public static readonly string[] Strength = { "C", "D", "H", "S" };
        public static int Of(string suit) => Array.IndexOf(ALL, suit);
    }

    sealed class Card
    {
        public string Rank { get; set; }
        public string Suit { get; set; }

        public Card(string rank, string suit)
        {
            Rank = rank;
            Suit = suit;
        }


        public bool IsJoker => Rank == "JOKER";

        public int Strength => Ranks.Strength(Rank);

        public override string ToString()
        {
            return IsJoker ? "JOKER" : Rank + Suit;
        }
    }


    sealed class Deck
    {
        private List<Card> _cards { get; set; } = new List<Card>();

        Random _rng;
        public Deck(bool isJokerIncluded = false, int deckCount = 1, string[] stripSuits = null, string[] stripRanks = null, int? seed = null)
        {
            _rng = seed != null ? new Random(seed.Value) : new Random();

            for (int i = 0; i < deckCount; i++)
            {
                foreach (var suit in Suits.ALL)
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

                if (isJokerIncluded)
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
                throw new InvalidOperationException("No Cards there to draw in deck");

            var top = _cards[_cards.Count - 1];
            _cards.RemoveAt(_cards.Count - 1);

            return top;
        }

        public List<Card> Draw(int range) => Enumerable.Range(0, range).Select(_ => Draw()).ToList();

        public int Count => _cards.Count;


    }

    sealed class Person
    {
        public Person(string name)
        {
            Name = name;
        }
        public string Name { get; }
        public List<Card> Hand { get; } = new List<Card>();
        public int Score { get; set; }

        public string ShowHand(string card) => string.Join(" ", Hand);
    }

    internal class Program
    {
        static void Main()
        {
            // ---- the domain (rank / points / suit are different) ------------------
            Harness.Section("Domain: rank order, ace-low, joker, display");
            Harness.Check(Ranks.Strength("Q") > Ranks.Strength("7"), "rank order: Q beats 7");
            Harness.Check(Ranks.Strength("A") < Ranks.Strength("2"), "ace is LOW by default (a PDF trap)");
            Harness.Check(Ranks.Strength("JOKER") > Ranks.Strength("K"), "joker outranks king");
            Harness.Check(new Card("Q", "D").ToString() == "QD", "display rule: rank+suit -> QD");
            Harness.Check(new Card("JOKER", null).ToString() == "JOKER", "joker displays WITHOUT a suit");

            // Mutation 'aces high' is pure DATA — a different array, zero code changes.
            //Harness.Check(RanksAceHigh.Strength("A") > RanksAceHigh.Strength("K"),
            //              "MUTATION 'aces high' = a one-line data move (RanksAceHigh)");

            // ---- deck composition is constructor params, not subclasses -----------
            Harness.Section("Deck: composition via constructor parameters");
            Harness.Check(new Deck().Count == 52, "standard deck = 52");
            Harness.Check(new Deck(isJokerIncluded: true).Count == 54, "with jokers = 54 (flag, not a subclass)");
            Harness.Check(new Deck(deckCount: 2).Count == 104, "two decks = 104 (param, not a subclass)");
            Harness.Check(new Deck(stripRanks: new[] { "2" }).Count == 48, "stripped 'remove all 2s' = 48");

            // Shuffle is reproducible with a seed; draw is O(1) from the end; empty throws.
            var deck = new Deck(seed: 42);
            deck.Shuffle();
            var five = deck.Draw(5);
            Harness.Check(five.Count == 5 && deck.Count == 47, "envelope check: draw 5 leaves 47 (52-5)");

            bool threw = false;
            try
            {
                new Deck(stripRanks: Ranks.Order).Draw();
            }
            catch (InvalidOperationException) { threw = true; }
            Harness.Check(threw, "empty deck FAILS LOUD (throws) — a clear crash beats silent wrong data");

            // ---- LINQ / collections the interview actually uses -------------------
            Harness.Section("LINQ & collections you actually use");
            var demoHand = new List<Card> { new Card("7","H"), new Card("7","S"), new Card("Q","D"),
                                        new Card("2","C"), new Card("9","H") };
            Harness.Check(demoHand.Sum(c => c.Strength + 1) == (7 + 7 + 12 + 2 + 9), "Sum over a hand");
            Harness.Check(demoHand.Count(c => c.Suit == "H") == 2, "Count(predicate): 2 hearts");
            Harness.Check(demoHand.All(c => c.Suit == "H") == false, "All (flush check) = false here");
            Harness.Check(demoHand.GroupBy(c => c.Rank).Any(g => g.Count() == 2), "GroupBy finds the pair of 7s");
            Harness.Check(string.Join(" ", demoHand.OrderBy(c => c.Strength).Select(c => c.Rank))
                                == "2 7 7 9 Q", "OrderBy is for DISPLAY — the hand itself is untouched");

        }
    }
}