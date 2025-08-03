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

## Playing Blackjack via WebSocket (with HTML Client)

1. **Start the FastAPI server:**
   ```sh
   uvicorn app.main:app --reload
   ```
2. **Open the HTML client:**
   - Open `static/blackjack.html` in your web browser (double-click or right-click and choose "Open with browser").
   - The client will connect to the backend at `ws://localhost:8000/ws/game`.
   - Use the "Start Game", "Hit", and "Stand" buttons to play.

**Note:** If you want to serve the HTML file via FastAPI, you can add this to your `main.py`:
```python
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")
```
Then access the client at [http://localhost:8000/static/blackjack.html](http://localhost:8000/static/blackjack.html).

---

**Notes:**
- Make sure your virtual environment is activated before running any of the above commands.
- If you use Poetry, you can run commands with `poetry run`, for example:
  ```sh
  poetry run python -m console.console_runner
  ```