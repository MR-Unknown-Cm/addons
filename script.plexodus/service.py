# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import xbmcaddon


def main():
    if xbmc.getInfoLabel('Window(10000).Property(script.plexodus.service.started)'):
        # Prevent add-on updates from starting a new version of the addon
        return

    xbmcgui.Window(10000).setProperty('script.plexodus.service.started', '1')

    if xbmcaddon.Addon().getSetting('kiosk.mode') == 'true':
        xbmc.log('script.plexodus: Starting from service (Kiosk Mode)', xbmc.LOGNOTICE)
        xbmc.executebuiltin('RunScript(script.plexodus)')


if __name__ == '__main__':
    main()
