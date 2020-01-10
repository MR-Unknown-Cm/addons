# -*- coding: utf-8 -*-

"""
    ego Add-on
"""

import os, sys, re, json, zipfile
import StringIO, urllib, urllib2, urlparse
import datetime, copy

from resources.lib.modules import trakt
from resources.lib.modules import cleangenre
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views
from resources.lib.modules import metacache
from resources.lib.modules import utils
from resources.lib.extensions import tools

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', ''))) if len(sys.argv) > 1 else dict()
action = params.get('action')


class Episodes:
    def __init__(self, type='show', notifications=True):
        self.list = []
        self.threads = []
        self.type = type
        self.lang = control.apiLanguage()['tvdb']
        self.season_special = False
        self.notifications = notifications
        control.playlist.clear()

        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours=5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.today_date = (self.datetime).strftime('%Y-%m-%d')

        self.fanart_tv_user = control.setting('fanart.tv.user')
        if self.fanart_tv_user == '' or self.fanart_tv_user is None:
            self.fanart_tv_user = 'cf0ebcc2f7b824bd04cf3a318f15c17d'
        self.user = self.fanart_tv_user + str('')
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/tv/%s'

        #        self.tvdb_key = control.setting('tvdb.user')
        #        if self.tvdb_key == '' or self.tvdb_key is None:
        #            self.tvdb_key = '1D62F2F90030C444'
        self.tvdb_key = 'MUQ2MkYyRjkwMDMwQzQ0NA=='
        self.tvdb_info_link = 'http://thetvdb.com/api/%s/series/%s/all/%s.zip' % (
            self.tvdb_key.decode('base64'), '%s', '%s')
        self.tvdb_by_query = 'http://thetvdb.com/api/GetSeries.php?seriesname=%s'
        self.tvdb_image = 'http://thetvdb.com/banners/'
        self.tvdb_poster = 'http://thetvdb.com/banners/_cache/'

        self.trakt_link = 'http://api.trakt.tv'
        self.trakt_user = control.setting('trakt.user').strip()
        self.onDeck_link = 'http://api.trakt.tv/sync/playback/episodes?extended=full&limit=40'
        self.traktlist_link = 'http://api.trakt.tv/users/%s/lists/%s/items'
        self.traktlists_link = 'http://api.trakt.tv/users/me/lists'
        self.traktwatchlist_link = 'http://api.trakt.tv/users/me/watchlist/episodes'
        self.traktlikedlists_link = 'http://api.trakt.tv/users/likes/lists?limit=1000000'
        self.mycalendar_link = 'http://api.trakt.tv/calendars/my/shows/date[29]/60/'
        self.trakthistory_link = 'http://api.trakt.tv/users/me/history/shows?limit=300'
        self.progress_link = 'http://api.trakt.tv/users/me/watched/shows'
        self.hiddenprogress_link = 'http://api.trakt.tv/users/hidden/progress_watched?limit=1000&type=show'
        self.traktcollection_link = 'http://api.trakt.tv/users/me/collection/shows'
        self.traktfeatured_link = 'http://api.trakt.tv/recommendations/shows?limit=40'
        self.traktunfinished_link = 'http://api.trakt.tv/sync/playback/episodes'

        self.tvmaze_link = 'http://api.tvmaze.com'
        self.added_link = 'http://api.tvmaze.com/schedule'
        self.calendar_link = 'http://api.tvmaze.com/schedule?date=%s'

        self.showunaired = control.setting('showunaired') or 'true'
        self.unairedcolor = control.setting('unaired.identify')
        if self.unairedcolor == '': self.unairedcolor = 'red'
        self.unairedcolor = self.getUnairedColor(self.unairedcolor)


    def getUnairedColor(self, n):
        if n == '0':
            n = 'blue'
        elif n == '1':
            n = 'red'
        elif n == '2':
            n = 'yellow'
        elif n == '3':
            n = 'deeppink'
        elif n == '4':
            n = 'cyan'
        elif n == '5':
            n = 'lawngreen'
        elif n == '6':
            n = 'gold'
        elif n == '7':
            n = 'magenta'
        elif n == '8':
            n = 'yellowgreen'
        elif n == '9':
            n = 'nocolor'
        else:
            n == 'blue'
        return n


    @classmethod
    def mark(self, title, imdb, tvdb, season, episode, watched=True):
        if watched:
            self.markWatch(title=title, imdb=imdb, tvdb=tvdb, season=season, episode=episode)
        else:
            self.markUnwatch(title=title, imdb=imdb, tvdb=tvdb, season=season, episode=episode)


    @classmethod
    def markWatch(self, title, imdb, tvdb, season, episode):
        control.busy()
        playcount.episodes(imdb, tvdb, season, episode, '7')
        control.hide()
        control.notification(title=35510, message=35513, icon='INFO', sound=True)


    @classmethod
    def markUnwatch(self, title, imdb, tvdb, season, episode):
        control.busy()
        playcount.episodes(imdb, tvdb, season, episode, '6')
        control.hide()
        control.notification(title=35511, message=35513, icon='INFO', sound=True)


    def sort(self, dateSort=False):
        try:
            attribute = int(control.setting('sort.shows.type'))
            reverse = int(control.setting('sort.shows.order')) == 1
            if attribute == 0: reverse = False
            if dateSort:
                dateOrder = int(control.setting('sort.shows.date'))
                if dateOrder > 0:
                    attribute = 4
                    reverse = dateOrder == 2
            if attribute > 0:
                if attribute == 1:
                    try:
                        self.list = sorted(self.list, key=lambda k: k['tvshowtitle'].lower(), reverse=reverse)
                    except:
                        self.list = sorted(self.list, key=lambda k: k['title'].lower(), reverse=reverse)
                elif attribute == 2:
                    self.list = sorted(self.list, key=lambda k: float(k['rating']), reverse=reverse)
                elif attribute == 3:
                    self.list = sorted(self.list, key=lambda k: int(k['votes'].replace(',', '')), reverse=reverse)
                elif attribute == 4:
                    for i in range(len(self.list)):
                        if not 'premiered' in self.list[i]: self.list[i]['premiered'] = ''
                    self.list = sorted(self.list, key=lambda k: k['premiered'], reverse=reverse)
                elif attribute == 5:
                    for i in range(len(self.list)):
                        if not 'added' in self.list[i]: self.list[i]['added'] = ''
                    self.list = sorted(self.list, key=lambda k: k['added'], reverse=reverse)
                elif attribute == 6:
                    for i in range(len(self.list)):
                        if not 'lastplayed' in self.list[i]: self.list[i]['lastplayed'] = ''
                    self.list = sorted(self.list, key=lambda k: k['lastplayed'], reverse=reverse)
            elif reverse:
                self.list = reversed(self.list)
        except:
            import traceback
            traceback.print_exc()


    def get(self, tvshowtitle, year, imdb, tvdb, season=None, episode=None, idx=True):
        from resources.lib.menus import seasons
        try:
            if idx is True:
                if season is None and episode is None:
                    self.list = cache.get(seasons.Seasons().tvdb_list, 1, tvshowtitle, year, imdb, tvdb, self.lang,
                                          '-1')
                elif episode is None:
                    self.list = cache.get(seasons.Seasons().tvdb_list, 1, tvshowtitle, year, imdb, tvdb, self.lang,
                                          season)
                else:
                    self.list = cache.get(seasons.Seasons().tvdb_list, 1, tvshowtitle, year, imdb, tvdb, self.lang,
                                          '-1')
                    num = \
                        [x for x, y in enumerate(self.list) if
                         y['season'] == str(season) and y['episode'] == str(episode)][-1]
                    self.list = [y for x, y in enumerate(self.list) if x >= num]

                self.episodeDirectory(self.list)
                return self.list
            else:
                self.list = seasons.Seasons().tvdb_list(tvshowtitle, year, imdb, tvdb, 'en', '-1')

                if not season is None:
                    self.list = [i for i in self.list if i['season'] == season]
                if not episode is None:
                    self.list = [i for i in self.list if i['episode'] == episode]
                return self.list
        except:
            pass


    def unfinished(self):
        try:
            self.list = cache.get(self.trakt_list, 0.3, self.traktunfinished_link, self.trakt_user, True)
            self.episodeDirectory(self.list)
            return self.list
        except:
            import traceback
            traceback.print_exc()
            try:
                invalid = (self.list is None or len(self.list) == 0)
            except:
                invalid = True
            if invalid:
                control.idle()
                control.notification(title=32326, message=33049, icon='INFO')


    def seasonCount(self, items, index):
        if not 'seasoncount' in items[index] or not items[index]['seasoncount']:
            thread = workers.Thread(self._seasonCount, items, index)
            self.threads.append(thread)
            thread.start()


    def seasonCountWait(self):
        [i.join() for i in self.threads]
        self.threads = []


    def _seasonCount(self, items, index):
        try:
            from resources.lib.menus import seasons
            items[index]['seasoncount'] = seasons.Seasons().seasonCount(items[index]['tvshowtitle'],
                                                                        items[index]['year'], items[index]['imdb'],
                                                                        items[index]['tvdb'], items[index]['season'])
        except:
            import traceback
            traceback.print_exc()


    def widget(self):
        if trakt.getTraktIndicatorsInfo() is True:
            setting = control.setting('tv.widget.alt')
        else:
            setting = control.setting('tv.widget')
        if setting == '2':
            self.calendar(self.progress_link)
        elif setting == '3':
            self.calendar(self.mycalendar_link)
        else:
            self.calendar(self.added_link)


    def calendar(self, url):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass

            if self.trakt_link in url and url == self.onDeck_link:
                self.blist = cache.get(self.trakt_episodes_list, 720, url, self.trakt_user, self.lang)
                self.list = []
                self.list = cache.get(self.trakt_episodes_list, 0.2, url, self.trakt_user, self.lang)
                self.list = self.list[::-1]

            elif self.trakt_link in url and url == self.progress_link:
                self.blist = cache.get(self.trakt_progress_list, 720, url, self.trakt_user, self.lang)
                self.list = []
                self.list = cache.get(self.trakt_progress_list, 0.2, url, self.trakt_user, self.lang)
                self.sort()

            elif self.trakt_link in url and url == self.mycalendar_link:
                self.blist = cache.get(self.trakt_episodes_list, 720, url, self.trakt_user, self.lang)
                self.list = []
                self.list = cache.get(self.trakt_episodes_list, 0.2, url, self.trakt_user, self.lang)
                self.sort(dateSort=True)

            elif self.trakt_link in url and '/users/' in url:
                self.list = cache.get(self.trakt_list, 0.2, url, self.trakt_user, True)
                self.list = self.list[::-1]

            elif self.trakt_link in url and not url == self.onDeck_link:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user, True)

            elif self.tvmaze_link in url and url == self.added_link:
                urls = [i['url'] for i in self.calendars(idx=False)][:5]
                self.list = []
                for url in urls:
                    self.list += cache.get(self.tvmaze_list, 720, url, True)

            elif self.tvmaze_link in url:
                self.list = cache.get(self.tvmaze_list, 1, url, False)

            self.episodeDirectory(self.list)
            return self.list
        except:
            pass


    def calendars(self, idx=True):
        m = control.lang(32060).encode('utf-8').split('|')
        try:
            months = [(m[0], 'January'), (m[1], 'February'), (m[2], 'March'), (m[3], 'April'), (m[4], 'May'),
                      (m[5], 'June'), (m[6], 'July'), (m[7], 'August'), (m[8], 'September'), (m[9], 'October'),
                      (m[10], 'November'), (m[11], 'December')]
        except:
            months = []

        d = control.lang(32061).encode('utf-8').split('|')
        try:
            days = [(d[0], 'Monday'), (d[1], 'Tuesday'), (d[2], 'Wednesday'), (d[3], 'Thursday'), (d[4], 'Friday'),
                    (d[5], 'Saturday'), (d[6], 'Sunday')]
        except:
            days = []

        for i in range(0, 30):
            try:
                name = (self.datetime - datetime.timedelta(days=i))
                name = (control.lang(32062) % (name.strftime('%A'), name.strftime('%d %B'))).encode('utf-8')
                for m in months:
                    name = name.replace(m[1], m[0])
                for d in days:
                    name = name.replace(d[1], d[0])
                try:
                    name = name.encode('utf-8')
                except:
                    pass
                url = self.calendar_link % (self.datetime - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                self.list.append({'name': name, 'url': url, 'image': 'calendar.png', 'action': 'calendar'})
            except:
                pass
        if idx is True: self.addDirectory(self.list)
        return self.list


    def userlists(self):
        userlists = []
        try:
            if not trakt.getTraktCredentialsInfo(): raise Exception()
            activity = trakt.getActivity()
        except:
            pass

        try:
            if not trakt.getTraktCredentialsInfo(): raise Exception()
            self.list = []
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link,
                                            self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 3, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass

        try:
            if not trakt.getTraktCredentialsInfo(): raise Exception()
            self.list = []
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link,
                                            self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 3, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
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

        for i in range(0, len(self.list)): self.list[i].update({'image': 'trakt.png', 'action': 'calendar'})

        # Watchlist
        if trakt.getTraktCredentialsInfo():
            self.list.insert(0, {'name': control.lang(32033).encode('utf-8'), 'url': self.traktwatchlist_link,
                                 'image': 'trakt.png', 'action': 'tvshows'})

        self.addDirectory(self.list, queue=True)
        return self.list


    def trakt_list(self, url, user, count=False):
        try:
            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i,
                                  (self.datetime - datetime.timedelta(days=int(i))).strftime('%Y-%m-%d'))

            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q

            itemlist = []
            items = trakt.getTraktAsJson(u)
        except:
            return

        for item in items:
            try:
                if not 'show' in item or not 'episode' in item:
                    raise Exception()

                title = item['episode']['title']
                if title is None or title == '': raise Exception()
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                season = item['episode']['season']
                season = re.sub('[^0-9]', '', '%01d' % int(season))
                if season == '0': raise Exception()
                season = season.encode('utf-8')

                episode = item['episode']['number']
                episode = re.sub('[^0-9]', '', '%01d' % int(episode))
                if episode == '0': raise Exception()
                episode = episode.encode('utf-8')

                tvshowtitle = item['show']['title']
                if tvshowtitle is None or tvshowtitle == '': raise Exception()
                tvshowtitle = client.replaceHTMLCodes(tvshowtitle)
                tvshowtitle = tvshowtitle.encode('utf-8')

                year = item['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                year = year.encode('utf-8')

                try:
                    progress = max(0, min(1, item['progress'] / 100.0))
                except:
                    progress = None

                try:
                    imdb = item['show']['ids']['imdb']
                    if imdb is None or imdb == '':
                        imdb = '0'
                    else:
                        imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                    imdb = imdb.encode('utf-8')
                except:
                    imdb = '0'

                try:
                    tmdb = item['show']['ids']['tmdb']
                    if tmdb is None or tmdb == '':
                        tmdb = '0'
                    else:
                        tmdb = re.sub('[^0-9]', '', str(tmdb))
                    tmdb = tmdb.encode('utf-8')
                except:
                    tmdb = '0'

                try:
                    tvdb = item['show']['ids']['tvdb']
                    if tvdb is None or tvdb == '':
                        tvdb = '0'
                    else:
                        tvdb = re.sub('[^0-9]', '', str(tvdb))
                    tvdb = tvdb.encode('utf-8')
                except:
                    tvdb = '0'

### episode IDS
                try:
                    episodeIDS = trakt.getEpisodeSummary(imdb, season, episode, full=False)
                    episodeIDS = episodeIDS.get('ids', {})
                except:
                    episodeIDS = {}
##------------------

                premiered = item['episode']['first_aired']
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')

                try:
                    added = item['show']['updated_at']
                except:
                    added = None

                try:
                    lastplayed = item['show']['last_watched_at']
                except:
                    lastplayed = None

                studio = item['show']['network']
                if studio is None: studio = '0'
                studio = studio.encode('utf-8')

                genre = item['show']['genres']
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = ' / '.join(genre)
                genre = genre.encode('utf-8')

                if 'duration' in item and not item['duration'] is None and not item['duration'] == '':
                    duration = item['duration']
                else:
                    try:
                        duration = str(item['show']['runtime'])
                    except:
                        duration = '0'
                    if duration is None: duration = '0'
                    duration = duration.encode('utf-8')

                try:
                    rating = str(item['episode']['rating'])
                except:
                    rating = '0'
                if rating is None or rating == '0.0': rating = '0'
                rating = rating.encode('utf-8')

                try:
                    votes = str(item['show']['votes'])
                except:
                    votes = '0'
                try:
                    votes = str(format(int(votes), ',d'))
                except:
                    pass
                if votes is None: votes = '0'
                votes = votes.encode('utf-8')

                if 'mpaa' in item and not item['mpaa'] is None and not item['mpaa'] == '':
                    mpaa = item['mpaa']
                else:
                    mpaa = item['show']['certification']
                    if mpaa is None: mpaa = '0'
                    mpaa = mpaa.encode('utf-8')

                plot = item['episode']['overview']
                if plot is None or plot == '': plot = item['show']['overview']
                if plot is None or plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)

                values = {'title': title, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle,
                            'year': year, 'premiered': premiered, 'added': added, 'lastplayed': lastplayed,
                            'status': 'Continuing', 'studio': studio, 'genre': genre, 'duration': duration,
                            'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot, 'imdb': imdb, 'tmdb': tmdb,
                            'tvdb': tvdb, 'progress': progress, 'episodeIDS': episodeIDS}

                if 'airday' in item and not item['airday'] is None and not item['airday'] == '':
                    values['airday'] = item['airday']
                if 'airtime' in item and not item['airtime'] is None and not item['airtime'] == '':
                    values['airtime'] = item['airtime']
                if 'airzone' in item and not item['airzone'] is None and not item['airzone'] == '':
                    values['airzone'] = item['airzone']
                try:
                    air = item['show']['airs']
                    if not 'airday' in item or item['airday'] is None or item['airday'] == '':
                        values['airday'] = air['day'].strip()
                    if not 'airtime' in item or item['airtime'] is None or item['airtime'] == '':
                        values['airtime'] = air['time'].strip()
                    if not 'airzone' in item or item['airzone'] is None or item['airzone'] == '':
                        values['airzone'] = air['timezone'].strip()
                except:
                    pass
                itemlist.append(values)

                if count:
                    self.seasonCount(itemlist, len(itemlist) - 1)
            except:
                pass
        if count:
            self.seasonCountWait()
        itemlist = itemlist[::-1]
        return itemlist


    def trakt_progress_list(self, url, user, lang):
        from resources.lib.menus import seasons
        try:
            url += '?extended=full'
            result = trakt.getTrakt(url)
            result = json.loads(result)
            items = []
        except:
            return

        for item in result:
            try:
                num_1 = 0
                for i in range(0, len(item['seasons'])):
                    num_1 += len(item['seasons'][i]['episodes'])
                num_2 = int(item['show']['aired_episodes'])
                if num_1 >= num_2:
                    raise Exception()

                season = str(item['seasons'][-1]['number'])
                season = season.encode('utf-8')

                episode = str(item['seasons'][-1]['episodes'][-1]['number'])
                episode = episode.encode('utf-8')

                tvshowtitle = item['show']['title']
                if tvshowtitle is None or tvshowtitle == '':
                    raise Exception()
                tvshowtitle = client.replaceHTMLCodes(tvshowtitle)
                tvshowtitle = tvshowtitle.encode('utf-8')

                year = item['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                if int(year) > int(self.datetime.strftime('%Y')):
                    raise Exception()

                try:
                    imdb = item['show']['ids']['imdb']
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                    imdb = imdb.encode('utf-8')
                except:
                    imdb = '0'

                try:
                    tmdb = item['show']['ids']['tmdb']
                    tmdb = re.sub('[^0-9]', '', str(tmdb))
                    tmdb = tmdb.encode('utf-8')
                except:
                    tmdb = '0'

                try:
                    tvdb = item['show']['ids']['tvdb']
                    tvdb = re.sub('[^0-9]', '', str(tvdb))
                    tvdb = tvdb.encode('utf-8')
                except:
                    tvdb = '0'

### episode IDS
                try:
                    episodeIDS = trakt.getEpisodeSummary(imdb, season, episode, full=False)
                    episodeIDS = episodeIDS.get('ids', {})
                except:
                    episodeIDS = {}
##------------------

                try:
                    added = item['show']['updated_at']
                except:
                    added = None

                try:
                    lastplayed = item['show']['last_watched_at']
                except:
                    try:
                        lastplayed = item['last_watched_at']
                    except:
                        lastplayed = None

                values = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'snum': season,
                              'enum': episode, 'added': added, 'lastplayed': lastplayed, 'episodeIDS': episodeIDS}

                try:
                    air = item['show']['airs']
                    values['airday'] = air['day'].strip()
                    values['airtime'] = air['time'].strip()
                    values['airzone'] = air['timezone'].strip()
                    values['duration'] = air['runtime']
                    values['mpaa'] = air['certification'].strip()
                except:
                    pass
                items.append(values)
            except:
                pass
        try:
            result = trakt.getTrakt(self.hiddenprogress_link)
            result = json.loads(result)
            result = [str(i['show']['ids']['tvdb']) for i in result]
            items = [i for i in items if not i['tvdb'] in result]
        except:
            pass

        def items_list(i):
            try:
                item = [x for x in self.blist if x['tvdb'] == i['tvdb'] and x['snum'] == i['snum'] and x['enum'] == i['enum']][0]
                item['action'] = 'episodes'
                self.list.append(item)
                return
            except:
                pass

            try:
                url = self.tvdb_info_link % (i['tvdb'], lang)
                data = urllib2.urlopen(url, timeout=10).read()

                zip = zipfile.ZipFile(StringIO.StringIO(data))
                result = zip.read('%s.xml' % lang)
                artwork = zip.read('banners.xml')
                zip.close()

                result = result.split('<Episode>')
                item = [x for x in result if '<EpisodeNumber>' in x]
                item2 = result[0]

                num = [x for x, y in enumerate(item) if
                       re.compile('<SeasonNumber>(.+?)</SeasonNumber>').findall(y)[0] == str(i['snum']) and
                       re.compile('<EpisodeNumber>(.+?)</EpisodeNumber>').findall(y)[0] == str(i['enum'])][-1]
                item = [y for x, y in enumerate(item) if x > num][0]

                premiered = client.parseDOM(item, 'FirstAired')[0]
                if premiered == '' or '-00' in premiered:
                    premiered = '0'
                premiered = client.replaceHTMLCodes(premiered)
                premiered = premiered.encode('utf-8')
                try:
                    added = i['added']
                except:
                    added = None

                try:
                    lastplayed = i['lastplayed']
                except:
                    lastplayed = None

                try:
                    status = client.parseDOM(item2, 'Status')[0]
                except:
                    status = ''
                if status == '':
                    status = 'Ended'
                status = client.replaceHTMLCodes(status)
                status = status.encode('utf-8')
                unaired = ''
                if status == 'Ended':
                    pass
                elif premiered == '0':
                    raise Exception()
                elif int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(self.today_date))):
                    unaired = 'true'
                    if self.showunaired != 'true':
                        raise Exception()

                title = client.parseDOM(item, 'EpisodeName')[0]
                if title == '':
                    title = '0'
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                season = client.parseDOM(item, 'SeasonNumber')[0]
                season = '%01d' % int(season)
                season = season.encode('utf-8')
                episode = client.parseDOM(item, 'EpisodeNumber')[0]
                episode = re.sub('[^0-9]', '', '%01d' % int(episode))
                episode = episode.encode('utf-8')
                seasoncount = seasons.Seasons.seasonCountParse(season=season, items=result)
                tvshowtitle = i['tvshowtitle']
                imdb, tmdb, tvdb = i['imdb'], i['tmdb'], i['tvdb']

### episode IDS
                try:
                    episodeIDS = trakt.getEpisodeSummary(imdb, season, episode, full=False)
                    episodeIDS = episodeIDS.get('ids', {})
                except:
                    episodeIDS = {}
##------------------

                year = i['year']
                try:
                    year = year.encode('utf-8')
                except:
                    pass
                tvshowyear = '0'
                tvshowyear = i['year']
                try:
                    tvshowyear = i['tvshowyear']
                except:
                    pass
                try:
                    tvshowyear = tvshowyear.encode('utf-8')
                except:
                    pass
                try:
                    poster = client.parseDOM(item2, 'poster')[0]
                except:
                    poster = ''
                if not poster == '':
                    poster = self.tvdb_image + poster
                else:
                    poster = '0'
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')
                try:
                    banner = client.parseDOM(item2, 'banner')[0]
                except:
                    banner = ''
                if not banner == '':
                    banner = self.tvdb_image + banner
                else:
                    banner = '0'
                banner = client.replaceHTMLCodes(banner)
                banner = banner.encode('utf-8')
                try:
                    fanart = client.parseDOM(item2, 'fanart')[0]
                except:
                    fanart = ''
                if not fanart == '':
                    fanart = self.tvdb_image + fanart
                else:
                    fanart = '0'
                fanart = client.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')
                try:
                    thumb = client.parseDOM(item, 'filename')[0]
                except:
                    thumb = ''
                if not thumb == '':
                    thumb = self.tvdb_image + thumb
                else:
                    thumb = '0'
                thumb = client.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')
                if not poster == '0':
                    pass
                elif not fanart == '0':
                    poster = fanart
                elif not banner == '0':
                    poster = banner

                if not banner == '0':
                    pass
                elif not fanart == '0':
                    banner = fanart
                elif not poster == '0':
                    banner = poster

                if not thumb == '0':
                    pass
                elif not fanart == '0':
                    thumb = fanart.replace(self.tvdb_image, self.tvdb_poster)
                elif not poster == '0':
                    thumb = poster

                try:
                    studio = client.parseDOM(item2, 'Network')[0]
                except:
                    studio = ''
                if studio == '': studio = '0'
                studio = client.replaceHTMLCodes(studio)
                studio = studio.encode('utf-8')
                try:
                    genre = client.parseDOM(item2, 'Genre')[0]
                except:
                    genre = ''
                genre = [x for x in genre.split('|') if not x == '']
                genre = ' / '.join(genre)
                if genre == '': genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')
                if 'duration' in i and not i['duration'] is None and not i['duration'] == '':
                    duration = i['duration']
                else:
                    try:
                        duration = client.parseDOM(item2, 'Runtime')[0]
                    except:
                        duration = ''
                    if duration == '': duration = '0'
                    duration = client.replaceHTMLCodes(duration)
                    duration = duration.encode('utf-8')
                try:
                    rating = client.parseDOM(item, 'Rating')[0]
                except:
                    rating = ''
                if rating == '': rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')
                try:
                    votes = client.parseDOM(item2, 'RatingCount')[0]
                except:
                    votes = '0'
                if votes == '': votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')
                if 'mpaa' in i and not i['mpaa'] is None and not i['mpaa'] == '':
                    mpaa = i['mpaa']
                else:
                    try:
                        mpaa = client.parseDOM(item2, 'ContentRating')[0]
                    except:
                        mpaa = ''
                    if mpaa == '': mpaa = '0'
                    mpaa = client.replaceHTMLCodes(mpaa)
                    mpaa = mpaa.encode('utf-8')
                try:
                    director = client.parseDOM(item, 'Director')[0]
                except:
                    director = ''
                director = [x for x in director.split('|') if not x == '']
                director = ' / '.join(director)
                if director == '': director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')
                try:
                    writer = client.parseDOM(item, 'Writer')[0]
                except:
                    writer = ''
                writer = [x for x in writer.split('|') if not x == '']
                writer = ' / '.join(writer)
                if writer == '': writer = '0'
                writer = client.replaceHTMLCodes(writer)
                writer = writer.encode('utf-8')
                try:
                    cast = client.parseDOM(item2, 'Actors')[0]
                except:
                    cast = ''
                cast = [x for x in cast.split('|') if not x == '']
                try:
                    cast = [(x.encode('utf-8'), '') for x in cast]
                except:
                    cast = []
                try:
                    plot = client.parseDOM(item, 'Overview')[0]
                except:
                    plot = ''
                if plot == '':
                    try:
                        plot = client.parseDOM(item2, 'Overview')[0]
                    except:
                        plot = ''
                if plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                values = {'title': title, 'seasoncount': seasoncount, 'season': season, 'episode': episode,
                          'year': year, 'tvshowtitle': tvshowtitle, 'tvshowyear': tvshowyear, 'premiered': premiered,
                          'added': added, 'lastplayed': lastplayed, 'status': status, 'studio': studio, 'genre': genre,
                          'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director,
                          'writer': writer, 'cast': cast, 'plot': plot, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': poster,
                          'banner': banner, 'fanart': fanart, 'thumb': thumb, 'snum': i['snum'], 'enum': i['enum'],
                          'unaired': unaired, 'episodeIDS': episodeIDS}

                values['action'] = 'episodes'
                if 'airday' in i and not i['airday'] is None and not i['airday'] == '':
                    values['airday'] = i['airday']
                if 'airtime' in i and not i['airtime'] is None and not i['airtime'] == '':
                    values['airtime'] = i['airtime']
                if 'airzone' in i and not i['airzone'] is None and not i['airzone'] == '':
                    values['airzone'] = i['airzone']
                self.list.append(values)
            except:
                pass

        items = items[:100]

        threads = []
        for i in items:
            threads.append(workers.Thread(items_list, i))
        [i.start() for i in threads]
        [i.join() for i in threads]
        return self.list


    def trakt_episodes_list(self, url, user, lang):
        from resources.lib.menus import seasons
        items = self.trakt_list(url, user)

        def items_list(i):
            try:
                item = [x for x in self.blist if x['tvdb'] == i['tvdb'] and x['season'] == i['season'] and x['episode'] == i['episode']][0]
                # item = [x for x in self.blist if
                        # x['tvdb'] == i['tvdb'] and x['season'] == i['season'] and x['episode'] == i['episode']][0]
                if item['poster'] == '0': raise Exception()
                self.list.append(item)
                return
            except:
                pass

            try:
                url = self.tvdb_info_link % (i['tvdb'], lang)
                data = urllib2.urlopen(url, timeout=10).read()

                zip = zipfile.ZipFile(StringIO.StringIO(data))
                result = zip.read('%s.xml' % lang)
                artwork = zip.read('banners.xml')
                zip.close()

                result = result.split('<Episode>')
                item = [(re.findall('<SeasonNumber>%01d</SeasonNumber>' % int(i['season']), x),
                         re.findall('<EpisodeNumber>%01d</EpisodeNumber>' % int(i['episode']), x), x) for x in result]
                item = [x[2] for x in item if len(x[0]) > 0 and len(x[1]) > 0][0]
                item2 = result[0]

                premiered = client.parseDOM(item, 'FirstAired')[0]
                if premiered == '' or '-00' in premiered: premiered = '0'
                premiered = client.replaceHTMLCodes(premiered)
                premiered = premiered.encode('utf-8')

                try:
                    status = client.parseDOM(item2, 'Status')[0]
                except:
                    status = ''
                if status == '': status = 'Ended'
                status = client.replaceHTMLCodes(status)
                status = status.encode('utf-8')

                title = client.parseDOM(item, 'EpisodeName')[0]
                if title == '': title = '0'
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                season = client.parseDOM(item, 'SeasonNumber')[0]
                season = '%01d' % int(season)
                season = season.encode('utf-8')

                episode = client.parseDOM(item, 'EpisodeNumber')[0]
                episode = re.sub('[^0-9]', '', '%01d' % int(episode))
                episode = episode.encode('utf-8')

                seasoncount = seasons.Seasons.seasonCountParse(season=season, items=result)

                tvshowtitle = i['tvshowtitle']
                imdb, tmdb, tvdb = i['imdb'], i['tmdb'], i['tvdb']

### episode IDS
                try:
                    episodeIDS = trakt.getEpisodeSummary(imdb, season, episode, full=False)
                    episodeIDS = episodeIDS.get('ids', {})
                except:
                    episodeIDS = {}
##------------------

                year = i['year']
                try:
                    year = year.encode('utf-8')
                except:
                    pass

                tvshowyear = i['year']
                try:
                    tvshowyear = i['tvshowyear']
                except:
                    pass
                try:
                    tvshowyear = tvshowyear.encode('utf-8')
                except:
                    pass

                try:
                    poster = client.parseDOM(item2, 'poster')[0]
                except:
                    poster = ''
                if not poster == '':
                    poster = self.tvdb_image + poster
                else:
                    poster = '0'
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try:
                    banner = client.parseDOM(item2, 'banner')[0]
                except:
                    banner = ''
                if not banner == '':
                    banner = self.tvdb_image + banner
                else:
                    banner = '0'
                banner = client.replaceHTMLCodes(banner)
                banner = banner.encode('utf-8')

                try:
                    fanart = client.parseDOM(item2, 'fanart')[0]
                except:
                    fanart = ''
                if not fanart == '':
                    fanart = self.tvdb_image + fanart
                else:
                    fanart = '0'
                fanart = client.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                try:
                    thumb = client.parseDOM(item, 'filename')[0]
                except:
                    thumb = ''
                if not thumb == '':
                    thumb = self.tvdb_image + thumb
                else:
                    thumb = '0'
                thumb = client.replaceHTMLCodes(thumb)
                thumb = thumb.encode('utf-8')

                if not poster == '0':
                    pass
                elif not fanart == '0':
                    poster = fanart
                elif not banner == '0':
                    poster = banner

                if not banner == '0':
                    pass
                elif not fanart == '0':
                    banner = fanart
                elif not poster == '0':
                    banner = poster

                if not thumb == '0':
                    pass
                elif not fanart == '0':
                    thumb = fanart.replace(self.tvdb_image, self.tvdb_poster)
                elif not poster == '0':
                    thumb = poster

                try:
                    studio = client.parseDOM(item2, 'Network')[0]
                except:
                    studio = ''
                if studio == '': studio = '0'
                studio = client.replaceHTMLCodes(studio)
                studio = studio.encode('utf-8')

                try:
                    genre = client.parseDOM(item2, 'Genre')[0]
                except:
                    genre = ''
                genre = [x for x in genre.split('|') if not x == '']
                genre = ' / '.join(genre)
                if genre == '': genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                if 'duration' in i and not i['duration'] is None and not i['duration'] == '':
                    duration = i['duration']
                else:
                    try:
                        duration = client.parseDOM(item2, 'Runtime')[0]
                    except:
                        duration = ''
                    if duration == '': duration = '0'
                    duration = client.replaceHTMLCodes(duration)
                    duration = duration.encode('utf-8')

                try:
                    rating = client.parseDOM(item, 'Rating')[0]
                except:
                    rating = ''
                if rating == '':
                    rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try:
                    votes = client.parseDOM(item2, 'RatingCount')[0]
                except:
                    votes = '0'
                if votes == '': votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                if 'mpaa' in i and not i['mpaa'] is None and not i['mpaa'] == '':
                    mpaa = i['mpaa']
                else:
                    try:
                        mpaa = client.parseDOM(item2, 'ContentRating')[0]
                    except:
                        mpaa = ''
                    if mpaa == '':
                        mpaa = '0'
                    mpaa = client.replaceHTMLCodes(mpaa)
                    mpaa = mpaa.encode('utf-8')

                try:
                    director = client.parseDOM(item, 'Director')[0]
                except:
                    director = ''
                director = [x for x in director.split('|') if not x == '']
                director = ' / '.join(director)
                if director == '':
                    director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try:
                    writer = client.parseDOM(item, 'Writer')[0]
                except:
                    writer = ''
                writer = [x for x in writer.split('|') if not x == '']
                writer = ' / '.join(writer)
                if writer == '': writer = '0'
                writer = client.replaceHTMLCodes(writer)
                writer = writer.encode('utf-8')

                try:
                    cast = client.parseDOM(item2, 'Actors')[0]
                except:
                    cast = ''
                cast = [x for x in cast.split('|') if not x == '']
                try:
                    cast = [(x.encode('utf-8'), '') for x in cast]
                except:
                    cast = []

                try:
                    plot = client.parseDOM(item, 'Overview')[0]
                except:
                    plot = ''
                if plot == '':
                    try:
                        plot = client.parseDOM(item2, 'Overview')[0]
                    except:
                        plot = ''
                if plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                values = {'title': title, 'seasoncount': seasoncount, 'season': season, 'episode': episode,
                          'year': year, 'tvshowtitle': tvshowtitle, 'tvshowyear': tvshowyear, 'premiered': premiered,
                          'status': status, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating,
                          'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast,
                          'plot': plot, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': poster, 'banner': banner,
                          'fanart': fanart, 'thumb': thumb, 'episodeIDS': episodeIDS}

                if 'airday' in i and not i['airday'] is None and not i['airday'] == '':
                    values['airday'] = i['airday']
                if 'airtime' in i and not i['airtime'] is None and not i['airtime'] == '':
                    values['airtime'] = i['airtime']
                if 'airzone' in i and not i['airzone'] is None and not i['airzone'] == '':
                    values['airzone'] = i['airzone']
                try:
                    air = i['show']['airs']
                    if not 'airday' in i or i['airday'] is None or i['airday'] == '':
                        values['airday'] = air['day'].strip()
                    if not 'airtime' in i or i['airtime'] is None or i['airtime'] == '':
                        values['airtime'] = air['time'].strip()
                    if not 'airzone' in i or i['airzone'] is None or i['airzone'] == '':
                        values['airzone'] = air['timezone'].strip()
                except:
                    pass
                self.list.append(values)
            except:
                pass

        items = items[:100]

        threads = []
        for i in items:
            threads.append(workers.Thread(items_list, i))
        [i.start() for i in threads]
        [i.join() for i in threads]
        return self.list


    def trakt_user_list(self, url, user):
        try:
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
                self.list.append({'name': name, 'url': url})
            except:
                pass
        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        #        self.list = sorted(self.list, key=lambda k: re.sub('(^the |^a |^an )', '', k['name'].lower()))
        return self.list


    def tvmaze_list(self, url, limit, count=True):
        try:
            result = client.request(url)
            itemlist = []
            items = json.loads(result)
        except:
            return

        for item in items:
            try:
                if not 'english' in item['show']['language'].lower():
                    raise Exception()

                if limit is True and not 'scripted' in item['show']['type'].lower():
                    raise Exception()

                try:
                    tvshowtitle = (item.get('show', {}).get('name', 0)).encode('utf-8')
                except:
                    raise Exception()

                try:
                    title = (item.get('name', 0)).encode('utf-8')
                except:
                    raise Exception()

                season = item['season']
                season = re.sub('[^0-9]', '', '%01d' % int(season))
                if season == '0':
                    raise Exception()
                season = season.encode('utf-8')

                episode = item['number']
                episode = re.sub('[^0-9]', '', '%01d' % int(episode))
                if episode == '0':
                    raise Exception()
                episode = episode.encode('utf-8')

                year = item['show']['premiered']
                year = re.findall('(\d{4})', year)[0]
                year = year.encode('utf-8')

                try:
                    tvshowyear = item['show']['year']
                except:
                    tvshowyear = year

                try:
                    imdb = (item.get('show', {}).get('externals', {}).get('imdb', 0)).encode('utf-8')
                except:
                    imdb = '0'

                tmdb = '0'

                try:
                    tvdb = str(item.get('show', {}).get('externals', {}).get('thetvdb', 0))
                    tvdb = tvdb.encode('utf-8')
                except:
                    tvdb = '0'

### episode IDS
                try:
                    episodeIDS = trakt.getEpisodeSummary(imdb, season, episode, full=False)
                    episodeIDS = episodeIDS.get('ids', {})
                except:
                    episodeIDS = {}
##------------------

                try:
                    poster = (item.get('show', {}).get('image', {}).get('original', 0)).encode('utf-8')
                except:
                    poster = '0'

                try:
                    thumb1 = item['show']['image']['original']
                except:
                    thumb1 = '0'
                try:
                    thumb2 = item['image']['original']
                except:
                    thumb2 = '0'
                if thumb2 is None or thumb2 == '0':
                    thumb = thumb1
                else:
                    thumb = thumb2
                if thumb is None or thumb == '': thumb = '0'
                thumb = thumb.encode('utf-8')

                premiered = item['airdate']
                try:
                    premiered = re.findall('(\d{4}-\d{2}-\d{2})', premiered)[0]
                except:
                    premiered = '0'
                premiered = premiered.encode('utf-8')

                try:
                    studio = (item.get('show', {}).get('network', {}).get('name', 0)).encode('utf-8')
                except:
                    studio = '0'

                try:
                    genre = item['show']['genres']
                except:
                    genre = '0'
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = ' / '.join(genre)
                genre = genre.encode('utf-8')

                try:
                    duration = str(item.get('show', {}).get('runtime', 0))
                    duration = duration.encode('utf-8')
                except:
                    duration = '0'

                try:
                    rating = str(item.get('show', {}).get('rating', {}).get('average', 0))
                    rating = rating.encode('utf-8')
                except:
                    rating = '0'

                try:
                    status = str(item.get('show', {}).get('status', 0))
                    status = status.encode('utf-8')
                except:
                    status = '0'

                try:
                    plot = item.get('show', {}).get('summary', 0)
                    plot = re.sub('<.+?>|</.+?>|\n', '', plot)
                except:
                    plot = '0'
                plot = plot.encode('utf-8')
                # log_utils.log('plot = %s' % plot, __name__, log_utils.LOGDEBUG)

                values = {'title': title, 'season': season, 'episode': episode, 'year': year, 'tvshowtitle': tvshowtitle, 'tvshowyear': tvshowyear,
                                'premiered': premiered, 'status': status, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating,
                                'plot': plot, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': poster, 'thumb': thumb, 'episodeIDS': episodeIDS}

                if 'airday' in item and not item['airday'] is None and not item['airday'] == '':
                    values['airday'] = item['airday']
                if 'airtime' in item and not item['airtime'] is None and not item['airtime'] == '':
                    values['airtime'] = item['airtime']
                if 'airzone' in item and not item['airzone'] is None and not item['airzone'] == '':
                    values['airzone'] = item['airzone']

                try:
                    air = item['show']['airs']
                    if not 'airday' in item or item['airday'] is None or item['airday'] == '':
                        values['airday'] = air['day'].strip()
                    if not 'airtime' in item or item['airtime'] is None or item['airtime'] == '':
                        values['airtime'] = air['time'].strip()
                    if not 'airzone' in item or item['airzone'] is None or item['airzone'] == '':
                        values['airzone'] = air['timezone'].strip()
                except:
                    pass

                itemlist.append(values)

                if count:
                    self.seasonCount(itemlist, len(itemlist) - 1)
            except:
                pass
        if count:
            self.seasonCountWait()

        itemlist = itemlist[::-1]
        return itemlist


    def metadataRetrieve(self, title, year, imdb, tvdb):
        self.list = [{'metacache': False, 'title': title, 'year': year, 'imdb': imdb, 'tvdb': tvdb}]
        self.worker()
        return self.list[0]


    def episodeDirectory(self, items):
        # Retrieve additional metadata if not super info was retireved (eg: Trakt lists, such as Unfinished and History)
        try:
            if not 'extended' in items[0] or not items[0]['extended']:
                from resources.lib.menus import tvshows
                show = tvshows.TVshows(type=self.type)
                show.list = copy.deepcopy(self.list)
                show.worker()
                for i in range(len(self.list)):
                    self.list[i] = dict(show.list[i].items() + self.list[i].items())
        except:
            import traceback
            traceback.print_exc()
            pass

        if isinstance(items, dict) and 'value' in items:
            items = items['value']
        if isinstance(items, basestring):
            try:
                items = json.loads(items)
            except:
                pass

        if items is None or len(items) == 0:
            control.idle()
            control.notification(title=32326, message=33049, icon='INFO')
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()
        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        try:
            multi = [i['tvshowtitle'] for i in items]
        except:
            multi = []
        multi = len([x for y, x in enumerate(multi) if x not in multi[:y]])
        multi = True if multi > 1 else False

        try:
            sysaction = items[0]['action']
        except:
            sysaction = ''

        isFolder = False if not sysaction == 'episodes' else True
        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'

        airEnabled = control.setting('tvshows.air.enabled')
        if airEnabled == 'true':
            airZone = control.setting('tvshows.air.zone')
            airLocation = control.setting('tvshows.air.location')
            airFormat = control.setting('tvshows.air.format')
            airFormatDay = control.setting('tvshows.air.day')
            airFormatTime = control.setting('tvshows.air.time')
            airBold = control.setting('tvshows.air.bold')
            airLabel = '[B]' + control.lang(35032).encode('utf-8') + '[/B]' + ': '

        # try:
            # isOld = False;
            # control.item().getArt('type')
        # except:
            # isOld = True
        if control.setting('hosts.mode') == '2' or control.setting('enable.upnext') == 'true':
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
        tvshowBrowserMenu = control.lang(32071).encode('utf-8')
        addToLibrary = control.lang(32551).encode('utf-8')

        for i in items:
            try:
                imdb, tvdb, year, season, episode, premiered = i['imdb'], i['tvdb'], i['year'], i['season'], i['episode'], i['premiered']
                if not 'label' in i:
                    i['label'] = i['title']

                if i['label'] == '0':
                    label = '%sx%02d . %s %s' % (i['season'], int(i['episode']), 'Episode', i['episode'])
                else:
                    label = '%sx%02d . %s' % (i['season'], int(i['episode']), i['label'])

                if self.season_special is False and control.setting('tv.specials') == 'true':
                    self.season_special = True if int(season) == 0 else False

                if multi is True:
                    label = '%s - %s' % (i['tvshowtitle'], label)

                try:
                    labelProgress = label + ' [' + str(int(i['progress'] * 100)) + '%]'
                except:
                    labelProgress = label

                try:
                    if i['unaired'] == 'true':
                        labelProgress = '[COLOR %s][I]%s[/I][/COLOR]' % (self.unairedcolor, labelProgress)
                except:
                    pass

                systitle = urllib.quote_plus(i['title'])
                systvshowtitle = urllib.quote_plus(i['tvshowtitle'])
                syspremiered = urllib.quote_plus(i['premiered'])

                try:
                    seasoncount = i['seasoncount']
                except:
                    seasoncount = None

                # UpNext requires all data
                # meta = dict((k, v) for k, v in i.iteritems() if not v == '0')
                meta = dict((k, v) for k, v in i.iteritems())
                meta.update({'mediatype': 'episode'})
                meta.update({'trailer': '%s?action=trailer&name=%s&imdb=%s' % (sysaddon, systvshowtitle, imdb)})

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
                except: pass
                try:
                    meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except: pass
                try:
                    meta.update({'title': i['label']})
                except: pass
                try:
                    meta.update({'year': re.findall('(\d{4})', i['premiered'])[0]})
                except: pass
                try:
                    # Kodi uses the year (the year the show started) as the year for the episode. Change it from the premiered date.
                    meta.update({'tvshowyear': i['year']})
                except: pass
                if airEnabled == 'true':
                    air = []
                    airday = None
                    airtime = None
                    if 'airday' in meta and not meta['airday'] is None and not meta['airday'] == '':
                        airday = meta['airday']
                    if 'airtime' in meta and not meta['airtime'] is None and not meta['airtime'] == '':
                        airtime = meta['airtime']
                        if 'airzone' in meta and not meta['airzone'] is None and not meta['airzone'] == '':
                            if airZone == '1':
                                zoneTo = meta['airzone']
                            elif airZone == '2':
                                # zoneTo = tools.Time.ZoneUtc
                                zoneTo = 'utc'
                            else:
                                # zoneTo = tools.Time.ZoneLocal
                                zoneTo = 'local'

                            if airFormatTime == '1':
                                formatOutput = '%I:%M'
                            elif airFormatTime == '2':
                                formatOutput = '%I:%M %p'
                            else:
                                formatOutput = '%H:%M'

                            abbreviate = airFormatDay == '1'
                            airtime = tools.Time.convert(stringTime=airtime, stringDay=airday, zoneFrom=meta['airzone'],
                                                         zoneTo=zoneTo, abbreviate=abbreviate,
                                                         formatOutput=formatOutput)
                            if airday:
                                airday = airtime[1]
                                airtime = airtime[0]
                    if airday: air.append(airday)
                    if airtime: air.append(airtime)
                    if len(air) > 0:
                        if airFormat == '0':
                            air = airtime
                        elif airFormat == '1':
                            air = airday
                        elif airFormat == '2':
                            air = air = ' '.join(air)

                        if airLocation == '0' or airLocation == '1':
                            air = '[%s]' % air

                        if airBold: air = '[B]' + str(air) + '[/B]'

                        if airLocation == '0':
                            labelProgress = '%s %s' % (air, labelProgress)
                        elif airLocation == '1':
                            labelProgress = '%s %s' % (labelProgress, air)
                        elif airLocation == '2':
                            meta['plot'] = '%s%s\r\n%s' % (airLabel, air, meta['plot'])
                        elif airLocation == '3':
                            meta['plot'] = '%s\r\n%s%s' % (meta['plot'], airLabel, air)

                poster = '0'
                if poster == '0' and 'poster3' in i: poster = i['poster3']
                if poster == '0' and 'poster2' in i: poster = i['poster2']
                if poster == '0' and 'poster' in i: poster = i['poster']

                icon = '0'
                if icon == '0' and 'icon3' in i: icon = i['icon3']
                if icon == '0' and 'icon2' in i: icon = i['icon2']
                if icon == '0' and 'icon' in i: icon = i['icon']

                thumb = '0'
                if thumb == '0' and 'thumb3' in i: thumb = i['thumb3']
                if thumb == '0' and 'thumb2' in i: thumb = i['thumb2']
                if thumb == '0' and 'thumb' in i: thumb = i['thumb']

                banner = '0'
                if banner == '0' and 'banner3' in i: banner = i['banner3']
                if banner == '0' and 'banner2' in i: banner = i['banner2']
                if banner == '0' and 'banner' in i: banner = i['banner']

                fanart = '0'
                if settingFanart:
                    if fanart == '0' and 'fanart3' in i: fanart = i['fanart3']
                    if fanart == '0' and 'fanart2' in i: fanart = i['fanart2']
                    if fanart == '0' and 'fanart' in i: fanart = i['fanart']

                clearlogo = '0'
                if clearlogo == '0' and 'clearlogo' in i: clearlogo = i['clearlogo']

                clearart = '0'
                if clearart == '0' and 'clearart' in i: clearart = i['clearart']

                if poster == '0': poster = addonPoster
                if icon == '0': icon = poster
                if thumb == '0': thumb = poster
                if banner == '0': banner = addonBanner
                if fanart == '0': fanart = addonFanart

                art = {}
                if not poster == '0' and not poster is None:
                    art.update({'poster': poster, 'tvshow.poster': poster, 'season.poster': poster})
                if not fanart == '0' and not fanart is None:
                    art.update({'fanart' : fanart})
                if not icon == '0' and not icon is None:
                    art.update({'icon': icon})
                if not thumb == '0' and not thumb is None:
                    art.update({'thumb': thumb})
                if not banner == '0' and not banner is None:
                    art.update({'banner': banner})
                if not clearlogo == '0' and not clearlogo is None:
                    art.update({'clearlogo': clearlogo})
                if not clearart == '0' and not clearart is None:
                    art.update({'clearart': clearart})


####-Context Menu and Overlays-####
                cm = []

                if traktCredentials is True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&tvdb=%s&season=%s&episode=%s)' % (
                                                sysaddon, systvshowtitle, imdb, tvdb, season, episode)))
                try:
                    indicators = playcount.getTVShowIndicators()
                    overlay = int(playcount.getEpisodeOverlay(indicators, imdb, tvdb, season, episode))
                    watched = overlay == 7
                    if watched:
                        meta.update({'playcount': 1, 'overlay': 7})
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=episodePlaycount&imdb=%s&tvdb=%s&season=%s&episode=%s&query=6)' % (
                                                sysaddon, imdb, tvdb, season, episode)))
                    else:
                        meta.update({'playcount': 0, 'overlay': 6})
                        cm.append((watchedMenu, 'RunPlugin(%s?action=episodePlaycount&imdb=%s&tvdb=%s&season=%s&episode=%s&query=7)' % (
                                                sysaddon, imdb, tvdb, season, episode)))
                except:
                    import traceback
                    traceback.print_exc()
                    pass

                sysmeta = urllib.quote_plus(json.dumps(meta))
                sysart = urllib.quote_plus(json.dumps(art))
                syslabelProgress = urllib.quote_plus(labelProgress)

                url = '%s?action=play&title=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=%s&meta=%s&t=%s' % (
                                        sysaddon, systitle, year, imdb, tvdb, season, episode, systvshowtitle, syspremiered, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)

                if isFolder is True:
                    url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s&season=%s&episode=%s' % (
                                        sysaddon, systvshowtitle, year, imdb, tvdb, season, episode)

                cm.append((playlistManagerMenu, 'RunPlugin(%s?action=playlistManager&name=%s&url=%s&meta=%s&art=%s)' % (
                                        sysaddon, syslabelProgress, sysurl, sysmeta, sysart)))
                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem&name=%s)' % (sysaddon, syslabelProgress)))

                if multi is True:
                    cm.append((tvshowBrowserMenu, 'Container.Update(%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s,return)' % (
                                        sysaddon, systvshowtitle, year, imdb, tvdb)))
                if isFolder is False:
                    cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (
                                        sysaddon, sysurl, sysmeta)))
                # if isOld is True:
                    # cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))
                cm.append((addToLibrary, 'RunPlugin(%s?action=tvshowToLibrary&tvshowtitle=%s&year=%s&imdb=%s&tvdb=%s)' % (
                                        sysaddon, systvshowtitle, year, imdb, tvdb)))
                cm.append(('[COLOR red]BoneCrusher Reborn Settings[/COLOR]', 'RunPlugin(%s?action=openSettings&query=(0,0))' % sysaddon))
####################################

                item = control.item(label=labelProgress)

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
                    if control.setting('tv.specials') == 'false' or self.season_special is False:
                        total_seasons = total_seasons - 1
                    item.setProperty('TotalSeasons', str(total_seasons))

                if 'episodeIDS' in i:
                    item.setUniqueIDs(i['episodeIDS'])
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
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

                if control.setting('auto.playlistcreate') == 'true':
                    control.playlist.add(url=url, listitem=item)

            except:
                import traceback
                traceback.print_exc()
                pass
        # Show multi as show, in order to display unwatched count.
        if multi:
            control.content(syshandle, 'tvshows')
            control.directory(syshandle, cacheToDisc=True)
            views.setView('shows', {'skin.estuary': 55, 'skin.confluence': 500})
        else:
            control.content(syshandle, 'episodes')
            control.directory(syshandle, cacheToDisc=True)
            views.setView('episodes', {'skin.estuary': 55, 'skin.confluence': 504})


    def addDirectory(self, items, queue=False):
        if items is None or len(items) == 0:
            control.hide()
            control.notification(title=32326, message=33049, icon='INFO')
            sys.exit()

        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])

        addonFanart = control.addonFanart()
        addonThumb = control.addonThumb()
        artPath = control.artPath()
        queueMenu = control.lang(32065).encode('utf-8')

        for i in items:
            try:
                name = i['name']
                link = i['url']
                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib.quote_plus(link)
                except:
                    pass

                item = control.item(label=name)

                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath is None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb

                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart is None:
                    item.setProperty('Fanart_Image', addonFanart)

                cm = []
                if queue is True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
