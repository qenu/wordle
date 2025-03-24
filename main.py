import json
import time
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
    time_consumed = []
    for target_word in answer_words:  # Limit for testing
        game = WordleGame(target_word)
        solver.reset()
        start_ts = time.time()
        while not game.is_over():
            remain_size = len(solver.candidates)
            guess = solver.suggest_guess()
            entropy = solver.compute_entropy(guess)
            feedback = game.play_round(guess)
            solver.process_feedback(guess, feedback)
            reduction = (1 - (len(solver.candidates) / remain_size)) * 100
            print(
                f"Guess: {guess}, "
                f"Feedback: {feedback}, "
                f"Reduce: {reduction:>5.2f}%, "
                f"Remain: {len(solver.candidates):>3}, "
                f"Entropy: {entropy:.3f}"
            )

        attempts = game.attempts
        total_attempts.append(attempts)
        time_consumed.append(time.time() - start_ts)
        print(
            f"Solve: {target_word}, "
            f"Attempts: {attempts}, "
            f"Result: {'WIN' if game.won else 'FAIL'}, "
            f"Time used: {time_consumed[-1]:.2f}s"
            "\n"
        )
        if not game.won:
            game_lost.append(target_word)

    print("Game Summary")
    print("============")
    print(f"Total Guess: {len(total_attempts):,}")
    print(f"Ran Attempts: {sum(total_attempts):,}")
    print(f"Max Attempts: {max(total_attempts)}")
    print(f"Avg Attempts: {sum(total_attempts) / len(total_attempts):.2f}")
    print("\n")
    print(f"Total Time: {sum(time_consumed):.2f}s")
    print(f"Avg Time: {sum(time_consumed) / len(time_consumed):.2f}s")
    print(f"Max Time: {max(time_consumed):.2f}s")
    print("\n")
    print(f"Lost: {game_lost if game_lost else 'None'}")
    print("\n")
    print("Attempt Distribution")
    for i in range(1, max(total_attempts) + 1):
        count = total_attempts.count(i)
        if count:
            print(
                f"Attempts: {i}, "
                f"Count: {count:>5,}, "
                f"Ratio: {count / len(total_attempts):.2%}"
                )
    print("============")


if __name__ == "__main__":
    main()
