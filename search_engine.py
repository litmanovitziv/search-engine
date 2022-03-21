import sys
import json

from numpy import doc

from entities.Doc import *
from entities.Word import *


class Review(Doc):

    def __init__(self, review_id, json_string):
        super().__init__(doc_id=review_id)
        record = json.loads(json_string)
        self.product_id = record['product_id']
        self.body = record['body']

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        self._product_id = product_id

    def get_text(self):
       """
       get relevant text in review
       """
       return self.body


class ReviewSearchEngine:

    def __init__(self, **parsing):
        try:
            stopwords = open(parsing['stopwords'], 'r')
            self.stopwords = stopwords.read().splitlines()
        except: self.stopwords = ''
        self.invert_tbl = dict()

    @property
    def stopwords(self):
        return self._stopwords

    @stopwords.setter
    def stopwords(self, words_list):
        self._stopwords = words_list

    @property
    def invert_tbl(self):
        return self._invert_tbl

    @invert_tbl.setter
    def invert_tbl(self, tbl):
        self._invert_tbl = tbl

    def add(self, review:Review):
        """
        adds a review to search engine DB
        :param review: the review to add
        :return:
        """
        for word in review.parse_words():
            if len(word) == 1:
                continue

            if word.isdigit():
                continue

            # skip up stop words
            if word in self.stopwords:
                continue

            record = self.invert_tbl.get(word)
            if record:
                record.add_doc(review)
            else: self.invert_tbl[word] = Word(word, review)

    def search(self, word:str, n:int=None):
        """
        search reviews by input word, case insensitive
        :param word: string containing single word
        :param n: optional, number of top matches to return
        :return: list of matching Reviews, sorted by number of appearances of word in the review text
        """
        word = word.strip().lower()
        if word in self.invert_tbl:
            sorted_docs = sorted(self.invert_tbl.get(word).docs_list, key=lambda doc: doc.histogram.get(word), reverse=True)
            return [doc.body for doc in sorted_docs][:n]
        return list()

    def most_common(self, n:int):
        """
        return list of n most common words and the number of reviews they appeared in (each word is counted only once per review)
        :param n: length of list to return
        :return: list of tuples (word, n_reviews_appeared_in) sorted by n_reviews_appeared_in (desceding)
        """
        sorted_words = sorted(self.invert_tbl.values(), key=lambda word: word.total, reverse=True)
        sorted_words = [(word.key, word.total) for word in sorted_words]
        return sorted_words[:n]


if __name__ == '__main__':

    search_engine = ReviewSearchEngine(stopwords=sys.argv[1])

    file_path = "sample_reviews.txt"
    lines = open(file_path).readlines()
    for count, line in enumerate(lines):
        review = Review(count, line)
        search_engine.add(review)

    search_words = ["Great", "product", "love", "happy"]
    for word in search_words:
        search_res = search_engine.search(word, 5)
        print("{:20} : {:4} results.".format(word, len(search_res)))
        print("\n".join(search_res))

    print("Most Common Words")
    for word, num_results in search_engine.most_common(10):
        print("{:20} : {} results".format(word, num_results))



