import math


class Word:
    """ word statistics

    Attributes
    ----------
    _key : int
    _docs_list : list
        the occurrences of the word in documents
    _cooccure_words : dict
        the co-occurrences of the word with others
    _rank : int
    """

    def __init__(self, word):
        self.key = word
        self._docs_list = list()
        self._cooccure_words = dict() # the co-occurrences of the word with others
        self._rank = 0

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
        return len(self._docs_list)

    def add_doc(self, doc):
        """ adds an entity whose the word occurs
        :param entity: the entity to add
        :return:
        """

        if doc not in self._docs_list:
            self._docs_list.append(doc)
            self.add_cooccurrences([k for k in [*doc.histogram] if k is not self._key])

    def add_cooccurrences(self, terms):
        new_occurances = dict.fromkeys(terms, 1)
        self._cooccure_words = {k: self._cooccure_words.get(k, 0) + new_occurances.get(k, 0)
                                for k in set(self._cooccure_words) | set(new_occurances)}

    @property
    def rank(self):
        return self._rank

    def set_rank(self, factor):
        self._rank = math.log(factor/self.total)
        for doc in self._docs_list:
            doc.set_token_weight(self._key, self._rank)

    def get_docs(self, *args):
        return [doc.to_dict(args) for doc in self._docs_list]

    def get_sum(self):
        return dict(key=self.key, rank=self.rank, df=self.total)
