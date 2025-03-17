import json
import random
from collections import Counter

source = "wordlist.json"
length_check = 3189


class WordleSolver:
    def __init__(self) -> None:
        self.word_list: list = self._loader(source)
        self.guess_list: list = self.word_list.copy()
        self.letter_removed: str = ""
        self.letter_solved: str = "_____"
        self.letter_found: str = ""
        self.reload()

    def _loader(self, path: str) -> list:
        with open(path) as file:
            result: list = json.load(file)
        return result

    def _word_weight(self) -> list[tuple]:
        freq: Counter = Counter()
        for word in self.guess_list:
            for letter in set(word):
                freq[letter] += 1

        max_freq = max(freq.values())
        for k, v in list(freq.items()):
            if v == max_freq:
                del freq[k]

        if len(freq) < 4:
            return [(self.guess_list[0],0)]

        result: dict = {
            word: sum([freq[lt] for lt in set(word)])
            for word in self.word_list
        }

        return sorted(result.items(), key=lambda x: x[1], reverse=True)
    
    def _word_weight_indexed(self) -> list[tuple]:
        if len(self.guess_list) == 1:
            return [(self.guess_list[0],0)]

        idx_freq: Counter = Counter()

        for word in self.guess_list:
            for idx, val in enumerate(word):
                idx_freq[(idx, val)] += 1

        if len(idx_freq) > 26:
            max_freq = max(idx_freq.values())
            for k, v in list(idx_freq.items()):
                if v == max_freq:
                    del idx_freq[k]

            # cum_freq: dict = {
            #     word: sum([idx_freq[(idx, val)] for idx, val in enumerate(word)])
            #     for word in self.word_list
            # }
            cum_freq = {}
            for word in self.word_list:
                _word = []
                _freq = []
                for idx, val in enumerate(word):
                    ratio = 1
                    if val in _word:
                        ratio *= 0.6
                    if val in self.letter_found:
                        ratio *= 0.6
                    _word.append(val)
                    _freq.append(round(idx_freq[(idx, val)]*ratio))
                cum_freq[word] = sum(_freq)

            sorted_cum: list = sorted(cum_freq.items(), key=lambda x: x[1], reverse=True)
            next_guess = [(k, v) for k, v in sorted_cum if v == max(cum_freq.values())]
            if len(next_guess) > 1:
                sorted_cum = [(word, val) for word, val in sorted_cum if self._word_match(word, self.letter_solved)]
            return sorted_cum
    
        else:
            return self._word_weight()

    def _word_weight_index(self):
        if len(self.guess_list) == 1:
            return [(self.guess_list[0],0)]

        indexed_freq: list[Counter] = [Counter()]*5

        for word in self.guess_list:
            for idx, val in enumerate(word):
                indexed_freq[idx][val] += 1

        for idx, lt in enumerate(self.letter_solved):
            if lt == '_':
                pass
            indexed_freq[idx][lt] = 0

        cum_freq = {}
        for word in self.word_list:
            _word = []
            _freq = []
            for idx, val in enumerate(word):
                ratio = 1
                if val in _word:
                    ratio *= 0.6
                if val in self.letter_found:
                    ratio *= 0.6
                _word.append(val)
                _freq.append(round(idx_freq[(idx, val)]*ratio))
            cum_freq[word] = sum(_freq)

        sorted_cum: list = sorted(cum_freq.items(), key=lambda x: x[1], reverse=True)
        next_guess = [(k, v) for k, v in sorted_cum if v == max(cum_freq.values())]
        if len(next_guess) > 1:
            sorted_cum = [(word, val) for word, val in sorted_cum if self._word_match(word, self.letter_solved)]
        return sorted_cum

    def next_guess(self) -> str:
        return next(iter(self.val))[0]

    def reload(self) -> None:
        self.val: list = self._word_weight_index()
        # self.val: list = self._word_weight_indexed()

    def remove_letters(self, s: str):
        self.guess_list = list(
            filter(lambda x: not any(
                lt in x for lt in s.upper()
                ), self.guess_list)
        )
        self.letter_removed = "".join(sorted(set(self.letter_removed + s)))

    def misplace_letters(self, s: str):
        """
        use _ to represent ignored letters.
        eg: '___r_'
        """
        self.guess_list = list(
            filter(
                lambda x: not any(
                    pair in tuple(enumerate(x))
                    for pair in tuple(enumerate(s.upper()))
                ),
                self.guess_list,
            )
        )
        self.guess_list = list(
            filter(lambda x: 
                   all([lt in x for lt in s.replace('_','').upper()]), 
                   self.guess_list)
            )
        for lt in s:
            if lt not in self.letter_found and lt != '_':
                self.letter_found += lt

    def correct_letters(self, s: str):
        """
        use _ to represent ignored letters.
        eg: '___r_'
        """
        if len(set(s)) == 1:
            return
        self.guess_list = list(
            filter(
                lambda x: all(
                    lt == '_' or (idx, lt) in tuple(enumerate(x))
                    for idx, lt in tuple(enumerate(s.upper()))
                ),
                self.guess_list,
            )
        )
        for idx, lt in enumerate(s):
            if lt != '_':
                self.letter_solved = self.letter_solved[:idx] + lt + self.letter_solved[idx+1:]
                if lt not in self.letter_found:
                    self.letter_found += lt

    def _word_match(self, word: str, mask: str):
        """ mask: ___R_ """
        return all(
                    lt == '_' or (idx, lt) in tuple(enumerate(word))
                    for idx, lt in tuple(enumerate(mask.upper()))
                )

    def update_list(self, s: str):
        """
        use o to represent correct word, correct placement.
        use x to represent correct word, incorrect placement.
        use _ to represent ignored letters.
        eg: 'o_x__'
        """

        self.remove_letters(
            "".join(
                [self.next_guess()[idx]
                 for idx, hint in list(enumerate(s.upper())) if hint == "_"]
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
        print(f"Remain word count: {len(self.guess_list):,}")
        print(f"Remain word percantage: {round(len(self.guess_list)/len(self.word_list)*100, 4)}%")
        print(f"Removed: {self.letter_removed}")
        print(f"Found: {self.letter_found}")
        print(f"Solved: {self.letter_solved}")
        print(f"Next guess: {self.next_guess()}")


class WordleGame:
    def __init__(self, riddle: str = "") -> None:
        if riddle:
            self.ans = riddle
        else:
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


def fast_game_result(riddle = ""):
    s = WordleSolver()
    g = WordleGame(riddle)

    for rnd in range(6):
        r = g.guess(s.next_guess())
        if r == "End":
            return rnd
        s.update_list(r)
    print("Failed: ", g.ans)
    return 6


def fast_games(count: int = 100):
    if count >= 3190:
        with open(source) as file:
            result: list = json.load(file)
        games = [fast_game_result(_) for _ in result]
    else:
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
        print(f"Value list: {s.val[:20]}")
        print(f"Guess list: {s.guess_list[:20]}")
        r = g.guess(s.next_guess())
        print(f"result: {r}")
        if r == "End":
            print("Game Over")
            break
        s.update_list(r)
        # break


if __name__ == "__main__":
    # fast_games()
    fast_games(3190)
    # custom_game('FAZED')
    # tried
    # salon