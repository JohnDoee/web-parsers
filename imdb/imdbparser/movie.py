from .base import Base
from .person import Person

class Movie(Base):
    base_url = 'http://akas.imdb.com/title/tt%s/'
    
    def _extract_person(self, element):
        name = element.xpath("./span[@itemprop='name']/text()")
        if not name:
            return
                    
        name = name[0]
        nm_id = element.attrib['href'].split('/')[2][2:]
        p = Person(nm_id, self.imdb)
        p.name = name
        return p
    
    def parse(self, html):
        super(Movie, self).parse(html)
        
        self.actors = []
        self.directors = []
        self.writers = []
        self.alternative_titles = []
        self.languages = []
        self.countries = []
        self.cover = None
        
        person_map = {
            'Director:': self.directors,
            'Writer:': self.writers,
        }
        
        self.duration = None
        
        titles = [x.strip() for x in self.tree.xpath('//h1//text()') if x.strip() and x not in ['(', ')']]
        self.title = titles[0]
        if self.title[0] == self.title[-1] == '"':
            self.title = self.title[1:-1]
        
        self.year = int(titles[1].strip(u'()').split(u'\u2013')[0])
        
        self.rating = float(self.tree.xpath("//span[@itemprop='ratingValue']/text()")[0])
        self.votes = int(self.tree.xpath("//span[@itemprop='ratingCount']/text()")[0].replace(',', ''))
        
        self.description = self.tree.xpath("//td[@id='overview-top']//p[@itemprop='description']/text()")[0].strip()
        self.plot = self.tree.xpath("//div[@id='titleStoryLine']//div[@itemprop='description']/p/text()")[0].strip()
        
        for element in self.tree.xpath("//div[@class='txt-block']"):
            key = element.xpath('./h4/text()')
            if not key:
                continue
            
            key = key[0]
            if key in ['Director:', 'Writer:']:
                for person in element.xpath('./a'):
                    person = self._extract_person(person)
                    if not person:
                        continue
                    
                    person_map[key].append(person)
                    
            elif key == 'Runtime:':
                value = element.xpath('./time/text()')
                if value:
                    self.duration = int(value[0].split(' ')[0])
            elif key == 'Country:':
                self.countries = element.xpath('./a/text()')
            elif key == 'Language:':
                self.languages = element.xpath('./a/text()')
            elif key == 'Also Known As:':
                self.alternative_titles.append(element.xpath('./text()')[1].strip())
        
        for person in self.tree.xpath("//div[@id='titleCast']//table[@class='cast_list']//tr/td[@itemprop='actor']/a"):
            person = self._extract_person(person)
            if not person:
                continue
            self.actors.append(person)
        
        self.genres = [x.strip() for x in self.tree.xpath("//div[@itemprop='genre']/a/text()")]
        
        cover = self.tree.xpath("//td[@id='img_primary']//img/@src")
        if cover:
            cover = cover[0].split('.')
            cover.pop(-2)
            self.cover = '.'.join(cover)
