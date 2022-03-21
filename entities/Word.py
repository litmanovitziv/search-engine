class Word:

    def __init__(self, word, doc):
        self.key = word
        self.docs_list = doc
        self.rank = 0

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, word):
        self._key = word

    @property
    def docs_list(self):
        return self._docs_list

    @property
    def total(self):
        return self._total

    @docs_list.setter
    def docs_list(self, doc):
        self._docs_list = [doc]
        self._total = 1

    def add_doc(self, doc):
        if doc not in self._docs_list:
            self._docs_list.append(doc)
            self._total += 1

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, rank):
        self._rank = rank

    def get_docs(self):
        return [doc.body for doc in self._docs_list]

    def print_entity(self):
        return '%s %s %s' % (self.rank, self.key, self.total)
