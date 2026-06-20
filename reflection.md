# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The first time I ran it, the game loaded fine and looked normal, but the hints could not be trusted. No matter what I guessed, it kept telling me to "Go LOWER," even when my guess was already below the secret number. The direction hints were also flat-out backwards: when I guessed too high it would tell me to go HIGHER, and when I guessed too low it would tell me to go LOWER, which is the opposite of what should happen. On top of that, the input wasn't validated at all — even though the range was supposed to be 1 to 100, I was able to type in 0 and the game accepted it as a real guess.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
| ---------- | ----------------- | --------------- | ---------------------- |
| Guess below the secret (e.g. secret 60, guess 30) | "Too Low" hint, telling me to go HIGHER | "Go LOWER" hint shown no matter what | none |
| Guess of 0 | Rejected since the range is 1 to 100 | Game accepted 0 as a valid guess and counted the attempt | none |
| Guess above the secret (e.g. secret 40, guess 80) | "Too High" hint, telling me to go LOWER | "Go HIGHER" hint shown (direction reversed) | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I described one specific glitch to the AI — that the direction hints were reversed, where guessing too high told me to "Go HIGHER" and guessing too low told me to "Go LOWER" — and asked it to explain the underlying logic. It pointed me to the `check_guess` function in app.py and explained that the outcome label ("Too High" / "Too Low") was actually being computed correctly, but the hint message paired with each branch was swapped: when `guess > secret` the code returned "Go HIGHER!" when it should say "Go LOWER!", and vice versa. It also flagged a second, deeper cause of my "always Go LOWER" bug: on every even-numbered attempt the code converts the secret to a string (`secret = str(st.session_state.secret)`), so it ends up comparing an int to a string. That makes `guess == secret` always False (you can never win on an even attempt) and `guess > secret` throw a TypeError, after which a fallback block compares the numbers as text lexicographically (so "9" counts as greater than "60"), producing erratic, stuck hints. Having the AI trace the logic line by line was far faster than me reading the whole file, and I verified each explanation by checking the exact lines it cited in app.py.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

A bug wasn't really fixed until two things were true: the pytest suite passed and I manually played a round in the live game where the hints matched reality. For the hint-direction bug I first wrote `test_high_hint_direction` — `check_guess(60, 50)` should return `"Too High"` — and ran `pytest tests/test_game_logic.py -v`. Before the refactor the app's inline version would have compared an int against a string on every even attempt and entered a broken fallback that swapped icons; after moving the clean `logic_utils.check_guess` into use all six tests went green in 0.02 s. I also wrote `test_even_attempt_no_string_coercion` to lock in the regression: it calls `check_guess` with three boundary values (`49`, `50`, `51`) and asserts each returns the right outcome string, making it impossible for the int-vs-string coercion to sneak back. The AI helped design the tests by suggesting I focus on the exact input that triggered the old fallback path (an even attempt number when secret was coerced to a string), and it recommended I document each test with a short comment explaining *which* old bug it guards against, not just what the function should return.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
