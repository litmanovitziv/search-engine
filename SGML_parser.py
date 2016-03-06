import sgmllib
import string, os, sys
from Doc import *
from WordsHistogram import *


class SGML_parser(sgmllib.SGMLParser):

    def __init__(self):
        # initialize base class
        sgmllib.SGMLParser.__init__(self)

        self.docs = []
        self.doc = self.data = self.tag = None

    @property
    def docs(self):
        return self._docs

    def handle_data(self, data):
        # called for each text section
        if self.data is not None:
            self.data.append(data)

    def start_reuters(self, attrs):
        for attr, value in attrs:
            if attr == "newid":
                self.doc = Doc(int(value))
                break

        if self.doc is None:
            raise sgmllib.SGMLParseError

    def end_reuters(self):
        self.docs.append(self.doc)

    def start_title(self, attrs):
        self.data = []
        self.tag = ""

    def end_title(self):
        self.tag = string.join(self.data, "")
        self.doc.subject = self.tag.strip()

    def start_body(self, attrs):
        self.data = []
        self.tag = ""

    def end_body(self):
        self.tag = string.join(self.data, "").strip()
        self.doc.body = ' '.join([line.strip() for line in self.tag.splitlines()])

"""
Arguments :
(0 - program name)
1 - input folder
2 - output file
3 - stopwords
"""
if __name__ == "__main__":
    parser = SGML_parser()
    for file in sorted(os.listdir(sys.argv[1])):
        file = open(sys.argv[1] + "/" + file, 'r')
        parser.feed(file.read())
    parser.close()
    docs = sorted(parser.docs, key=lambda doc : doc.id)

    if len(sys.argv) == 4:
        histogram = WordsHistogram(stopwords=sys.argv[3])
    else: histogram = WordsHistogram()

    for doc in docs:
        words = doc.parse_words()
        histogram.accumulate(words)
    histogram.rank(5)
    print histogram.dump_top(10)
    sys.exit()

    articles = ET.Element('articles')
    for doc in docs:
        articles.append(doc.dump_sentences_to_xml())
    tree = ET.ElementTree(articles)
    with open(sys.argv[2], 'wb') as output:
        tree.write(sys.stdout)
