import re
from decimal import Decimal

import lxml.html


class Base(object):
    fetched = False
    
    def __init__(self, mal_id, mal):
        self.mal_id = mal_id
        self.mal = mal
    
    def _get_url(self):
        return self.base_url % self.mal_id
    
    def fetch(self):
        if not self.fetched:
            return self.mal._fetch(self)
    
    def parse(self, html):
        # Ignoring errors here because MAL allows users to use their own encodings
        # Without testing, probably allows the users to store pictures from their latest vacation as a review
        # Anyways, anything we need is (hopefully) in utf-8
        tree = lxml.html.fromstring(html.decode('utf-8', errors='ignore')) 
        
        self.title = tree.xpath('//div[@id="contentWrapper"]/h1/text()')[0].strip()
        self.synopsis = tree.xpath('//h2[text()="Synopsis"]/../text()')[0].strip()
        self.cover = tree.xpath('//div[@id="content"]//img')[0].attrib['src']
        
        self.info = info = {}
        self.alternative_titles = alternative_titles = {}
        self.statistics = statistics = {}
        self.related = related = {}
        
        def duration2int(x):
            runtime = 0
            hours = re.findall(r'(\d+) hr', x)
            minutes = re.findall(r'(\d+) min', x)
            if hours:
                try:
                    runtime += int(hours[0])*60
                except ValueError:
                    pass
            
            if minutes:
                try:
                    runtime += int(minutes[0])
                except ValueError:
                    pass
            
            return runtime
        
        def num2int(x):
            try:
                return int(x.replace(',', ''))
            except ValueError:
                return None
        
        num2dec = lambda x:Decimal(x)
        strip2int = lambda x:int(x.strip('#'))
        
        loop_elements = [
            ('Alternative Titles', True, [], alternative_titles, {}),
            ('Information', False, ['Producers', 'Genres', 'Authors', 'Serialization'], info, {'Episodes': num2int, 'Duration': duration2int, 'Volumes': num2int, 'Chapters': num2int}),
            ('Statistics', False, [], statistics, {'Favorites': num2int, 'Members': num2int, 'Popularity': strip2int, 'Ranked': strip2int, 'Score': num2dec}),
        ]
        
        for block, splitlist, linklist, save_target, postprocess in loop_elements:
            for el in tree.xpath('//h2[text()="%s"]/following-sibling::*' % block):
                if el.tag != 'div' or not el.xpath('span') or ':' not in el.xpath('span/text()')[0]:
                    break
                
                info_type = el.xpath('span/text()')[0].strip(':')
                if info_type in linklist:
                    save_target[info_type] = []
                    
                    if 'None found' not in el.xpath('text()')[0]:
                        for a in el.xpath('a'):
                            save_target[info_type].append({
                                'id': int(re.findall('\d+', a.attrib['href'])[0]),
                                'name': a.text
                            })
                else:
                    save_target[info_type] = el.xpath('text()')[0].strip()
                    if splitlist:
                        save_target[info_type] = map(lambda x:x.strip(), save_target[info_type].split(','))
                    elif info_type in postprocess:
                        save_target[info_type] = postprocess[info_type](save_target[info_type])
        
        votes = re.findall(r'scored by (\d+) users', html)
        if votes:
            statistics['Votes'] = int(votes[0])
        
        found_h2 = False
        tags = iter(filter(lambda x:x, map(lambda x:x.strip(': ,'), tree.xpath('//h2[starts-with(text(), "Related ")]/../text()'))))
        current_tag = None
        
        for el in tree.xpath('//h2[starts-with(text(), "Related ")]/../*'):
            if el.tag == 'h2':
                if found_h2:
                    break
                if el.text in ['Related Anime', 'Related Manga']:
                    found_h2 = True
            
            if el.tag == 'a' and found_h2:
                if current_tag not in related:
                    related[current_tag] = []
                
                print el
                href = el.attrib['href'].split('/')
                
                if not el.xpath('text()') or not href:
                    continue
                
                related[current_tag].append({'type': href[3], 'id': int(href[4])})
            
            if el.tag == 'br':
                current_tag = next(tags)
        
        self.mal._handle_related(self)
        
        self.fetched = True