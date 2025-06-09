from app.services.simulation_service import SimulationService

if __name__ == "__main__":
    sim = SimulationService(num_decks=6, penetration=0.75)
    results = sim.run_simulation(num_hands=10000)

    total = sum(results.values())
    for k, v in results.items():
        print(f"{k.capitalize()}: {v} ({v/total:.2%})")
