import os.path as path
import sys
import glob
import xml.etree.ElementTree as ET

from entities.Article import *
from entities.Review import *
from entities.Word import *


class SearchEngine:

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

    def add(self, entity:Doc):
        """
        adds an entity to search engine DB
        :param entity: the entity to add
        :return:
        """
        for word in entity.parse_words():
            # skip up stop words
            if word in self.stopwords:
                continue

            record = self.invert_tbl.get(word)
            if record:
                record.add_doc(entity)
            else: self.invert_tbl[word] = Word(word, entity)

    def search(self, word:str, n:int=None):
        """
        search entities by input word, case insensitive
        :param word: string containing single word
        :param n: optional, number of top matches to return
        :return: list of matching Reviews, sorted by number of appearances of word in the entity text
        """
        word = word.strip().lower()
        if word in self.invert_tbl:
            sorted_docs = sorted(self.invert_tbl.get(word).docs_list, key=lambda doc: doc.histogram.get(word), reverse=True)
            return [doc.body for doc in sorted_docs][:n]
        return list()

    def most_common(self, n:int):
        """
        return list of n most common words and the number of entities they appeared in (each word is counted only once per entity)
        :param n: length of list to return
        :return: list of tuples (word, n_entities_appeared_in) sorted by n_entities_appeared_in (desceding)
        """
        sorted_words = sorted(self.invert_tbl.values(), key=lambda word: word.total, reverse=True)
        sorted_words = [(word.key, word.total) for word in sorted_words]
        return sorted_words[:n]


if __name__ == '__main__':

    search_engine = SearchEngine(stopwords=path.abspath(sys.argv[1]))

    # ./Corpus/sgml/reut2-00*.xml
    # for file in sorted(glob.glob(path.abspath(sys.argv[2]))):
    #     print(file)
    #     root = ET.parse(file).getroot()
    #     for article_xml in root.findall('REUTERS'):
    #         article = Article(article_xml.get('NEWID'), article_xml)
    #         search_engine.add(article)

    # ./Corpus/review_data.txt
    lines = open(path.abspath(sys.argv[2])).readlines()
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
