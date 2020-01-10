# -*- coding: utf-8 -*-

'''
    Bone Crusher Reborn Add-on
'''

import os, sys, xbmc

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache

try:
    sysaddon = sys.argv[0]
    syshandle = int(sys.argv[1])
except:
    sysaddon = ''
    syshandle = '1'
    pass


artPath = control.artPath()
addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True
traktCredentials = trakt.getTraktCredentialsInfo()
traktIndicators = trakt.getTraktIndicatorsInfo()


class Navigator:
    def root(self):
        self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem('swift streams', 'swiftNavigator', 'swift.png', 'DefaultTVShows.png')
        self.addDirectoryItem('docs', 'docuNavigator', 'doc.png', 'DefaultTVShows.png')

        if self.getMenuEnabled('mylists.widget') is True:
            self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png','DefaultVideoPlaylists.png')
            self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

        if not control.setting('newmovies.widget') == '0':
            indexer = 32478
            indexer_icon = 'imdb.png'
            setting = control.setting('newmovies.widget')
            if setting == '2':
                indexer = 32479
                indexer_icon = 'trakt.png'
            self.addDirectoryItem(32477 if control.setting('index.labels') == 'false' else indexer, 'newMovies', 'latest-movies.png' if control.setting('icon.logos') == 'Traditional' else indexer_icon, 'DefaultRecentlyAddedMovies.png')

        if (traktIndicators is True and not control.setting('tv.widget.alt') == '0') or (traktIndicators is False and not control.setting('tv.widget') == '0'):
            indexer = 32481
            indexer_icon = 'tvmaze.png'
            setting = control.setting('tv.widget.alt')
            if setting == '2' or setting == '3':
                indexer = 32482
                indexer_icon = 'trakt.png'
            self.addDirectoryItem(32480 if control.setting('index.labels') == 'false' else indexer, 'tvWidget', 'latest-episodes.png' if control.setting('icon.logos') == 'Traditional' else indexer_icon, 'DefaultRecentlyAddedEpisodes.png')
            self.addDirectoryItem(32483 if control.setting('index.labels') == 'false' else 32484, 'calendar&url=added', 'latest-episodes.png' if control.setting('icon.logos') == 'Traditional' else 'tvmaze.png', 'DefaultTVShows.png', queue=True)

        if not control.setting('furk.api') == '' or None:
            self.addDirectoryItem('Furk.net', 'furkNavigator', 'movies.png',  'DefaultMovies.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonService.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads is True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')
			
        if self.getMenuEnabled('navi.lists') is True:
           self.addDirectoryItem(32019, 'listNavigator', 'list.png', 'DefaultTVShows.png')
        self.endDirectory()

    def listnav(self):
        self.addDirectoryItem(32659, 'lists', 'list.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32486, 'lista', 'icon.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32487, 'listb', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32488, 'listc', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32489, 'listd', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32490, 'liste', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32491, 'listf', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32492, 'listg', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32493, 'listh', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32494, 'kidsi', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32495, 'listj', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32496, 'listk', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32497, 'listl', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32498, 'listm', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32499, 'listn', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32500, 'listo', 'list.png', 'DefaultTVShows.png')
        #self.addDirectoryItem(32504, 'listp', 'list.png', 'DefaultTVShows.png')
        self.endDirectory()

    def furk(self):
        self.addDirectoryItem('User Files', 'furkUserFiles', 'mytvnavigator.png', 'mytvnavigator.png')
        self.addDirectoryItem('Search', 'furkSearch', 'search.png', 'search.png')
        self.endDirectory()


    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'):
            return False
        return True


    def movies(self, lite=False):
        self.addDirectoryItem('omc requests movies', 'movies&url=omcmov','icon.png', 'DefaultMovies.png')
        self.addDirectoryItem('dark place movies requests', 'movies&url=dpmov','icon.png', 'DefaultMovies.png')
        self.addDirectoryItem('user requests movies', 'movies&url=usermov','icon.png', 'DefaultMovies.png')
        self.addDirectoryItem('firestick movies requests', 'movies&url=firemov', 'icon.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.movie.imdb.intheater') is True:
            self.addDirectoryItem(32420 if control.setting('index.labels') == 'false' else 32421, 'movies&url=theaters', 'in-theaters.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.movie.tmdb.nowplaying') is True:
            self.addDirectoryItem(32422 if control.setting('index.labels') == 'false' else 32423, 'tmdbmovies&url=tmdb_nowplaying', 'in-theaters.png' if control.setting('icon.logos') == 'Traditional' else 'tmdb.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.movie.trakt.anticipated') is True:
            self.addDirectoryItem(32424 if control.setting('index.labels') == 'false' else 32425, 'movies&url=traktanticipated', 'trakt.png' if control.setting('icon.logos') == 'Traditional' else 'trakt.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.movie.tmdb.upcoming') is True:
            self.addDirectoryItem(32426 if control.setting('index.labels') == 'false' else 32427, 'tmdbmovies&url=tmdb_upcoming', 'soon.png' if control.setting('icon.logos') == 'Traditional' else 'tmdb.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.movie.imdb.popular') is True:
            self.addDirectoryItem(32428 if control.setting('index.labels') == 'false' else 32429, 'movies&url=mostpopular', 'most-popular.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.movie.tmdb.popular') is True:
            self.addDirectoryItem(32430 if control.setting('index.labels') == 'false' else 32431, 'tmdbmovies&url=tmdb_popular', 'most-popular.png' if control.setting('icon.logos') == 'Traditional' else 'tmdb.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.movie.trakt.popular') is True:
            self.addDirectoryItem(32432 if control.setting('index.labels') == 'false' else 32433, 'movies&url=traktpopular', 'most-popular.png' if control.setting('icon.logos') == 'Traditional' else 'trakt.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.movie.imdb.boxoffice') is True:
            self.addDirectoryItem(32434 if control.setting('index.labels') == 'false' else 32435, 'movies&url=imdbboxoffice', 'box-office.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultMovies.png')

        if self.getMenuEnabled('navi.movie.trakt.boxoffice') is True:
            self.addDirectoryItem(32436 if control.setting('index.labels') == 'false' else 32437, 'movies&url=traktboxoffice', 'box-office.png' if control.setting('icon.logos') == 'Traditional' else 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32438 if control.setting('index.labels') == 'false' else 32439, 'movies&url=mostvoted', 'most-voted.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem(32440 if control.setting('index.labels') == 'false' else 32441, 'tmdbmovies&url=tmdb_toprated', 'rat.png' if control.setting('icon.logos') == 'Traditional' else 'tmdb.png', 'DefaultMovies.png')
        self.addDirectoryItem(32442 if control.setting('index.labels') == 'false' else 32443, 'movies&url=trakttrending', 'trakt.png' if control.setting('icon.logos') == 'Traditional' else 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32444 if control.setting('index.labels') == 'false' else 32445, 'movies&url=traktrecommendations', 'trakt.png' if control.setting('icon.logos') == 'Traditional' else 'trakt.png', 'DefaultMovies.png')
        self.addDirectoryItem(32446 if control.setting('index.labels') == 'false' else 32447, 'movies&url=featured', 'movies.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem(32451 if control.setting('index.labels') == 'false' else 32452, 'movies&url=oscars', 'imdb.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem(32453 if control.setting('index.labels') == 'false' else 32454, 'movies&url=oscarsnominees', 'imdb.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem(32455 if control.setting('index.labels') == 'false' else 32456, 'movieGenres', 'imdb.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultGenre.png')
        self.addDirectoryItem(32457 if control.setting('index.labels') == 'false' else 32458, 'movieYears', 'imdb.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultYear.png')
        self.addDirectoryItem(32459 if control.setting('index.labels') == 'false' else 32460, 'moviePersons', 'imdb.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultActor.png')
        self.addDirectoryItem(32461 if control.setting('index.labels') == 'false' else 32462, 'movieLanguages', 'imdb.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultCountry.png')
        self.addDirectoryItem(32463 if control.setting('index.labels') == 'false' else 32464, 'movieCertificates', 'imdb.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultMovies.png')
        self.addDirectoryItem('Latest Movies', 'movieWidget', 'latest-movies.png', 'DefaultMovies.png')
        if lite is False:
            if self.getMenuEnabled('mylists.widget') is True:
               self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32029, 'moviePerson', 'people-search.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultAddonsSearch.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultAddonsSearch.png')
        self.endDirectory()


    def mymovies(self, lite=False):
        self.accountCheck()
        self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultVideoPlaylists.png')

        if traktCredentials is True and imdbCredentials is True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

            if traktIndicators is True:
                self.addDirectoryItem(35308, 'movies&url=traktunfinished', 'trakt.png', 'DefaultMovies.png', queue=True)
                self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)
                self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

        elif traktCredentials is True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

            if traktIndicators is True:
                self.addDirectoryItem(35308, 'movies&url=traktunfinished', 'trakt.png', 'DefaultMovies.png', queue=True)
                self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

        elif imdbCredentials is True:
#            self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

        if lite is False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32029, 'moviePerson', 'people-search.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultAddonsSearch.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultAddonsSearch.png')
        self.endDirectory()


    def tvshows(self, lite=False):
        self.addDirectoryItem('omc requests tvshows', 'tvshows&url=omctv','icon.png', 'DefaultMovies.png')
        self.addDirectoryItem('dark place tvshows requests', 'tvshows&url=dptv','icon.png', 'DefaultMovies.png')
        self.addDirectoryItem('user requests tvshows', 'tvshows&url=usertv','icon.png', 'DefaultMovies.png')
        self.addDirectoryItem('firestick tvshows requests', 'tvshows&url=firetv', 'icon.png', 'DefaultMovies.png')
        if self.getMenuEnabled('navi.tv.imdb.popular') is True:
            self.addDirectoryItem(32428 if control.setting('index.labels') == 'false' else 32429, 'tvshows&url=popular', 'most-popular.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tv.tmdb.popular') is True:
            self.addDirectoryItem(32430 if control.setting('index.labels') == 'false' else 32431, 'tmdbTvshows&url=tmdb_popular', 'most-popular.png' if control.setting('icon.logos') == 'Traditional' else 'tmdb.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tv.trakt.popular') is True:
            self.addDirectoryItem(32432 if control.setting('index.labels') == 'false' else 32433, 'tvshows&url=traktpopular', 'most-popular.png' if control.setting('icon.logos') == 'Traditional' else 'trakt.png', 'DefaultTVShows.png', queue=True)
        if self.getMenuEnabled('navi.tv.imdb.mostvoted') is True:
            self.addDirectoryItem(32438 if control.setting('index.labels') == 'false' else 32439, 'tvshows&url=views', 'imdb.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultTVShows.png')
        if self.getMenuEnabled('navi.tv.tmdb.toprated') is True:
            self.addDirectoryItem(32440 if control.setting('index.labels') == 'false' else 32441, 'tmdbTvshows&url=tmdb_toprated', 'rat.png' if control.setting('icon.logos') == 'Traditional' else 'tmdb.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32442 if control.setting('index.labels') == 'false' else 32443, 'tvshows&url=trakttrending', 'trakt.png' if control.setting('icon.logos') == 'Traditional' else 'trakt.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32448 if control.setting('index.labels') == 'false' else 32449, 'tvshows&url=rating', 'highly-rated.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32444 if control.setting('index.labels') == 'false' else 32445, 'tvshows&url=traktrecommendations', 'trakt.png' if control.setting('icon.logos') == 'Traditional' else 'trakt.png', 'DefaultTVShows.png', queue=True)
        self.addDirectoryItem(32455 if control.setting('index.labels') == 'false' else 32456, 'tvGenres', 'genres.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultGenre.png')
        self.addDirectoryItem(32469 if control.setting('index.labels') == 'false' else 32470, 'tvNetworks', 'networks.png' if control.setting('icon.logos') == 'Traditional' else 'tvmaze.png', 'DefaultNetwork.png')
        self.addDirectoryItem(32461 if control.setting('index.labels') == 'false' else 32462, 'tvLanguages', 'languages.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultCountry.png')
        self.addDirectoryItem(32463 if control.setting('index.labels') == 'false' else 32464, 'tvCertificates', 'certificates.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32468, 'calendar&url=onDeck', 'trakt.png', 'DefaultYear.png')
        self.addDirectoryItem(32465 if control.setting('index.labels') == 'false' else 32467, 'tmdbTvshows&url=tmdb_airingtoday', 'airing-today.png' if control.setting('icon.logos') == 'Traditional' else 'tmdb.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32465 if control.setting('index.labels') == 'false' else 32466, 'tvshows&url=airing', 'airing-today.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32471 if control.setting('index.labels') == 'false' else 32472, 'tmdbTvshows&url=tmdb_ontheair', 'new-tvshows.png' if control.setting('icon.logos') == 'Traditional' else 'tmdb.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32473 if control.setting('index.labels') == 'false' else 32474, 'tvshows&url=active', 'returning-tvshows.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32475 if control.setting('index.labels') == 'false' else 32476, 'tvshows&url=premiere', 'new-tvshows.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32027 if control.setting('index.labels') == 'false' else 32450, 'calendars', 'calendar.png' if control.setting('icon.logos') == 'Traditional' else 'tvmaze.png', 'DefaultYear.png')

        if (traktIndicators is True and not control.setting('tv.widget.alt') == '0') or (traktIndicators is False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem(32006, 'tvWidget', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png')

        if lite is False:
            if self.getMenuEnabled('mylists.widget') is True:
               self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultTVShows.png')

            self.addDirectoryItem(32030, 'tvPerson', 'people-search.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultAddonsSearch.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultAddonsSearch.png')
        self.endDirectory()


    def mytvshows(self, lite=False):
        self.accountCheck()
        self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultVideoPlaylists.png')
        if traktCredentials is True and imdbCredentials is True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32041, 'episodesUserlists', 'userlists.png', 'DefaultVideoPlaylists.png')

            if traktIndicators is True:
                self.addDirectoryItem(35308, 'episodesUnfinished', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32027, 'calendar&url=mycalendar', 'trakt.png', 'DefaultYear.png', queue=True)
#                self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')  #sorts alphabetical
                self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')  # sorts by date added

        elif traktCredentials is True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32041, 'episodesUserlists', 'trakt.png', 'DefaultTVShows.png')

            if traktIndicators is True:
                self.addDirectoryItem(35308, 'episodesUnfinished', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultTVShows.png.png', queue=True)
                self.addDirectoryItem(32027, 'calendar&url=mycalendar', 'trakt.png', 'DefaultYear.png', queue=True)

        elif imdbCredentials is True:
#            self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')    #sorts alphabetical
            self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')  # sorts by date added

        if lite is False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32030, 'tvPerson', 'people-search.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultAddonsSearch.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png' if control.setting('icon.logos') == 'Traditional' else 'imdb.png', 'DefaultAddonsSearch.png')
        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32510, 'cfNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32609, 'resolveurl', 'resolveurl.png', 'DefaultAddonProgram.png')
        #-- Providers - 4
        self.addDirectoryItem(32651, 'openscrapersSettings&query=0.0', 'openscrapers.png', 'DefaultAddonProgram.png')
        #-- General - 0
        self.addDirectoryItem(32043, 'openSettings&query=0.1', 'tools.png', 'DefaultAddonProgram.png')
        #-- Navigation - 1
        self.addDirectoryItem(32362, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        #-- Playback - 3
        self.addDirectoryItem(32045, 'openSettings&query=3.0', 'tools.png', 'DefaultAddonProgram.png')
        #-- Api-keys - 8
        self.addDirectoryItem(32044, 'openSettings&query=8.0', 'tools.png', 'DefaultAddonProgram.png')
        #-- Downloads - 10
        self.addDirectoryItem(32048, 'openSettings&query=10.0', 'tools.png', 'DefaultAddonProgram.png')
        #-- Subtitles - 11
        self.addDirectoryItem(32046, 'openSettings&query=11.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32361, 'resetViewTypes', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt&opensettings=false', 'trakt.png', 'DefaultAddonProgram.png')
        self.endDirectory()


    def cf(self):
        self.addDirectoryItem(32610, 'clearAllCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32611, 'clearSources&opensettings=false', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32612, 'clearMetaCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32613, 'clearCache', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32614, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32615, 'clearBookmarks', 'tools.png', 'DefaultAddonProgram.png')
        self.endDirectory()


    def library(self):
#-- Library - 9
        self.addDirectoryItem(32557, 'openSettings&query=9.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonLibrary.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'movies.png', 'DefaultMovies.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)
        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')
        self.endDirectory()


    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')
        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)
        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultAddonsSearch.png')
        self.addDirectoryItem(32030, 'tvPerson', 'people-search.png', 'DefaultAddonsSearch.png')
        self.endDirectory()


    def views(self):
        try:
            control.idle()
            items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'),
                            (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]

            select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

            if select == -1:
                return

            content = items[select][1]
            title = control.lang(32059).encode('utf-8')
            url = '%s?action=addView&content=%s' % (sys.argv[0], content)
            poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()
            item = control.item(label=title)
            item.setInfo(type='video', infoLabels = {'title': title})
            item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
            item.setProperty('Fanart_Image', fanart)
            control.addItem(handle = int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            control.content(int(sys.argv[1]), content)
            control.directory(int(sys.argv[1]), cacheToDisc=True)
            from resources.lib.modules import views
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials is False and imdbCredentials is False:
            control.idle()
            control.notification(title='default', message=32042, icon='WARNING', sound=True)
            sys.exit()


    def infoCheck(self, version):
        try:
            control.notification(title='default', message=32074, icon='WARNING',  time=5000, sound=True)
            return '1'
        except:
            return '1'


    def clearCacheAll(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')

        if not yes:
            return

        try:
            from resources.lib.modules import cache
            cache.cache_clear_all()
            control.notification(title='default', message='All Cache Successfully Cleared!', icon='default', sound=True)
        except:
            import traceback
            traceback.print_exc()
            pass


    def clearCacheProviders(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')

        if not yes:
            return

        try:
            from resources.lib.modules import cache
            cache.cache_clear_providers()
            control.notification(title='default', message='Provider Cache Successfully Cleared!', icon='default', sound=True)
        except:
            import traceback
            traceback.print_exc()
            pass


    def clearCacheMeta(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')

        if not yes:
            return

        try:
            from resources.lib.modules import cache
            cache.cache_clear_meta()
            control.notification(title = 'default', message = 'Metadata Cache Successfully Cleared!', icon = 'default', sound = True)
        except:
            import traceback
            traceback.print_exc()
            pass


    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')

        if not yes:
            return

        try:
            from resources.lib.modules import cache
            cache.cache_clear()
            control.notification(title = 'default', message = 'Cache Successfully Cleared!', icon = 'default', sound = True)
        except:
            import traceback
            traceback.print_exc()
            pass


    def clearCacheSearch(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')

        if not yes:
            return

        try:
            from resources.lib.modules import cache
            cache.cache_clear_search()
            control.notification(title = 'default', message = 'Search History Successfully Cleared!', icon = 'default', sound = True)
        except:
            import traceback
            traceback.print_exc()
            pass


    def clearBookmarks(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')

        if not yes:
            return

        try:
            from resources.lib.modules import cache
            cache.cache_clear_bookmarks()
            control.notification(title = 'default', message = 'Bookmarks Successfully Cleared!', icon = 'default', sound = True)
        except:
            import traceback
            traceback.print_exc()
            pass


    def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True, isPlayable=False):
        try:
            if type(name) is str or type(name) is unicode:
                name = str(name)
            if type(name) is int:
                name = control.lang(name).encode('utf-8')
        except:
            import traceback
            traceback.print_exc()

        url = '%s?action=%s' % (sysaddon, query) if isAction else query

        thumb = os.path.join(artPath, thumb) if not artPath is None else icon

        if not icon.startswith('Default'):
             icon = os.path.join(artPath, icon)

        cm = []
        queueMenu = control.lang(32065).encode('utf-8')

        if queue is True:
            cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

        if not context is None:
            cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))

        cm.append(('[COLOR red]Bone Crusher Reborn Settings[/COLOR]', 'RunPlugin(%s?action=openSettings&query=0.0)' % sysaddon))

        item = control.item(label=name)
        item.addContextMenuItems(cm)

        if isPlayable:
            item.setProperty('IsPlayable', 'true')
        else:
            item.setProperty('IsPlayable', 'false')

        item.setArt({'icon': icon, 'poster': thumb, 'thumb': thumb})

        if not addonFanart is None:
            item.setProperty('Fanart_Image', addonFanart)

        control.addItem(handle=syshandle, url=url, listitem=item, isFolder= isFolder)


    def endDirectory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
        control.sleep(200)