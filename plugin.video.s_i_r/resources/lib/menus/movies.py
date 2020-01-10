# -*- coding: utf-8 -*-

'''
    Still i Rise Add-on
'''

import os, sys, re, datetime
import urllib, urlparse, json

from resources.lib.modules import trakt
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
# import requests

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()
action = params.get('action')


class Movies:
    def __init__(self, type='movie', notifications=True):
        self.count = 40
        self.type = type
        self.notifications = notifications
        self.list = []

        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.month_date = (self.datetime - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
        self.year_date = (self.datetime - datetime.timedelta(days = 365)).strftime('%Y-%m-%d')

        self.trakt_link = 'http://api.trakt.tv'
        self.trakt_user = control.setting('trakt.user').strip()
        self.lang = control.apiLanguage()['trakt']

        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        if self.imdb_user == '' or self.imdb_user is None:
            self.imdb_user = '98341406'

        self.tmdb_key = control.setting('tm.user')
        if self.tmdb_key == '' or self.tmdb_key is None:
            self.tmdb_key = '3320855e65a9758297fec4f7c9717698'

        self.user = str(self.imdb_user) + str(self.tmdb_key)

        self.hidecinema = control.setting('hidecinema')
        self.hidecinema_rollback = int(control.setting('hidecinema.rollback'))
        self.hidecinema_rollback2 = self.hidecinema_rollback * 30
        self.hidecinema_date = (datetime.date.today() - datetime.timedelta(days = self.hidecinema_rollback2)).strftime('%Y-%m')

        self.tmdb_popular_link = 'http://api.themoviedb.org/3/movie/popular?api_key=%s&language=en-US&region=US&page=1'
        self.tmdb_toprated_link = 'http://api.themoviedb.org/3/movie/top_rated?api_key=%s&page=1'
        self.tmdb_upcoming_link = 'http://api.themoviedb.org/3/movie/upcoming?api_key=%s&language=en-US&region=US&page=1' 
        self.tmdb_nowplaying_link = 'http://api.themoviedb.org/3/movie/now_playing?api_key=%s&language=en-US&region=US&page=1'

        self.imdb_link = 'https://www.imdb.com'
        self.tmdb_link = 'http://api.themoviedb.org'

        self.persons_link = 'https://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'https://www.imdb.com/search/name?count=100&gender=male,female'
        self.person_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&role=%s&sort=year,desc&count=40&start=1'
        self.keyword_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&keywords=%s&sort=moviemeter,asc&count=40&start=1'
        self.oscars_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_winners&sort=year,desc&count=40&start=1'
        self.oscarsnominees_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_nominees&sort=year,desc&count=40&start=1'
        self.theaters_link = 'https://www.imdb.com/search/title?title_type=feature&groups=now-playing-us&languages=en&sort=release_date,desc&count=40&start=1'
        self.year_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&year=%s,%s&sort=moviemeter,asc&count=40&start=1'

        if self.hidecinema == 'true':
            self.mostpopular_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&release_date=,%s&sort=moviemeter,asc&count=40&start=1' % (self.hidecinema_date)
            self.mostvoted_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=,%s&sort=num_votes,desc&count=40&start=1' % (self.hidecinema_date)
            self.featured_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=,%s&sort=moviemeter,asc&count=40&start=1' % (self.hidecinema_date)
            self.genre_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,%s&genres=%s&sort=moviemeter,asc&count=40&start=1' % (self.hidecinema_date, '%s')
            self.language_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&release_date=,%s&count=40&start=1' % ('%s', self.hidecinema_date)
            self.certification_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=%s&sort=moviemeter,asc&release_date=,%s&count=40&start=1' % ('%s', self.hidecinema_date)
            self.imdbboxoffice_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&release_date=,%s&count=40&start=1' % (self.hidecinema_date)
        else:
            self.mostpopular_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&sort=moviemeter,asc&count=40&start=1'
            self.mostvoted_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=num_votes,desc&count=40&start=1'
            self.featured_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=moviemeter,asc&count=40&start=1'
            self.genre_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&genres=%s&sort=moviemeter,asc&count=40&start=1'
            self.language_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=40&start=1'
            self.certification_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=%s&sort=moviemeter,asc&count=40&start=1'
            self.imdbboxoffice_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&count=40&start=1'

        self.added_link  = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&languages=en&num_votes=500,&production_status=released&release_date=%s,%s&sort=release_date,desc&count=20&start=1' % (self.year_date, self.today_date)
        self.imdblists_link = 'http://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'http://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=movie,short,tvMovie,tvSpecial,video&start=1'
        self.imdblist2_link = 'http://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=movie,short,tvMovie,tvSpecial,video&start=1'
        self.imdbwatchlist_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user
        self.keymovie_link = 'https://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,%s&keywords=%s&sort=moviemeter,asc&count=40&start=1' % (self.hidecinema_date, '%s')

        self.search_link = 'http://api.trakt.tv/search/movie?limit=20&page=1&query='
        self.top2_link = 'https://www.imdb.com/search/title?groups=top_250'
        self.G_link = 'https://www.imdb.com/search/title/?certificates=US%3AG'
        self.pg13_link = 'https://www.imdb.com/search/title/?certificates=US%3APG-13'
        self.PG1_link = 'https://www.imdb.com/search/title/?certificates=US%3APG'
        self.R_link = 'https://www.imdb.com/search/title/?certificates=US%3AR'
        self.N17_link = 'https://www.imdb.com/search/title/?certificates=US%3ANC-17'
        self.top3_link = 'https://www.imdb.com/search/title?title_type=feature&groups=top_100'
        self.top4_link = 'https://www.imdb.com/search/title?title_type=feature&groups=top_1000'
        self.bestd_link = 'https://www.imdb.com/search/title?title_type=feature&groups=best_director_winner&sort=user_rating,desc'
        self.nfb_link = 'https://www.imdb.com/search/title?title_type=feature&groups=national_film_preservation_board_winner&sort=user_rating,desc'
        self.para_link = 'https://www.imdb.com/search/title?title_type=feature&companies=paramount'
        self.mgm_link = 'https://www.imdb.com/search/title?title_type=feature&companies=mgm'
        self.warb_link = 'https://www.imdb.com/search/title?title_type=feature&companies=warner'
        self.disney1_link = 'https://www.imdb.com/search/title?user_rating=1.0,10.0&companies=disney'
        self.fammov_link = 'https://www.imdb.com/search/title/?title_type=feature&genres=family'
        self.dream_link = 'https://www.imdb.com/search/title?title_type=feature&companies=dreamworks'
        self.fox_link = 'https://www.imdb.com/search/title?title_type=feature&companies=fox'
        self.sony_link = 'https://www.imdb.com/search/title?title_type=feature&companies=sony'
        self.soon_link = 'https://www.imdb.com/movies-coming-soon/?ref_=nv_mv_cs'
        self.stan_link = 'https://www.imdb.com/list/ls040024780/'
        self.uni_link = 'https://www.imdb.com/search/title?title_type=feature&companies=universal'
        self.primev_link = 'https://www.imdb.com/search/title?title_type=feature&online_availability=US%2Ftoday%2FAmazon%2Fsubs'
        self.classmov_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31'
        self.classfant_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=fantasy'
        self.classhor_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=horror'
        self.classsci_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=sci_fi'
        self.classani_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=animation'
        self.classwar_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=war'
        self.classwest_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1900-01-01,1993-12-31&genres=western'
        self.eighties_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1980-01-01,1989-12-31'
        self.nineties_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=1990-01-01,1999-12-31'
        self.noughties_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=2000-01-01,2010-12-31'
        self.twentyten_link = 'https://www.imdb.com/search/title?title_type=feature&release_date=2010-01-01,2019-12-31'
        self.traktlist_link = 'http://api.trakt.tv/users/%s/lists/%s/items'
        self.traktlists_link = 'http://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'http://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktcollection_link = 'http://api.trakt.tv/users/me/collection/movies'
        self.traktwatchlist_link = 'http://api.trakt.tv/users/me/watchlist/movies'
        self.trakthistory_link = 'http://api.trakt.tv/users/me/history/movies?limit=%d&page=1' % self.count
        self.traktunfinished_link = 'http://api.trakt.tv/sync/playback/movies'

        self.traktanticipated_link = 'http://api.trakt.tv/movies/anticipated?limit=%d&page=1' % self.count
        self.traktrecommendations_link = 'http://api.trakt.tv/recommendations/movies?limit=%d' % self.count
        self.trakttrending_link = 'http://api.trakt.tv/movies/trending?limit=40&page=1'
        self.traktboxoffice_link = 'http://api.trakt.tv/movies/boxoffice?limit=40&page=1'
        self.traktpopular_link = 'http://api.trakt.tv/movies/popular?limit=40&page=1'


    def get(self, url, idx=True):
        try:
            try: url = getattr(self, url + '_link')
            except: pass

            try: u = urlparse.urlparse(url).netloc.lower()
            except: pass

            self.list = []
            if u in self.trakt_link and '/users/' in url:
                try:
                    if url == self.trakthistory_link: raise Exception()
                    if not '/users/me/' in url: raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user): raise Exception()
                    self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)
                except:
                    self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)

                # if '/users/me/' in url and '/collection/' in url:
                # self.list = sorted(self.list, key=lambda k: utils.title_key(k['title']))
                self.sort()
                if idx is True: self.worker()

            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx is True: self.worker(level=0)

            elif self.traktunfinished_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx is True: self.worker(level=0)

            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx is True: self.worker()

            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 3, url)
                self.sort()
                if idx is True: self.worker()

            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 96, url)
                if idx == True: self.worker()

            if self.list is None: self.list = []

            if idx is True: self.movieDirectory(self.list)
            return self.list
        except:
            try:
                invalid = (self.list is None or len(self.list) == 0)
            except:
                invalid = True
            if invalid:
                control.idle()
                if self.notifications: control.notification(title = 32001, message = 33049, icon = 'INFO')


    def getTMDb(self, url, idx=True):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass

            try:
                u = urlparse.urlparse(url).netloc.lower()
            except:
                pass

            if u in self.tmdb_link and ('/user/' in url or '/list/' in url):
                from resources.lib.indexers import tmdb
                self.list = cache.get(tmdb.Movies().tmdb_collections_list, 24, url)

            elif u in self.tmdb_link and not ('/user/' in url or '/list/' in url):
                from resources.lib.indexers import tmdb
                self.list = cache.get(tmdb.Movies().tmdb_list, 168, url)

            if self.list is None: 
                self.list = []
                raise Exception()
            if idx is True:
                self.movieDirectory(self.list)
            return self.list
        except:
            try:
                invalid = self.list is None or len(self.list) == 0
            except:
                invalid = True
            if invalid:
                control.idle()
                if self.notifications: control.notification(title = 32001, message = 33049, icon = 'INFO')


    def newMovies(self):
        setting = control.setting('newmovies.widget')
        if setting == '2':
            self.get(self.trakttrending_link)
        elif setting == '3':
            self.get(self.mostpopular_link)
        elif setting == '4':
            self.get(self.theaters_link)
        elif setting == '5':
            self.get(self.added_link)
        else:
            self.get(self.featured_link)


    def sort(self):
        try:
            attribute = int(control.setting('sort.movies.type'))
            reverse = int(control.setting('sort.movies.order')) == 1
            if attribute == 0: reverse = False
            if attribute > 0:
                if attribute == 1:
                    try:
                        self.list = sorted(self.list, key = lambda k: re.sub('(^the |^a |^an )', '', k['title'].lower()), reverse = reverse)
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
        navigator.Navigator().addDirectoryItem(32603, 'movieSearchnew', 'search.png', 'DefaultMovies.png')
        try:
            from sqlite3 import dbapi2 as database
        except:
            from pysqlite2 import dbapi2 as database
        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS movies (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
        except:
            pass
        dbcur.execute("SELECT * FROM movies ORDER BY ID DESC")
        lst = []
        delete_option = False
        for (id, term) in dbcur.fetchall():
            if term not in str(lst):
                delete_option = True
                navigator.Navigator().addDirectoryItem(term, 'movieSearchterm&name=%s' % term, 'search.png', 'DefaultMovies.png')
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
        dbcur.execute("INSERT INTO movies VALUES (?,?)", (None, q))
        dbcon.commit()
        dbcur.close()
        url = self.search_link + urllib.quote_plus(q)
        self.get(url)


    def search_term(self, name):
        url = self.search_link + urllib.quote_plus(name)
        self.get(url)


    def person(self):
        t = control.lang(32010).encode('utf-8')
        k = control.keyboard('', t) ; k.doModal()
        q = k.getText().strip() if k.isConfirmed() else None
        if not q: return
        url = self.persons_link + urllib.quote_plus(q)
        self.persons(url)


    def genres(self):
        genres = [
            ('Action', 'action', True), ('Adventure', 'adventure', True), ('Animation', 'animation', True),
            ('Biography', 'biography', True), ('Comedy', 'comedy', True), ('Crime', 'crime', True),
            ('Documentary', 'documentary', True), ('Drama', 'drama', True), ('Family', 'family', True),
            ('Fantasy', 'fantasy', True), ('Film-Noir', 'film-noir', True), ('History', 'history', True),
            ('Horror', 'horror', True), ('Music ', 'music', True), ('Musical', 'musical', True),
            ('Mystery', 'mystery', True), ('Romance', 'romance', True), ('Science Fiction', 'sci-fi', True),
            ('Sport', 'sport', True), ('Thriller', 'thriller', True), ('War', 'war', True),
            ('Western', 'western', True)
        ]
        for i in genres:
            self.list.append({'name': cleangenre.lang(i[0], self.lang), 'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1], 'image': 'genres.png', 'action': 'movies' })
        self.addDirectory(self.list)
        return self.list



    def keymovie(self):
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
            self.list.append({'name': cleangenre.lang(i[0], self.lang), 'url': self.keymovie_link % i[1] if i[2] else self.keyword_link % i[1], 'image': 'genres.png', 'action': 'movies' })
        self.addDirectory(self.list)
        return self.list

    def languages(self):
        languages = [('Arabic', 'ar'), ('Bosnian', 'bs'), ('Bulgarian', 'bg'), ('Chinese', 'zh'), ('Croatian', 'hr'), ('Dutch', 'nl'),
            ('English', 'en'), ('Finnish', 'fi'), ('French', 'fr'), ('German', 'de'), ('Greek', 'el'),('Hebrew', 'he'), ('Hindi ', 'hi'),
            ('Hungarian', 'hu'), ('Icelandic', 'is'), ('Italian', 'it'), ('Japanese', 'ja'), ('Korean', 'ko'), ('Macedonian', 'mk'),
            ('Norwegian', 'no'), ('Persian', 'fa'), ('Polish', 'pl'), ('Portuguese', 'pt'), ('Punjabi', 'pa'), ('Romanian', 'ro'),
            ('Russian', 'ru'), ('Serbian', 'sr'), ('Slovenian', 'sl'), ('Spanish', 'es'), ('Swedish', 'sv'), ('Turkish', 'tr'), ('Ukrainian', 'uk')]
        for i in languages:
            self.list.append({'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'languages.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def certifications(self):
        certificates = [
            ('General Audience (G)', 'G'),
            ('Parental Guidance (PG)', 'PG'),
            ('Parental Caution (PG-13)', 'PG-13'),
            ('Parental Restriction (R)', 'R'),
            ('Mature Audience (NC-17)', 'NC-17')
        ]
        for i in certificates: self.list.append({'name': str(i[0]), 'url': self.certification_link % self.certificatesFormat(i[1]), 'image': 'certificates.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def certificatesFormat(self, certificates):
        base = 'US%3A'
        if not isinstance(certificates, (tuple, list)): certificates = [certificates]
        return ','.join([base + i.upper() for i in certificates])


    def years(self):
        year = (self.datetime.strftime('%Y'))
        for i in range(int(year)-0, 1900, -1): self.list.append({'name': str(i), 'url': self.year_link % (str(i), str(i)), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def persons(self, url):
        if url is None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        if len(self.list) == 0:
            interface.Loader.hide()
            control.notification(title = 32010, message = 33049, icon = 'INFO')

        for i in range(0, len(self.list)): self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def userlists(self):
        userlists = []
        try:
            if trakt.getTraktCredentialsInfo() is False:
                raise Exception()
            activity = trakt.getActivity()
        except:
            pass

        try:
            if trakt.getTraktCredentialsInfo() is False:
                raise Exception()
            self.list = []
            lists = []

            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user):
                    raise Exception()
                lists += cache.get(self.trakt_user_list, 3, self.traktlists_link, self.trakt_user)
            except:
                lists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)

            for i in range(len(lists)):
                lists[i].update({'image': 'trakt.png'})
            userlists += lists
        except:
            pass

        try:
            if self.imdb_user == '':
                raise Exception()
            self.list = []
            lists = cache.get(self.imdb_user_list, 0, self.imdblists_link)
            for i in range(len(lists)):
                lists[i].update({'image': 'imdb.png'})
            userlists += lists
        except:
            pass

        try:
            if trakt.getTraktCredentialsInfo() is False:
                raise Exception()
            self.list = []
            lists = []

            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user):
                    raise Exception()
                lists += cache.get(self.trakt_user_list, 3, self.traktlikedlists_link, self.trakt_user)
            except:
                lists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)

            for i in range(len(lists)):
                lists[i].update({'image': 'trakt.png'})
            userlists += lists
        except:
            pass

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

        for i in range(0, len(self.list)): self.list[i].update({'action': 'movies'})

        # Watchlist
        if trakt.getTraktCredentialsInfo():
            self.list.insert(0, {'name': control.lang(32033).encode('utf-8'), 'url' : self.traktwatchlist_link, 'image': 'trakt.png', 'action': 'movies'})

        self.addDirectory(self.list, queue=True)
        return self.list


    def trakt_list(self, url, user):
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            result = trakt.getTraktAsJson(u)
            items = []

            for i in result:
                try:
                    movie = i['movie']
                    try:
                        movie['progress'] = max(0, min(1, i['progress'] / 100.0))
                    except:
                        pass
                    items.append(movie)
                except:
                    pass
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
                title = client.replaceHTMLCodes(title)
                # title = title.encode('utf-8')

                year = item['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                try:
                    if int(year) > int((self.datetime).strftime('%Y')): continue
                except: pass

                try:
                    progress = item['progress']
                except:
                    progress = None

                try:
                    imdb = item['ids']['imdb']
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                    imdb = imdb.encode('utf-8')
                except:
                    imdb = '0'

                tmdb = str(item.get('ids', {}).get('tmdb', 0))

                try:
                    premiered = item['released']
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                    premiered = premiered.encode('utf-8')
                except:
                    premiered = '0'

                try:
                    genre = item['genres']
                    genre = [i.title() for i in genre]
                    genre = ' / '.join(genre)
                    genre = genre.encode('utf-8')
                except: genre = 'NA'

                try:
                    duration = str(item['runtime'])
                    duration = duration.encode('utf-8')
                except: duration = '0'

                try:
                    rating = str(item['rating'])
                    rating = rating.encode('utf-8')
                except: rating = '0'

                try:
                    votes = str(item['votes'])
                    votes = str(format(int(votes),',d'))
                    votes = votes.encode('utf-8')
                except: votes = '0'

                try:
                    mpaa = item['certification']
                    mpaa = mpaa.encode('utf-8')
                except: mpaa = '0'

                try:
                    plot = item['overview'].encode('utf-8')
                    plot = client.replaceHTMLCodes(plot)
                    plot = plot.encode('utf-8')
                except: plot = '0'

                try:
                    tagline = item['tagline']
                    tagline = client.replaceHTMLCodes(tagline)
                except: tagline = '0'

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'genre': genre, 'duration': duration,
                                            'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot, 'tagline': tagline, 'imdb': imdb, 'tmdb': tmdb,
                                            'tvdb': '0', 'poster': '0', 'fanart': '0', 'next': next, 'progress': progress})
            except:
                pass
        return self.list


    def trakt_user_list(self, url, user):
        try:
#            items = trakt.getTraktAsJson(url)
            result = trakt.getTrakt(url)
            items = json.loads(result)

        except:
            pass
        for item in items:
            try:
                try: name = item['list']['name']
                except: name = item['name']
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
        list = []
        try:
            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))

            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url), 'meta', ret='content', attrs = {'property': 'pageId'})[0]
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
            # HTML syntax error, " directly followed by attribute name. Insert space in between. parseDOM can otherwise not handle it.
            result = result.replace('"class="lister-page-next', '" class="lister-page-next')

#            next = client.parseDOM(result, 'a', ret='href', attrs = {'class': '.+?ister-page-nex.+?'})
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
                year = re.findall('(\d{4})', year[0])[0]
                year = year.encode('utf-8')

                try: show = '–'.decode('utf-8') in str(year).decode('utf-8') or '-'.decode('utf-8') in str(year).decode('utf-8')
                except: show = False
                if show: raise Exception() # Some lists contain TV shows.

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                try: mpaa = client.parseDOM(item, 'span', attrs = {'class': 'certificate'})[0]
                except: mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = imdb.encode('utf-8')

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
                if rating == '0':
                    try:
                        rating = client.parseDOM(item, 'span', attrs = {'class': 'ipl-rating-star__rating'})[0]
                        if rating == '' or rating == '-': rating = '0'
                    except: pass
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

                try: director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', item)[0]
                except: director = '0'
                director = client.parseDOM(director, 'a')
                director = ' / '.join(director)
                if director == '': director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try: cast = re.findall('Stars(?:s|):(.+?)(?:\||</div>)', item)[0]
                except: cast = '0'
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
                if plot == '0':
                    try:
                        plot = client.parseDOM(item, 'div', attrs = {'class': 'lister-item-content'})[0]
                        plot = re.sub('<p\s*class="">', '<p class="plot_">', plot)
                        plot = client.parseDOM(plot, 'p', attrs = {'class': 'plot_'})[0]
                        plot = re.sub('<.+?>|</.+?>', '', plot)
                        if plot == '': plot = '0'
                    except: pass
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                list.append({'title': title, 'originaltitle': title, 'year': year, 'genre': genre, 'duration': duration, 'rating': rating,
                                            'votes': votes, 'mpaa': mpaa, 'director': director, 'cast': cast, 'plot': plot, 'imdb': imdb,
                                            'tmdb': '0', 'tvdb': '0', 'poster': poster, 'next': next})
            except:
                pass

        return list


    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            result = result.decode('iso-8859-1').encode('utf-8')
#            items = client.parseDOM(result, 'div', attrs = {'class': '.+?etail'})
            items = client.parseDOM(result, 'div', attrs = {'class': '.+? lister-item'}) + client.parseDOM(result, 'div', attrs = {'class': 'lister-item .+?'})
        except:
            import traceback
            traceback.print_exc()
            pass


        for item in items:
            try:
                name = client.parseDOM(item, 'a')[1]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = client.parseDOM(item, 'img', ret='src')[0]
                # if not ('._SX' in image or '._SY' in image): raise Exception()
                image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list


    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            result = result.decode('iso-8859-1').encode('utf-8')
            items = client.parseDOM(result, 'li', attrs = {'class': 'ipl-zebra-list__item user-list'})
#            items = client.parseDOM(result, 'div', attrs = {'class': 'list_name'})
        except:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

#        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a |^an )', '', k['name'].lower()))
        return self.list


    def worker(self, level=1):
        if self.list is None or self.list == []:
            return
        self.meta = []
        total = len(self.list)

        for i in range(0, total):
            self.list[i].update({'metacache': False})

        self.list = metacache.fetch(self.list, self.lang, self.user)

        for r in range(0, total, 40):
            threads = []
            for i in range(r, r + 40):
                if i <= total:
                    threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            if self.meta:
                metacache.insert(self.meta)

        self.list = [i for i in self.list if not i['imdb'] == '0']


    def metadataRetrieve(self, imdb, tmdb):
        self.list = [{'imdb': imdb, 'tmdb': tmdb}]
        self.worker()
        return self.list[0]


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] is True:
                raise Exception()

            imdb = self.list[i]['imdb']

            item = trakt.getMovieSummary(id=imdb)

            title = item.get('title')
            title = client.replaceHTMLCodes(title)

            originaltitle = title

            year = item.get('year', 0)
            year = re.sub('[^0-9]', '', str(year))

            # imdb = item.get('ids', {}).get('imdb', '0')
            # imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

            tmdb = str(item.get('ids', {}).get('tmdb', 0))

            premiered = item.get('released', '0')
            try:
                premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except:
                premiered = '0'

            genre = item.get('genres', [])
            genre = [x.title() for x in genre]
            genre = ' / '.join(genre).strip()
            if not genre:
                genre = 'NA'

            duration = str(item.get('runtime', 0))

            rating = item.get('rating', '0')
            if not rating or rating == '0.0':
                rating = '0'

            votes = item.get('votes', '0')
            try:
                votes = str(format(int(votes), ',d'))
            except:
                pass

            mpaa = item.get('certification', '0')
            if not mpaa:
                mpaa = '0'

            tagline = item.get('tagline', '0')

            plot = item.get('overview', '0')

            people = trakt.getPeople(imdb, 'movies')

            director = writer = ''
            if 'crew' in people and 'directing' in people['crew']:
                director = ', '.join([director['person']['name'] for director in people['crew']['directing'] if director['job'].lower() == 'director'])
            if 'crew' in people and 'writing' in people['crew']:
                writer = ', '.join([writer['person']['name'] for writer in people['crew']['writing'] if writer['job'].lower() in ['writer', 'screenplay', 'author']])

            cast = []
            for person in people.get('cast', []):
                cast.append({'name': person['person']['name'], 'role': person['character']})
            cast = [(person['name'], person['role']) for person in cast]

            try:
                if self.lang == 'en' or self.lang not in item.get('available_translations', [self.lang]):
                    raise Exception()
                trans_item = trakt.getMovieTranslation(imdb, self.lang, full = True)

                title = trans_item.get('title') or title
                tagline = trans_item.get('tagline') or tagline
                plot = trans_item.get('overview') or plot
            except:
                pass

            item = {'title': title, 'originaltitle': originaltitle, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'premiered': premiered,
                        'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director,
                        'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline, 'poster': '0', 'poster2': '0', 'poster3': '0',
                        'banner': '0', 'fanart': '0', 'fanart2': '0', 'fanart3': '0', 'clearlogo': '0', 'clearart': '0', 'landscape': '0',
                        'metacache': False}

            meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.lang, 'user': self.user, 'item': item}

            # fanart_thread = threading.Thread
            from resources.lib.indexers import fanarttv
            fanarttv_art = fanarttv.get_movie_art(imdb)

            if not fanarttv_art is None:
                item.update(fanarttv_art)
                meta.update(item)

            if item.get('poster2') == '0' or item.get('fanart2') == '0':
                try:
                    from resources.lib.indexers.tmdb import Movies
                    tmdb_art = Movies().tmdb_art(tmdb)
                except:
                    import traceback
                    traceback.print_exc()
                item.update(tmdb_art)
                meta.update(item)

            item = dict((k,v) for k, v in item.iteritems() if not v == '0')
            self.list[i].update(item)

            self.meta.append(meta)
        except:
            pass


    def movieDirectory(self, items):
        if items is None or len(items) == 0:
            control.idle()
            control.notification(title = 32001, message = 33049, icon = 'INFO')
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'

        if control.setting('hosts.mode') == '2':
            playbackMenu = control.lang(32063).encode('utf-8')
        else:
            playbackMenu = control.lang(32064).encode('utf-8')

        if trakt.getTraktIndicatorsInfo() is True:
            watchedMenu = control.lang(32068).encode('utf-8')
            unwatchedMenu = control.lang(32069).encode('utf-8')
        else:
            watchedMenu = control.lang(32066).encode('utf-8')
            unwatchedMenu = control.lang(32067).encode('utf-8')

        playlistManagerMenu = control.lang(35522).encode('utf-8')
        queueMenu = control.lang(32065).encode('utf-8')
        traktManagerMenu = control.lang(32070).encode('utf-8')
        nextMenu = control.lang(32053).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                imdb, tmdb, year = i['imdb'], i['tmdb'], i['year']
                try:
                    title = i['originaltitle']
                except:
                    title = i['title']

                label = '%s (%s)' % (i['title'], i['year'])

                try:
                    labelProgress = label + ' [' + str(int(i['progress'] * 100)) + '%]'
                except:
                    labelProgress = label

                sysname = urllib.quote_plus(label)
                systitle = urllib.quote_plus(title)

                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tmdb_id': tmdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, sysname)})

                # Some descriptions have a link at the end that. Remove it.
                try:
                    plot = meta['plot']
                    index = plot.rfind('See full summary')
                    if index >= 0:
                        plot = plot[:index]
                    plot = plot.strip()
                    if re.match('[a-zA-Z\d]$', plot):
                        plot += ' ...'
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
                try:
                    meta.update({'year': int(meta['year'])})
                except:
                    pass

                poster = [i[x] for x in ['poster3', 'poster', 'poster2'] if i.get(x, '0') != '0']
                poster = poster[0] if poster else addonPoster
                meta.update({'poster': poster})

                icon = '0'
                if icon == '0' and 'icon' in i: icon = i['icon']

                thumb = '0'
                if thumb == '0' and 'thumb' in i: thumb = i['thumb']

                banner = '0'
                if banner == '0' and 'banner' in i: banner = i['banner']

                poster = '0'
                if poster == '0' and 'poster3' in i: poster = i['poster3']
                if poster == '0' and 'poster2' in i: poster = i['poster2']
                if poster == '0' and 'poster' in i: poster = i['poster']

                fanart = '0'
                if settingFanart:
                    if fanart == '0' and 'fanart3' in i: fanart = i['fanart3']
                    if fanart == '0' and 'fanart2' in i: fanart = i['fanart2']
                    if fanart == '0' and 'fanart' in i: fanart = i['fanart']

                clearlogo = '0'
                if clearlogo == '0' and 'clearlogo' in i:
                    clearlogo = i['clearlogo']

                clearart = '0'
                if clearart == '0' and 'clearart' in i:
                    clearart = i['clearart']

                landscape = '0'
                if landscape == '0' and 'landscape' in i:
                    landscape = i['landscape']

                discart = '0'
                if discart == '0' and 'discart' in i:
                    discart = i['discart']

                if poster == '0': poster = addonPoster
                if icon == '0': icon = poster
                if thumb == '0': thumb = poster
                if banner == '0': banner = addonBanner
                if fanart == '0': fanart = addonFanart

                art = {}
                if not icon == '0' and not icon is None:
                    art.update({'icon' : icon})
                if not thumb == '0' and not thumb is None:
                    art.update({'thumb' : thumb})
                if not banner == '0' and not banner is None:
                    art.update({'banner' : banner})
                if not poster == '0' and not poster is None:
                    art.update({'poster' : poster})
                if not fanart == '0' and not fanart is None:
                    art.update({'fanart' : fanart})
                if not clearlogo == '0' and not clearlogo is None:
                    art.update({'clearlogo' : clearlogo})
                if not clearart == '0' and not clearart is None:
                    art.update({'clearart' : clearart})
                if not landscape == '0' and not landscape is None:
                    art.update({'landscape' : landscape})
                if not discart == '0' and not discart is None:
                    art.update({'discart' : discart})

####-Context Menu and Overlays-####
                cm = []
                if traktCredentials is True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s)' % (sysaddon, sysname, imdb)))

                try:
                    indicators = playcount.getMovieIndicators()
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                        # lastplayed = trakt.watchedMoviesTime(imdb)
                        # meta.update({'lastplayed': lastplayed})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                sysmeta = urllib.quote_plus(json.dumps(meta))
                sysart = urllib.quote_plus(json.dumps(art))

                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)

                cm.append(('Find similar', 'ActivateWindow(10025,%s?action=movies&url=http://api.trakt.tv/movies/%s/related,return)' % (sysaddon, imdb)))
                cm.append((playlistManagerMenu, 'RunPlugin(%s?action=playlistManager&name=%s&url=%s&meta=%s&art=%s)' % (sysaddon, sysname, sysurl, sysmeta, sysart)))
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem&name=%s)' % (sysaddon, sysname)))
                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))
                cm.append((addToLibrary, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, sysname, systitle, year, imdb, tmdb)))
                cm.append(('[COLOR red]Still i Rise Settings[/COLOR]', 'RunPlugin(%s?action=openSettings&query=(0,0))' % sysaddon))
####################################

                item = control.item(label=labelProgress)
                if 'cast' in i:
                    item.setCast(i['cast'])
                if not fanart == '0' and not fanart is None:
                    item.setProperty('Fanart_Image', fanart)
                item.setArt(art)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='video', infoLabels=control.metadataClean(meta))
                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)
                item.addContextMenuItems(cm)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                pass

        if next:
            try:
                url = items[0]['next']
                if url == '':
                    raise Exception()

                if not self.tmdb_link in url:
                    url = '%s?action=moviePage&url=%s' % (sysaddon, urllib.quote_plus(url))

                elif self.tmdb_link in url:
                    url = '%s?action=tmdbmoviePage&url=%s' % (sysaddon, urllib.quote_plus(url))

                item = control.item(label=nextMenu)
                icon = control.addonNext()
                item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
                if not addonFanart is None:
                    item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                import traceback
                traceback.print_exc()
                pass
        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('movies', {'skin.estuary': 55, 'skin.confluence': 500})


    def addDirectory(self, items, queue=False):
        if items is None or len(items) == 0:
            control.idle()
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

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath is None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])

                try:
                    url += '&url=%s' % urllib.quote_plus(i['url'])
                except:
                    pass

                cm = []
                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=movie&url=%s)' % (sysaddon, urllib.quote_plus(i['url']))))

                if queue is True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    cm.append((addToLibrary, 'RunPlugin(%s?action=moviesToLibrary&url=%s)' % (sysaddon, urllib.quote_plus(i['context']))))
                except:
                    pass

                cm.append(('[COLOR red]Still i Rise Settings[/COLOR]', 'RunPlugin(%s?action=openSettings&query=(0,0))' % sysaddon))

                item = control.item(label = name)

                item.setArt({'icon': thumb, 'thumb': thumb, 'poster': thumb, 'banner': thumb})
                if not addonFanart is None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
