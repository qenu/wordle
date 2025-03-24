import json

from wordle_game import WordleGame
from wordle_solver import WordleSolver

guess_json = "guess.json"
answer_json = "answer.json"


def load_word_lists():
    with open(guess_json) as file:
        guess_words = json.load(file)
    with open(answer_json) as file:
        answer_words = json.load(file)
    return answer_words, guess_words


def main():
    answer_words, guess_words = load_word_lists()
    solver = WordleSolver(answer_words, guess_words)

    total_attempts = []
    failures = []
    for target_word in answer_words[:500]:  # Limit for testing
        game = WordleGame(target_word)
        solver.reset()
        print(f"Target word: {target_word}")

        while not game.is_over():
            guess = solver.suggest_guess()
            feedback = game.play_round(guess)
            solver.process_feedback(guess, feedback)
            print(f"Guess: {guess}, Feedback: {feedback}")

        attempts = game.attempts
        total_attempts.append(attempts)
        print(f"Result: {'WIN' if game.won else 'FAIL'} in {attempts} attempts\n")
        if not game.won:
            failures.append(target_word)

    print(f"Max Attempts: {max(total_attempts)}")
    print(f"Avg Attempts: {sum(total_attempts) / len(total_attempts):.2f}")
    print(f"Fails: {failures}")


if __name__ == "__main__":
    main()
