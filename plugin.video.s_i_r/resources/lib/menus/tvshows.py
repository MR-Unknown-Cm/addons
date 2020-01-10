# -*- coding: utf-8 -*-

'''
    Still i Rise Add-on
'''

import os, sys, re
import json, urllib, urlparse, datetime

from resources.lib.modules import trakt
from resources.lib.modules import cleantitle
from resources.lib.modules import cleangenre
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views
from resources.lib.modules import utils
from resources.lib.menus import navigator

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()
action = params.get('action')


class TVshows:
    def __init__(self, type = 'show', notifications = True):
        self.count = 40
        self.list = []
        self.meta = []
        self.threads = []
        self.type = type
        self.lang = control.apiLanguage()['tvdb']
        self.season_special = False
        self.notifications = notifications

        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))

        self.fanart_tv_user = control.setting('fanart.tv.user')
        if self.fanart_tv_user == '' or self.fanart_tv_user is None:
            self.fanart_tv_user = 'cf0ebcc2f7b824bd04cf3a318f15c17d'
        self.user = self.fanart_tv_user + str('')
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/tv/%s'

        # self.tvdb_key = control.setting('tvdb.user')
        # if self.tvdb_key == '' or self.tvdb_key is None:
            # self.tvdb_key = '1D62F2F90030C444'
        self.tvdb_key = 'MUQ2MkYyRjkwMDMwQzQ0NA=='
        self.tvdb_info_link = 'http://thetvdb.com/api/%s/series/%s/%s.xml' % (self.tvdb_key.decode('base64'), '%s', self.lang)
        self.tvdb_by_imdb = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s'
        self.tvdb_by_query = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.tvdb_image = 'http://thetvdb.com/banners/'

        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.imdb_link = 'http://www.imdb.com'
        self.persons_link = 'http://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'http://www.imdb.com/search/name?count=100&gender=male,female'
        self.popular_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=moviemeter,asc&count=40&start=1'
        self.airing_link = 'http://www.imdb.com/search/title?title_type=tv_episode&release_date=date[1],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.active_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=10,&production_status=active&sort=moviemeter,asc&count=40&start=1'
        #self.premiere_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&languages=en&num_votes=10,&release_date=date[60],date[0]&sort=moviemeter,asc&count=40&start=1'
        self.premiere_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&languages=en&num_votes=10,&release_date=date[60],date[0]&sort=release_date,desc&count=40&start=1'
        self.rating_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=5000,&release_date=,date[0]&sort=user_rating,desc&count=40&start=1'
        self.views_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&release_date=,date[0]&sort=num_votes,desc&count=40&start=1'
        self.person_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&role=%s&sort=year,desc&count=40&start=1'
        self.genre_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=40&start=1'
        self.keyword_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=40&start=1'
        self.language_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=40&start=1'
        self.certification_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&certificates=%s&sort=moviemeter,asc&count=40&start=1'
        self.usprime_link = 'https://www.imdb.com/search/title?title_type=tv_series&online_availability=US%2Ftoday%2FAmazon%2Fsubs'
        self.classtv_link = 'https://www.imdb.com/search/title?title_type=tv_series&release_date=1900-01-01,1993-12-31&sort=moviemeter,asc'
        self.ghostadv_link = 'https://www.imdb.com/search/title?title=ghost+adventures&title_type=tv_series'
        self.mosth_link = 'https://www.imdb.com/search/title?title=most+haunted&title_type=tv_series&release_date=2002-01-01,2002-12-31'
        self.ghosth_link = 'https://www.imdb.com/search/title?title=ghost+hunters&title_type=tv_series&release_date=2004-01-01,2004-12-31'
        self.paraw_link = 'https://www.imdb.com/search/title?title=paranormal+witness&title_type=tv_series'
        self.paral_link = 'https://www.imdb.com/search/title?title=paranormal+lockdown'
        self.haunt_link = 'https://www.imdb.com/search/title?title=a+haunting&title_type=tv_series&release_date=2005-01-01,2005-12-31'
        self.hauntc_link = 'https://www.imdb.com/search/title?title=haunted+collector&title_type=tv_series'
        self.deadp_link = 'https://www.imdb.com/search/title?title=deadly+possessions&title_type=tv_series'
        self.ghosta_link = 'https://www.imdb.com/search/title?title=ghost+asylum&title_type=tv_series'
        self.paran_link = 'https://www.imdb.com/list/ls064706619/'
        self.ghosti_link = 'https://www.imdb.com/search/title?title=the+ghost+inside+my+child&title_type=tv_series'
        self.docsa_link = 'https://www.imdb.com/search/title?title_type=tv_series&genres=documentary'
        self.myst_link = 'https://www.imdb.com/search/title?title_type=tv_series&genres=mystery'
        self.scifi1_link = 'https://www.imdb.com/search/title?title_type=tv_series&genres=sci_fi'
        self.userr_link = 'https://www.imdb.com/search/title?title_type=tv_series&user_rating=7.0,10.0'
        self.mini_link = 'https://www.imdb.com/search/title?title_type=tv_miniseries'
        self.pg_link = 'https://www.imdb.com/search/title?title_type=tv_series&certificates=US%3Ag,US%3Apg'
        self.famtv_link = 'https://www.imdb.com/search/title/?title_type=tv_series&genres=family'
        self.scian_link = 'https://www.imdb.com/search/title?title_type=tv_series&genres=animation,sci_fi'
        self.ani1_link = 'https://www.imdb.com/search/title?title_type=tv_series&genres=animation&countries=%C2%B7%C2%B7%C2%B7%C2%A0Common+Countries%C2%A0%C2%B7%C2%B7%C2%B7'
        self.rtv_link = 'https://www.imdb.com/search/title?title_type=tv_series&genres=reality_tv'
        self.waltd_link = 'https://www.imdb.com/search/title?title_type=tv_series&companies=disney'
        self.dreamw_link = 'https://www.imdb.com/search/title?title_type=tv_series&companies=dreamworks'
        self.sony3_link = 'https://www.imdb.com/search/title?title_type=tv_series&companies=sony'
        self.warnerbro1_link = 'https://www.imdb.com/search/title?title_type=tv_series&companies=warner'
        self.uni1_link = 'https://www.imdb.com/search/title?title_type=tv_series&companies=universal'
        self.fox11_link = 'https://www.imdb.com/search/title?title_type=tv_series&companies=fox'
        self.para4_link = 'https://www.imdb.com/search/title?title_type=tv_series&companies=paramount'
        self.mgm5_link = 'https://www.imdb.com/search/title?title_type=tv_series&companies=mgm'
        self.imdblists_link = 'http://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'http://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=tvSeries,tvMiniSeries&start=1'
        self.imdblist2_link = 'http://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=tvSeries,tvMiniSeries&start=1'
        self.imdbwatchlist_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user
        self.keytv_link = 'http://www.imdb.com/search/title?title_type=tv_series,mini_series&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=40&start=1'

        self.trakt_user = control.setting('trakt.user').strip()
        self.trakt_link = 'http://api.trakt.tv'
        self.search_link = 'http://api.trakt.tv/search/show?limit=20&page=1&query='

        self.trakttrending_link = 'http://api.trakt.tv/shows/trending?limit=40&page=1'
        self.traktpopular_link = 'http://api.trakt.tv/shows/popular?limit=40&page=1'
        self.traktlist_link = 'http://api.trakt.tv/users/%s/lists/%s/items'
        self.traktlists_link = 'http://api.trakt.tv/users/me/lists'
        self.traktwatchlist_link = 'http://api.trakt.tv/users/me/watchlist/'
        self.traktlikedlists_link = 'http://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktcollection_link = 'http://api.trakt.tv/users/me/collection/shows'
        self.traktrecommendations_link = 'http://api.trakt.tv/recommendations/shows?limit=%d' % self.count

        self.tvmaze_link = 'http://www.tvmaze.com'
        # self.tvmaze_info_link = 'http://api.tvmaze.com/shows/%s'

        self.tmdb_key = control.setting('tm.user')
        if self.tmdb_key == '' or self.tmdb_key is None:
            self.tmdb_key = '3320855e65a9758297fec4f7c9717698'
        self.tmdb_link = 'http://api.themoviedb.org'

        self.tmdb_lang = 'en-US'
        self.tmdb_popular_link = 'http://api.themoviedb.org/3/tv/popular?api_key=%s&language=en-US&region=US&page=1'
        self.tmdb_toprated_link = 'http://api.themoviedb.org/3/tv/top_rated?api_key=%s&language=en-US&region=US&page=1'
        self.tmdb_ontheair_link = 'http://api.themoviedb.org/3/tv/on_the_air?api_key=%s&language=en-US&region=US&page=1'
        self.tmdb_airingtoday_link = 'http://api.themoviedb.org/3/tv/airing_today?api_key=%s&language=en-US&region=US&page=1'


    def get(self, url, idx=True):
        try:
            try: url = getattr(self, url + '_link')
            except: pass

            try: u = urlparse.urlparse(url).netloc.lower()
            except: pass

            if u in self.trakt_link and '/users/' in url:
                urls = []

                # Must only check if no type is specified at the end of the link, since this function can be called for specific show, season, and episode lists.
                if url.endswith('/watchlist/'):
                    urls.append(url + 'shows')
                    urls.append(url + 'seasons')
                    urls.append(url + 'episodes')
                else:
                    urls.append(url)

                lists = []
                for u in urls:
                    self.list = []
                    try:
                        if not '/users/me/' in url: raise Exception()
                        if trakt.getActivity() > cache.timeout(self.trakt_list, u, self.trakt_user): raise Exception()
                        result = cache.get(self.trakt_list, 0, u, self.trakt_user)
                        if result: lists += result
                    except:
                        result = cache.get(self.trakt_list, 0, u, self.trakt_user)
                        if result: lists += result
                self.list = lists
                self.sort()
                if idx is True: self.worker()

            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx is True: self.worker(level = 0)

            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx is True: self.worker()

            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 1, url)
                self.sort()
                if idx is True: self.worker()

            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 168, url)
                if idx is True: self.worker()

            if self.list is None: self.list = []

            if len(self.list) == 0 and self.search_link in url:
                control.hide()
                if self.notifications: control.notification(title=32010, message=33049, icon='INFO')

            if idx is True: self.tvshowDirectory(self.list)
            return self.list
        except:
            try:
                invalid = (self.list is None or len(self.list) == 0)
            except:
                invalid = True
            if invalid:
                control.hide()
                if self.notifications: control.notification(title=32002, message=33049, icon='INFO')


    def getTMDb(self, url, idx=True):
        try:
            try: url = getattr(self, url + '_link')
            except: pass

            try: u = urlparse.urlparse(url).netloc.lower()
            except: pass

            if u in self.tmdb_link and ('/user/' in url or '/list/' in url):
                from resources.lib.indexers import tmdb
                self.list = cache.get(tmdb.TVshows().tmdb_collections_list, 24, url)

            elif u in self.tmdb_link and not ('/user/' in url or '/list/' in url):
                from resources.lib.indexers import tmdb
                self.list = cache.get(tmdb.TVshows().tmdb_list, 168, url)

            if self.list is None:
                self.list = []
                raise Exception()
            if idx is True: self.tvshowDirectory(self.list)
            return self.list
        except:
            try:
                invalid = (self.list is None or len(self.list) == 0)
            except:
                invalid = True
            if invalid:
                control.idle()
                if self.notifications: control.notification(title = 32002, message = 33049, icon = 'INFO')


    def getTVmaze(self, url, idx=True):
        from resources.lib.indexers import tvmaze
        try:
            try: url = getattr(self, url + '_link')
            except: pass

            self.list = cache.get(tvmaze.tvshows().tvmaze_list, 168, url)

            if self.list is None:
                self.list = []
                raise Exception()
            if idx is True: self.tvshowDirectory(self.list)
            return self.list
        except:
            try:
                invalid = (self.list is None or len(self.list) == 0)
            except:
                invalid = True
            if invalid:
                control.idle()
                if self.notifications: control.notification(title = 32002, message = 33049, icon = 'INFO')


    def sort(self):
        try:
            attribute = int(control.setting('sort.shows.type'))
            reverse = int(control.setting('sort.shows.order')) == 1
            if attribute == 0: reverse = False
            if attribute > 0:
                if attribute == 1:
                    try:
                        self.list = sorted(self.list, key = lambda k: k['tvshowtitle'].lower(), reverse = reverse)
                    except: self.list = sorted(self.list, key = lambda k: k['title'].lower(), reverse = reverse)
                elif attribute == 2:
                    self.list = sorted(self.list, key = lambda k: float(k['rating']), reverse = reverse)
                elif attribute == 3:
                    self.list = sorted(self.list, key = lambda k: int(k['votes'].replace(',', '')), reverse = reverse)
                elif attribute == 4:
                    for i in range(len(self.list)):
                        if not 'premiered' in self.list[i]: self.list[i]['premiered'] = ''
                    self.list = sorted(self.list, key = lambda k: k['premiered'], reverse = reverse)
                elif attribute == 5:
                    for i in range(len(self.list)):
                        if not 'added' in self.list[i]: self.list[i]['added'] = ''
                    self.list = sorted(self.list, key = lambda k: k['added'], reverse = reverse)
                elif attribute == 6:
                    for i in range(len(self.list)):
                        if not 'lastplayed' in self.list[i]: self.list[i]['lastplayed'] = ''
                    self.list = sorted(self.list, key = lambda k: k['lastplayed'], reverse = reverse)
            elif reverse:
                self.list = reversed(self.list)
        except:
            import traceback
            traceback.print_exc()


    def search(self):
        navigator.Navigator().addDirectoryItem(32603, 'tvSearchnew', 'search.png', 'DefaultTVShows.png')
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS tvshow (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
        except:
            pass
        dbcur.execute("SELECT * FROM tvshow ORDER BY ID DESC")
        lst = []
        delete_option = False
        for (id,term) in dbcur.fetchall():
            if term not in str(lst):
                delete_option = True
                navigator.Navigator().addDirectoryItem(term, 'tvSearchterm&name=%s' % term, 'search.png', 'DefaultTVShows.png')
                lst += [(term)]
        dbcur.close()
        if delete_option:
            navigator.Navigator().addDirectoryItem(32605, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        navigator.Navigator().endDirectory()


    def search_new(self):
        t = control.lang(32010).encode('utf-8')
        k = control.keyboard('', t)
        k.doModal()
        q = k.getText() if k.isConfirmed() else None
        if (q is None or q == ''):
            return
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("INSERT INTO tvshow VALUES (?,?)", (None, q))
        dbcon.commit()
        dbcur.close()
        url = self.search_link + urllib.quote_plus(q)
        self.get(url)


    def search_term(self, name):
        url = self.search_link + urllib.quote_plus(name)
        self.get(url)


    def person(self):
        try:
            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t) ; k.doModal()
            q = k.getText().strip() if k.isConfirmed() else None
            if not q: return
            url = self.persons_link + urllib.quote_plus(q)
            self.persons(url)
        except:
            return


    def genres(self):
        genres = [
            ('Action', 'action', True), ('Adventure', 'adventure', True), ('Animation', 'animation', True),
            ('Anime', 'anime', False), ('Biography', 'biography', True), ('Comedy', 'comedy', True),
            ('Crime', 'crime', True), ('Drama', 'drama', True), ('Family', 'family', True),
            ('Fantasy', 'fantasy', True), ('Game-Show', 'game_show', True),
            ('History', 'history', True), ('Horror', 'horror', True), ('Music ', 'music', True),
            ('Musical', 'musical', True), ('Mystery', 'mystery', True), ('News', 'news', True),
            ('Reality-TV', 'reality_tv', True), ('Romance', 'romance', True), ('Science Fiction', 'sci_fi', True),
            ('Sport', 'sport', True), ('Talk-Show', 'talk_show', True), ('Thriller', 'thriller', True),
            ('War', 'war', True), ('Western', 'western', True)
        ]
        for i in genres:
            self.list.append({'name': cleangenre.lang(i[0], self.lang), 'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1], 'image': 'genres.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list

    def keytv(self):
        genres = [
            ('action-hero', 'action-hero', True),
            ('alternate-history', 'alternate-history', True),
            ('ambiguous-ending', 'ambiguous-ending', True),
            ('americana', 'americana', True),
            ('anime', 'anime', True),
            ('anti-hero', 'anti-hero', True),
            ('avant-garde', 'avant-garde', True),
            ('b-movie', 'b-movie', True),
            ('bank-heist', 'bank-heist', True),
            ('based-on-book', 'based-on-book', True),
            ('based-on-play', 'based-on-play', True),
            ('based-on-comic', 'based-on-comic', True),
            ('based-on-comic-book', 'based-on-comic-book', True),
            ('based-on-novel', 'based-on-novel', True),
            ('based-on-novella', 'based-on-novella', True),
            ('based-on-short-story', 'based-on-short-story', True),
            ('battle', 'battle', True),
            ('betrayal', 'betrayal', True),
            ('biker', 'biker', True),
            ('black-comedy', 'black-comedy', True),
            ('blockbuster', 'blockbuster', True),
            ('bollywood', 'bollywood', True),
            ('breaking-the-fourth-wall', 'breaking-the-fourth-wall', True),
            ('business', 'business', True),
            ('caper', 'caper', True),
            ('car-accident', 'car-accident', True),
            ('car-chase', 'car-chase', True),
            ('car-crash', 'car-crash', True),
            ('character-name-in-title', 'character-name-in-title', True),
            ('characters-point-of-view-camera-shot', 'characters-point-of-view-camera-shot', True),
            ('chick-flick', 'chick-flick', True),
            ('coming-of-age', 'coming-of-age', True),
            ('competition', 'competition', True),
            ('conspiracy', 'conspiracy', True),
            ('corruption', 'corruption', True),
            ('criminal-mastermind', 'criminal-mastermind', True),
            ('cult', 'cult', True),
            ('cult-film', 'cult-film', True),
            ('cyberpunk', 'cyberpunk', True),
            ('dark-hero', 'dark-hero', True),
            ('deus-ex-machina', 'deus-ex-machina', True),
            ('dialogue-driven', 'dialogue-driven', True),
            ('dialogue-driven-storyline', 'dialogue-driven-storyline', True),
            ('directed-by-star', 'directed-by-star', True),
            ('director-cameo', 'director-cameo', True),
            ('double-cross', 'double-cross', True),
            ('dream-sequence', 'dream-sequence', True),
            ('dystopia', 'dystopia', True),
            ('ensemble-cast', 'ensemble-cast', True),
            ('epic', 'epic', True),
            ('espionage', 'espionage', True),
            ('experimental', 'experimental', True),
            ('experimental-film', 'experimental-film', True),
            ('fairy-tale', 'fairy-tale', True),
            ('famous-line', 'famous-line', True),
            ('famous-opening-theme', 'famous-opening-theme', True),
            ('famous-score', 'famous-score', True),
            ('fantasy-sequence', 'fantasy-sequence', True),
            ('farce', 'farce', True),
            ('father-daughter-relationship', 'father-daughter-relationship', True),
            ('father-son-relationship', 'father-son-relationship', True),
            ('femme-fatale', 'femme-fatale', True),
            ('fictional-biography', 'fictional-biography', True),
            ('flashback', 'flashback', True),
            ('french-new-wave', 'french-new-wave', True),
            ('futuristic', 'futuristic', True),
            ('good-versus-evil', 'good-versus-evil', True),
            ('heist', 'heist', True),
            ('hero', 'hero', True),
            ('high-school', 'high-school', True),
            ('husband-wife-relationship', 'husband-wife-relationship', True),
            ('idealism', 'idealism', True),
            ('independent-film', 'independent-film', True),
            ('investigation', 'investigation', True),
            ('kidnapping', 'kidnapping', True),
            ('knight', 'knight', True),
            ('kung-fu', 'kung-fu', True),
            ('macguffin', 'macguffin', True),
            ('medieval-times', 'medieval-times', True),
            ('mockumentary', 'mockumentary', True),
            ('monster', 'monster', True),
            ('mother-daughter-relationship', 'mother-daughter-relationship', True),
            ('mother-son-relationship', 'mother-son-relationship', True),
            ('multiple-actors-playing-same-role', 'multiple-actors-playing-same-role', True),
            ('multiple-endings', 'multiple-endings', True),
            ('multiple-perspectives', 'multiple-perspectives', True),
            ('multiple-storyline', 'multiple-storyline', True),
            ('multiple-time-frames', 'multiple-time-frames', True),
            ('murder', 'murder', True),
            ('musical-number', 'musical-number', True),
            ('neo-noir', 'neo-noir', True),
            ('neorealism', 'neorealism', True),
            ('ninja', 'ninja', True),
            ('no-background-score', 'no-background-score', True),
            ('no-music', 'no-music', True),
            ('no-opening-credits', 'no-opening-credits', True),
            ('no-title-at-beginning', 'no-title-at-beginning', True),
            ('nonlinear-timeline', 'nonlinear-timeline', True),
            ('on-the-run', 'on-the-run', True),
            ('one-against-many', 'one-against-many', True),
            ('one-man-army', 'one-man-army', True),
            ('opening-action-scene', 'opening-action-scene', True),
            ('organized-crime', 'organized-crime', True),
            ('parenthood', 'parenthood', True),
            ('parody', 'parody', True),
            ('plot-twist', 'plot-twist', True),
            ('police-corruption', 'police-corruption', True),
            ('police-detective', 'police-detective', True),
            ('post-apocalypse', 'post-apocalypse', True),
            ('postmodern', 'postmodern', True),
            ('psychopath', 'psychopath', True),
            ('race-against-time', 'race-against-time', True),
            ('redemption', 'redemption', True),
            ('remake', 'remake', True),
            ('rescue', 'rescue', True),
            ('road-movie', 'road-movie', True),
            ('robbery', 'robbery', True),
            ('robot', 'robot', True),
            ('rotoscoping', 'rotoscoping', True),
            ('satire', 'satire', True),
            ('self-sacrifice', 'self-sacrifice', True),
            ('serial-killer', 'serial-killer', True),
            ('shakespeare', 'shakespeare', True),
            ('shootout', 'shootout', True),
            ('show-within-a-show', 'show-within-a-show', True),
            ('slasher', 'slasher', True),
            ('southern-gothic', 'southern-gothic', True),
            ('spaghetti-western', 'spaghetti-western', True),
            ('spirituality', 'spirituality', True),
            ('spoof', 'spoof', True),
            ('steampunk', 'steampunk', True),
            ('subjective-camera', 'subjective-camera', True),
            ('superhero', 'superhero', True),
            ('supernatural', 'supernatural', True),
            ('surprise-ending', 'surprise-ending', True),
            ('swashbuckler', 'swashbuckler', True),
            ('sword-and-sandal', 'sword-and-sandal', True),
            ('tech-noir', 'tech-noir', True),
            ('time-travel', 'time-travel', True),
            ('title-spoken-by-character', 'title-spoken-by-character', True),
            ('told-in-flashback', 'told-in-flashback', True),
            ('vampire', 'vampire', True),
            ('virtual-reality', 'virtual-reality', True),
            ('voice-over-narration', 'voice-over-narration', True),
            ('whistleblower', 'whistleblower', True),
            ('wilhelm-scream', 'wilhelm-scream', True),
            ('wuxia', 'wuxia', True),
            ('zombie', 'zombie', True)

        ]
        for i in genres:
            self.list.append({'name': cleangenre.lang(i[0], self.lang), 'url': self.keytv_link % i[1] if i[2] else self.keyword_link % i[1], 'image': 'genres.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list



    def networks(self):
        if control.setting('tvshows.networks.view') == '0':
            from resources.lib.indexers.tvmaze import networks_this_season as networks

        if control.setting('tvshows.networks.view') == '1':
            from resources.lib.indexers.tvmaze import networks_view_all as networks

        networks = sorted(networks, key=lambda x: x[0])

        for i in networks:
            self.list.append({'name': i[0], 'url': self.tvmaze_link + i[1], 'image': i[2], 'action': 'tvmazeTvshows'})
        self.addDirectory(self.list)
        return self.list


    def languages(self):
        languages = [('Arabic', 'ar'), ('Bosnian', 'bs'), ('Bulgarian', 'bg'), ('Chinese', 'zh'), ('Croatian', 'hr'), ('Dutch', 'nl'),
            ('English', 'en'), ('Finnish', 'fi'), ('French', 'fr'), ('German', 'de'), ('Greek', 'el'), ('Hebrew', 'he'), ('Hindi ', 'hi'),
            ('Hungarian', 'hu'), ('Icelandic', 'is'), ('Italian', 'it'), ('Japanese', 'ja'), ('Korean', 'ko'), ('Norwegian', 'no'),
            ('Persian', 'fa'), ('Polish', 'pl'), ('Portuguese', 'pt'), ('Punjabi', 'pa'), ('Romanian', 'ro'), ('Russian', 'ru'),
            ('Serbian', 'sr'), ('Spanish', 'es'), ('Swedish', 'sv'), ('Turkish', 'tr'), ('Ukrainian', 'uk')]
        for i in languages:
            self.list.append({'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'languages.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def certifications(self):
        certificates = [
            ('Child Audience (Y)', 'TV-Y'),
            ('Young Audience (Y7)', 'TV-Y7'),
            ('Parental Guidance (PG)', 'TV-PG'),
            ('Youth Audience (14)', 'TV-13', 'TV-14'),
            ('Mature Audience (MA)', 'TV-MA')
        ]
        for i in certificates: self.list.append({'name': str(i[0]), 'url': self.certification_link % self.certificatesFormat(i[1]), 'image': 'certificates.png', 'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def certificatesFormat(self, certificates):
        base = 'US%3A'
        if not isinstance(certificates, (tuple, list)): certificates = [certificates]
        return ','.join([base + i.upper() for i in certificates])


    def persons(self, url):
        if url is None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)
        for i in range(0, len(self.list)): self.list[i].update({'action': 'tvshows'})
        self.addDirectory(self.list)
        return self.list


    def userlists(self):
        userlists = []
        try:
            if trakt.getTraktCredentialsInfo() is False: raise Exception()
            activity = trakt.getActivity()
            self.list = []
            lists = []

            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user): raise Exception()
                lists += cache.get(self.trakt_user_list, 3, self.traktlists_link, self.trakt_user)
            except:
                lists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
            for i in range(len(lists)): lists[i].update({'image': 'trakt.png'})
            userlists += lists
        except: pass

        try:
            if self.imdb_user == '': raise Exception()
            self.list = []
            lists = cache.get(self.imdb_user_list, 0, self.imdblists_link)
            for i in range(len(lists)): lists[i].update({'image': 'imdb.png'})
            userlists += lists
        except: pass

        try:
            if trakt.getTraktCredentialsInfo() is False: raise Exception()
            self.list = []
            lists = []

            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user): raise Exception()
                lists += cache.get(self.trakt_user_list, 3, self.traktlikedlists_link, self.trakt_user)
            except:
                lists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)

                for i in range(len(lists)): lists[i].update({'image': 'trakt.png'})
                userlists += lists
        except: pass

        self.list = []

        # Filter the user's own lists that were
        for i in range(len(userlists)):
            contains = False
            adapted = userlists[i]['url'].replace('/me/', '/%s/' % self.trakt_user)
            for j in range(len(self.list)):
                if adapted == self.list[j]['url'].replace('/me/', '/%s/' % self.trakt_user):
                    contains = True
                    break
            if not contains:
                self.list.append(userlists[i])

        for i in range(len(self.list)): self.list[i].update({'action': 'tvshows'})

        # imdb Watchlist
        if self.imdb_user != '':
            imdb_watchlist = self.imdbwatchlist2_link
            self.list.insert(0, {'name': control.lang(32033).encode('utf-8'), 'url': imdb_watchlist, 'image': 'imdb.png', 'action': 'tvshows'})

        # Trakt Watchlist
        if trakt.getTraktCredentialsInfo():
            trakt_watchlist = self.traktwatchlist_link + 'shows'
            self.list.insert(0, {'name': control.lang(32033).encode('utf-8'), 'url': trakt_watchlist, 'image': 'trakt.png', 'action': 'tvshows'})

        self.addDirectory(self.list)
        return self.list


    def trakt_list(self, url, user):
        try:
            dupes = []

            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q

            result = trakt.getTraktAsJson(u)

            items = []
            for i in result:
                try: items.append(i['show'])
                except: pass
            if len(items) == 0:
                items = result
        except:
            return

        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            if not int(q['limit']) == len(items): raise Exception()
            q.update({'page': str(int(q['page']) + 1)})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = item['title']
                title = re.sub('\s(|[(])(UK|US|AU|\d{4})(|[)])$', '', title)
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = item['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                # try:
                    # if int(year) > int((self.datetime).strftime('%Y')): continue
                # except: pass

                try:
                    imdb = item['ids']['imdb']
                    if imdb is None or imdb == '':
                        imdb = '0'
                    else:
                        imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                    imdb = imdb.encode('utf-8')
                except:
                    imdb = '0'

                try:
                    tmdb = item['ids']['tmdb']
                    if tmdb is None or tmdb == '':
                        tmdb = '0'
                    else:
                        tmdb = re.sub('[^0-9]', '', str(tmdb))
                    tmdb = tmdb.encode('utf-8')
                except:
                    tmdb = '0'

                try:
                    tvdb = item['ids']['tvdb']
                    if tvdb is None or tvdb == '':
                        tvdb = '0'
                    else:
                        tvdb = re.sub('[^0-9]', '', str(tvdb))
                    tvdb = tvdb.encode('utf-8')
                except:
                    tvdb = '0'

                if tvdb is None or tvdb == '' or tvdb in dupes: raise Exception()
                dupes.append(tvdb)

                try: premiered = item['first_aired']
                except: premiered = '0'
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'
                premiered = premiered.encode('utf-8')

                try: studio = item['network']
                except: studio = '0'
                if studio is None: studio = '0'
                studio = studio.encode('utf-8')

                try: genre = item['genres']
                except: genre = '0'
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = ' / '.join(genre)
                genre = genre.encode('utf-8')

                try: duration = str(item['runtime'])
                except: duration = '0'
                if duration is None: duration = '0'
                genre = genre.encode('utf-8')

                try: rating = str(item['rating'])
                except: rating = '0'
                if rating is None or rating == '0.0': rating = '0'
                rating = rating.encode('utf-8')

                try: votes = str(item['votes'])
                except: votes = '0'
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes is None: votes = '0'
                votes = votes.encode('utf-8')

                try: mpaa = item['certification']
                except: mpaa = '0'
                if mpaa is None: mpaa = '0'
                mpaa = mpaa.encode('utf-8')

                try: plot = item['overview'].encode('utf-8')
                except: plot = '0'
                if plot is None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating,
                                            'votes': votes, 'mpaa': mpaa, 'plot': plot, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': '0', 'fanart': '0', 'next': next})
            except:
                pass

        return self.list


    def trakt_user_list(self, url, user):
        try:
            # items = trakt.getTraktAsJson(url)
            result = trakt.getTrakt(url)
            items = json.loads(result)
        except:
            pass

        for item in items:
            try:
                try:
                    name = item['list']['name']
                except:
                    name = item['name']
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                try:
                    url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except:
                    url = ('me', item['ids']['slug'])

                url = self.traktlist_link % url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

#        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a |^an )', '', k['name'].lower()))
        return self.list


    def imdb_list(self, url):
        try:
            dupes = []

            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))

            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url).decode('iso-8859-1').encode('utf-8'), 'meta', ret='content', attrs = {'property': 'pageId'})[0]

            if url == self.imdbwatchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url
            elif url == self.imdbwatchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist2_link % url

            result = client.request(url)

            result = result.replace('\n', ' ')
            result = result.decode('iso-8859-1').encode('utf-8')

            items = client.parseDOM(result, 'div', attrs = {'class': '.+? lister-item'}) + client.parseDOM(result, 'div', attrs = {'class': 'lister-item .+?'})
            items += client.parseDOM(result, 'div', attrs = {'class': 'list_item.+?'})
        except:
            return

        try:
#            HTML syntax error, " directly followed by attribute name. Insert space in between. parseDOM can otherwise not handle it.
            result = result.replace('"class="lister-page-next', '" class="lister-page-next')

            next = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'lister-page-next.+?'})

            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs = {'class': 'pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]

            next = url.replace(urlparse.urlparse(url).query, urlparse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[1]
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = client.parseDOM(item, 'span', attrs = {'class': 'lister-item-year.+?'})
                year += client.parseDOM(item, 'span', attrs = {'class': 'year_type'})
                year = re.findall('(\d{4})', year[0])[0]
                year = year.encode('utf-8')

                # if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = imdb.encode('utf-8')

                if imdb in dupes: raise Exception()
                dupes.append(imdb)

#                parseDOM cannot handle elements without a closing tag.
#                try: poster = client.parseDOM(item, 'img', ret='loadlate')[0]
#                except: poster = '0'
                try:
                    from bs4 import BeautifulSoup
                    html = BeautifulSoup(item, "html.parser")
                    poster = html.find_all('img')[0]['loadlate']
                except:
                    poster = '0'

                if '/nopicture/' in poster: poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try: genre = client.parseDOM(item, 'span', attrs = {'class': 'genre'})[0]
                except: genre = '0'
                genre = ' / '.join([i.strip() for i in genre.split(',')])
                if genre == '': genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: duration = re.findall('(\d+?) min(?:s|)', item)[-1]
                except: duration = '0'
                duration = duration.encode('utf-8')

                rating = '0'
                try: rating = client.parseDOM(item, 'span', attrs = {'class': 'rating-rating'})[0]
                except:
                    try: rating = client.parseDOM(rating, 'span', attrs = {'class': 'value'})[0]
                    except:
                        try: rating = client.parseDOM(item, 'div', ret='data-value', attrs = {'class': '.*?imdb-rating'})[0]
                        except: pass
                if rating == '' or rating == '-': rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                votes = '0'
                try: votes = client.parseDOM(item, 'span', attrs = {'name': 'nv'})[0]
                except:
                    try: votes = client.parseDOM(item, 'div', ret='title', attrs = {'class': '.*?rating-list'})[0]
                    except:
                        try: votes = re.findall('\((.+?) vote(?:s|)\)', votes)[0]
                        except: pass
                if votes == '': votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                try: mpaa = client.parseDOM(item, 'span', attrs = {'class': 'certificate'})[0]
                except: mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                try: director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', item)[0]
                except: director = '0'
                director = client.parseDOM(director, 'a')
                director = ' / '.join(director)
                if director == '': director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try:
                    cast = re.findall('Stars(?:s|):(.+?)(?:\||</div>)', item)[0]
                except:
                    cast = '0'
                cast = client.replaceHTMLCodes(cast)
                cast = cast.encode('utf-8')
                cast = client.parseDOM(cast, 'a')
                if cast == []: cast = '0'

                plot = '0'
                try: plot = client.parseDOM(item, 'p', attrs = {'class': 'text-muted'})[0]
                except:
                    try: plot = client.parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
                    except: pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                plot = re.sub('<.+?>|</.+?>', '', plot)
                if plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes,
                                            'mpaa': mpaa, 'director': director, 'cast': cast, 'plot': plot, 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'poster': poster, 'next': next})
            except:
                pass

        return self.list


    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            result = result.decode('iso-8859-1').encode('utf-8')
            items = client.parseDOM(result, 'div', attrs = {'class': '.+? lister-item'}) + client.parseDOM(result, 'div', attrs = {'class': 'lister-item .+?'})
        except:
            import traceback
            traceback.print_exc()

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[1]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[1]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % (url, self.certificates)
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = client.parseDOM(item, 'img', ret='src')[0]
                image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                import traceback
                traceback.print_exc()

        return self.list


    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'li', attrs={'class': 'ipl-zebra-list__item user-list'})
        except:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list

#        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a |^an )', '', k['name'].lower()))

        return self.list


    def worker(self, level = 1):
        try:
            if self.list is None or self.list == []:
                return
            self.meta = []
            total = len(self.list)

            self.fanart_tv_headers = {'api-key': '9f846e7ec1ea94fad5d8a431d1d26b43'}
            if not self.fanart_tv_user == '':
                self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})

            for i in range(0, total):
                self.list[i].update({'metacache': False})

            self.list = metacache.fetch(self.list, self.lang, self.user)

            for r in range(0, total, 40):
                threads = []
                for i in range(r, r + 40):
                    if i <= total: threads.append(workers.Thread(self.super_info, i))
                [i.start() for i in threads]
                [i.join() for i in threads]

                if self.meta:
                    metacache.insert(self.meta)

            self.list = [i for i in self.list if not i['tvdb'] == '0']

            if self.fanart_tv_user == '':
                for i in self.list:
                    i.update({'clearlogo': '0', 'clearart': '0'})
        except:
            import traceback
            traceback.print_exc()


    def metadataRetrieve(self, title, year, imdb, tmdb, tvdb):
        self.list = [{'metacache': False, 'title': title, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb}]
        self.worker()
        return self.list[0]


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] is True:
                raise Exception()

            imdb = self.list[i]['imdb'] if 'imdb' in self.list[i] else '0'
            tmdb = self.list[i]['tmdb'] if 'tmdb' in self.list[i] else '0'
            tvdb = self.list[i]['tvdb'] if 'tvdb' in self.list[i] else '0'

            if imdb == '0' or tmdb == '0':
                try:
                    trakt_ids = trakt.SearchTVShow(urllib.quote_plus(self.list[i]['title']), self.list[i]['year'], full = False)[0]
                    trakt_ids = trakt_ids.get('show', '0')
                    if imdb == '0':
                        imdb = trakt_ids.get('ids', {}).get('imdb', '0')
                        imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                        if not imdb:
                            imdb = '0'
                except:
                    imdb = '0'

                if tmdb == '0':
                    try:
                        tmdb = trakt_ids.get('ids', {}).get('tmdb', '0')
                        tmdb = re.sub('[^0-9]', '', str(tmdb))
                        if not tmdb:
                            tmdb = '0'
                    except:
                        tmdb = '0'

            if tvdb == '0' and not imdb == '0':
                url = self.tvdb_by_imdb % imdb
                result = client.request(url, timeout = '10')

                try: tvdb = client.parseDOM(result, 'seriesid')[0]
                except: tvdb = '0'

                try: name = client.parseDOM(result, 'SeriesName')[0]
                except: name = '0'
                dupe = re.findall('[***]Duplicate (\d*)[***]', name)
                if dupe: tvdb = str(dupe[0])
                if tvdb == '':
                    tvdb = '0'

###--Check TVDb for missing info
            if tvdb == '0' or imdb == '0':
                url = self.tvdb_by_query % (urllib.quote_plus(self.list[i]['title']))
                item2 = client.request(url, timeout='20')
                item2 = re.sub(r'[^\x00-\x7F]+', '', item2)
                item2 = client.replaceHTMLCodes(item2)
                item2 = client.parseDOM(item2, 'Series')
                if tvdb == '0':
                    try: tvdb = client.parseDOM(item2, 'seriesid')[0]
                    except: tvdb = '0'
                if imdb == '0':
                    try: imdb = client.parseDOM(item2, 'IMDB_ID')[0]
                    except: imdb = '0'

            url = self.tvdb_info_link % tvdb
            item = client.request(url, timeout = '20', error = True)

            if item is None:
                raise Exception()

            if imdb == '0':
                try: imdb = client.parseDOM(item, 'IMDB_ID')[0]
                except: pass
                if imdb == '': imdb = '0'
                imdb = imdb.encode('utf-8')

            try: title = client.parseDOM(item, 'SeriesName')[0]
            except: title = ''
            if title == '': title = '0'
            title = client.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            try: year = client.parseDOM(item, 'FirstAired')[0]
            except: year = ''
            try: year = re.compile('(\d{4})').findall(year)[0]
            except: year = ''
            if year == '': year = '0'
            year = year.encode('utf-8')

            try: premiered = client.parseDOM(item, 'FirstAired')[0]
            except: premiered = '0'
            if premiered == '': premiered = '0'
            premiered = client.replaceHTMLCodes(premiered)
            premiered = premiered.encode('utf-8')

            if not 'studio' in self.list[i] or self.list[i]['studio'] == '0':
                try: studio = client.parseDOM(item, 'Network')[0]
                except: studio = '0'
                studio = client.replaceHTMLCodes(studio)
                studio = studio.encode('utf-8')
            else: studio = self.list[i]['studio']

            try: genre = client.parseDOM(item, 'Genre')[0]
            except: genre = ''
            genre = [x for x in genre.split('|') if not x == '']
            genre = ' / '.join(genre)
            if genre == '': genre = '0'
            genre = client.replaceHTMLCodes(genre)
            genre = genre.encode('utf-8')

            if not 'duration' in self.list[i] or self.list[i]['duration'] == '0':
                try: duration = client.parseDOM(item, 'Runtime')[0]
                except: duration = ''
                if duration == '': duration = '0'
                duration = client.replaceHTMLCodes(duration)
                duration = duration.encode('utf-8')
            else: duration = self.list[i]['duration']

            try: rating = client.parseDOM(item, 'Rating')[0]
            except: rating = ''
            if 'rating' in self.list[i] and not self.list[i]['rating'] == '0':
                rating = self.list[i]['rating']
            if rating == '': rating = '0'
            rating = client.replaceHTMLCodes(rating)
            rating = rating.encode('utf-8')

            try: votes = client.parseDOM(item, 'RatingCount')[0]
            except: votes = ''
            if 'votes' in self.list[i] and not self.list[i]['votes'] == '0':
                votes = self.list[i]['votes']
            if votes == '': votes = '0'
            votes = client.replaceHTMLCodes(votes)
            votes = votes.encode('utf-8')

            try: mpaa = client.parseDOM(item, 'ContentRating')[0]
            except: mpaa = ''
            if mpaa == '': mpaa = '0'
            mpaa = client.replaceHTMLCodes(mpaa)
            mpaa = mpaa.encode('utf-8')

            try: cast = client.parseDOM(item, 'Actors')[0]
            except: cast = ''
            cast = [x for x in cast.split('|') if not x == '']
            try: cast = [(x.encode('utf-8'), '') for x in cast]
            except: cast = []
            if cast == []: cast = '0'

            try: plot = client.parseDOM(item, 'Overview')[0]
            except: plot = ''
            if plot == '': plot = '0'
            plot = client.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            try: poster = client.parseDOM(item, 'poster')[0]
            except: poster = ''
            if not poster == '': poster = self.tvdb_image + poster
            else: poster = '0'
            if 'poster' in self.list[i] and poster == '0': poster = self.list[i]['poster']
            poster = client.replaceHTMLCodes(poster)
            poster = poster.encode('utf-8')

            try: banner = client.parseDOM(item, 'banner')[0]
            except: banner = ''
            if not banner == '': banner = self.tvdb_image + banner
            else: banner = '0'
            banner = client.replaceHTMLCodes(banner)
            banner = banner.encode('utf-8')

            try: fanart = client.parseDOM(item, 'fanart')[0]
            except: fanart = ''
            if not fanart == '': fanart = self.tvdb_image + fanart
            else: fanart = '0'
            fanart = client.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')

###--Fanart.tv artwork
            try:
                artmeta = True
                art = client.request(self.fanart_tv_art_link % tvdb, headers=self.fanart_tv_headers, timeout ='10', error=True)
                try: art = json.loads(art)
                except: artmeta = False
            except:
                pass

            try:
                poster2 = art['tvposter']
                poster2 = [(x['url'], x['likes']) for x in poster2 if x.get('lang') == self.lang] + [(x['url'], x['likes']) for x in poster2 if x.get('lang') == '']
                poster2 = [(x[0], x[1]) for x in poster2]
                poster2 = sorted(poster2, key=lambda x: int(x[1]), reverse=True)
                poster2 = [x[0] for x in poster2][0]
                poster2 = poster2.encode('utf-8')
            except:
                poster2 = '0'

            try:
                fanart2 = art['showbackground']
                fanart2 = [(x['url'], x['likes']) for x in fanart2 if x.get('lang') == self.lang] + [(x['url'], x['likes']) for x in fanart2 if x.get('lang') == '']
                fanart2 = [(x[0], x[1]) for x in fanart2]
                fanart2 = sorted(fanart2, key=lambda x: int(x[1]), reverse=True)
                fanart2 = [x[0] for x in fanart2][0]
                fanart2 = fanart2.encode('utf-8')
            except:
                fanart2 = '0'

            try:
                banner2 = art['tvbanner']
                banner2 = [(x['url'], x['likes']) for x in banner2 if x.get('lang') == self.lang] + [(x['url'], x['likes']) for x in banner2 if x.get('lang') == '']
                banner2 = [(x[0], x[1]) for x in banner2]
                banner2 = sorted(banner2, key=lambda x: int(x[1]), reverse=True)
                banner2 = [x[0] for x in banner2][0]
                banner2 = banner2.encode('utf-8')
            except:
                banner2 = '0'

            try:
                if 'hdtvlogo' in art: clearlogo = art['hdtvlogo']
                else: clearlogo = art['clearlogo']
                clearlogo = [(x['url'], x['likes']) for x in clearlogo if x.get('lang') == self.lang] + [(x['url'], x['likes']) for x in clearlogo if x.get('lang') == '']
                clearlogo = [(x[0], x[1]) for x in clearlogo]
                clearlogo = sorted(clearlogo, key=lambda x: int(x[1]), reverse=True)
                clearlogo = [x[0] for x in clearlogo][0]
                clearlogo = clearlogo.encode('utf-8')
            except:
                clearlogo = '0'

            try:
                if 'hdclearart' in art: clearart = art['hdclearart']
                else: clearart = art['clearart']
                clearart = [(x['url'], x['likes']) for x in clearart if x.get('lang') == self.lang] + [(x['url'], x['likes']) for x in clearart if x.get('lang') == '']
                clearart = [(x[0], x[1]) for x in clearart]
                clearart = sorted(clearart, key=lambda x: int(x[1]), reverse=True)
                clearart = [x[0] for x in clearart][0]
                clearart = clearart.encode('utf-8')
            except:
                clearart = '0'

            try:
                if 'tvthumb' in art: landscape = art['tvthumb']
                else: landscape = art['showbackground']
                landscape = [(x['url'], x['likes']) for x in landscape if x.get('lang') == self.lang] + [(x['url'], x['likes']) for x in landscape if x.get('lang') == '']
                landscape = [(x[0], x[1]) for x in landscape]
                landscape = sorted(landscape, key=lambda x: int(x[1]), reverse=True)
                landscape = [x[0] for x in landscape][0]
                landscape = landscape.encode('utf-8')
            except:
                landscape = '0'

            item = {'extended': True, 'title': title, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': poster, 'poster2': poster2, 'banner': banner, 'banner2': banner2,
                        'fanart': fanart, 'fanart2': fanart2, 'clearlogo': clearlogo, 'clearart': clearart, 'landscape': landscape, 'premiered': premiered, 'studio': studio,
                        'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'cast': cast, 'plot': plot}
            item = dict((k,v) for k, v in item.iteritems() if not v == '0')
            self.list[i].update(item)

            if artmeta is False: raise Exception()

            meta = {'imdb': imdb, 'tvdb': tvdb, 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)

        except:
            pass


    def tvshowDirectory(self, items, next=True):
        if items is None or len(items) == 0:
            control.idle()
            control.notification(title = 32002, message = 33049, icon = 'INFO')
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        # try: isOld = False ; control.item().getArt('type')
        # except: isOld = True

        flatten = True if control.setting('flatten.tvshows') == 'true' else False

        if trakt.getTraktIndicatorsInfo() is True:
            watchedMenu = control.lang(32068).encode('utf-8')
            unwatchedMenu = control.lang(32069).encode('utf-8')
        else:
            watchedMenu = control.lang(32066).encode('utf-8')
            unwatchedMenu = control.lang(32067).encode('utf-8')

        traktManagerMenu = control.lang(32070).encode('utf-8')
        playlistManagerMenu = control.lang(35522).encode('utf-8')
        queueMenu = control.lang(32065).encode('utf-8')
        showPlaylistMenu = control.lang(35517).encode('utf-8')
        clearPlaylistMenu = control.lang(35516).encode('utf-8')
        nextMenu = control.lang(32053).encode('utf-8')
        playRandom = control.lang(32535).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                imdb, tvdb, year = i['imdb'], i['tvdb'], i['year']
                label = i['title']

                systitle = sysname = urllib.quote_plus(i['originaltitle'])
                sysimage = urllib.quote_plus(i['poster'])

                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tvdb_id': tvdb})
                meta.update({'mediatype': 'tvshow'})
                meta.update({'tvshowtitle': systitle})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(label))})

                try:
                    plot = meta['plot']
                    index = plot.rfind('See full summary')
                    if index >= 0: plot = plot[:index]
                    plot = plot.strip()
                    if re.match('[a-zA-Z\d]$', plot): plot += ' ...'
                    meta['plot'] = plot
                except:
                    pass

                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except:
                    pass

                poster = '0'
                # if poster == '0' and 'poster3' in i: poster = i['poster3']
                if poster == '0' and 'poster2' in i: poster = i['poster2']
                if poster == '0' and 'poster' in i: poster = i['poster']

                icon = '0'
                # if icon == '0' and 'icon3' in i: icon = i['icon3']
                if icon == '0' and 'icon2' in i: icon = i['icon2']
                if icon == '0' and 'icon' in i: icon = i['icon']

                thumb = '0'
                # if thumb == '0' and 'thumb3' in i: thumb = i['thumb3']
                if thumb == '0' and 'thumb2' in i: thumb = i['thumb2']
                if thumb == '0' and 'thumb' in i: thumb = i['thumb']

                banner = '0'
                # if banner == '0' and 'banner3' in i: banner = i['banner3']
                if banner == '0' and 'banner2' in i: banner = i['banner2']
                if banner == '0' and 'banner' in i: banner = i['banner']

                fanart = '0'
                if settingFanart:
                    # if fanart == '0' and 'fanart3' in i: fanart = i['fanart3']
                    if fanart == '0' and 'fanart2' in i: fanart = i['fanart2']
                    if fanart == '0' and 'fanart' in i: fanart = i['fanart']

                clearlogo = '0'
                if clearlogo == '0' and 'clearlogo' in i: clearlogo = i['clearlogo']

                clearart = '0'
                if clearart == '0' and 'clearart' in i: clearart = i['clearart']

                landscape = '0'
                if landscape == '0' and 'landscape' in i: landscape = i['landscape']

                if poster == '0': poster = addonPoster
                if icon == '0': icon = poster
                if thumb == '0': thumb = poster
                if banner == '0': banner = addonBanner
                if fanart == '0': fanart = addonFanart

                art = {}
                if not poster == '0' and not poster is None:
                    art.update({'poster' : poster, 'tvshow.poster' : poster, 'season.poster' : poster})
                if not fanart == '0' and not fanart is None:
                    art.update({'fanart' : fanart})
                if not icon == '0' and not icon is None:
                    art.update({'icon' : icon})
                if not thumb == '0' and not thumb is None:
                    art.update({'thumb' : thumb})
                if not banner == '0' and not banner is None:
                    art.update({'banner' : banner})
                if not clearlogo == '0' and not clearlogo is None:
                    art.update({'clearlogo' : clearlogo})
                if not clearart == '0' and not clearart is None:
                    art.update({'clearart' : clearart})
                if not landscape == '0' and not landscape is None:
                    art.update({'landscape' : landscape})

                if flatten is True:
                    url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (sysaddon, systitle, year, imdb, tvdb)
                else:
                    url = '%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s' % (sysaddon, systitle, year, imdb, tvdb)


####-Context Menu and Overlays-####
                cm = []

                if traktCredentials is True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&tvdb=%s)' % (sysaddon, sysname, imdb, tvdb)))
                try:
                    indicators = playcount.getTVShowIndicators()
                    overlay = int(playcount.getTVShowOverlay(indicators, imdb, tvdb))
                    watched = overlay == 7
                    if watched:
                        meta.update({'playcount': 1, 'overlay': 7})
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&query=6)' % (sysaddon, systitle, imdb, tvdb)))
                    else:
                        meta.update({'playcount': 0, 'overlay': 6})
                        cm.append((watchedMenu, 'RunPlugin(%s?action=tvPlaycount&name=%s&imdb=%s&tvdb=%s&query=7)' % (sysaddon, systitle, imdb, tvdb)))
                except:
                    pass

                sysmeta = urllib.quote_plus(json.dumps(meta))
                sysart = urllib.quote_plus(json.dumps(art))

                cm.append(('Find similar', 'ActivateWindow(10025,%s?action=tvshows&url=http://api.trakt.tv/shows/%s/related,return)' % (sysaddon, imdb)))
                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=season&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' % (
                                    sysaddon, urllib.quote_plus(systitle), urllib.quote_plus(year), urllib.quote_plus(imdb), urllib.quote_plus(tvdb))))
                # cm.append((playlistManagerMenu, 'RunPlugin(%s?action=playlistManager&name=%s&url=%s&meta=%s&art=%s)' % (sysaddon, systitle, sysurl, sysmeta, sysart)))
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem&name=%s)' % (sysaddon, systitle)))
                cm.append((showPlaylistMenu, 'RunPlugin(%s?action=showPlaylist)' % sysaddon))
                cm.append((clearPlaylistMenu, 'RunPlugin(%s?action=clearPlaylist)' % sysaddon))

                # if isOld is True:
                    # cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))
                cm.append((addToLibrary, 'RunPlugin(%s?action=tvshowToLibrary&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' % (sysaddon, systitle, year, imdb, tvdb)))
                cm.append(('[COLOR red]Still i Rise Settings[/COLOR]', 'RunPlugin(%s?action=openSettings&query=(0,0))' % sysaddon))
####################################

                item = control.item(label = label)

                unwatchedEnabled = True
                unwatchedLimit = False

                if unwatchedEnabled:
                    count = playcount.getShowCount(indicators, imdb, tvdb, unwatchedLimit)
                    if count:
                        item.setProperty('TotalEpisodes', str(count['total']))
                        item.setProperty('WatchedEpisodes', str(count['watched']))
                        item.setProperty('UnWatchedEpisodes', str(count['unwatched']))

                total_seasons = trakt.getSeasons(imdb, full=False)
                if not total_seasons is None:
                    total_seasons = [i['number'] for i in total_seasons]
                    total_seasons = len(total_seasons)
                    # if control.setting('tv.specials') == 'true' and self.season_special is True:
                        # total_seasons = total_seasons - 1
                    item.setProperty('TotalSeasons', str(total_seasons))

                if not fanart == '0' and not fanart is None:
                    item.setProperty('Fanart_Image', fanart)
                item.setArt(art)
                item.setInfo(type='video', infoLabels=control.metadataClean(meta))
                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)
                item.addContextMenuItems(cm)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        if next:
            try:
                url = items[0]['next']
                if url == '': raise Exception()

                if self.imdb_link in url or self.trakt_link in url:
                    url = '%s?action=tvshowPage&url=%s' % (sysaddon, urllib.quote_plus(url))

                elif self.tmdb_link in url:
                    url = '%s?action=tmdbTvshowPage&url=%s' % (sysaddon, urllib.quote_plus(url))

                elif self.tvmaze_link in url:
                    url = '%s?action=tvmazeTvshowPage&url=%s' % (sysaddon, urllib.quote_plus(url))

                item = control.item(label=nextMenu)
                icon = control.addonNext()
                item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
                if not addonFanart is None: item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        control.content(syshandle, 'tvshows')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('shows', {'skin.estuary': 55, 'skin.confluence': 500})


    def addDirectory(self, items, queue=False):
        if items is None or len(items) == 0: 
            control.idle()
            control.notification(title = 32002, message = 33049, icon = 'INFO')
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        queueMenu = control.lang(32065).encode('utf-8')
        playRandom = control.lang(32535).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                name = i['name']
                link = i['url']
                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(link)
                except: pass

                item = control.item(label = name)

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath is None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                cm = []
                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=show&url=%s)' % (sysaddon, urllib.quote_plus(i['url']))))
                if queue is True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
                try: cm.append((addToLibrary, 'RunPlugin(%s?action=tvshowsToLibrary&url=%s)' % (sysaddon, urllib.quote_plus(i['context']))))
                except: pass

                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart is None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)
                control.addItem(handle = syshandle, url = url, listitem = item, isFolder = True)
            except:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc = True)
