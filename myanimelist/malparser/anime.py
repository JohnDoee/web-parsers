import urllib
import re
from decimal import Decimal
from datetime import datetime

import lxml.html


class Anime(object):
    fetched = False
    base_url = 'http://myanimelist.net/anime/%s/'
    
    def __init__(self, mal_id):
        self.mal_id = mal_id
    
    def _get_url(self):
        return self.base_url % self.mal_id
    
    def fetch(self):
        data = urllib.urlopen(self._get_url()).read()
        self.parse(data)
    
    def parse_date(self, d):
        if '?' in d:
            return None
        
        d = d.strip()
        spaces = len(d.split(' '))
        if spaces == 1:
            return datetime.strptime(d, '%Y').date()
        elif spaces == 2:
            return datetime.strptime(d, '%b %Y').date()
        else:
            return datetime.strptime(d, '%b  %d, %Y').date()
    
    def get_season(self, d):
        if d.month in [2, 3, 4]:
            return ('Spring', d.year)
        elif d.month in [5, 6, 7]:
            return ('Summer', d.year)
        elif d.month in [8, 9, 10]:
            return ('Fall', d.year)
        else:
            return ('Winter', d.year)
    
    def parse(self, html):
        # Ignoring errors here because MAL allows users to use their own encodings
        # Without testing, probably allows the users to store pictures from their latest vacation as a review
        # Anyways, anything we need is (hopefully) in utf-8
        tree = lxml.html.fromstring(html.decode('utf-8', errors='ignore')) 
        
        self.title = tree.xpath('//div[@id="contentWrapper"]/h1/text()')[0]
        self.synopsis = tree.xpath('//h2[text()="Synopsis"]/../text()')[0].strip()
        self.cover = tree.xpath('//div[@id="content"]//img')[0].attrib['src']
        
        self.info = info = {}
        self.alternative_titles = alternative_titles = {}
        self.statistics = statistics = {}
        self.related_anime = related_anime = {}
        
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
            ('Information', False, ['Producers', 'Genres'], info, {'Episodes': num2int, 'Duration': duration2int}),
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
                                'id': int(a.attrib['href'].split('=')[-1]),
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
        tags = iter(filter(lambda x:x, map(lambda x:x.strip(': ,'), tree.xpath('//h2[text()="Related Anime"]/../text()'))))
        current_tag = None
        self.related_anime = related_anime = {}
        
        for el in tree.xpath('//h2[text()="Related Anime"]/../*'):
            if el.tag == 'h2':
                if found_h2:
                    break
                found_h2 = True
            
            if el.tag == 'a':
                if current_tag not in related_anime:
                    related_anime[current_tag] = []
                
                href = el.attrib['href'].split('/')
                
                if not el.xpath('text()') or not href:
                    continue
                
                if href[3] == 'anime':
                    related_anime[current_tag].append(Anime(int(href[4])))
                elif href[3] == 'manga':
                    pass # not implemented
                else:
                    pass # unknown type
            
            if el.tag == 'br':
                current_tag = next(tags)
        
        self.aired = aired = {
            'Aired_start': None,
            'Aired_end': None,
            'Season': None,
        }
        
        if 'Aired' in self.info:
            if self.info['Aired'] != 'Not yet aired':
                if ' to ' in self.info['Aired']:
                    aired['Aired_start'], aired['Aired_end'] = self.info['Aired'].split(' to ')
                else:
                    aired['Aired_start'] = aired['Aired_end'] = self.info['Aired']
                
                aired['Aired_start'] = self.parse_date(aired['Aired_start'])
                aired['Aired_end'] = self.parse_date(aired['Aired_end'])
                
                aired['Season'] = self.get_season(aired['Aired_start'])
        
        self.fetched = True
    
    def __repr__(self):
        return 'Anime(mal_id=%r)' % self.mal_id
    