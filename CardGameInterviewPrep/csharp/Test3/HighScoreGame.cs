using static Deck;

namespace Test3
{
    internal class HighScoreGame
    {
        public List<Player> Players { get; }
        public Deck Deck { get; }
        public HighScoreGame(string[] names, bool includeJokers = false, int? seed = null)
        {
            Players = names.Select(x => new Player(x)).ToList();
            Deck = new Deck(includeJokers: includeJokers, seed: seed);
            Deck.Shuffle();
        }

        public void Deal(int cardsEach)
        {
            for (int i = 0; i < cardsEach; i++)
            {
                foreach (var item in Players)
                {
                    item.Hand.Add(Deck.Draw());
                }
            }
        }

        public virtual int PointsOf(Card card) => card.Strength + 1;

        public virtual int ScoreHand(Player player) => player.Hand.Sum(PointsOf);

        public List<Player> Winners()
        {
            int best = Players.Max(ScoreHand);
            return Players.Where(x => ScoreHand(x) == best).ToList();
        }

        public static void RunChecks()
        {
            Harness.Section("High Score game + mutations (each change in ONE place)");
            var q = new Card("Q", "D");
            var five5 = new Card("5", "D");
            var five5h = new Card("5", "H");

            var baseGame = new HighScoreGame(new[] { "A" });
            Harness.Check(baseGame.PointsOf(q) == 12, "default points: Q = 12 (strength+1)");

            //var faces = new FaceCardsAreTenGame(new[] { "A" });
            //Harness.Check(faces.PointsOf(q) == 10, "MUTATION 'J/Q/K=10' lands in PointsOf only");

            //var dd = new DoubleDiamondsGame(new[] { "A" });
            //Harness.Check(dd.PointsOf(five5) == 10 && dd.PointsOf(five5h) == 5,
            //              "MUTATION 'diamonds double': 5D=10, 5H=5 — PointsOf only, display untouched");

            // Winners always returns a LIST (ties are real). Force a tie and prove two winners.
            var tieGame = new HighScoreGame(new[] { "X", "Y" });
            tieGame.Players[0].Hand.Add(new Card("K", "C"));   // 13
            tieGame.Players[1].Hand.Add(new Card("K", "D"));   // 13
            Harness.Check(tieGame.Winners().Count == 2, "ties are real: Winners() returns BOTH tied players");

            //// 'Lowest wins' = Max->Min in Winners only.
            //var low = new LowestWinsGame(new[] { "Lo", "Hi" });
            //low.Players[0].Hand.Add(new Card("2", "C"));       // 2
            //low.Players[1].Hand.Add(new Card("K", "C"));       // 13
            //Harness.Check(low.Winners().Single().Name == "Lo", "MUTATION 'lowest wins' = Max->Min in Winners only");

            //// Rule of two: two scorings coexist behind ONE call site via a delegate.
            //var strat = new StrategyScoredGame(new[] { "A" }, c => c.IsJoker ? 20 : c.Strength + 1);
            //Harness.Check(strat.PointsOf(new Card("JOKER", null)) == 20,
            //              "RULE OF TWO: swap scoring via a delegate (extract on the SECOND variant)");

            // A full demo round — what Part 2 output actually looks like (seed 42 = deterministic).
            Harness.Section("Demo: a full High Score round");
            var game = new HighScoreGame(new[] { "Alice", "Bob", "Cara" }, seed: 42);
            game.Deal(5);
            foreach (var p in game.Players)
                Console.WriteLine($"  {p.Name,-6} score {game.ScoreHand(p),3}   {p.ShowHand()}");
            Console.WriteLine("  Winner(s): " + string.Join(", ", game.Winners().Select(w => w.Name)));
        }
    }
}
