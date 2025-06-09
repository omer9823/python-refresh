from app.services.simulation_service import SimulationService

if __name__ == "__main__":
    num_hands = 100000
    sim = SimulationService(num_decks=6, penetration=0.75, base_bet=10)

    print("Running Basic Strategy Simulation...")
    basic_stats = sim.run_simulation(num_hands=num_hands, strategy="basic")

    print("\nRunning Count-Aware Strategy Simulation...")
    count_stats = sim.run_simulation(num_hands=num_hands, strategy="count")

    def print_results(stats, name):
        results = stats["results"]
        profit = stats["profit"]
        total = sum(results.values())

        print(f"\n{name} Results:")
        for k, v in results.items():
            print(f"{k.capitalize()}: {v} ({v/total:.2%})")
        print(f"Total Profit: {profit} ({profit/(total*10):.2%} relative to total bets)")

    print_results(basic_stats, "Basic Strategy")
    print_results(count_stats, "Count-Aware Strategy")
