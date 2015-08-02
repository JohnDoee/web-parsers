from .base import Base

class Person(Base):
    name = None
    
    base_url = 'http://akas.imdb.com/name/nm%s/'
    
    def __repr__(self):
        return 'Person(%r, %r)' % (self.imdb_id, self.name)