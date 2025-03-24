class WordleGame:
    def __init__(self, target_word: str, max_attempts: int = 6):
        self.target_word = target_word
        self.max_attempts = max_attempts
        self.attempts = 0
        self.won = False

    def get_feedback(self, guess: str) -> str:
        feedback = ["b"] * 5
        answer_chars = list(self.target_word)

        for i in range(5):
            if guess[i] == self.target_word[i]:
                feedback[i] = "g"
                answer_chars[i] = None

        for i in range(5):
            if feedback[i] == "b" and guess[i] in answer_chars:
                feedback[i] = "y"
                answer_chars[answer_chars.index(guess[i])] = None

        return "".join(feedback)

    def play_round(self, guess: str) -> str:
        self.attempts += 1
        feedback = self.get_feedback(guess.upper())
        if feedback == "ggggg":
            self.won = True
        return feedback

    def is_over(self) -> bool:
        return self.won or self.attempts >= self.max_attempts
