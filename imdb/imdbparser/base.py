import re
from decimal import Decimal

import lxml.html


class Base(object):
    fetched = False
    
    def __init__(self, imdb_id, imdb):
        self.imdb_id = str(imdb_id).zfill(7)
        self.imdb = imdb
    
    def _get_url(self):
        return self.base_url % self.imdb_id
    
    def fetch(self):
        if not self.fetched:
            return self.imdb._fetch(self)
    
    def parse(self, html):
        self.tree = lxml.html.fromstring(html)