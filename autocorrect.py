import re
from collections import Counter

class Autocorrect:
    def __init__(self, corpus_path):
        self.words = self.load_words(corpus_path)
        self.word_freq = Counter(self.words)

    def load_words(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read().lower()
        return re.findall(r'\w+', text)

    def edits1(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def known(self, words):
        return set(w for w in words if w in self.word_freq)

    def correct(self, word):
        candidates = (
            self.known([word]) or
            self.known(self.edits1(word)) or
            self.known(self.edits2(word)) or
            [word]
        )
        return max(candidates, key=self.word_freq.get)

if __name__ == "__main__":
    ac = Autocorrect("big.txt")
    while True:
        word = input("Enter a word: ")
        print("Did you mean:", ac.correct(word))