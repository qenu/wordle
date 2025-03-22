import requests
from wordle_game import WordleGame
from wordle_solver import WordleSolver

def load_word_lists():
    url = "https://raw.githubusercontent.com/tabatkins/wordle-list/main/words"
    response = requests.get(url)
    words = response.text.splitlines()
    answer_words = words[:2315]
    guess_words = words
    return answer_words, guess_words

def main():
    answer_words, guess_words = load_word_lists()
    solver = WordleSolver(answer_words, guess_words)

    total_attempts = []
    for target_word in answer_words[:10]:  # Limit for testing
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

    print(f"Max Attempts: {max(total_attempts)}")
    print(f"Avg Attempts: {sum(total_attempts) / len(total_attempts):.2f}")

if __name__ == "__main__":
    main()