# -*- coding: utf-8 -*-

'''
    Still i Rise Add-on
'''

import urlparse, sys, urllib, xbmc
from resources.lib.modules import control

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
action = params.get('action')

subid = params.get('subid')
name = params.get('name')
title = params.get('title')
year = params.get('year')
imdb = params.get('imdb')
tvdb = params.get('tvdb')
tmdb = params.get('tmdb')
season = params.get('season')
episode = params.get('episode')
tvshowtitle = params.get('tvshowtitle')
premiered = params.get('premiered')
url = params.get('url')
image = params.get('image')
meta = params.get('meta')
art = params.get('art')
select = params.get('select')
query = params.get('query')
source = params.get('source')
content = params.get('content')

windowedtrailer = params.get('windowedtrailer')
windowedtrailer = int(windowedtrailer) if windowedtrailer in ("0","1") else 0


if action is None:
    from resources.lib.menus import navigator
    from resources.lib.modules import cache
    run = control.setting('first.info')
    if run == '': run = 'true' 
    if cache._find_cache_version(): run = 'true'  
    if run == 'true':
        from resources.lib.modules import changelog
        changelog.get()
        control.setSetting(id='first.info', value='false')
    cache.cache_version_check()
    navigator.Navigator().root()



####################################################
#---News and Updates
####################################################
elif action == 'infoCheck':
    from resources.lib.menus import navigator
    navigator.Navigator().infoCheck('')

elif action == 'ShowNews':
    from resources.lib.modules import newsinfo
    newsinfo.news()

elif action == 'ShowChangelog':
    from resources.lib.modules import changelog
    changelog.get()



####################################################
#---MOVIE
####################################################
elif action == 'movieNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().mymovies(lite=True)

elif action == 'movies':
    from resources.lib.menus import movies
    movies.Movies().get(url)

elif action == 'moviePage':
    from resources.lib.menus import movies
    movies.Movies().get(url)

elif action == 'tmdbmovies':
    from resources.lib.menus import movies
    movies.Movies().getTMDb(url)

elif action == 'tmdbmoviePage':
    from resources.lib.menus import movies
    movies.Movies().getTMDb(url)

elif action == 'newMovies':
    from resources.lib.menus import movies
    movies.Movies().newMovies()

elif action == 'movieSearch':
    from resources.lib.menus import movies
    movies.Movies().search()

elif action == 'movieSearchnew':
    from resources.lib.menus import movies
    movies.Movies().search_new()

elif action == 'movieSearchterm':
    from resources.lib.menus import movies
    movies.Movies().search_term(name)

elif action == 'moviePerson':
    from resources.lib.menus import movies
    movies.Movies().person()

elif action == 'movieGenres':
    from resources.lib.menus import movies
    movies.Movies().genres()

elif action == 'movieLanguages':
    from resources.lib.menus import movies
    movies.Movies().languages()

elif action == 'movieCertificates':
    from resources.lib.menus import movies
    movies.Movies().certifications()

elif action == 'movieYears':
    from resources.lib.menus import movies
    movies.Movies().years()

elif action == 'moviePersons':
    from resources.lib.menus import movies
    movies.Movies().persons(url)

elif action == 'movieUserlists':
    from resources.lib.menus import movies
    movies.Movies().userlists()



####################################################
#---Collections
####################################################
elif action == 'collectionsNavigator':
    from resources.lib.menus import collections
    # navigator.Navigator().collections()
    collections.Collections().collectionsNavigator()

elif action == 'collectionActors':
    from resources.lib.menus import collections
    collections.Collections().collectionActors()

elif action == 'collectionBoxset':
    from resources.lib.menus import collections
    collections.Collections().collectionBoxset()

elif action == 'collectionKids':
    from resources.lib.menus import collections
    collections.Collections().collectionKids()

elif action == 'collectionBoxsetKids':
    from resources.lib.menus import collections
    collections.Collections().collectionBoxsetKids()

elif action == 'collectionSuperhero':
    from resources.lib.menus import collections
    collections.Collections().collectionSuperhero()

elif action == 'collections':
    from resources.lib.menus import collections
    collections.Collections().get(url)



####################################################
#---Furk
####################################################
elif action == "furkNavigator":
    from resources.lib.menus import navigator
    navigator.Navigator().furk()

elif action == "furkMetaSearch":
    from resources.lib.menus import furk
    furk.Furk().furk_meta_search(url)

elif action == "furkSearch":
    from resources.lib.menus import furk
    furk.Furk().search()

elif action == "furkUserFiles":
    from resources.lib.menus import furk
    furk.Furk().user_files()

elif action == "furkSearchNew":
    from resources.lib.menus import furk
    furk.Furk().search_new()



####################################################
# TV Shows
####################################################
elif action == 'tvNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().mytvshows(lite=True)

elif action == 'channels':
    from resources.lib.menus import channels
    channels.channels().get()

elif action == 'tvshows':
    from resources.lib.menus import tvshows
    tvshows.TVshows().get(url)

elif action == 'tvshowPage':
    from resources.lib.menus import tvshows
    tvshows.TVshows().get(url)

elif action == 'tmdbTvshows':
    from resources.lib.menus import tvshows
    tvshows.TVshows().getTMDb(url)

elif action == 'tmdbTvshowPage':
    from resources.lib.menus import tvshows
    tvshows.TVshows().getTMDb(url)

elif action == 'tvmazeTvshows':
    from resources.lib.menus import tvshows
    tvshows.TVshows().getTVmaze(url)

elif action == 'tvmazeTvshowPage':
    from resources.lib.menus import tvshows
    tvshows.TVshows().getTVmaze(url)

elif action == 'tvSearch':
    from resources.lib.menus import tvshows
    tvshows.TVshows().search()

elif action == 'tvSearchnew':
    from resources.lib.menus import tvshows
    tvshows.TVshows().search_new()

elif action == 'tvSearchterm':
    from resources.lib.menus import tvshows
    tvshows.TVshows().search_term(name)

elif action == 'tvPerson':
    from resources.lib.menus import tvshows
    tvshows.TVshows().person()

elif action == 'tvGenres':
    from resources.lib.menus import tvshows
    tvshows.TVshows().genres()

elif action == 'tvNetworks':
    from resources.lib.menus import tvshows
    tvshows.TVshows().networks()

elif action == 'tvLanguages':
    from resources.lib.menus import tvshows
    tvshows.TVshows().languages()

elif action == 'tvCertificates':
    from resources.lib.menus import tvshows
    tvshows.TVshows().certifications()

elif action == 'tvPersons':
    from resources.lib.menus import tvshows
    tvshows.TVshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.menus import tvshows
    tvshows.TVshows().userlists()



####################################################
# SEASON
####################################################
elif action == 'seasons':
    from resources.lib.menus import seasons
    seasons.Seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'seasonsUserlists':
    from resources.lib.indexers import seasons
    seasons.Seasons().userlists()

elif action == 'seasonsList':
    from resources.lib.menus import seasons
    seasons.Seasons().seasonList(url)



####################################################
# EPISODES
####################################################
elif action == 'episodes':
    from resources.lib.menus import episodes
    episodes.Episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'tvWidget':
    from resources.lib.menus import episodes
    episodes.Episodes().widget()

elif action == 'calendar':
    from resources.lib.menus import episodes
    episodes.Episodes().calendar(url)

elif action == 'calendars':
    from resources.lib.menus import episodes
    episodes.Episodes().calendars()

elif action == 'episodesUnfinished':
    from resources.lib.menus import episodes
    episodes.Episodes().unfinished()

elif action == 'episodesUserlists':
    from resources.lib.menus import episodes
    episodes.Episodes().userlists()



####################################################
#---Tools
####################################################
elif action == 'download':
    import json
    from resources.lib.modules import sources
    from resources.lib.modules import downloader
    try:
        downloader.download(name, image, sources.Sources().sourcesResolve(json.loads(source)[0], True))
    except:
        pass

elif action == 'downloadNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().downloads()

elif action == 'libraryNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().library()

elif action == 'toolNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().views()

elif action == 'resetViewTypes':
    from resources.lib.modules import views
    views.clearViews()

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'refresh':
    from resources.lib.modules import control
    control.refresh()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'open.Settings.CacheProviders':
    from resources.lib.modules import control
    control.openSettings(query)

elif action == 'artwork':
    from resources.lib.modules import control
    control.artwork()





####################################################
#---Playcount
####################################################
elif action == 'moviePlaycount':
    from resources.lib.modules import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.modules import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.modules import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)



####################################################
#---Trakt
####################################################
elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, season, episode)
    # trakt.manager2(name, imdb, tvdb, season, episode)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()
    if params['opensettings'] == 'true':
        control.openSettings(query, "plugin.video.s_i_r")

elif action == 'cachesyncMovies':
    from resources.lib.modules import trakt
    trakt.cachesyncMovies()

elif action == 'cachesyncTVShows':
    from resources.lib.modules import trakt
    trakt.cachesyncTVShows()


####################################################
# PLAYLIST
####################################################
elif action == 'playlistManager':
    from resources.lib.modules import playlist
    playlist.playlistManager(name, url, meta, art)

elif action == 'showPlaylist':
    from resources.lib.modules import playlist
    playlist.playlistShow()

elif action == 'clearPlaylist':
    from resources.lib.modules import playlist
    playlist.playlistClear()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()
    if name is None:
        control.notification(title = 35515, message = 35519, icon = 'INFO', sound = False)
    else:
        control.notification(title = name, message = 35519, icon = 'INFO', sound = False)



####################################################
#---Player
####################################################
elif action == 'play':
    from resources.lib.indexersb import noname
    if not content == None:
        noname.player().play(url, content)
    else:
        from resources.lib.modules import sources
        sources.Sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'playItem':
    from resources.lib.modules import sources
    sources.Sources().playItem(title, source)

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.Trailer().play(name, url, windowedtrailer)

elif action == 'addItem':
    from resources.lib.modules import sources
    sources.Sources().addItem(title)

elif action == 'alterSources':
    from resources.lib.modules import sources
    sources.Sources().alterSources(url, meta)

elif action == 'random':
    rtype = params.get('rtype')

    if rtype == 'movie':
        from resources.lib.menus import movies
        rlist = movies.Movies().get(url, create_directory=False)
        r = sys.argv[0]+"?action=play"

    elif rtype == 'episode':
        from resources.lib.menus import episodes
        rlist = episodes.Episodes().get(tvshowtitle, year, imdb, tvdb, season, create_directory=False)
        r = sys.argv[0]+"?action=play"

    elif rtype == 'season':
        from resources.lib.menus import seasons
        rlist = seasons.Seasons().get(tvshowtitle, year, imdb, tvdb, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=episode"

    elif rtype == 'show':
        from resources.lib.menus import tvshows
        rlist = tvshows.TVshows().get(url, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=season"

    from resources.lib.modules import control
    from random import randint
    import json

    try:
        rand = randint(1,len(rlist))-1

        for p in ['title','year','imdb','tvdb','season','episode','tvshowtitle','premiered','select']:

            if rtype == "show" and p == "tvshowtitle":
                try:
                    r += '&'+p+'='+urllib.quote_plus(rlist[rand]['title'])
                except:
                    pass
            else:
                try:
                    r += '&'+p+'='+urllib.quote_plus(rlist[rand][p])
                except:
                    pass

        try:
            r += '&meta='+urllib.quote_plus(json.dumps(rlist[rand]))
        except:
            r += '&meta='+urllib.quote_plus("{}")

        if rtype == "movie":
            try:
                control.infoDialog(rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except:
                pass

        elif rtype == "episode":
            try:
                control.infoDialog(rlist[rand]['tvshowtitle']+" - Season "+rlist[rand]['season']+" - "+rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except:
                pass
        control.execute('RunPlugin(%s)' % r)
    except:
        control.infoDialog(control.lang(32537).encode('utf-8'), time=8000)



####################################################
#----Library Actions
####################################################
elif action == 'movieToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().range(url)

elif action == 'moviesToLibrarySilent':
    from resources.lib.modules import libtools
    libtools.libmovies().silent(url)

elif action == 'tvshowToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tvdb)

elif action == 'tvshowsToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)

elif action == 'tvshowsToLibrarySilent':
    from resources.lib.modules import libtools
    libtools.libtvshows().silent(url)

elif action == 'updateLibrary':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()



####################################################
#---Clear Cache actions
####################################################
elif action == 'cfNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().cf()

elif action == 'clearAllCache':
    from resources.lib.menus import navigator
    navigator.Navigator().clearCacheAll()

elif action == 'clearSources':
    from resources.lib.menus import navigator
    navigator.Navigator().clearCacheProviders()
    if params['opensettings'] == 'true':
        control.openSettings(query, 'plugin.video.s_i_r')

elif action == 'clearMetaCache':
    from resources.lib.menus import navigator
    navigator.Navigator().clearCacheMeta()

elif action == 'clearCache':
    from resources.lib.menus import navigator
    navigator.Navigator().clearCache()

elif action == 'clearCacheSearch':
    from resources.lib.menus import navigator
    navigator.Navigator().clearCacheSearch()

elif action == 'clearBookmarks':
    from resources.lib.menus import navigator
    navigator.Navigator().clearBookmarks()



####################################################
#---Provider Source actions
####################################################
elif action == 'openscrapersSettings':
    from resources.lib.modules import control
    control.openSettings('0.0', 'script.module.openscrapers')
    # if params['opensettings'] == 'true':
        # control.openSettings(query, "plugin.video.s_i_r")

elif action == 'resolveurl':
    try: import resolveurl
    except: pass
    resolveurl.display_settings()

elif action == 'resolveurlRDTorrent':
    from resources.lib.modules import control
    control.openSettings(query, "script.module.resolveurl")

elif action == "toggleAll":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.all_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

elif action == "toggleAllHosters":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.hoster_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Hoster providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

elif action == "toggleAllForeign":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.all_foreign_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Foregin providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

elif action == "toggleAllSpanish":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.spanish_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Spanish providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

elif action == "toggleAllGerman":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.german_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All German providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

elif action == "toggleAllGreek":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.greek_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Greek providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

elif action == "toggleAllPolish":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.polish_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Polish providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

elif action == "toggleAllPaid":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.all_paid_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Paid providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

elif action == "toggleAllDebrid":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.debrid_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Debrid providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

elif action == "toggleAllTorrent":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.torrent_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Torrent providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

if action == "toggleDefaults":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.all_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        default = control.getSettingDefault(source_setting)
        control.setSetting(source_setting, default)
#    xbmc.log('All providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.s_i_r")

############################lists##########################

elif action == 'listNavigator':
    from resources.lib.menus import navigator
    navigator.Navigator().listnav()

if action == 'lists':
    from resources.lib.indexersb import noname
    noname.indexer().root()
	
if action == 'lista':
    from resources.lib.indexersb import noname
    noname.indexer().root_lista()

if action == 'listb':
    from resources.lib.indexersb import noname
    noname.indexer().root_listb()
    
if action == 'listc':
    from resources.lib.indexersb import noname
    noname.indexer().root_listc()

if action == 'listd':
    from resources.lib.indexersb import noname
    noname.indexer().root_listd()

if action == 'liste':
    from resources.lib.indexersb import noname
    noname.indexer().root_liste()

if action == 'listf':
    from resources.lib.indexersb import noname
    noname.indexer().root_listf()

if action == 'plistg':
    from resources.lib.indexersb import noname
    noname.indexer().root_listg()

if action == 'listg':
    from resources.lib.indexersb import noname
    noname.indexer().root_klistg()

if action == 'listh':
    from resources.lib.indexersb import noname
    noname.indexer().root_listh()

if action == 'listi':
    from resources.lib.indexersb import noname
    noname.indexer().root_listi()

if action == 'listj':
    from resources.lib.indexersb import noname
    noname.indexer().root_listj()  

if action == 'listk':
    from resources.lib.indexersb import noname
    noname.indexer().root_listk()

if action == 'listl':
    from resources.lib.indexersb import noname
    noname.indexer().root_listl()

if action == 'listm':
    from resources.lib.indexersb import noname
    noname.indexer().root_listm()

if action == 'listn':
    from resources.lib.indexersb import noname
    noname.indexer().root_listn()

if action == 'listo':
    from resources.lib.indexersb import noname
    noname.indexer().root_listo()
  
elif action == 'directory':
    from resources.lib.indexersb import noname
    noname.indexer().get(url)

elif action == 'qdirectory':
    from resources.lib.indexersb import noname
    noname.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexersb import noname
    noname.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexersb import noname
    noname.indexer().developer()

elif action == 'tvtuner':
    from resources.lib.indexersb import noname
    noname.indexer().tvtuner(url)

elif 'youtube' in str(action):
    from resources.lib.indexersb import noname
    noname.indexer().youtube(url, action)

elif action == 'browser':
    from resources.lib.indexersb import noname
    sports.resolver().browser(url)

elif action == 'queueItem':
    from resources.lib.modulesb import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modulesb import control
    control.openSettings()

elif action == 'resolveurlSettings':
    from resources.lib.modulesb import control
    control.openSettings(id='script.module.resolveurl')

elif action == 'addView':
    from resources.lib.modulesb import views
    views.addView(content)

elif action == 'downloader':
    from resources.lib.modulesb import downloader
    downloader.downloader()

elif action == 'addDownload':
    from resources.lib.modulesb import downloader
    downloader.addDownload(name,url,image)

elif action == 'removeDownload':
    from resources.lib.modulesb import downloader
    downloader.removeDownload(url)

elif action == 'startDownload':
    from resources.lib.modulesb import downloader
    downloader.startDownload()

elif action == 'startDownloadThread':
    from resources.lib.modulesb import downloader
    downloader.startDownloadThread()

elif action == 'stopDownload':
    from resources.lib.modulesb import downloader
    downloader.stopDownload()

elif action == 'statusDownload':
    from resources.lib.modulesb import downloader
    downloader.statusDownload()

elif action == 'trailer':
    from resources.lib.modulesb import trailer
    trailer.trailer().play(name)

elif action == 'clearCache':
    from resources.lib.modulesb import cache
    cache.clear()
############################################################################################################


elif action == 'swiftNavigator':
    from resources.lib.indexers import swift
    swift.swift().root()

elif action == 'swiftCat':
    from resources.lib.indexers import swift
    swift.swift().swiftCategory(url)

elif action == 'swiftPlay':
    from resources.lib.indexers import swift
    swift.swift().swiftPlay(url)

elif action == 'docuNavigator':
    from resources.lib.indexers import docu
    docu.documentary().root()

elif action == 'docuHeaven':
    from resources.lib.indexers import docu
    if not docu_category == None:
        docu.documentary().docu_list(docu_category)
    elif not docu_watch == None:
        docu.documentary().docu_play(docu_watch)
    else:
        docu.documentary().root()
######################################menus######################################################################

elif action == 'jspttvNavigator':
    from resources.lib.indexersc import jsptnav
    jsptnav.navigator().tvshows()

if action == 'jsptnavigator':
    from resources.lib.indexersc import jsptnav
    jsptnav.navigator().root()

elif action == 'jsptmovieNavigator':
    from resources.lib.indexersc import jsptnav
    jsptnav.navigator().movies()

if action == 'gtnavigator':
    from resources.lib.indexersc import gtnav
    gtnav.navigator().root()

elif action == 'gtmaremovieNavigator':
    from resources.lib.indexersc import gtnav
    gtnav.navigator().movies()

elif action == 'gtmaretvNavigator':
    from resources.lib.indexersc import gtnav
    gtnav.navigator().tvshows()

if action == 'dracnavigator':
    from resources.lib.indexersc import dafnav
    dafnav.navigator().root()

if action == 'lfcsnavigator':
    from resources.lib.indexersc import lfcsnav
    lfcsnav.navigator().root()

elif action == 'lfcsmovieNavigator':
    from resources.lib.indexersc import lfcsnav
    lfcsnav.navigator().movies()

elif action == 'lfcstvNavigator':
    from resources.lib.indexersc import lfcsnav
    lfcsnav.navigator().tvshows()

elif action == 'lfcsmovieCertificates':
    from resources.lib.indexersc import lfcsnav
    lfcsnav.navigator().certificationsnew()

elif action == 'lfcstvCertificates':
    from resources.lib.indexersc import lfcsnav
    lfcsnav.navigator().certificationsnewtv()

if action == 'nightnavigator':
    from resources.lib.indexersc import nightnav
    nightnav.navigator().root()

elif action == 'nightmaremovieNavigator':
    from resources.lib.indexersc import nightnav
    nightnav.navigator().movies()

elif action == 'nightmaretvNavigator':
    from resources.lib.indexersc import nightnav
    nightnav.navigator().tvshows()

elif action == 'nightmaremovieCertificates':
    from resources.lib.indexersc import nightnav
    nightnav.navigator().certificationsnew()

elif action == 'nightmaretvCertificates':
    from resources.lib.indexersc import nightnav
    nightnav.navigator().certificationsnewtv()

if action == 'liunavigator':
    from resources.lib.indexersc import liunav
    liunav.navigator().root()

elif action == 'liumovieNavigator':
    from resources.lib.indexersc import liunav
    liunav.navigator().movies()

elif action == 'liutvNavigator':
    from resources.lib.indexersc import liunav
    liunav.navigator().tvshows()

if action == 'hddnavigator':
    from resources.lib.indexersc import hddnav
    hddnav.navigator().root()

elif action == 'hddmovieNavigator':
    from resources.lib.indexersc import hddnav
    hddnav.navigator().movies()

elif action == 'hddtvNavigator':
    from resources.lib.indexersc import hddnav
    hddnav.navigator().tvshows()

elif action == 'hddmovieCertificates':
    from resources.lib.indexersc import hddnav
    hddnav.navigator().certificationsnew()

elif action == 'hddtvCertificates':
    from resources.lib.indexersc import hddnav
    hddnav.navigator().certificationsnewtv()

if action == 'deepnavigator':
    from resources.lib.indexersc import deepnav
    deepnav.navigator().root()

elif action == 'deepmovieNavigator':
    from resources.lib.indexersc import deepnav
    deepnav.navigator().movies()

elif action == 'deeptvNavigator':
    from resources.lib.indexersc import deepnav
    deepnav.navigator().tvshows()

elif action == 'deepmovieCertificates':
    from resources.lib.indexersc import deepnav
    deepnav.navigator().certificationsnew()

elif action == 'deeptvCertificates':
    from resources.lib.indexersc import deepnav
    deepnav.navigator().certificationsnewtv()

if action == 'jcanavigator':
    from resources.lib.indexersc import jcanav
    jcanav.navigator().root()

elif action == 'jcamovieNavigator':
    from resources.lib.indexersc import jcanav
    jcanav.navigator().movies()

elif action == 'jcatvNavigator':
    from resources.lib.indexersc import jcanav
    jcanav.navigator().tvshows()

elif action == 'jcamovieCertificates':
    from resources.lib.indexersc import jcanav
    jcanav.navigator().certificationsnew()

elif action == 'jcatvCertificates':
    from resources.lib.indexersc import jcanav
    jcanav.navigator().certificationsnewtv()

if action == 'bbtlNavigator':
    from resources.lib.indexersc import bbtlnav
    bbtlnav.navigator().root()

elif action == 'bbtlmovieNavigator':
    from resources.lib.indexersc import bbtlnav
    bbtlnav.navigator().movies()

elif action == 'bbtltvNavigator':
    from resources.lib.indexersc import bbtlnav
    bbtlnav.navigator().tvshows()

elif action == 'bbtlmovieCertificates':
    from resources.lib.indexersc import bbtlnav
    bbtlnav.navigator().certificationsnew()

elif action == 'bbtltvCertificates':
    from resources.lib.indexersc import bbtlnav
    bbtlnav.navigator().certificationsnewtv()

if action == 'nightmareNavigator':
    from resources.lib.indexersc import nightnav
    nightnav.navigator().root()

elif action == 'nightmaremovieNavigator':
    from resources.lib.indexersc import nightnav
    nightnav.navigator().movies()

elif action == 'nightmaretvNavigator':
    from resources.lib.indexersc import nightnav
    nightnav.navigator().tvshows()

elif action == 'nightmaremovieCertificates':
    from resources.lib.indexersc import nightnav
    nightnav.navigator().certificationsnew()

elif action == 'nightmaretvCertificates':
    from resources.lib.indexersc import nightnav
    nightnav.navigator().certificationsnewtv()

    
if action == 'dracmov':
    from resources.lib.indexersc import dafnav
    dafnav.navigator().movies()
    
if action == 'dractv':
    from resources.lib.indexersc import dafnav
    dafnav.navigator().tvshows()
    
elif action == 'jsptmovieCertificates':
    from resources.lib.indexersc import jsptnav
    jsptnav.navigator().certificationsnew()

elif action == 'jspttvCertificates':
    from resources.lib.indexersc import jsptnav
    jsptnav.navigator().certificationsnewtv()
    
elif action == 'gtmaremovieCertificates':
    from resources.lib.indexersc import gtnav
    gtnav.navigator().certificationsnew()

elif action == 'gtmaretvCertificates':
    from resources.lib.indexersc import gtnav
    gtnav.navigator().certificationsnewtv()

######################navs###########################################
    
elif action == 'movieGenres50':
    from resources.lib.indexers import mcmovies
    mcmovies.movies().genres50()
    
elif action == 'movieGenres60':
    from resources.lib.indexers import mcmovies
    mcmovies.movies().genres60()
    
elif action == 'movieGenres70':
    from resources.lib.indexers import mcmovies
    mcmovies.movies().genres70()
    
elif action == 'movieGenres80':
    from resources.lib.indexers import mcmovies
    mcmovies.movies().genres80()

elif action == 'odintoons':
    from resources.lib.indexers import odintoons
    odintoons.movies().get(url)


elif action == 'jsptmovieGenres':
    from resources.lib.indexers import odintoons
    odintoons.movies().genres()

elif action == 'jsptmovieLanguages':
    from resources.lib.indexers import odintoons
    odintoons.movies().languages()

elif action == 'jsptmovieYears':
    from resources.lib.indexers import odintoons
    odintoons.movies().years()


elif action == 'nmaremov':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().get(url)


elif action == 'nightmaremovieGenres':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().genres()

elif action == 'nightmaremovieLanguages':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().languages()

elif action == 'nightmaremovieYears':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().years()

elif action == 'lfcsmov':
    from resources.lib.indexers import lfcsmov
    lfcsmov.movies().get(url)


elif action == 'lfcsmovieGenres':
    from resources.lib.indexers import lfcsmov
    lfcsmov.movies().genres()

elif action == 'lfcsmovieLanguages':
    from resources.lib.indexers import lfcsmov
    lfcsmov.movies().languages()

elif action == 'lfcsmovieYears':
    from resources.lib.indexers import lfcsmov
    lfcsmov.movies().years()


elif action == 'wwmovies':
    from resources.lib.indexers import wwmovies
    wwmovies.movies().get(url)


elif action == 'gtmaremovieGenres':
    from resources.lib.indexers import wwmovies
    wwmovies.movies().genres()

elif action == 'gtmaremovieLanguages':
    from resources.lib.indexers import wwmovies
    wwmovies.movies().languages()

elif action == 'gtmaremovieYears':
    from resources.lib.indexers import wwmovies
    wwmovies.movies().years()

elif action == 'nmaremov':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().get(url)


elif action == 'nightmaremovieGenres':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().genres()

elif action == 'nightmaremovieLanguages':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().languages()

elif action == 'nightmaremovieYears':
    from resources.lib.indexers import nmaremov
    nmaremov.movies().years()

elif action == 'dkmov':
    from resources.lib.indexers import dkmov
    dkmov.movies().get(url)


elif action == 'bbtlmovieGenres':
    from resources.lib.indexers import dkmov
    dkmov.movies().genres()

elif action == 'bbtlmovieLanguages':
    from resources.lib.indexers import dkmov
    dkmov.movies().languages()

elif action == 'bbtlmovieYears':
    from resources.lib.indexers import dkmov
    dkmov.movies().years()

    
elif action == 'apmovies':
    from resources.lib.indexers import apmovies
    apmovies.movies().get(url)


elif action == 'jcamovieGenres':
    from resources.lib.indexers import apmovies
    apmovies.movies().genres()

elif action == 'jcamovieLanguages':
    from resources.lib.indexers import apmovies
    apmovies.movies().languages()

elif action == 'jcamovieYears':
    from resources.lib.indexers import apmovies
    apmovies.movies().years()


elif action == 'asmovies':
    from resources.lib.indexers import asmovies
    asmovies.movies().get(url)


elif action == 'deepmovieGenres':
    from resources.lib.indexers import asmovies
    asmovies.movies().genres()

elif action == 'deepmovieLanguages':
    from resources.lib.indexers import asmovies
    asmovies.movies().languages()

elif action == 'deepmovieYears':
    from resources.lib.indexers import asmovies
    asmovies.movies().years()

    
elif action == 'hmmm':
    from resources.lib.indexers import hmmm
    hmmm.movies().get(url)


elif action == 'hddmovieGenres':
    from resources.lib.indexers import hmmm
    hmmm.movies().genres()

elif action == 'hddmovieLanguages':
    from resources.lib.indexers import hmmm
    hmmm.movies().languages()

elif action == 'hddmovieYears':
    from resources.lib.indexers import hmmm
    hmmm.movies().years()


elif action == 'lhmovies':
    from resources.lib.indexers import lhmovies
    lhmovies.movies().get(url)


elif action == 'liumovieGenres':
    from resources.lib.indexers import lhmovies
    lhmovies.movies().genres()

elif action == 'liumovieLanguages':
    from resources.lib.indexers import lhmovies
    lhmovies.movies().languages()

elif action == 'liumovieYears':
    from resources.lib.indexers import lhmovies
    lhmovies.movies().years()


elif action == 'nmaretv':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().get(url)


elif action == 'nightmaretvGenres':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().genres()

elif action == 'nightmaretvNetworks':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().networks()

elif action == 'nightmaretvLanguages':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().languages()

elif action == 'nightmaretvYears':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().years()



elif action == 'dktvshows':
    from resources.lib.indexers import dktvshows
    dktvshows.tvshows().get(url)


elif action == 'bbtltvGenres':
    from resources.lib.indexers import dktvshows
    dktvshows.tvshows().genres()

elif action == 'bbtltvNetworks':
    from resources.lib.indexers import dktvshows
    dktvshows.tvshows().networks()

elif action == 'bbtltvLanguages':
    from resources.lib.indexers import dktvshows
    dktvshows.tvshows().languages()

elif action == 'bbtltvYears':
    from resources.lib.indexers import dktvshows
    dktvshows.tvshows().years()


elif action == 'aptvshows':
    from resources.lib.indexers import aptvshows
    aptvshows.tvshows().get(url)


elif action == 'jcatvGenres':
    from resources.lib.indexers import aptvshows
    aptvshows.tvshows().genres()

elif action == 'jcatvNetworks':
    from resources.lib.indexers import aptvshows
    aptvshows.tvshows().networks()

elif action == 'jcatvLanguages':
    from resources.lib.indexers import aptvshows
    aptvshows.tvshows().languages()

elif action == 'jcatvYears':
    from resources.lib.indexers import aptvshows
    aptvshows.tvshows().years()

elif action == 'astvshows':
    from resources.lib.indexers import astvshows
    astvshows.tvshows().get(url)


elif action == 'deeptvGenres':
    from resources.lib.indexers import astvshows
    astvshows.tvshows().genres()

elif action == 'deeptvNetworks':
    from resources.lib.indexers import astvshows
    astvshows.tvshows().networks()

elif action == 'deeptvLanguages':
    from resources.lib.indexers import astvshows
    astvshows.tvshows().languages()

elif action == 'deeptvYears':
    from resources.lib.indexers import astvshows
    astvshows.tvshows().years()


elif action == 'hmmtv':
    from resources.lib.indexers import hmmtv
    hmmtv.tvshows().get(url)


elif action == 'hddtvGenres':
    from resources.lib.indexers import hmmtv
    hmmtv.tvshows().genres()

elif action == 'hddtvNetworks':
    from resources.lib.indexers import hmmtv
    hmmtv.tvshows().networks()

elif action == 'hddtvLanguages':
    from resources.lib.indexers import hmmtv
    hmmtv.tvshows().languages()

elif action == 'hddtvYears':
    from resources.lib.indexers import hmmtv
    hmmtv.tvshows().years()



elif action == 'lhtvshows':
    from resources.lib.indexers import lhtvshows
    lhtvshows.tvshows().get(url)


elif action == 'liutvGenres':
    from resources.lib.indexers import lhtvshows
    lhtvshows.tvshows().genres()

elif action == 'liutvNetworks':
    from resources.lib.indexers import lhtvshows
    lhtvshows.tvshows().networks()

elif action == 'liutvLanguages':
    from resources.lib.indexers import lhtvshows
    lhtvshows.tvshows().languages()

elif action == 'liutvYears':
    from resources.lib.indexers import lhtvshows
    lhtvshows.tvshows().years()

elif action == 'nmaretv':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().get(url)


elif action == 'nightmaretvGenres':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().genres()

elif action == 'nightmaretvNetworks':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().networks()

elif action == 'nightmaretvLanguages':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().languages()

elif action == 'nightmaretvYears':
    from resources.lib.indexers import nmaretv
    nmaretv.tvshows().years()	

elif action == 'lfcstv':
    from resources.lib.indexers import lfcstv
    lfcstv.tvshows().get(url)


elif action == 'lfcstvGenres':
    from resources.lib.indexers import lfcstv
    lfcstv.tvshows().genres()

elif action == 'lfcstvNetworks':
    from resources.lib.indexers import lfcstv
    lfcstv.tvshows().networks()

elif action == 'lfcstvLanguages':
    from resources.lib.indexers import lfcstv
    lfcstv.tvshows().languages()

elif action == 'lfcstvYears':
    from resources.lib.indexers import lfcstv
    lfcstv.tvshows().years()


elif action == 'tvGenres50':
    from resources.lib.indexers import mctvshows
    mctvshows.tvshows().genres50()

	
elif action == 'tvGenres50':
    from resources.lib.indexers import mctvshows
    mctvshows.tvshows().genres50()

elif action == 'tvGenres60':
    from resources.lib.indexers import mctvshows
    mctvshows.tvshows().genres60()


elif action == 'tvGenres70':
    from resources.lib.indexers import mctvshows
    mctvshows.tvshows().genres70()

elif action == 'tvGenres80':
    from resources.lib.indexers import mctvshows
    mctvshows.tvshows().genres80()

elif action == 'odintvtoons':
    from resources.lib.indexers import odintvtoons
    odintvtoons.tvshows().get(url)


elif action == 'jspttvGenres':
    from resources.lib.indexers import odintvtoons
    odintvtoons.tvshows().genres()

elif action == 'jspttvNetworks':
    from resources.lib.indexers import odintvtoons
    odintvtoons.tvshows().networks()

elif action == 'jspttvLanguages':
    from resources.lib.indexers import odintvtoons
    odintvtoons.tvshows().languages()

elif action == 'jspttvYears':
    from resources.lib.indexers import odintvtoons
    odintvtoons.tvshows().years()

elif action == 'wwtvshows':
    from resources.lib.indexers import wwtvshows
    wwtvshows.tvshows().get(url)


elif action == 'gtmaretvGenres':
    from resources.lib.indexers import wwtvshows
    wwtvshows.tvshows().genres()

elif action == 'gtmaretvNetworks':
    from resources.lib.indexers import wwtvshows
    wwtvshows.tvshows().networks()

elif action == 'gtmaretvLanguages':
    from resources.lib.indexers import wwtvshows
    wwtvshows.tvshows().languages()

elif action == 'gtmaretvYears':
    from resources.lib.indexers import wwtvshows
    wwtvshows.tvshows().years()


elif action == 'keymovie':
    from resources.lib.menus import movies
    movies.Movies().keymovie()

elif action == 'keytv':
    from resources.lib.menus import tvshows
    tvshows.TVshows().keytv()