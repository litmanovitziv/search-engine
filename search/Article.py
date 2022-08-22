from datetime import datetime
from search.Doc import Doc


class Article(Doc):

    def __init__(self, article_id, xml_element):
        super().__init__(doc_id=article_id)
        self.article_id = xml_element.get('NEWID')
        self.date = xml_element.find('DATE').text
        text_sec = xml_element.find('TEXT')
        if text_sec.get('TYPE') == 'BRIEF':
            # only title
            self.title = text_sec.find('TITLE').text
            self.body = ""
        elif text_sec.get('TYPE') == 'UNPROC':
            # nor title or body
            self.title = ""
            self.body = text_sec.text
        else:
            # title and body
            self.title = text_sec.find('TITLE').text
            self.body = text_sec.find('BODY').text

    @property
    def article_id(self):
        return self._article_id

    @article_id.setter
    def article_id(self, article_id):
        self._article_id = article_id

    @property
    def body(self):
       return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def title(self):
       return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def date(self):
       return self._date

    @date.setter
    def date(self, date):
        self._date = datetime.strptime(date.strip(), '%d-%b-%Y %H:%M:%S.%f')
