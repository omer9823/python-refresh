poetry run python -m console.player_runner

uvicorn app.main:app --reload

poetry run python simulation/simulation_runner.py