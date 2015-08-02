import urllib2

from imdbparser.movie import Movie

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "User-Agent": "Scrapy/0.24.2 (+http://scrapy.org)",
}

class IMDB(object):
    def _fetch(self, obj):
        req = urllib2.Request(obj._get_url(), None, HEADERS)
        data = urllib2.urlopen(req).read()
        obj.parse(data)
    
    def get_movie(self, imdb_id):
        return Movie(imdb_id, self)