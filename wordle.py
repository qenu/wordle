import json 
from collections import Counter
source = 'wordlist.json'
length_check = 3189

class WordleSolver:
    def __init__(self) -> None:
        self.word_list: list = self.source_loader(source)
        self.reload()

    def source_loader(self, path: str) -> list:
        with open(path) as file:
            result: list = json.load(file)
        return result
    
    def letter_frequency(self) -> Counter:
        freq: Counter = Counter()
        for word in self.word_list:
            for letter in set(word):
                freq[letter] += 1
        return freq
    
    def word_value(self) -> dict:
        result: dict = {word: sum([self.frequency[lt] for lt in set(word)]) for word in self.word_list}
        return sorted(result.items(), key=lambda x: x[1], reverse=True)

    def get_alpha(self) -> tuple:
        return next(iter(self.val))
    
    def reload(self) -> None:
        self.frequency: Counter = self.letter_frequency()
        self.val: dict = self.word_value()

    def remove_letters(self, s: str):
        self.word_list = list(filter(lambda x: not any(lt in x for lt in s.upper()), self.word_list))                

    def misplace_letters(self, s: str):
        ''' use _ to represent ignored letters. eg: '___r_' '''
        self.word_list = list(filter(lambda x: not any(pair in tuple(enumerate(x)) for pair in tuple(enumerate(s.upper()))), self.word_list))

    def correct_letters(self, s: str):
        ''' use _ to represent ignored letters. eg: '___r_' '''
        self.word_list = list(filter(lambda x: any(pair in tuple(enumerate(x)) for pair in tuple(enumerate(s.upper()))), self.word_list))


if __name__ == '__main__':
    ws = WordleSolver()
