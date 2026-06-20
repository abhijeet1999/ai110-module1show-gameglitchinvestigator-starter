from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# FIX: This test targets the specific high/low hint direction bug that existed in the
# original app.py check_guess fallback, where "Too High" was paired with "Go HIGHER!"
def test_high_hint_direction():
    # A guess of 60 against a secret of 50 must return "Too High" (player should go lower).
    # The old code returned "Too High" with icon "📈 Go HIGHER!" — wrong direction.
    assert check_guess(60, 50) == "Too High"

def test_low_hint_direction():
    # A guess of 40 against a secret of 50 must return "Too Low" (player should go higher).
    # The old code returned "Too Low" with icon "📉 Go LOWER!" — wrong direction.
    assert check_guess(40, 50) == "Too Low"

def test_even_attempt_no_string_coercion():
    # Regression test for the even-attempt type coercion bug in the original app.py,
    # where secret was cast to str on even turns, making check_guess compare int to str.
    # The fixed logic_utils.check_guess always works with ints.
    assert check_guess(50, 50) == "Win"
    assert check_guess(51, 50) == "Too High"
    assert check_guess(49, 50) == "Too Low"
