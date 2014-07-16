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
        
        self.assertEqual(anime.reviews, [{'rating': 9, 'review': 'Lucky star is one of those unique Comedy anime that comes very rarely. It manages to put a comedic twist to normal everyday occurances, and many pop culutre references. The entire show is not your typical slice of life high school comedy anime, rather its show structure follows more of a western style of comedy, a sitcom to be exact. Instead  of having a direct storyline, like  most anime viewers are used to, it focuses more of everyday observations and Jpop culture as their source of comedy.\r\n\r\n---Theres always a storyline no matter how broad it is. Many ppl say theres no story linebut, there has to be a "story" of sorts or else this stuff cant be funny. If you had to put a plot to this show it would "A group of high school children trying to make it all the way through high school." With such a broad plot, the creators can do as they please. By the way, that is how most western sitcoms can list 5-10 seasons without it getting old (i.e. Simpsons, Family Guy, Cheers, etc.) Mind you thats the only connection this show has with a western sitcom. \n\r\n---I have noticed many people bash the begging episodes of the show but i found them equally entertaining as the rest of them. It really depends on what the viewer does in their own daily lives is what truly makes this show funny. Somone who doesnt eat curry/rice or grilled meat sticks for dinner with their family wont understand a joke about it. But with all the jokes and references  in this show you\'re bound to laugh out loud at all they throw at you! They\'ve thoguht of everything for this show. \n\r\n\r\n---Art and animation of the show is your typical comedy anime fair. Simple characters simple backgrounds simple static objects. But they manage to take "simple" to a whole different level. For example, the characters are only shown from the waist up for about 80% of the entire show. But the characters are drawn very simplistic and the coloring for each looks like it doesnt exeed 12 different colors for each person for the most part. But they are definitely drawn in a cute manner, if thats your thing. The simple-ness is what gives the show its charm too. The art style is so popular and easy to draw im sure you\'ll find spoofs for dozens of other non related characters around the internet. \n\r\n\r\n---The Sound is your standard comedy sound efects from light hearted piano songs, to bing bangs and bongs, they\'re all there and accounted for. Music is mostly absent from the show aside from helping out certain jokes.\n\r\n---You will definitely notice the lack of background music in the show but with such a powerful seiyu cast, one could understand that they didnt want to distract from the well executed voice acting. Of course most people will notice Aya Hirano and maybe even Minori Chihara. Its hard to believe that most of the main characters are voiced by relatively newcomers. Which also helps seperate Lucky Star from sounding the same as all the other school anime out there. You\'ll enjoy Kagami\'s singing voice by the way. \n\r\n\r\nWith the uniqe sound comes the "unique" (or not so unique) character types associated with each seiyu.  Theres also ALOT more characters but you\'ll have to watch it to see them all ^_^  Speaking of characters you\'ll actually end up seeing all of them fairly regurlarly. Either supporting cast or main cast. By the end of the show, you\'ll get the feeling that not one person recieved more time than another. Even the extra characters get more than enough airtime to fully acknowledge them as essential parts of the anime. \n\r\n\r\n---The enjoyment factor is through the roof in my opinion. The comedy aspect of this show covers so many angles and hits so many things perfectly its hard not to give a perfect score. I find it very hard for somone to hate this anime. That is, if you dont like japanese pop cultre, anime references and funny common occurences. If youre that type then why are you watching anime? ^_^\n\r\n---Also, if you dont like western style sitcoms where the end of every episode will always leave the same way they started, this is definitely not for you. If youre looking for a romantic comedy or bloody action school go somewhere else.  If you\'re willing to give up about 20 minutes of your time for pure entertainment, WATCH THIS SHOW!\n\r\n\r\nIf you find anything funnier pm me i\'ll give it a shot but for now this the funniest anime i\'ve watched to date ^_^'}, {'rating': 6, 'review': 'Lucky Star is a 4-panel manga series by Kagami Yoshimizu that began publishing in 2004, and is still being published today. In 2007, Kyoto Animation, hot off the success of Haruhi, made an anime adaptation. I watched it. I also sampled the manga version. It was . . . okay, I guess. But let\'s elaborate on the anime some more, shall we?\r\n\r\nStory: In present-day Japan, a number of girls in high school live out their lives studying, making jokes about Gundam, being eccentric, making fun of cliches in fiction, and . . . that\'s about it, really. The four main girls are Konata Izumi, aself-proclaimed otaku (though fortunately one more functional than every real-life otaku I\'ve met), Kagami Hiiragi, a no-nonsense "Tsundere", Tsukasa Hiiragi, Kagami\'s moeblob twin-sister, and Miyuki Takara, a really smart moeblob. There are many more characters than this, but they\'re the main focus.\n\r\n\r\nBecause this is based off a 4-panel series, many plot threads, if you can call them that, often end abruptly, with little-to-no resolution. Some of the jokes from the manga don\'t translate as well into anime format. The show never veers into anything truly dark in terms of plot. It\'s mostly jokes and weird observations. Essentially, it\'s like Azumanga Daioh, but with characters with wild hair colors. And after the series and OVA sequel ends, there\'s no resolution of any sort.\n\r\n\r\nHowever, every episode also ends with a segment called "Lucky Channel", which features different characters and actually has an ongoing (and pretty funny) story. Sadly, these segments aren\'t that long. Yeah, Lucky Star is not something you watch for enlightenment. 3/10.\n\r\n\r\nArt: I\'m gonna be honest; I don\'t like the artwork of Lucky Star. The character designs are meant to be cute, but most of them don\'t look cute, just childish. The coloring is often garish, and Miyuki\'s hair is so bright, it nearly blinded me on a few occasions.\n\r\n\r\nWith that said, the animation is somewhat fluid for a tv series. So it\'s not a complete disaster on the visual front, but this show obviously does not focus on visuals. 5/10.\n\r\n\r\nSound: The theme song is infamous. Some hate it, some love it. I find it . . . okay. The ending themes are renditions of earlier anime ending themes, most of which I didn\'t recognize. They\'re alright. The background music is just there, doesn\'t really add anything.\n\r\n\r\nI saw this in English, as well as bits in Japanese on random Youtube channels. Weirdly enough, Lucky Star has one of the best English dubs I have ever heard. Its voice-acting is even better than most American cartoon shows I\'ve seen! I\'m not kidding! Look at this old quote of mine from tvtropes.org:\n\r\n\r\n"Lucky Star has one of the best English dubs I\'ve ever heard. Every character sounds exactly how I would picture their voices to be. None of the voices are annoying nor awkward sounding. They also match the lip flaps pretty closely, too. Wendee Lee especially displays great range in Konata\'s voice. It\'s impossible for me to watch the show in Japanese now; the dub is that good."\n\r\n\r\nI still stand by that today. Also, Kari Wahlgren\'s version of Kagami blows her Japanese counterpart completely out of the water. Anyone who does English dubs of Japanese productions, be they industry professionals or fandubbers, watch Lucky Star and take notes; THIS is how you do an English dub. And you wonder why I worship every Bandai dub out there that\'s not Code Geass. 7/10.\n\r\n\r\nCharacterization: For all of its faults, some of the characters are quite likable and amusing. Konata is silly, yet charming. Kagami\'s bewilderment is amusing. Many side characters, such as Konata\'s dad and Anime Tenchou are funny. The best characters, however, are the Lucky Channels stars Akira Kogami and Minoru Shiraishi.\n\r\n\r\nHowever, there\'s not a lot of depth to Lucky Star\'s cast. Also, several of its female characters are moe archetypes (or moeblobs) that don\'t really do much. Well, Konata\'s cousin Yutaka is adorable, but none of the others strike me as cute, just shallow. (Well, Tsukasa has a couple of funny moments.) And even the characters I do like don\'t have much to their characterizations. Look, Konata\'s comparing something to a game/anime again! Kagami is frustrated with someone\'s antics again! Tsukasa is clueless about something again! The characters aren\'t annoying, but I can only rate them slightly above-average. 6/10.\n\r\n\r\nEnjoyment: I will say this, there\'s usually only one funny moment per episode of Lucky Star outside of Lucky Channel, but that one moment is usually laugh-out-loud hilarious. Also, most of Lucky Channel is flat out hilarious. The English dub really helps with my enjoyment.\n\r\n\r\nBut for a show focused only on comedy, it\'s not one of the better examples of anime comedy I\'ve seen. Haruhi Suzumiya was funnier, and also served an interesting sci-fi plot. Soul Eater is way funnier, and also has cool action scenes and characters. Welcome to the NHK was funnier, and deeper and more dramatic. Sgt Frog and Gintama are both more centered on comedy, and also funnier.\n\r\n\r\nWith that said, I do like the anime version of Lucky Star more than the anime version of Azumanga Daioh. And believe me when I say I\'ve seen a lot worse than Lucky Star out there, too. However, LS is, at best, only slightly rising above mediocrity. 6/10.\n\r\n\r\nI do like the manga version of Lucky Star more, but only slightly. (I would probably give that a 7 out of 10, despite the lack of Lucky Channel in that.) I don\'t want to say LS is overrated. Yeah, it\'s not as good as I hoped it would be, but I\'ve been let down by other animes a lot more. At least I was able to finish LS. It\'s not a classic, but if you\'re bored enough, you might want to check it out. Just mind the bright colors.'}])

    def test_mixed_encoding_html(self):
        anime = MALDummy().get_anime(2904)
        anime.fetch()
        self.assertEqual(anime.title, 'Code Geass: Hangyaku no Lelouch R2', 'Was not fetched properly')
    
    def test_long_anime(self):
        anime = MALDummy().get_anime(585)
        anime.fetch()
        self.assertEqual(anime.info['Duration'], 111, 'Wrong duration found')
    
    def test_failing_anime(self):
        anime = MALDummy().get_anime(20431)
        anime.fetch()
