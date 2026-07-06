using System;
using System.Collections.Generic;
using System.Linq;

namespace Concepts.Ace
{
    static class Ranks
    {
        public static readonly string[] Order = { "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "JOKER" };

        public static int Strength(string rank) => Array.IndexOf(Order, rank);
    }

    static class Suits
    {
        public static readonly string[] All = { "C", "D", "H", "S" }; // ♣ ♦ ♥ ♠

        public static readonly string[] Strength = { "C", "D", "H", "S" }; // ♣ ♦ ♥ ♠
        public static int Of(string suit) => Array.IndexOf(Strength, suit);
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
        public override string ToString() => IsJoker ? "JOKER" : Rank + Suit;
    }

    sealed class Deck
    {
        public List<Card> _cards = new List<Card>();
        public Random _rng;
        public Deck(bool isJokerIncluded, int deckCount, string[] skipRanks = null, string[] skipSuits = null, int? seed = null)
        {
            _rng = seed != null ? new Random(seed.Value) : new Random();
            var suits = new HashSet<string>(skipSuits ?? Array.Empty<string>());
            var ranks = new HashSet<string>(skipRanks ?? Array.Empty<string>());
            for (int i = 0; i < deckCount; i++)
            {
                foreach (var suit in Suits.All)
                {
                    if (!suits.Contains(suit))
                    {
                        foreach (var rank in Ranks.Order)
                        {
                            if (rank != "JOKER" && !ranks.Contains(rank))
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
                throw new InvalidOperationException("Can not draw from an empty deck");
            var top = _cards[_cards.Count - 1];
            _cards.RemoveAt(_cards.Count - 1);
            return top;
        }

        public List<Card> Draw(int n) => Enumerable.Range(0, n).Select(_ => Draw()).ToList();
    }

    sealed class Person
    {
        public Person(string name)
        {
            Name = name;
        }
        public string Name { get; set; }

        public List<Card> Hand { get; set; } = new List<Card>();

        public int Score { get; set; }

        public string ShowHand() => string.Join(" ", Hand);
    }

    internal class Program2
    {
    }
}
