# -*- coding: utf-8 -*-

'''
    plexOdus Add-on
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
        self.addDirectoryItem(32001, 'movieNavigator', 'icon.png', 'icon.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'icon.png', 'icon.png')
        #self.addDirectoryItem('lists', 'listNavigator', 'icon.png', 'icon.png')

        self.addDirectoryItem("plex", 'plexNavigator', 'icon.png', 'icon.png')
        if self.getMenuEnabled('mylists.widget') is True:
            self.addDirectoryItem(32003, 'mymovieNavigator', 'icon.png','icon.png')
            self.addDirectoryItem(32004, 'mytvNavigator', 'icon.png', 'icon.png')

        if not control.setting('newmovies.widget') == '0':
            indexer = 32478
            indexer_icon = 'icon.png'
            setting = control.setting('newmovies.widget')
            if setting == '2':
                indexer = 32479
                indexer_icon = 'icon.png'
            self.addDirectoryItem(32477 if control.setting('index.labels') == 'false' else indexer, 'newMovies', 'icon.png' if control.setting('icon.logos') == 'Traditional' else indexer_icon, 'icon.png')

        if (traktIndicators is True and not control.setting('tv.widget.alt') == '0') or (traktIndicators is False and not control.setting('tv.widget') == '0'):
            indexer = 32481
            indexer_icon = 'icon.png'
            setting = control.setting('tv.widget.alt')
            if setting == '2' or setting == '3':
                indexer = 32482
                indexer_icon = 'icon.png'
            self.addDirectoryItem(32480 if control.setting('index.labels') == 'false' else indexer, 'tvWidget', 'icon.png' if control.setting('icon.logos') == 'Traditional' else indexer_icon, 'icon.png')
            self.addDirectoryItem(32483 if control.setting('index.labels') == 'false' else 32484, 'calendar&url=added', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png', queue=True)
        #if self.getMenuEnabled('navi.lists') is True:
           #self.addDirectoryItem(32485, 'listNavigator', 'list.png', 'icon.png')
        if not control.setting('furk.api') == '' or None:
            self.addDirectoryItem('Furk.net', 'furkNavigator', 'icon.png',  'icon.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'icon.png', 'icon.png')
        self.addDirectoryItem(32008, 'toolNavigator', 'icon.png', 'DefaultAddonService.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads is True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.endDirectory()

    #def listnav(self):
        #self.addDirectoryItem(32485, 'lists', 'list.png', 'icon.png')
        #self.addDirectoryItem(32486, 'lista', 'list.png', 'icon.png')
        #self.addDirectoryItem(32487, 'listb', 'list.png', 'icon.png')
        #self.addDirectoryItem(32488, 'listc', 'list.png', 'icon.png')
        #self.addDirectoryItem(32489, 'listd', 'list.png', 'icon.png')
        #self.addDirectoryItem(32490, 'liste', 'list.png', 'icon.png')
        #self.addDirectoryItem(32491, 'listf', 'list.png', 'icon.png')
        #self.addDirectoryItem(32492, 'listg', 'list.png', 'icon.png')
        #self.addDirectoryItem(32493, 'listh', 'list.png', 'icon.png')
        #self.addDirectoryItem(32494, 'kidsi', 'list.png', 'icon.png')
        #self.addDirectoryItem(32495, 'listj', 'list.png', 'icon.png')
        #self.addDirectoryItem(32496, 'listk', 'list.png', 'icon.png')
        #self.addDirectoryItem(32497, 'listl', 'list.png', 'icon.png')
        #self.addDirectoryItem(32498, 'listm', 'list.png', 'icon.png')
        #self.addDirectoryItem(32499, 'listn', 'list.png', 'icon.png')
        #self.addDirectoryItem(32500, 'listo', 'list.png', 'icon.png')
        #self.addDirectoryItem(32504, 'listp', 'list.png', 'icon.png')
        #self.endDirectory()

    def furk(self):
        self.addDirectoryItem('User Files', 'furkUserFiles', 'icon.png', 'icon.png')
        self.addDirectoryItem('Search', 'furkSearch', 'icon.png', 'icon.png')
        self.endDirectory()

    def plexn(self):
        self.addDirectoryItem('plexodus plex', 'plexodus', 'icon.png', 'icon.png')
        self.addDirectoryItem('plex', 'plexorg', 'icon.png', 'icon.png')
        self.endDirectory()

    def plex(self):
        xbmc.executebuiltin('Action(back)')
        xbmc.executebuiltin('RunScript(script.plexo)')
        self.endDirectory()

    def plexo(self):
        xbmc.executebuiltin('Action(back)')
        xbmc.executebuiltin('RunScript(script.plexodus)')
        self.endDirectory()


    def getMenuEnabled(self, menu_title):
        is_enabled = control.setting(menu_title).strip()
        if (is_enabled == '' or is_enabled == 'false'):
            return False
        return True


    def movies(self, lite=False):
        if self.getMenuEnabled('navi.movie.imdb.intheater') is True:
            self.addDirectoryItem(32420 if control.setting('index.labels') == 'false' else 32421, 'movies&url=theaters', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')

        if self.getMenuEnabled('navi.movie.tmdb.nowplaying') is True:
            self.addDirectoryItem(32422 if control.setting('index.labels') == 'false' else 32423, 'tmdbmovies&url=tmdb_nowplaying', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')

        if self.getMenuEnabled('navi.movie.trakt.anticipated') is True:
            self.addDirectoryItem(32424 if control.setting('index.labels') == 'false' else 32425, 'movies&url=traktanticipated', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')

        if self.getMenuEnabled('navi.movie.tmdb.upcoming') is True:
            self.addDirectoryItem(32426 if control.setting('index.labels') == 'false' else 32427, 'tmdbmovies&url=tmdb_upcoming', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')

        if self.getMenuEnabled('navi.movie.imdb.popular') is True:
            self.addDirectoryItem(32428 if control.setting('index.labels') == 'false' else 32429, 'movies&url=mostpopular', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')

        if self.getMenuEnabled('navi.movie.tmdb.popular') is True:
            self.addDirectoryItem(32430 if control.setting('index.labels') == 'false' else 32431, 'tmdbmovies&url=tmdb_popular', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')

        if self.getMenuEnabled('navi.movie.trakt.popular') is True:
            self.addDirectoryItem(32432 if control.setting('index.labels') == 'false' else 32433, 'movies&url=traktpopular', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')

        if self.getMenuEnabled('navi.movie.imdb.boxoffice') is True:
            self.addDirectoryItem(32434 if control.setting('index.labels') == 'false' else 32435, 'movies&url=imdbboxoffice', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')

        if self.getMenuEnabled('navi.movie.trakt.boxoffice') is True:
            self.addDirectoryItem(32436 if control.setting('index.labels') == 'false' else 32437, 'movies&url=traktboxoffice', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32438 if control.setting('index.labels') == 'false' else 32439, 'movies&url=mostvoted', 'most-voted.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32440 if control.setting('index.labels') == 'false' else 32441, 'tmdbmovies&url=tmdb_toprated', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32442 if control.setting('index.labels') == 'false' else 32443, 'movies&url=trakttrending', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32444 if control.setting('index.labels') == 'false' else 32445, 'movies&url=traktrecommendations', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32446 if control.setting('index.labels') == 'false' else 32447, 'movies&url=featured', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32451 if control.setting('index.labels') == 'false' else 32452, 'movies&url=oscars', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32453 if control.setting('index.labels') == 'false' else 32454, 'movies&url=oscarsnominees', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32455 if control.setting('index.labels') == 'false' else 32456, 'movieGenres', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32457 if control.setting('index.labels') == 'false' else 32458, 'movieYears', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32459 if control.setting('index.labels') == 'false' else 32460, 'moviePersons', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32461 if control.setting('index.labels') == 'false' else 32462, 'movieLanguages', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'DefaultCountry.png')
        self.addDirectoryItem(32463 if control.setting('index.labels') == 'false' else 32464, 'movieCertificates', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem('Latest Movies', 'movieWidget', 'icon.png', 'icon.png')
        if lite is False:
            if self.getMenuEnabled('mylists.widget') is True:
               self.addDirectoryItem(32003, 'mymovieliteNavigator', 'icon.png', 'icon.png')
            self.addDirectoryItem(32029, 'moviePerson', 'people-icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
            self.addDirectoryItem(32010, 'movieSearch', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.endDirectory()


    def mymovies(self, lite=False):
        self.accountCheck()
        self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'icon.png')

        if traktCredentials is True and imdbCredentials is True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'icon.png', 'icon.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'icon.png', 'icon.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

            if traktIndicators is True:
                self.addDirectoryItem(35308, 'movies&url=traktunfinished', 'icon.png', 'icon.png', queue=True)
                self.addDirectoryItem(32036, 'movies&url=trakthistory', 'icon.png', 'icon.png', queue=True)
                self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'icon.png', 'icon.png', queue=True)

        elif traktCredentials is True:
            self.addDirectoryItem(32032, 'movies&url=traktcollection', 'icon.png', 'icon.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'icon.png', 'icon.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

            if traktIndicators is True:
                self.addDirectoryItem(35308, 'movies&url=traktunfinished', 'icon.png', 'icon.png', queue=True)
                self.addDirectoryItem(32036, 'movies&url=trakthistory', 'icon.png', 'icon.png', queue=True)

        elif imdbCredentials is True:
#            self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'icon.png', 'icon.png', queue=True)
            self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'icon.png', 'icon.png', queue=True)

        if lite is False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'icon.png', 'icon.png')
            self.addDirectoryItem(32029, 'moviePerson', 'people-icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
            self.addDirectoryItem(32010, 'movieSearch', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.endDirectory()


    def tvshows(self, lite=False):
        if self.getMenuEnabled('navi.tv.imdb.popular') is True:
            self.addDirectoryItem(32428 if control.setting('index.labels') == 'false' else 32429, 'tvshows&url=popular', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        if self.getMenuEnabled('navi.tv.tmdb.popular') is True:
            self.addDirectoryItem(32430 if control.setting('index.labels') == 'false' else 32431, 'tmdbTvshows&url=tmdb_popular', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        if self.getMenuEnabled('navi.tv.trakt.popular') is True:
            self.addDirectoryItem(32432 if control.setting('index.labels') == 'false' else 32433, 'tvshows&url=traktpopular', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png', queue=True)
        if self.getMenuEnabled('navi.tv.imdb.mostvoted') is True:
            self.addDirectoryItem(32438 if control.setting('index.labels') == 'false' else 32439, 'tvshows&url=views', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        if self.getMenuEnabled('navi.tv.tmdb.toprated') is True:
            self.addDirectoryItem(32440 if control.setting('index.labels') == 'false' else 32441, 'tmdbTvshows&url=tmdb_toprated', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32442 if control.setting('index.labels') == 'false' else 32443, 'tvshows&url=trakttrending', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32448 if control.setting('index.labels') == 'false' else 32449, 'tvshows&url=rating', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32444 if control.setting('index.labels') == 'false' else 32445, 'tvshows&url=traktrecommendations', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png', queue=True)
        self.addDirectoryItem(32455 if control.setting('index.labels') == 'false' else 32456, 'tvGenres', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32469 if control.setting('index.labels') == 'false' else 32470, 'tvNetworks', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'DefaultNetwork.png')
        self.addDirectoryItem(32461 if control.setting('index.labels') == 'false' else 32462, 'tvLanguages', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'DefaultCountry.png')
        self.addDirectoryItem(32463 if control.setting('index.labels') == 'false' else 32464, 'tvCertificates', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32468, 'calendar&url=onDeck', 'icon.png', 'icon.png')
        self.addDirectoryItem(32465 if control.setting('index.labels') == 'false' else 32467, 'tmdbTvshows&url=tmdb_airingtoday', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32465 if control.setting('index.labels') == 'false' else 32466, 'tvshows&url=airing', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32471 if control.setting('index.labels') == 'false' else 32472, 'tmdbTvshows&url=tmdb_ontheair', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32473 if control.setting('index.labels') == 'false' else 32474, 'tvshows&url=active', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32475 if control.setting('index.labels') == 'false' else 32476, 'tvshows&url=premiere', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem(32027 if control.setting('index.labels') == 'false' else 32450, 'calendars', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.addDirectoryItem('channels', 'channels', 'list.png', 'icon.png')
        if (traktIndicators is True and not control.setting('tv.widget.alt') == '0') or (traktIndicators is False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem(32006, 'tvWidget', 'icon.png', 'icon.png')

        if lite is False:
            if self.getMenuEnabled('mylists.widget') is True:
               self.addDirectoryItem(32004, 'mytvliteNavigator', 'icon.png', 'icon.png')

            self.addDirectoryItem(32030, 'tvPerson', 'people-icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
            self.addDirectoryItem(32010, 'tvSearch', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.endDirectory()


    def mytvshows(self, lite=False):
        self.accountCheck()
        self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'icon.png')
        if traktCredentials is True and imdbCredentials is True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'icon.png', 'icon.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'icon.png', 'icon.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32041, 'episodesUserlists', 'userlists.png', 'icon.png')

            if traktIndicators is True:
                self.addDirectoryItem(35308, 'episodesUnfinished', 'icon.png', 'icon.png', queue=True)
                self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'icon.png', 'icon.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'icon.png', 'icon.png', queue=True)
                self.addDirectoryItem(32027, 'calendar&url=mycalendar', 'icon.png', 'icon.png', queue=True)
#                self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'icon.png', 'icon.png')  #sorts alphabetical
                self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'icon.png', 'icon.png')  # sorts by date added

        elif traktCredentials is True:
            self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'icon.png', 'icon.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
            self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'icon.png', 'icon.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
            self.addDirectoryItem(32041, 'episodesUserlists', 'icon.png', 'icon.png')

            if traktIndicators is True:
                self.addDirectoryItem(35308, 'episodesUnfinished', 'icon.png', 'icon.png', queue=True)
                self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'icon.png', 'icon.png', queue=True)
                self.addDirectoryItem(32037, 'calendar&url=progress', 'icon.png', 'icon.png.png', queue=True)
                self.addDirectoryItem(32027, 'calendar&url=mycalendar', 'icon.png', 'icon.png', queue=True)

        elif imdbCredentials is True:
#            self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'icon.png', 'icon.png')    #sorts alphabetical
            self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'icon.png', 'icon.png')  # sorts by date added

        if lite is False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'icon.png', 'icon.png')
            self.addDirectoryItem(32030, 'tvPerson', 'people-icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
            self.addDirectoryItem(32010, 'tvSearch', 'icon.png' if control.setting('icon.logos') == 'Traditional' else 'icon.png', 'icon.png')
        self.endDirectory()


    def tools(self):
        self.addDirectoryItem(32510, 'cfNavigator', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32609, 'resolveurl', 'resolveurl.png', 'DefaultAddonProgram.png')
        #-- Providers - 4
        self.addDirectoryItem(32651, 'openscrapersSettings&query=0.0', 'openscrapers.png', 'DefaultAddonProgram.png')
        #-- General - 0
        self.addDirectoryItem(32043, 'openSettings&query=0.1', 'icon.png', 'DefaultAddonProgram.png')
        #-- Navigation - 1
        self.addDirectoryItem(32362, 'openSettings&query=1.0', 'icon.png', 'DefaultAddonProgram.png')
        #-- Playback - 3
        self.addDirectoryItem(32045, 'openSettings&query=3.0', 'icon.png', 'DefaultAddonProgram.png')
        #-- Api-keys - 8
        self.addDirectoryItem(32044, 'openSettings&query=8.0', 'icon.png', 'DefaultAddonProgram.png')
        #-- Downloads - 10
        self.addDirectoryItem(32048, 'openSettings&query=10.0', 'icon.png', 'DefaultAddonProgram.png')
        #-- Subtitles - 11
        self.addDirectoryItem(32046, 'openSettings&query=11.0', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32361, 'resetViewTypes', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32073, 'authTrakt&opensettings=false', 'icon.png', 'DefaultAddonProgram.png')
        self.endDirectory()


    def cf(self):
        self.addDirectoryItem(32610, 'clearAllCache', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32611, 'clearSources&opensettings=false', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32612, 'clearMetaCache', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32613, 'clearCache', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32614, 'clearCacheSearch', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32615, 'clearBookmarks', 'icon.png', 'DefaultAddonProgram.png')
        self.endDirectory()


    def library(self):
#-- Library - 9
        self.addDirectoryItem(32557, 'openSettings&query=9.0', 'icon.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'icon.png', 'DefaultAddonLibrary.png')
        self.addDirectoryItem(32559, control.setting('library.movie'), 'icon.png', 'icon.png', isAction=False)
        self.addDirectoryItem(32560, control.setting('library.tv'), 'icon.png', 'icon.png', isAction=False)
        if trakt.getTraktCredentialsInfo():
            self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'icon.png', 'icon.png')
            self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'icon.png', 'icon.png')
            self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'icon.png', 'icon.png')
            self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'icon.png', 'icon.png')
        self.endDirectory()


    def downloads(self):
        movie_downloads = control.setting('movie.download.path')
        tv_downloads = control.setting('tv.download.path')
        if len(control.listDir(movie_downloads)[0]) > 0:
            self.addDirectoryItem(32001, movie_downloads, 'icon.png', 'icon.png', isAction=False)
        if len(control.listDir(tv_downloads)[0]) > 0:
            self.addDirectoryItem(32002, tv_downloads, 'icon.png', 'icon.png', isAction=False)
        self.endDirectory()


    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'icon.png', 'icon.png')
        self.addDirectoryItem(32002, 'tvSearch', 'icon.png', 'icon.png')
        self.addDirectoryItem(32029, 'moviePerson', 'people-icon.png', 'icon.png')
        self.addDirectoryItem(32030, 'tvPerson', 'people-icon.png', 'icon.png')
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

        cm.append(('[COLOR red]plexOdus Settings[/COLOR]', 'RunPlugin(%s?action=openSettings&query=0.0)' % sysaddon))

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