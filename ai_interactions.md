# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I gave Claude Code (agent mode) this multi-step instruction:

> "Move the `check_guess` and `parse_guess` functions to `logic_utils.py`, update the logic to fix the high/low bug and the even-attempt string coercion bug, and update the import in `app.py`."

**What did the agent do?**

The agent executed the following steps autonomously:

1. Read `app.py`, `logic_utils.py`, and `tests/test_game_logic.py` to understand the current state.
2. Identified that `logic_utils.py` already had correct versions of all four functions; the problem was that `app.py` was using its own broken inline copies.
3. Rewrote `app.py` to remove the four duplicate function definitions and add `from logic_utils import parse_guess, check_guess, update_score, get_range_for_difficulty`.
4. Removed the even-attempt string coercion block (`if st.session_state.attempts % 2 == 0: secret = str(...)`) and updated the `check_guess` call to use the new single-return-value signature.
5. Added a `HINT_MESSAGES` dict to map outcome strings to player-facing emoji text.
6. Fixed the New Game button to use `random.randint(low, high)` instead of the hardcoded `(1, 100)` and to reset all session state fields.
7. Added a `#FIX:` comment to `logic_utils.check_guess` documenting the collaboration.
8. Ran `pytest tests/test_game_logic.py -v` to verify all tests passed before reporting back.

**What did you have to verify or fix manually?**

- I reviewed every diff the agent produced before accepting it. The logic in `app.py` was 100% correct, but I confirmed the `HINT_MESSAGES` dictionary had the right emoji for each outcome (📉 Go LOWER for Too High, 📈 Go HIGHER for Too Low) since the original code had those swapped.
- I verified the New Game state reset was complete — the agent correctly reset `score`, `history`, and `status` in addition to `attempts` and `secret`, which the original button had missed.
- I ran the live Streamlit app manually after the agent finished and confirmed that guessing above the secret showed "📉 Go LOWER!" and guessing below showed "📈 Go HIGHER!" on both even and odd attempts.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Hint direction: guess above secret | "Generate a pytest case that verifies a guess of 60 against secret 50 returns 'Too High'" | `assert check_guess(60, 50) == "Too High"` (test_high_hint_direction) | Yes | The old app.py code paired "Too High" with "📈 Go HIGHER!" — this test catches the direction mismatch at the outcome level |
| Hint direction: guess below secret | "Generate a pytest case that verifies a guess of 40 against secret 50 returns 'Too Low'" | `assert check_guess(40, 50) == "Too Low"` (test_low_hint_direction) | Yes | Mirror of the above — covers the "Too Low → Go LOWER" direction bug |
| Even-attempt type coercion regression | "Write a test that proves check_guess always returns correct results regardless of attempt parity" | Three assertions in one test: Win, Too High, Too Low with int inputs (test_even_attempt_no_string_coercion) | Yes | The AI suggested combining three boundary assertions in one test to guard against the int-vs-str coercion that only appeared on even attempts |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
