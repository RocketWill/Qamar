# -*- coding: utf-8 -*-
import time



class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl( path ):
        return path

    @staticmethod
    def buildStaticUrl(path, show_ver = "Yes"):
        from application import app
        release_ver = app.config.get("RELEASE_VERSION")
        ver = "%s"%( int(time.time()) ) if not release_ver else release_ver
        #ver = "%s" % (int(time.time()))

        if show_ver == "Yes":
            path =  "/static" + path + "?ver=" + ver
        elif show_ver =="No":
            path = "/static" + path
        return UrlManager.buildUrl( path )

    @staticmethod
    def buildImageUrl(path):
        from application import app
        url = app.config['APP']['domain'] + app.config['UPLOAD']['prefix_url'] + path
        return url