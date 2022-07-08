import json
from datetime import datetime
from entities.Doc import Doc


class Review(Doc):

    def __init__(self, review_id, json_string):
        super().__init__(doc_id=review_id)
        record = json.loads(json_string)
        self.product_id = record['product_id']
        self.date = record['date']
        self.title = record['title']
        self.body = record['body']
        self.price = record['price'] if 'price' in record else -1

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        self._product_id = product_id

    @property
    def title(self):
       return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def date(self):
       return self._date

    @date.setter
    def date(self, date):
        self._date = datetime.strptime(date.strip(), '%Y-%m-%d %H:%M:%S')

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = float(price)
