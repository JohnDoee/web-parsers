MAL Parser
=====================

Library to parse [MyAnimeList] pages, contains lots more features than un-official API

Getting started
---------------

To get it up and running, do::

```sh
pip install malparser
```

This is an example of almost anything this library can:
```python
>>> from malparser import MAL
>>> mal = MAL()
>>> anime = mal.get_anime(1575)
>>> anime.fetched
False
>>> anime.fetch()
>>> anime.fetched
True

>>> anime.aired
{'Aired_end': datetime.date(2007, 7, 28), 'Aired_start': datetime.date(2006, 10, 6), 'Season': ('Fall', 2006)}
>>> anime.title
'Code Geass: Hangyaku no Lelouch'
>>> anime.mal_id
1575

>>> from pprint import pprint
>>> pprint(anime.__dict__)
{'aired': {'Aired_end': datetime.date(2007, 7, 28),
           'Aired_start': datetime.date(2006, 10, 6),
           'Season': ('Fall', 2006)},
 'alternative_titles': {'English': ['Code Geass: Lelouch of the Rebellion'],
                        'Japanese': [u'\u30b3\u30fc\u30c9\u30ae\u30a2\u30b9 \u53cd\u9006\u306e\u30eb\u30eb\u30fc\u30b7\u30e5']},
 'cover': 'http://cdn.myanimelist.net/images/anime/10/18746.jpg',
 'fetched': True,
 'info': {'Aired': 'Oct  6, 2006 to Jul  28, 2007',
          'Duration': 24, # Length in minutes
          'Episodes': 25,
          'Genres': [{'id': 1, 'name': 'Action'},
                     {'id': 18, 'name': 'Mecha'},
                     {'id': 23, 'name': 'School'},
                     {'id': 24, 'name': 'Sci-Fi'},
                     {'id': 31, 'name': 'Super Power'},
                     {'id': 38, 'name': 'Military'}],
          'Producers': [{'id': 14, 'name': 'Sunrise'},
                        {'id': 143, 'name': 'Mainichi Broadcasting'},
                        {'id': 233, 'name': 'Bandai Entertainment'},
                        {'id': 757, 'name': 'Sony Music Entertainment'}],
          'Rating': 'R+ - Mild Nudity',
          'Status': 'Finished Airing',
          'Type': 'TV'},
 'mal_id': 1575,
 'related_anime': {'Adaptation': [],
                   'Other': [Anime(mal_id=8888)],
                   'Sequel': [Anime(mal_id=2904)],
                   'Side story': [Anime(mal_id=1953)],
                   'Spin-off': [Anime(mal_id=12685), Anime(mal_id=17277)],
                   'Summary': [Anime(mal_id=2124), Anime(mal_id=4596)]},
 'statistics': {'Favorites': 22331,
                'Members': 239512,
                'Popularity': 3,
                'Ranked': 12,
                'Score': Decimal('8.88'),
                'Votes': 169408},
 'synopsis': "On August 10th of the year 2010 the Holy Empire of Britannia began a campaign of conquest, its sights set on Japan. Operations were completed in one month thanks to Britannia's deployment of new mobile humanoid armor vehicles dubbed Knightmare Frames. Japan's rights and identity were stripped away, the once proud nation now referred to as Area 11. Its citizens, Elevens, are forced to scratch out a living while the Britannian aristocracy lives comfortably within their settlements. Pockets of resistance appear throughout Area 11, working towards independence for Japan.",
 'title': 'Code Geass: Hangyaku no Lelouch'}

>>> sequel_anime = anime.related_anime['Sequel'][0]
>>> sequel_anime.fetched
False
>>> sequel_anime.fetch()
>>> sequel_anime.fetched
True
>>> sequel_anime.title
'Code Geass: Hangyaku no Lelouch R2'
```

Requirements
------------

* [lxml]

More stuff and contact
----------------------
See http://github.com/JohnDoee for anything you might need

License
--------
See LICENSE

[lxml]: http://lxml.de/
[MyAnimeList]: http://myanimelist.net
