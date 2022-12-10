from .Doc import *
from .Word import *


class Corpus:
    """
    Indexing all document in the corpus

    Attributes
    ----------
    _stopwords : set
    _docs_list : list
    _invert_tbl : dict
    """

    def __init__(self, **parsing):
        try:
            stopwords = open(parsing['stopwords'], 'r')
            self._stopwords = set(stopwords.read().splitlines())
        except: self._stopwords = set()
        self._docs_list = list()
        self._invert_tbl = dict()

    @property
    def stopwords(self):
        return self._stopwords

    @stopwords.setter
    def stopwords(self, words_list):
        self._stopwords = set(words_list)

    @property
    def docs_list(self):
        return self._docs_list

    @property
    def total_docs(self):
        return len(self._docs_list)

    @property
    def invert_tbl(self):
        return self._invert_tbl

    @invert_tbl.setter
    def invert_tbl(self, tbl):
        self._invert_tbl = tbl

    @property
    def total_terms(self):
        return len(self._invert_tbl)

    @property
    def terms(self):
        return [*self._invert_tbl]

    def get_docs(self, filter_out=None):
        filter_out = self._stopwords.union([] if filter_out is None else filter_out)
        return [list(set(doc.histogram) - filter_out) for doc in self._docs_list]

    def get_bow(self, filter_out=None):
        filter_out = list(self._stopwords.union([] if filter_out is None else filter_out))
        for doc in self._docs_list:
            yield {k: v['tf'] for k, v in doc.histogram.items() if k not in filter_out}

    def add_doc(self, entity:Doc):
        """
        adds an entity to search engine DB
        :param entity: the entity to add
        :return:
        """
        if entity in self._docs_list:
            return

        self._docs_list.append(entity)
        for word in [*entity.histogram]:
            # skip up stop words
            if word in self.stopwords:
                continue

            term = self._invert_tbl.get(word, Word(word))
            term.add_doc(entity)
            term.set_rank(self.total_docs)
            self._invert_tbl.setdefault(word, term)

    def search(self, word:str, n:int=None):
        """
        search entities by input word, case insensitive
        :param word: string containing single word
        :param n: optional, number of top matches to return
        :return: list of matching Docs, sorted by total occurrences of a word in the entity text
        """
        word = word.strip().lower()
        if word in self.invert_tbl:
            sorted_docs = sorted(self.invert_tbl.get(word).docs_list, key=lambda doc: (doc.get_term_metrics(word))['tf'], reverse=True)
            return [doc.body for doc in sorted_docs][:n]
        return list()

    def most_common(self, n:int):
        """
        return list of n most common words and the number of entities they appeared in (each word is counted only once per entity)
        :param n: length of list to return
        :return: list of tuples (word, n_entities_appeared_in) sorted by n_entities_appeared_in (desceding)
        """
        sorted_words = sorted(self.invert_tbl.values(), key=lambda word: word.total, reverse=True)
        sorted_words = [word.get_sum() for word in sorted_words]
        return sorted_words[:n]
