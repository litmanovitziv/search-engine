import sys
from Word import *
from Doc import *


class Normlizer:

    def __init__(self):
        pass

    @staticmethod
    def get_normalizer(bound, divisor):
        def get_rank(value):
            for i in range(1,divisor+1):
                if value < i*(bound/divisor):
                    return '*' * i
        return get_rank


class WordsHistogram:
    stopwords = ''
    histogram = {}

    def __init__(self, **parsing):
        try:
            stopwords = open(parsing['stopwords'], 'r')
            self.stopwords = stopwords.read().replace('\n', ' ')
        except: pass

    def accumulate(self, words):
        for word in words:
            if len(word) == 1:
                continue

            if word.isdigit():
                continue

            # skip up stop words
            if word in self.stopwords:
                continue

            record = self.histogram.get(word)
            if record:
                record.incCounter()
            else: self.histogram[word] = Word(word)

    # normalizing and ranking records
    def rank(self, divisor):
        max_count = max(self.histogram.values(), key=lambda x: x.counter).counter
        normalizer = Normlizer.get_normalizer(max_count - int(max_count/10) + 10, divisor)
        for record in self.histogram.values():
            record.rank = normalizer(record.counter)

    def sort_by_counter(self):
        self.histogram = sorted(self.histogram.values(), key=lambda x : x.counter, reverse=True)

    def dump_top(self, top):
        self.sort_by_counter()
        return '\n'.join(record.print_entity() for record in self.histogram[:top])

    def dump(self):
        return '\n'.join(record.print_entity() for record in self.histogram)

"""
Arguments :
(0 - program name)
1 - input file
2 - output file
3 - stopwords
"""
if __name__ == "__main__":
    histogram = None
    if len(sys.argv) == 4:
        histogram = WordsHistogram(stopwords=sys.argv[3])
    else: histogram = WordsHistogram()

    with open(sys.argv[1], 'r') as inputfile:
        doc = Doc(0)
        doc.body = inputfile.read()
        histogram.accumulate(doc.parse_words())
    histogram.rank(5)
    histogram.sort_by_counter()

    with open(sys.argv[2], 'w') as outputfile:
        outputfile.write(histogram.dump())
