import os
import unittest
import datetime
from decimal import Decimal

from malparser.anime import Anime
from malparser.manga import Manga
from malparser.mal import MAL

test_files = os.path.join(os.path.dirname(__file__), 'testfiles', 'anime')

class MALDummy(MAL):
    def _fetch(self, obj):
        f = os.path.join(test_files, '%s.html' % obj.mal_id)
        obj.parse(open(f).read())

class TestAnime(unittest.TestCase):
    def test_title_encoding(self):
        anime = MALDummy().get_anime(1887)
        self.assertFalse(anime.fetched, 'Anime is not yet fetched')
        anime.fetch()
        self.assertTrue(anime.fetched, 'Anime should be fetched')
        self.assertEqual(anime.title, u'Lucky\u2606Star', 'Title parsed wrong')
        
        self.assertEqual(anime.aired, {'Aired_end': datetime.date(2007, 9, 17),
                                       'Aired_start': datetime.date(2007, 4, 8),
                                       'Season': ('Spring', 2007)},
                         'Dates were not parsed correctly')
        
        self.assertEqual(anime.alternative_titles, {'Synonyms': ['Lucky Star'],
                                                    'English': [u'Lucky\u2606Star'],
                                                    'Japanese': [u'\u3089\u304d\u2606\u3059\u305f']},
                         'Incorrect alternative titles found')
        
        self.assertEqual(anime.cover, 'http://cdn.myanimelist.net/images/anime/13/15010.jpg', 'Wrong cover URL')
        self.assertEqual(anime.info, {'Aired': 'Apr 8, 2007 to Sep 17, 2007',
                                      'Duration': 24,
                                      'Episodes': 24,
                                      'Genres': [{'id': 4, 'name': 'Comedy'},
                                                 {'id': 20, 'name': 'Parody'},
                                                 {'id': 23, 'name': 'School'},
                                                 {'id': 36, 'name': 'Slice of Life'}],
                                      'Producers': [{'id': 2, 'name': 'Kyoto Animation'},
                                                    {'id': 102, 'name': 'FUNimation Entertainment'},
                                                    {'id': 104, 'name': 'Lantis'},
                                                    {'id': 211, 'name': 'Rakuonsha'},
                                                    {'id': 262, 'name': 'Kadokawa Pictures USA'},
                                                    {'id': 657, 'name': 'Lucky Paradise'}],
                                      'Rating': 'PG-13 - Teens 13 or older',
                                      'Status': 'Finished Airing',
                                      'Type': 'TV'},
                         'Infobox was parsed incorrectly')
        
        self.assertEqual(anime.statistics, {'Favorites': 7341,
                                            'Members': 245845,
                                            'Popularity': 61,
                                            'Ranked': 602,
                                            'Score': Decimal('7.94'),
                                            'Votes': 134616},
                         'Statistics box was parsed incorrectly')
        
        self.assertEqual(anime.synopsis, u'Having fun in school, doing homework together, cooking and eating, playing videogames, watching anime. All those little things make up the daily life of the anime\u2014and chocolate-loving\u2014Izumi Konata and her friends. Sometimes relaxing but more than often simply funny!',
                         'Synopsis was parsed incorrectly')
        
        self.assertEqual(sorted(anime.related.keys()), ['Adaptation', 'Character', 'Sequel', 'Spin-off'], 'Wrong related anime types found')
        
        self.assertEqual(len(anime.related['Adaptation']), 1, 'Wrong number of adaptations found')
        self.assertEqual(anime.related['Adaptation'][0].mal_id, 587, 'Wrong adaption related anime found')
        self.assertIsInstance(anime.related['Adaptation'][0], Manga, 'Wrong type of adaption related anime found')
        
        self.assertEqual(len(anime.related['Character']), 1, 'Wrong number of characters found')
        self.assertEqual(anime.related['Character'][0].mal_id, 3080, 'Wrong characters related anime found')
        self.assertIsInstance(anime.related['Character'][0], Anime, 'Wrong type of characters related anime found')
        
        self.assertEqual(len(anime.related['Sequel']), 1, 'Wrong number of sequels found')
        self.assertEqual(anime.related['Sequel'][0].mal_id, 4472, 'Wrong sequels related anime found')
        self.assertIsInstance(anime.related['Sequel'][0], Anime, 'Wrong type of sequels related anime found')
        
        self.assertEqual(len(anime.related['Spin-off']), 1, 'Wrong number of spin-offs found')
        self.assertEqual(anime.related['Spin-off'][0].mal_id, 17637, 'Wrong spin-offs related anime found')
        self.assertIsInstance(anime.related['Spin-off'][0], Anime, 'Wrong type of spin-offs related anime found')
        
        self.assertEqual(len(anime.reviews), 4)
        self.assertEqual(anime.reviews[0]['rating'], 9)
        self.assertTrue(len(anime.reviews[0]['review']) > 100)
        self.assertEqual(anime.reviews[1]['rating'], 10)
        self.assertTrue(len(anime.reviews[1]['review']) > 100)
        self.assertEqual(anime.reviews[2]['rating'], 2)
        self.assertTrue(len(anime.reviews[2]['review']) > 100)
        self.assertEqual(anime.reviews[3]['rating'], 2)
        self.assertTrue(len(anime.reviews[3]['review']) > 100)

    def test_mixed_encoding_html(self):
        anime = MALDummy().get_anime(2904)
        anime.fetch()
        self.assertEqual(anime.title, 'Code Geass: Hangyaku no Lelouch R2', 'Was not fetched properly')
    
    def test_long_anime(self):
        anime = MALDummy().get_anime(585)
        anime.fetch()
        self.assertEqual(anime.info['Duration'], 111, 'Wrong duration found')
    
    def test_failing_anime(self):
        anime = MALDummy().get_anime(1633)
        anime.fetch()
        
        self.assertEqual(anime.statistics['Ranked'], None, 'Statistics box was parsed incorrectly for hentai')