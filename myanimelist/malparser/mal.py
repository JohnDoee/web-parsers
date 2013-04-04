import urllib

from malparser.anime import Anime

class MAL(object):
    def _fetch(self, obj):
        data = urllib.urlopen(obj._get_url()).read()
        obj.parse(data)
    
    def get_anime(self, mal_id):
        return Anime(mal_id, self)