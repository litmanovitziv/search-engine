import string
import functools
import math


class Doc:
    """ Text unit for indexing

    Attributes
    ----------
    _id : int
    _lang : str
    _body : str
    _histogram : dict
    """

    stopchars = string.punctuation

    def __init__(self, doc_id, language='english'):
        self._id = doc_id
        self._lang = language
        self._histogram = dict()

    @property
    def id(self):
        return self._id

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body
        self.parse_words()

    @property
    def histogram(self):
        return self._histogram

    @property
    def terms(self):
        return [*self._histogram]

    def get_term_metrics(self, term):
        try:
            return self._histogram[term]
        except: return None

    def set_histogram(self, tokens_list):
        """ Construct index of document's terms including their frequencies """
        self._histogram = dict(zip(tokens_list, [dict(tf=(tokens_list.count(i))) for i in tokens_list]))    # math.log1p

    def set_token_weight(self, token, weight):
        self._histogram[token].update(dict(w=(self._histogram[token]['tf'])*weight))

    def parse_sentences(self, delimiter='.'):
        """ Parse text by specified delimiter """

        if bool(self.body):
            return [sentence for sentence in self.body.split(delimiter)]
        else: return []

    def parse_words(self, syntactic_func=lambda x: x):
        words = []

        if self.body is not None:
            for sentence in self.parse_sentences():
                # remove leading and trailing whitespaces
                sentence = sentence.strip()

                # remove attached punctuation
                for c in self.stopchars:
                    sentence = sentence.replace(c, "")

                # convert lowercase
                sentence = sentence.lower()

                # tokenize the sentence by spaces. Skip up stop words, single char and decimals
                tokens = [token for token in sentence.split()
                          if (token.isalpha() and not(token.isdigit()) and len(token) > 1)]
                words.extend(tokens)

        words = syntactic_func(words)
        self.set_histogram(words)

    def to_dict(self, *args):
        res = dict(id=self.id, sentences=self.parse_sentences(), histogram=self.histogram)
        res.update({k: getattr(self, k) for k in args})
        return res
