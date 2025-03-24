import json
from os.path import join

from wordle_game import WordleGame
from wordle_solver import WordleSolver

guess_json = "guess.json"
answer_json = "answer.json"


def load_word_lists():
    with open(join("source", guess_json)) as file:
        guess_words = json.load(file)
    with open(join("source", answer_json)) as file:
        answer_words = json.load(file)
    return answer_words, guess_words


def main():
    answer_words, guess_words = load_word_lists()
    solver = WordleSolver(answer_words, guess_words)

    total_attempts = []
    game_lost = []
    for target_word in answer_words:  # Limit for testing
        game = WordleGame(target_word)
        solver.reset()
        print(f"Target word: {target_word}")
        while not game.is_over():
            remain_size = len(solver.candidates)
            guess = solver.suggest_guess()
            feedback = game.play_round(guess)
            solver.process_feedback(guess, feedback)
            print(
                f"Guess: {guess}, "
                f"Feedback: {feedback}, "
                f"Reduce: {(
                    1-(len(solver.candidates)/remain_size)
                    )*100:.2f}%, "
                f"Remain: {len(solver.candidates)}"
            )

        attempts = game.attempts
        total_attempts.append(attempts)
        print(f"Result: {'WIN' if game.won else 'FAIL'} in {attempts} attempts\n")
        if not game.won:
            game_lost.append(target_word)

    print(f"Max Attempts: {max(total_attempts)}")
    print(f"Avg Attempts: {sum(total_attempts) / len(total_attempts):.2f}")

    print(f"Lost: {game_lost if game_lost else 'None'}")


if __name__ == "__main__":
    main()
