import string
from pandas import Series


class Doc:
    stopchars = string.punctuation

    def __init__(self, doc_id):
        self.id = doc_id
        self.histogram = dict()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def histogram(self):
        return self._histogram

    @histogram.setter
    def histogram(self, histogram):
        self._histogram = histogram

    def parse_sentences(self):
        if bool(self.body):
            return [sentence.strip() for sentence in self.body.split('.')]
        else: return []

    def parse_words(self):
        words = []

        if self.body is not None:
            for sentence in self.parse_sentences():
                # remove leading and trailing whitespaces
                sentence = sentence.strip()

                # remove attached punctuation
                for c in self.stopchars:
                    sentence = sentence.replace(c,"")

                # convert lowercase
                sentence = sentence.lower()

                # tokenize the sentence by spaces
                words.extend(sentence.split())
                self._histogram = Series(words).value_counts().to_dict()

        return words

    def dump_sentences_to_string(self):
        return 'Id: %s\nSubject: %s\nSentences:\n%s\n' % (self.id, self.subject, '\n'.join(self.parse_sentences()))
