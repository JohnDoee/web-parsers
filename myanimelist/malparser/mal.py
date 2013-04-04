import urllib

from malparser.anime import Anime
from malparser.manga import Manga

class MAL(object):
    def _fetch(self, obj):
        data = urllib.urlopen(obj._get_url()).read()
        obj.parse(data)
    
    def _handle_related(self, obj):
        related = {'manga': Manga, 'anime': Anime}
        
        for key, values in obj.related.items():
            obj.related[key] = [related[v['type']](v['id'], self) for v in values]
    
    def get_anime(self, mal_id):
        return Anime(mal_id, self)
    
    def get_manga(self, mal_id):
        return Manga(mal_id, self)