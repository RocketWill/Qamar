# -*- coding: utf-8 -*-
import time


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl( path ):
        return path

    @staticmethod
    def buildStaticUrl(path):
        from application import app
        release_ver = app.config.get("RELEASE_VERSION")
        ver = "%s"%( int(time.time()) ) if not release_ver else release_ver
        #ver = "%s" % (int(time.time()))
        path =  "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl( path )