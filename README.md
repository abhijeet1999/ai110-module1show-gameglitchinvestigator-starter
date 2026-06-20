# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

An AI "built" a number guessing game in Streamlit, then left behind three silent bugs that made the game unplayable:

- Hints were backwards — "Too High" told you to go HIGHER, "Too Low" told you to go LOWER.
- On every even-numbered attempt the secret was secretly converted to a string, making it impossible to win on those turns and causing hints to freeze on "Go LOWER" regardless of your guess.
- The New Game button reset attempts to 0 (skipping the first turn) and always used a hardcoded range of 1–100, ignoring the selected difficulty.

This project is about finding those bugs, fixing them with the help of an AI coding assistant (Claude Code), writing automated tests that prove the fixes hold, and reflecting on how human + AI collaboration works in practice.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the fixed app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask your AI assistant: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** Move the logic into `logic_utils.py`, run `pytest`, and keep fixing until all tests pass.

## 📝 Bugs Found and Fixed

| Bug | Root Cause | Fix Applied |
|-----|-----------|-------------|
| Hints always said "Go LOWER" regardless of guess | On even attempts, `secret` was cast to `str`, so int-vs-string comparison always fell into the wrong branch | Removed the `str()` coercion; `check_guess` now always receives two ints |
| Hint direction reversed (Too High → "Go HIGHER") | `check_guess` in app.py had the emoji icons swapped in its fallback block | Replaced app.py's inline `check_guess` with the correct version from `logic_utils.py` |
| New Game ignored difficulty range | `random.randint(1, 100)` was hardcoded; attempts reset to 0 instead of 1 | Updated to use `random.randint(low, high)` from `get_range_for_difficulty`; resets all state cleanly |
| Duplicate logic in app.py and logic_utils.py | `parse_guess`, `check_guess`, `update_score` were defined in both files | Removed duplicates from app.py; app now imports from `logic_utils` |

## 📸 Demo Walkthrough

A step-by-step walkthrough of the fixed game on Normal difficulty (range 1–100, 8 attempts):

1. Launch the app with `streamlit run app.py`. The sidebar shows **Normal** difficulty, range 1–100, 8 attempts allowed.
2. Expand **Developer Debug Info** to reveal the secret number (e.g., 63).
3. Type **80** in the guess box and click **Submit Guess**. The hint reads "📉 Go LOWER!" — correct, because 80 > 63.
4. Type **40** and submit. The hint reads "📈 Go HIGHER!" — correct, because 40 < 63.
5. Type **63** and submit. Balloons appear and the success banner shows "You won! The secret was 63."
6. Click **New Game**. The secret resets to a fresh random number within 1–100 and the attempt counter returns to 1.
7. Switch to **Hard** difficulty in the sidebar. The sidebar now shows range 1–200 and 5 attempts. Click New Game — the new secret respects the Hard range.

## 🧪 Test Results

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/abhijeetcherungottil/Desktop/Codepath/ai110-module1show-gameglitchinvestigator-starter
collected 6 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 16%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 33%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 50%]
tests/test_game_logic.py::test_high_hint_direction PASSED                [ 66%]
tests/test_game_logic.py::test_low_hint_direction PASSED                 [ 83%]
tests/test_game_logic.py::test_even_attempt_no_string_coercion PASSED    [100%]

============================== 6 passed in 0.04s ==============================
```

## 🚀 Stretch Features

- [x] **SF7 — Test Generation:** Used Claude Code to design targeted regression tests for the hint-direction and even-attempt type-coercion bugs (documented in `ai_interactions.md`).
- [x] **SF8 — Agent Workflow:** Used Claude Code agent mode to issue a multi-step instruction that moved functions to `logic_utils.py`, fixed the bugs, and updated imports in one pass (documented in `ai_interactions.md`).
