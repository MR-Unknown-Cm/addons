# -*- coding: utf-8 -*-

"""
plexOdus
"""


import threading
from resources.lib.modules import control,log_utils,trakt


control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))
traktCredentials = trakt.getTraktCredentialsInfo()

try:
    AddonVersion = control.addon('plugin.video.plexodus').getAddonInfo('version')
    RepoVersion = control.addon('repository.reponame').getAddonInfo('version')
    log_utils.log('################### plexOdus ######################', log_utils.LOGNOTICE)
    log_utils.log('####### CURRENT plexOdus VERSIONS REPORT ##########', log_utils.LOGNOTICE)
    log_utils.log('######### plexOdus PLUGIN VERSION: %s #########' % str(AddonVersion), log_utils.LOGNOTICE)
    log_utils.log('####### reponame REPOSITORY VERSION: %s #######' % str(RepoVersion), log_utils.LOGNOTICE)
    log_utils.log('################################################', log_utils.LOGNOTICE)

except:
    log_utils.log('############################# plexOdus ############################', log_utils.LOGNOTICE)
    log_utils.log('################# CURRENT plexOdus VERSIONS REPORT ################', log_utils.LOGNOTICE)
    log_utils.log('# ERROR GETTING plexOdus VERSION - Missing Repo of failed Install #', log_utils.LOGNOTICE)
    log_utils.log('################################################################', log_utils.LOGNOTICE)


def syncTraktLibrary():
    control.execute('RunPlugin(plugin://%s)' % 'plugin.video.plexodus/?action=tvshowsToLibrarySilent&url=traktcollection')
    control.execute('RunPlugin(plugin://%s)' % 'plugin.video.plexodus/?action=moviesToLibrarySilent&url=traktcollection')


def syncTraktWatched():
    control.execute('RunPlugin(plugin://%s)' % 'plugin.video.plexodus/?action=cachesyncTVShows')
    control.execute('RunPlugin(plugin://%s)' % 'plugin.video.plexodus/?action=cachesyncMovies')
    # if control.setting('trakt.notifications') == 'true':
        # control.notification(title = 'default', message = 'Trakt Watched Status Sync Complete', icon='default', time=1, sound=False)


if traktCredentials is True:
    syncTraktWatched()


if control.setting('autoTraktOnStart') == 'true':
    syncTraktLibrary()


if int(control.setting('schedTraktTime')) > 0:
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
    log_utils.log('#################### STARTING TRAKT SCHEDULING ################', log_utils.LOGNOTICE)
    log_utils.log('#################### SCHEDULED TIME FRAME '+ control.setting('schedTraktTime')  + ' HOURS ###############', log_utils.LOGNOTICE)
    timeout = 3600 * int(control.setting('schedTraktTime'))
    schedTrakt = threading.Timer(timeout, syncTraktLibrary)
    schedTrakt.start()



