# -*- coding: utf-8 -*-


import base64
import urlparse
import urllib
import hashlib
import re

from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import trakt
from resources.lib.modules import pyaes


RES_4K = ['4k', 'hd4k', 'hd4k ', '4khd', '4khd ', 'uhd', 'ultrahd', 'ultra hd', 'ultra high', '2160', '2160p', '2160i', 'hd2160', '2160hd',
                        '2160 ', '2160p ', '2160i ', 'hd2160 ', '2160hd ', '1716p', '1716i', 'hd1716', '1716hd', '1716p ', '1716i ', 'hd1716 ',
                        '1716hd ', '2664p', '2664i', 'hd2664', '2664hd', '2664p ', '2664i ', 'hd2664 ', '2664hd ', '3112p', '3112i', 'hd3112',
                        '3112hd', '3112p ', '3112i ', 'hd3112 ', '3112hd ', '2880p', '2880i', 'hd2880', '2880hd', '2880p ', '2880i ', 'hd2880 ',
                        '2880hd ']
RES_2K = ['2k', 'hd2k', 'hd2k ', '2khd', '2khd ', '2048p', '2048i', 'hd2048', '2048hd', '2048p ', '2048i ', 'hd2048 ', '2048hd ',
                        '1332p', '1332i', 'hd1332', '1332hd', '1332p ', '1332i ', 'hd1332 ', '1332hd ', '1556p', '1556i', 'hd1556', '1556hd',
                        '1556p ', '1556i ', 'hd1556 ', '1556hd ', ]

RES_1080 = ['1080', '1080p', '1080i', 'hd1080', '1080hd', '1080 ', '1080p ', '1080i ', 'hd1080 ', '1080hd ', '1200p', '1200i', 'hd1200',
                        '1200hd', '1200p ', '1200i ', 'hd1200 ', '1200hd ']
RES_HD = ['720', '720p', '720i', 'hd720', '720hd', 'hd', '720 ', '720p ', '720i ', 'hd720 ', '720hd ']
RES_SD = ['576', '576p', '576i', 'sd576', '576sd', '576 ', '576p ', '576i ', 'sd576 ', '576sd ', '480', '480p', '480i', 'sd480', '480sd',
                        '480 ', '480p ', '480i ', 'sd480 ', '480sd ', '360', '360p', '360i', 'sd360', '360sd', '360 ', '360p ', '360i ', 'sd360 ', '360sd ',
                        '240', '240p', '240i', 'sd240', '240sd', '240 ', '240p ', '240i ', 'sd240 ', '240sd ']
SCR = ['dvdscr', 'screener', 'scr', 'r5', 'r6', 'dvdscr ', 'r5 ', 'r6 ']
CAM = ['camrip', 'cam rip', 'tsrip', 'ts rip', 'hdcam', 'hd cam', 'hdts', 'hd ts', 'dvdcam', 'dvd cam', 'dvdts', 'dvd ts', 'cam', 'telesync',
                'tele sync', 'ts', 'camrip ', 'tsrip ', 'hcam', 'hdts ', 'dvdcam ', 'dvdts ', 'telesync ']


CODEC_H265 = ['hevc', 'h265', 'h.265', 'x265', 'x.265 ', '265 ']
CODEC_H264 = ['avc', 'h264', 'h.264', 'x264', 'x.264', '264 ']
CODEC_XVID = ['xvid', 'xvid ']
CODEC_DIVX = ['divx', 'divx ', 'div2', 'div2 ', 'div3', 'div3 ']
CODEC_MPEG = ['mp4', 'mpeg', 'm4v', 'mpg', 'mpg1', 'mpg2', 'mpg3', 'mpg4', 'mp4 ', 'mpeg ', 'msmpeg', 'msmpeg4', 'mpegurl',
                                'm4v ', 'mpg ', 'mpg1 ', 'mpg2 ', 'mpg3 ', 'mpg4 ', 'msmpeg ', 'msmpeg4 ']
CODEC_AVI  = ['avi']
CODEC_MKV  = ['mkv', 'mkv ', '.mkv', 'matroska', 'matroska ']


AUDIO_8CH = ['ch8', '8ch', 'ch7', '7ch', '7 1', 'ch7 1', '7 1ch', 'ch8 ', '8ch ', 'ch7 ', '7ch ', '.ddp']
AUDIO_6CH = ['ch6', '6ch', 'ch6', '6ch', '6 1', 'ch6 1', '6 1ch', '5 1', 'ch5 1', '5 1ch', '5.1.', 'ch6 ', '6ch ', 'ch6 ', '6ch ']
AUDIO_2CH = ['ch2', '2ch', 'stereo', 'dualaudio', 'dual-audio', 'dual', '2 0', 'ch2 0', '2 0ch', 'ch2 ', '2ch ', 'stereo ', 'dual audio', 'dual ']
AUDIO_1CH = ['ch1', '1ch', 'mono', 'monoaudio', 'ch1 0', '1 0ch', 'ch1 ', '1ch ', 'mono ']

VIDEO_3D = ['3d', 'sbs', 'hsbs', 'sidebyside', 'side by side', 'stereoscopic', 'tab', 'htab', 'topandbottom', 'top and bottom']



def is_anime(content, type, type_id):
    try:
        r = trakt.getGenre(content, type, type_id)
        return 'anime' in r or 'animation' in r
    except:
        return False


def get_release_quality(release_name, release_link=None):
    if release_name is None:
        return

    try:
        release_name = release_name.encode('utf-8')
    except:
        pass

    try:
        quality = None
        release_name = release_name.upper()
        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', release_name)
        fmt = re.split('\.|\(|\)|\[|\]|\s|-', fmt)
        fmt = [i.lower() for i in fmt]

        if any(value in fmt for value in RES_4K):
            quality = "4K"

        elif any(value in fmt for value in RES_1080):
            quality = "1080p"

        elif any(value in fmt for value in RES_HD):
            quality = "720p"

        elif any(value in fmt for value in RES_SD):
            quality = "480p"

        elif any(value in fmt for value in SCR):
            quality = 'SCR'

        elif any(value in fmt for value in CAM):
            quality = 'CAM'

        if not quality:
            if release_link:
                release_link = release_link.lower()
                try:
                    release_link = release_link.encode('utf-8')
                except:
                    pass

                if any(value in release_link for value in RES_4K):
                    quality = "4K"

                elif any(value in release_link for value in RES_1080):
                    quality = "1080p"

                elif any(value in release_link for value in RES_HD):
                    quality = "720p"

                elif any(value in release_link for value in RES_SD):
                    quality = "480p"

                elif any(value in release_link for value in SCR):
                    quality = 'SCR'

                elif any(value in release_link for value in CAM):
                    quality = 'CAM'
            else:
                quality = 'SD'

        info = []
        if any(value in release_name for value in VIDEO_3D):
            info.append('3D')

        if any(value in fmt for value in CODEC_H265):
            info.append('HEVC')

        return quality, info

    except:
        return 'SD', []


def getFileType(url):
    try:
        url = url.lower()
    except:
        url = str(url)

    type = ''

    if any(value in url for value in ['bluray', 'blu-ray']):
        type += ' BLURAY /'

    if any(value in url for value in ['.web-dl', '.webdl']):
        type += ' WEB-DL /'

    if any(value in url for value in ['hdrip', 'hd-rip']):
        type += ' HDRip /'

    if any(value in url for value in ['bd-r', 'bd.r', 'bdr', 'bd-rip', 'bd.rip', 'bdrip']):
        type += ' BD-R /'

    if any(value in url for value in ['.dd5.1', 'dolby-digital', 'dolby.digital']):
        type += ' DOLBYDIGITAL /'

    if any(value in url for value in ['.ddex', 'dolby-ex', 'dd-ex']):
        type += ' DOLBYDIGITAL-EX /'

    if any(value in url for value in ['dolby-digital-plus', 'dolby.digital.plus']):
        type += ' DOLBYDIGITAL-Plus /'

    if any(value in url for value in ['truehd', '.ddhd']):
        type += ' DOLBY-TRUEHD /'

    if 'atmos' in url:
        type += ' DOLBY-ATMOS /'

    if '.dts.' in url:
        type += ' DTS /'

    if any(value in url for value in ['dts-hd', 'dtshd']):
        type += ' DTS-HD /'

    if any(value in url for value in ['dts-es', 'dtses']):
        type += ' DTS-ES /'

    if any(value in url for value in ['dts-neo', 'dtsneo']):
        type += ' DTS-NEO /'

    if '.thx.' in url:
        type += ' THX /'

    if any(value in url for value in ['.thx-ex', 'thxex']):
        type += ' THX-EX /'

    if any(value in url for value in AUDIO_8CH):
        type += ' 8CH /'

    if any(value in url for value in AUDIO_6CH):
        type += ' 6CH /'

    if 'xvid' in url:
        type += ' XVID /'

    if 'divx' in url:
        type += ' DIVX /'

    if any(value in url for value in CODEC_MPEG):
        type += ' MPEG /'

    if '.avi' in url:
        type += ' AVI /'

    if 'ac3' in url:
        type += ' AC3 /'

    if any(value in url for value in CODEC_H264):
        type += ' x264 /'

    if any(value in url for value in CODEC_H265):
        type += ' x265 /'

    if any(value in url for value in CODEC_MKV):
        type += ' MKV /'

    if 'subs' in url: 
        if type != '':
            type += ' - WITH SUBS'
        else:
            type = 'SUBS'
    type = type.rstrip('/')
    return type


def check_sd_url(release_link):
    release_link = release_link.lower()
    try:
        release_link = release_link.encode('utf-8')
    except:
        pass

    try:
        if '2160' in release_link:
            quality = '4K'
        elif '4k' in release_link:
            quality = '4K'
        elif 'uhd' in release_link:
            quality = '4K'
        elif '1080' in release_link:
            quality = '1080p'
        elif '720' in release_link:
            quality = '720p'
        elif 'hd.' in release_link:
            quality = '720p'
        elif '.hd' in release_link:
            quality = '720p'
        elif 'HD' in release_link:
            quality = '720p'
        elif 'hdtv' in release_link:
            quality = '720p'
        elif 'bluray' in release_link:
            quality = '720p'
        elif 'BluRay' in release_link:
            quality = '720p'
        elif '.BluRay.' in release_link:
            quality = '720p'
        elif 'webrip' in release_link:
            quality = '720p'
        elif '.WEBRip.' in release_link:
            quality = '720p'
        elif any(i in ['dvdscr', 'r5', 'r6'] for i in release_link):
            quality = 'SCR'
        elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in release_link):
            quality = 'CAM'
        else:
            quality = 'SD'
        return quality
    except:
        return 'SD'


def check_direct_url(url):
    try:
        if '2160' in url:
            quality = '4K'
        elif '4k' in url:
            quality = '4K'
        elif '1080p' in url:
            quality = '1080p'
        elif '1080' in url:
            quality = '1080p'
        elif '720p' in url:
            quality = '720p'
        elif '720' in url:
            quality = '720p'
        elif 'hd' in url:
            quality = '720p'
        elif '.hd' in url:
            quality = '720p'
        elif 'HD' in url:
            quality = '720p'
        elif 'hdtv' in url:
            quality = '720p'
        elif 'bluray' in url:
            quality = '720p'
        elif 'BluRay' in url:
            quality = '720p'
        elif '480p' in url:
            quality = '480p'
        elif '480' in url:
            quality = '480p'
        elif any(i in ['dvdscr', 'r5', 'r6'] for i in url):
            quality = 'SCR'
        elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in url):
            quality = 'CAM'
        else:
            quality = 'SD'
        return quality
    except:
        return 'SD'


def check_url(url):
    try:
        if '2160p' in url:
            quality = '4K'
        elif '2160' in url:
            quality = '4K'
        elif '4k' in url:
            quality = '4K'
        elif 'uhd' in url:
            quality = '4K'
        elif '1080p' in url:
            quality = '1080p'
        elif '1080' in url:
            quality = '1080p'
        elif '720p' in url:
            quality = '720p'
        elif '720' in url:
            quality = '720p'
        elif '.hd.' in url:
            quality = '720p'
        elif 'hd' in url:
            quality = '720p'
        elif 'HD' in url:
            quality = '720p'
        elif 'hdtv' in url:
            quality = '720p'
        elif 'BluRay' in url:
            quality = '720p'
        elif '.BluRay.' in url:
            quality = '720p'
        elif '.WEBRip.' in url:
            quality = '720p'
        elif '480p' in url:
            quality = 'SD'
        elif '480' in url:
            quality = 'SD'
        elif any(i in ['dvdscr', 'r5', 'r6'] for i in url):
            quality = 'SCR'
        elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in url):
            quality = 'CAM'
        else:
            quality = 'SD'
        return quality
    except:
        return 'SD'


def label_to_quality(label):
    try:
        try:
            label = int(re.search('(\d+)', label).group(1))
        except:
            label = 0

        if label >= 2160:
            return '4K'
        elif label >= 1440:
            return '1440p'
        elif label >= 1080:
            return '1080p'
        elif 720 <= label < 1080:
            return '720p'
        elif label < 720:
            return 'SD'
    except:
        return 'SD'


def strip_domain(url):
    try:
        if url.lower().startswith('http') or url.startswith('/'):
            url = re.findall('(?://.+?|)(/.+)', url)[0]
        url = client.replaceHTMLCodes(url)
        url = url.encode('utf-8')
        return url
    except:
        return


def is_host_valid(url, domains):
    try:
        host = __top_domain(url)
        hosts = [domain.lower() for domain in domains if host and host in domain.lower()]
        if hosts and '.' not in host:
            host = hosts[0]
        if hosts and any([h for h in ['google', 'picasa', 'blogspot'] if h in host]):
            host = 'gvideo'
        if hosts and any([h for h in ['akamaized','ocloud'] if h in host]):
            host = 'CDN'
        return any(hosts), host
    except:
        return False, ''


def __top_domain(url):
    elements = urlparse.urlparse(url)
    domain = elements.netloc or elements.path
    domain = domain.split('@')[-1].split(':')[0]
    regex = "(?:www\.)?([\w\-]*\.[\w\-]{2,3}(?:\.[\w\-]{2,3})?)$"
    res = re.search(regex, domain)
    if res:
        domain = res.group(1)
    domain = domain.lower()
    return domain


def aliases_to_array(aliases, filter=None):
    try:
        if not filter:
            filter = []
        if isinstance(filter, str):
            filter = [filter]
        return [x.get('title') for x in aliases if not filter or x.get('country') in filter]
    except:
        return []


def append_headers(headers):
    return '|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(headers[key])) for key in headers])


def get_size(url):
    try:
        size = client.request(url, output='file_size')
        if size == '0':
            size = False
        size = convert_size(size)
        return size
    except:
        return False


def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    if size_name[i] == 'B' or size_name[i] == 'KB':
        return None
    return "%s %s" % (s, size_name[i])


def check_directstreams(url, hoster='', quality='SD'):
    urls = []
    host = hoster

    if 'google' in url or any(x in url for x in ['youtube.', 'docid=']):
        urls = directstream.google(url)

        if not urls:
            tag = directstream.googletag(url)
            if tag: urls = [{'quality': tag[0]['quality'], 'url': url}]

        if urls:
            host = 'gvideo'

    elif 'ok.ru' in url:
        urls = directstream.odnoklassniki(url)
        if urls: host = 'vk'

    elif 'vk.com' in url:
        urls = directstream.vk(url)
        if urls: host = 'vk'

    elif any(x in url for x in ['akamaized', 'blogspot', 'ocloud.stream']):
        urls = [{'url': url}]
        if urls: host = 'CDN'

    direct = True if urls else False

    if not urls:
        urls = [{'quality': quality, 'url': url}]

    return urls, host, direct


def evp_decode(cipher_text, passphrase, salt=None):
    cipher_text = base64.b64decode(cipher_text)
    if not salt:
        salt = cipher_text[8:16]
        cipher_text = cipher_text[16:]
    data = evpKDF(passphrase, salt)
    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(data['key'], data['iv']))
    plain_text = decrypter.feed(cipher_text)
    plain_text += decrypter.feed()
    return plain_text


def evpKDF(passwd, salt, key_size=8, iv_size=4, iterations=1, hash_algorithm="md5"):
    target_key_size = key_size + iv_size
    derived_bytes = ""
    number_of_derived_words = 0
    block = None
    hasher = hashlib.new(hash_algorithm)
    while number_of_derived_words < target_key_size:
        if block is not None:
            hasher.update(block)
        hasher.update(passwd)
        hasher.update(salt)
        block = hasher.digest()
        hasher = hashlib.new(hash_algorithm)
        for _i in range(1, iterations):
            hasher.update(block)
            block = hasher.digest()
            hasher = hashlib.new(hash_algorithm)
        derived_bytes += block[0: min(len(block), (target_key_size - number_of_derived_words) * 4)]
        number_of_derived_words += len(block) / 4
    return {"key": derived_bytes[0: key_size * 4], "iv": derived_bytes[key_size * 4:]}

