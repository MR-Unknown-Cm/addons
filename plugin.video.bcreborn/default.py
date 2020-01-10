# -*- coding: utf-8 -*-

'''
    Bone Crusher Reborn Add-on
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
        control.openSettings(query, "plugin.video.bcreborn")

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
        control.openSettings(query, 'plugin.video.bcreborn')

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
        # control.openSettings(query, "plugin.video.bcreborn")

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
    control.openSettings(query, "plugin.video.bcreborn")

elif action == "toggleAllHosters":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.hoster_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Hoster providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.bcreborn")

elif action == "toggleAllForeign":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.all_foreign_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Foregin providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.bcreborn")

elif action == "toggleAllSpanish":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.spanish_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Spanish providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.bcreborn")

elif action == "toggleAllGerman":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.german_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All German providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.bcreborn")

elif action == "toggleAllGreek":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.greek_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Greek providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.bcreborn")

elif action == "toggleAllPolish":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.polish_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Polish providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.bcreborn")

elif action == "toggleAllPaid":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.all_paid_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Paid providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.bcreborn")

elif action == "toggleAllDebrid":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.debrid_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Debrid providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.bcreborn")

elif action == "toggleAllTorrent":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.torrent_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
#    xbmc.log('All Torrent providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.bcreborn")

if action == "toggleDefaults":
    sourceList = []
    from resources.lib import sources
    sourceList = sources.all_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        default = control.getSettingDefault(source_setting)
        control.setSetting(source_setting, default)
#    xbmc.log('All providers = %s' % sourceList, 2)
    control.openSettings(query, "plugin.video.bcreborn")

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
##################################################################################################################
