import json
import random
from collections import Counter

source = "wordlist.json"
length_check = 3189


class WordleSolver:
    def __init__(self) -> None:
        self.word_list: list = self._loader(source)
        self.reload()

    def _loader(self, path: str) -> list:
        with open(path) as file:
            result: list = json.load(file)
        return result

    def _word_weight(self) -> dict:
        freq: Counter = Counter()
        for word in self.word_list:
            for letter in set(word):
                freq[letter] += 1

        result: dict = {
            word: sum([freq[lt] for lt in set(word)])
            for word in self.word_list
        }

        return sorted(result.items(), key=lambda x: x[1], reverse=True)

    def next_guess(self) -> str:
        return next(iter(self.val))[0]

    def reload(self) -> None:
        self.val: dict = self._word_weight()

    def remove_letters(self, s: str):
        self.word_list = list(
            filter(lambda x: not any(
                lt in x for lt in s.upper()
                ), self.word_list)
        )

    def misplace_letters(self, s: str):
        """
        use _ to represent ignored letters.
        eg: '___r_'
        """
        self.word_list = list(
            filter(
                lambda x: not any(
                    pair in tuple(enumerate(x))
                    for pair in tuple(enumerate(s.upper()))
                ),
                self.word_list,
            )
        )

    def correct_letters(self, s: str):
        """
        use _ to represent ignored letters.
        eg: '___r_'
        """
        if len(set(s)) == 1:
            return
        self.word_list = list(
            filter(
                lambda x: all(
                    lt == '_' or (idx, lt) in tuple(enumerate(x))
                    for idx, lt in tuple(enumerate(s.upper()))
                ),
                self.word_list,
            )
        )

    def update_list(self, s: str):
        """
        use o to represent correct word, correct placement.
        use x to represent correct word, incorrect placement.
        use _ to represent ignored letters.
        eg: 'o_x__'
        """
        filter_list: list[tuple] = list(enumerate(s.upper()))

        self.remove_letters(
            "".join(
                [self.next_guess()[idx]
                 for idx, hint in filter_list if hint == "_"]
                )
            )

        self.misplace_letters(
            "".join(
                [lt if lt == "_" else self.next_guess()[idx]
                 for idx, lt in list(enumerate(s.upper().replace("O", "_")))]
                )
            )

        self.correct_letters(
            "".join(
                [lt if lt == "_" else self.next_guess()[idx]
                 for idx, lt in list(enumerate(s.upper().replace("X", "_")))]
                )
            )

        self.reload()

    @property
    def status(self) -> None:
        print(f"Word count: {len(self.word_list):,}")
        print(f"Next guess: {self.next_guess()}")


class WordleGame:
    def __init__(self) -> None:
        self.ans: str = self._random_word()

    def _random_word(self) -> str:
        with open(source) as file:
            word_list: list = json.load(file)
        return random.choice(word_list)

    def guess(self, word: str) -> str:
        if word == self.ans:
            return "End"
        response: str = ""
        for idx, lt in enumerate(word):
            if lt == self.ans[idx]:
                response += "O"
            elif lt in self.ans:
                response += "X"
            else:
                response += "_"
        return response


def fast_game_result():
    s = WordleSolver()
    g = WordleGame()

    for rnd in range(6):
        r = g.guess(s.next_guess())
        if r == "End":
            return rnd
        s.update_list(r)
    print("Failed: ", g.ans)
    return 6


def fast_games(count: int = 100):
    games = [fast_game_result() for _ in range(count)]
    print(f"Average rounds: {sum(games) / len(games)}")
    print(f"Round 1: {games.count(1)}")
    print(f"Round 2: {games.count(2)}")
    print(f"Round 3: {games.count(3)}")
    print(f"Round 4: {games.count(4)}")
    print(f"Round 5: {games.count(5)}")
    print(f"Round Failed: {games.count(6)}")


def custom_game(ans: str = ''):
    s = WordleSolver()
    g = WordleGame()
    if ans:
        g.ans = ans
    print(f"=> {g.ans}")
    for rnd in range(10):
        print("-" * 20)
        print(f"Round {rnd + 1}")
        s.status
        print(f"Guesses: {s.val[:5]}")
        r = g.guess(s.next_guess())
        print(f"result: {r}")
        if r == "End":
            print("Game Over")
            break
        s.update_list(r)
        # break


if __name__ == "__main__":
    fast_games()
    # custom_game('SOUND')
    # tried
    # salon
