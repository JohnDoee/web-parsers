import os
import unittest
import datetime
from decimal import Decimal

from malparser.anime import Anime

test_files = os.path.join(os.path.dirname(__file__), 'testfiles')

from pprint import pprint

class AnimeDummy(Anime):
    def fetch(self):
        f = os.path.join(test_files, '%s.html' % self.mal_id)
        self.parse(open(f).read())


class TestAnime(unittest.TestCase):
    def test_title_encoding(self):
        anime = AnimeDummy(1887)
        self.assertFalse(anime.fetched, 'Anime is not yet fetched')
        anime.fetch()
        self.assertTrue(anime.fetched, 'Anime should be fetched')
        self.assertEqual(anime.title, u'Lucky\u2606Star', 'Title parsed wrong')
        
        self.assertEqual(anime.aired, {'Aired_end': datetime.date(2007, 9, 17),
                                       'Aired_start': datetime.date(2007, 4, 9),
                                       'Season': ('Spring', 2007)},
                         'Dates were not parsed correctly')
        
        self.assertEqual(anime.alternative_titles, {'English': [u'Lucky\u2606Star'],
                                                    'Japanese': [u'\u3089\u304d\u2606\u3059\u305f']},
                         'Incorrect alternative titles found')
        
        self.assertEqual(anime.cover, 'http://cdn.myanimelist.net/images/anime/3/29625.jpg', 'Wrong cover URL')
        self.assertEqual(anime.info, {'Aired': 'Apr  9, 2007 to Sep  17, 2007',
                                      'Duration': 24,
                                      'Episodes': 24,
                                      'Genres': [{'id': 4, 'name': 'Comedy'},
                                                 {'id': 20, 'name': 'Parody'},
                                                 {'id': 23, 'name': 'School'},
                                                 {'id': 36, 'name': 'Slice of Life'}],
                                      'Producers': [{'id': 2, 'name': 'Kyoto Animation'},
                                                    {'id': 104, 'name': 'Lantis'},
                                                    {'id': 211, 'name': 'Rakuonsha'},
                                                    {'id': 262, 'name': 'Kadokawa Pictures USA'},
                                                    {'id': 657, 'name': 'Lucky Paradise'}],
                                      'Rating': 'PG-13 - Teens 13 or older',
                                      'Status': 'Finished Airing',
                                      'Type': 'TV'},
                         'Infobox was parsed incorrectly')
        
        self.assertEqual(anime.statistics, {'Favorites': 6239,
                                            'Members': 145990,
                                            'Popularity': 26,
                                            'Ranked': 337,
                                            'Score': Decimal('8.13'),
                                            'Votes': 86406},
                         'Statistics box was parsed incorrectly')
        
        self.assertEqual(anime.synopsis, 'Having fun in school, doing homework together, cooking and eating, playing videogames, watching anime. All those little things make up the daily life of the anime- and chocolate-loving Izumi Konata and her friends. Sometimes relaxing but more than often simply funny!',
                         'Synopsis was parsed incorrectly')
        
        self.assertEqual(sorted(anime.related_anime.keys()), ['Adaptation', 'Character', 'Sequel', 'Spin-off'], 'Wrong related anime types found')
        self.assertEqual(len(anime.related_anime['Adaptation']), 0, 'Wrong number of adaptations found')
        self.assertEqual(len(anime.related_anime['Character']), 1, 'Wrong number of characters found')
        self.assertEqual(len(anime.related_anime['Sequel']), 1, 'Wrong number of sequels found')
        self.assertEqual(len(anime.related_anime['Spin-off']), 1, 'Wrong number of spin-offs found')
        self.assertEqual(anime.related_anime['Character'][0].mal_id, 3080, 'Wrong characters related anime found')
        self.assertEqual(anime.related_anime['Sequel'][0].mal_id, 4472, 'Wrong sequels related anime found')
        self.assertEqual(anime.related_anime['Spin-off'][0].mal_id, 17637, 'Wrong spin-offs related anime found')

    def test_mixed_encoding_html(self):
        anime = AnimeDummy(2904)
        anime.fetch()
        self.assertEqual(anime.title, 'Code Geass: Hangyaku no Lelouch R2', 'Was not fetched properly')
    
    def test_long_anime(self):
        anime = AnimeDummy(585)
        anime.fetch()
        self.assertEqual(anime.info['Duration'], 111, 'Wrong duration found')
