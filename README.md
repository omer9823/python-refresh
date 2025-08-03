# Blackjack Casino Project

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

---

## Running the Console Blackjack Game

To play blackjack in your terminal:
```sh
python -m console.console_runner
```

---

## Running the Full Web App (Casino UI)

1. **Start the FastAPI server:**
   ```sh
   uvicorn app.main:app --reload
   ```
2. **Open the casino client in your browser:**
   [http://localhost:8000/static/blackjack.html](http://localhost:8000/static/blackjack.html)

- Play blackjack with a modern casino interface.
- The AI Advisor panel shows real-time basic and count-adjusted strategy.
- Place bets visually (betting is currently visual only).
- Play using the Deal, Hit, and Stand buttons.

---

**Notes:**
- Make sure your virtual environment is activated before running any of the above commands.
- You do NOT need Poetry or pyproject.toml for this project. All dependencies are managed with `requirements.txt` and `pip`.