import math
from collections import Counter, defaultdict
from typing import List


class WordleSolver:
    def __init__(self, answer_words: List[str], guess_words: List[str] = None):
        self.answer_words = answer_words
        self.guess_words = guess_words or answer_words
        self.candidates = answer_words.copy()
        self.past_route = {"init": "TARSE"}
        self.current_route = ""

    def reset(self):
        self.candidates = self.answer_words.copy()
        self.current_route = ""

    def process_feedback(self, guess: str, feedback: str):
        guess = guess.upper()
        self.candidates = [
            word
            for word in self.candidates
            if self.is_candidate_valid(word, guess, feedback)
        ]
        if self.current_route:
            self.past_route[self.current_route] = guess
        self.current_route = "".join([self.current_route, guess, feedback])

    def is_candidate_valid(self, word: str, guess: str, feedback: str) -> bool:
        used = [False] * 5

        for i in range(5):
            if feedback[i] == "g":
                if word[i] != guess[i]:
                    return False
                used[i] = True

        for i in range(5):
            if feedback[i] == "y":
                if guess[i] == word[i]:
                    return False
                found = False
                for j in range(5):
                    if (not used[j]
                            and word[j] == guess[i]
                            and guess[j] != word[j]):
                        used[j] = True
                        found = True
                        break
                if not found:
                    return False

        for i in range(5):
            if feedback[i] == "b":
                letter = guess[i]
                count_in_guess = sum(
                    1
                    for j in range(5)
                    if guess[j] == letter and feedback[j] in {"g", "y"}
                )
                count_in_word = sum(1 for j in range(5) if word[j] == letter)
                if count_in_word > count_in_guess:
                    return False

        return True

    def get_feedback(self, guess: str, answer: str) -> str:
        feedback = ["b"] * 5
        answer_chars = list(answer)

        for i in range(5):
            if guess[i] == answer[i]:
                feedback[i] = "g"
                answer_chars[i] = None

        for i in range(5):
            if feedback[i] == "b" and guess[i] in answer_chars:
                feedback[i] = "y"
                answer_chars[answer_chars.index(guess[i])] = None

        return "".join(feedback)

    def compute_entropy(self, guess: str) -> float:
        feedback_buckets = defaultdict(int)
        for answer in self.candidates:
            fb = self.get_feedback(guess, answer)
            feedback_buckets[fb] += 1

        total = len(self.candidates)
        entropy = 0.0
        for count in feedback_buckets.values():
            p = count / total
            entropy -= p * math.log2(p)
        return entropy

    def suggest_guess(self) -> str:
        if len(self.candidates) == len(self.answer_words):
            return self.past_route["init"]

        if len(self.candidates) == 1:
            return self.candidates[0]

        if self.past_route.get(self.current_route, 0):
            return self.past_route[self.current_route]

        def unique_letter_bonus(word):
            return len(set(word)) * 0.0001

        def letter_frequency_bonus(word):
            counts = Counter("".join(self.candidates))
            return sum([counts[c] for c in set(word)]) * 0.0001

        def position_frequency_bonus(word):
            position_counts = [Counter()] * 5
            for w in self.candidates:
                for i, c in enumerate(w):
                    position_counts[i][c]
            return sum(
                position_counts[i][c]
                for i, c in enumerate(word)
                ) * 0.0001

        def is_candicate(word):
            return 0.01 if word in self.candidates else 0

        def score(g):
            e = self.compute_entropy(g)
            bonus = 0
            bonus += is_candicate(g)
            bonus += unique_letter_bonus(g)
            bonus += letter_frequency_bonus(g)
            bonus += position_frequency_bonus(g)
            return e + bonus

        return max(self.guess_words, key=score)
