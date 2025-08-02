# Python Refresh Project

## Prerequisites

- Python 3.8 or higher
- (Recommended) Virtual environment (venv)

## Setup Instructions

1. Open a terminal in the project root directory.
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Console Runner

To start the main console interface:
```sh
python -m console.console_runner
```

To run the player runner:
```sh
python -m console.player_runner
```

## Running the Simulation

```sh
python simulation/simulation_runner.py
```

## Running the FastAPI Server

```sh
uvicorn app.main:app --reload
```

---

**Notes:**
- Make sure your virtual environment is activated before running any of the above commands.
- If you use Poetry, you can run commands with `poetry run`, for example:
  ```sh
  poetry run python -m console.console_runner
  ```