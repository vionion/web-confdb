# -*- coding: utf-8 -*-
import cherrypy

class Root(object):
    @cherrypy.expose
    def index(self):
        # Get the SQLAlchemy session associated
        # with this request.
        # It'll be released once the request
        # processing terminates
        db = cherrypy.request.db

        return "Hello World"
        
if __name__ == '__main__':
    # Register the SQLAlchemy plugin
    from saplugin import SAEnginePlugin
#    SAEnginePlugin(cherrypy.engine, 'oracle://cms_hlt_gdr:convertiMi!@(DESCRIPTION = (LOAD_BALANCE=on) (FAILOVER=ON) (ADDRESS = (PROTOCOL = TCP)(HOST = int2r2-s.cern.ch)(PORT = 10121)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = int2r_nolb.cern.ch)))').subscribe()
    
    SAEnginePlugin(cherrypy.engine, 'oracle://cms_hlt_gdr_r:convertMe!@(DESCRIPTION = (LOAD_BALANCE=on) (FAILOVER=ON) (ADDRESS = (PROTOCOL = TCP)(HOST = cmsr1-s.cern.ch)(PORT = 10121)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = cms_cond.cern.ch)))').subscribe()
    #'sqlite:///my.db' cmsr.cern.ch

    # Register the SQLAlchemy tool
    from satool import SATool
    cherrypy.tools.db = SATool()
    
    cherrypy.quickstart(Root(), '', {'/': {'tools.db.on': True}})

    