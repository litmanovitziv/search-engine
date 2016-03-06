class Word:

    def __init__(self, word):
        self.key = word
        self.counter = 1
        self.rank = ''

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, word):
        self._key = word

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, counter):
        self._counter = counter

    def incCounter(self):
        self.counter += 1

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, rank):
        self._rank = rank

    def print_entity(self):
        return '%s %s %s' % (self.rank, self.key, self.counter)
