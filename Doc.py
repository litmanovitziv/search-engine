import xml.etree.ElementTree as ET
import string


class Doc:
    stopchars = string.punctuation

    def __init__(self, id, sub, body):
        self.id = id
        self.subject = sub
        self.body = body

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject):
        self._subject = subject

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

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

        return words

    def dump_sentences_to_string(self):
        return 'Id: %s\nSubject: %s\nSentences:\n%s\n' % (self.id, self.subject, '\n'.join(self.parse_sentences()))

    def dump_sentences_to_xml(self):
        article = ET.Element('doc', {'id':self.id})
        entity = ET.SubElement(article, 'subject')
        entity.text = self.subject
        if self.body is not None:
            for sentence in self.parse_sentences():
                entity = ET.SubElement(article, 'sentence')
                entity.text = sentence
        return article
