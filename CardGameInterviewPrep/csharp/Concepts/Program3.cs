using System;
using System.Collections.Generic;
using System.Linq;

namespace Concepts.Pratice3
{

    static class Ranks
    {
        public static readonly string[] Order = { "" };
        public static int Strength(string rank) => Array.IndexOf(Order, rank);
    }

    static class Suits
    {
        public static readonly string[] All = { "" };
        public static readonly string[] Strength = { "" };
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

        public int Strength => Ranks.Strength(Rank);

        public override string ToString()
        {
            return IsJoker ? "JOKER" : Rank + Suit;
        }
    }

    sealed class Deck
    {
        public List<Card> _cards { get; set; } = new List<Card>();
        Random _rng;

        public Deck(bool includeJoker, int deckCount, string[] skipRanks = null, string[] skipSuits = null, int? seeds = null)
        {
            _rng = seeds != null ? new Random(seeds.Value) : new Random();
            for (int i = 0; i < deckCount; i++)
            {
                foreach (var suit in Suits.All)
                {
                    if (skipRanks == null || !skipRanks.Contains(suit))
                    {
                        foreach (var rank in Ranks.Order)
                        {
                            if (rank != "JOKER" && (skipSuits == null || !skipSuits.Contains(rank)))
                            {
                                _cards.Add(new Card(rank, suit));
                            }
                        }
                    }
                }

                if (includeJoker)
                {
                    _cards.Add(new Card("JOKER", null));
                    _cards.Add(new Card("JOKER", null));
                }
            }
        }

        public int Count => _cards.Count;

        public void Shuffle()
        {
            for (int i = _cards.Count; i > 0; i--)
            {
                int j = _rng.Next(i + 1);
                (_cards[i], _cards[j]) = (_cards[j], _cards[i]);
            }
        }

        public int Draw()
        {
            if(_cards.Count == 0)
            {
                throw new InvalidOperationException("Can not draw from empty declk");

            }
        }


    }













}
