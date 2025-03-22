import math
from collections import defaultdict
from typing import List

class WordleSolver:
    def __init__(self, answer_words: List[str], guess_words: List[str] = None):
        self.answer_words = answer_words
        self.guess_words = guess_words or answer_words
        self.candidates = answer_words.copy()

    def reset(self):
        self.candidates = self.answer_words.copy()

    def process_feedback(self, guess: str, feedback: str):
        self.candidates = [
            word for word in self.candidates
            if self.is_candidate_valid(word, guess, feedback)
        ]

    def is_candidate_valid(self, word: str, guess: str, feedback: str) -> bool:
        used = [False] * 5

        for i in range(5):
            if feedback[i] == 'g':
                if word[i] != guess[i]:
                    return False
                used[i] = True

        for i in range(5):
            if feedback[i] == 'y':
                if guess[i] == word[i]:
                    return False
                found = False
                for j in range(5):
                    if not used[j] and word[j] == guess[i] and guess[j] != word[j]:
                        used[j] = True
                        found = True
                        break
                if not found:
                    return False

        for i in range(5):
            if feedback[i] == 'b':
                letter = guess[i]
                count_in_guess = sum(
                    1 for j in range(5)
                    if guess[j] == letter and feedback[j] in {'g', 'y'}
                )
                count_in_word = sum(
                    1 for j in range(5)
                    if word[j] == letter
                )
                if count_in_word > count_in_guess:
                    return False

        return True

    def get_feedback(self, guess: str, answer: str) -> str:
        feedback = ['b'] * 5
        answer_chars = list(answer)

        for i in range(5):
            if guess[i] == answer[i]:
                feedback[i] = 'g'
                answer_chars[i] = None

        for i in range(5):
            if feedback[i] == 'b' and guess[i] in answer_chars:
                feedback[i] = 'y'
                answer_chars[answer_chars.index(guess[i])] = None

        return ''.join(feedback)

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
        return max(self.guess_words, key=lambda g: self.compute_entropy(g))