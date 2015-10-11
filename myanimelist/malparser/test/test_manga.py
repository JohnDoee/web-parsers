import os
import unittest
import datetime
from decimal import Decimal

from malparser.manga import Manga
from malparser.anime import Anime
from malparser.mal import MAL

test_files = os.path.join(os.path.dirname(__file__), 'testfiles', 'manga')

class MALDummy(MAL):
    def _fetch(self, obj):
        f = os.path.join(test_files, '%s.html' % obj.mal_id)
        obj.parse(open(f).read())

class TestManga(unittest.TestCase):
    def test_normal_manga(self):
        manga = MALDummy().get_manga(1528)
        self.assertFalse(manga.fetched, 'Manga is not yet fetched')
        manga.fetch()
        self.assertTrue(manga.fetched, 'Manga should be fetched')
        
        self.assertEqual(manga.mal_id, 1528, 'Wrong MAL id')
        self.assertEqual(manga.title, 'Code Geass: Hangyaku no Lelouch', 'Title parsed wrong')
        
        self.assertEqual(manga.alternative_titles, {'English': ['Code Geass: Lelouch of the Rebellion'],
                                                    'Japanese': [u'\u30b3\u30fc\u30c9\u30ae\u30a2\u30b9 \u53cd\u9006\u306e\u30eb\u30eb\u30fc\u30b7\u30e5']},
                         'Incorrect alternative titles found')
        from pprint import pprint; pprint(manga.statistics)
        self.assertEqual(manga.cover, 'http://cdn.myanimelist.net/images/manga/3/121659.jpg', 'Wrong cover URL')
        self.assertEqual(manga.info, {'Authors': [{'id': 3066, 'name': 'Taniguchi, Goro'},
                                                  {'id': 3067, 'name': 'Okouchi, Ichiro'},
                                                  {'id': 3081, 'name': 'Majiko!'}],
                                      'Chapters': 40,
                                      'Genres': [{'id': 1, 'name': 'Action'},
                                                 {'id': 8, 'name': 'Drama'},
                                                 {'id': 18, 'name': 'Mecha'},
                                                 {'id': 23, 'name': 'School'},
                                                 {'id': 24, 'name': 'Sci-Fi'},
                                                 {'id': 25, 'name': 'Shoujo'},
                                                 {'id': 37, 'name': 'Supernatural'},
                                                 {'id': 38, 'name': 'Military'}],
                                      'Published': 'Aug  24, 2006 to Feb  24, 2010',
                                      'Serialization': [{'id': 14, 'name': 'Asuka (Monthly)'}],
                                      'Status': 'Finished',
                                      'Type': 'Manga',
                                      'Volumes': 8},
                         'Infobox was parsed incorrectly')
        
        self.assertEqual(manga.statistics, {'Favorites': 367,
                                            'Members': 6923,
                                            'Popularity': 293,
                                            'Ranked': 2109,
                                            'Score': Decimal('7.71'),
                                            'Votes': 4300},
                         'Statistics box was parsed incorrectly')
        
        self.assertEqual(manga.synopsis, "The Empire of Brittania has invaded Japan using giant robot weapons called Knightmare Frames. Japan is now referred to as Area 11, and its people the 11s. A Brittanian who was living in Japan at the time, Lelouch, vowed to his Japanese friend Suzaku that he'd destroy Brittania. Years later, Lelouch is in high school, but regularly skips out of school to go play chess and gamble on himself.",
                         'Synopsis was parsed incorrectly')

        self.assertEqual(sorted(manga.related.keys()), ['Adaptation', 'Alternative setting', 'Alternative version', 'Prequel', 'Spin-off'], 'Wrong related manga types found')
        self.assertEqual(len(manga.related['Adaptation']), 2, 'Wrong number of adaptations found')
        self.assertEqual(manga.related['Adaptation'][0].mal_id, 1575)
        self.assertIsInstance(manga.related['Adaptation'][0], Anime)
        self.assertEqual(manga.related['Adaptation'][1].mal_id, 2904)
        self.assertIsInstance(manga.related['Adaptation'][1], Anime)
        
        self.assertEqual(len(manga.related['Alternative setting']), 2, 'Wrong number of alternative settings found')
        self.assertEqual(manga.related['Alternative setting'][0].mal_id, 10167)
        self.assertIsInstance(manga.related['Alternative setting'][0], Manga)
        self.assertEqual(manga.related['Alternative setting'][1].mal_id, 25854)
        self.assertIsInstance(manga.related['Alternative setting'][1], Manga)
        
        self.assertEqual(len(manga.related['Alternative version']), 3, 'Wrong number of alternative versions found')
        self.assertEqual(manga.related['Alternative version'][0].mal_id, 1547)
        self.assertIsInstance(manga.related['Alternative version'][0], Manga)
        self.assertEqual(manga.related['Alternative version'][1].mal_id, 1530)
        self.assertIsInstance(manga.related['Alternative version'][1], Manga)
        self.assertEqual(manga.related['Alternative version'][2].mal_id, 11496)
        self.assertIsInstance(manga.related['Alternative version'][2], Manga)
        
        self.assertEqual(len(manga.related['Prequel']), 1, 'Wrong number of prequels found')
        self.assertEqual(manga.related['Prequel'][0].mal_id, 17311)
        self.assertIsInstance(manga.related['Prequel'][0], Manga)
        
        self.assertEqual(len(manga.related['Spin-off']), 3, 'Wrong number of spin-offs found')
        self.assertEqual(manga.related['Spin-off'][0].mal_id, 11968)
        self.assertIsInstance(manga.related['Spin-off'][0], Manga)
        self.assertEqual(manga.related['Spin-off'][1].mal_id, 12042)
        self.assertIsInstance(manga.related['Spin-off'][1], Manga)
        self.assertEqual(manga.related['Spin-off'][2].mal_id, 10822)
        self.assertIsInstance(manga.related['Spin-off'][2], Manga)
