# -*- coding: utf-8 -*-
import cherrypy
import os

__all__ = [ 'SATool' ]

class SATool(cherrypy.Tool):
    def __init__(self, current_dir = "", log = None):
        """
        The SA tool is responsible for associating a SA session
        to the SA engine and attaching it to the current request.
        Since we are running in a multithreaded application,
        we use the scoped_session that will create a session
        on a per thread basis so that you don't worry about
        concurrency on the session object itself.

        This tools binds a session to the engine each time
        a requests starts and commits/rollbacks whenever
        the request terminates.
        """
        self.current_dir = current_dir
        self.log = log
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.bind_session,
                               priority=20)

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource',
                                      self.commit_transaction,
                                      priority=80)
        cherrypy.request.hooks.attach('on_end_resource',
                                      self.cleanup_files,
                                      priority=80)
    def bind_session(self):
        """
        Attaches a session to the request's scope by requesting
        the SA plugin to bind a session to the SA engine.
        """
#        session = cherrypy.engine.publish('bind-session').pop()
#        cherrypy.request.db = session

        session_online = cherrypy.engine.publish('bind-online-session').pop()
        session_offline = cherrypy.engine.publish('bind-offline-session').pop()
        session_cache = cherrypy.engine.publish('bind-cache-session').pop()

        cherrypy.request.db_online = session_online
        cherrypy.request.db_offline = session_offline
        cherrypy.request.db_cache = session_cache

    def commit_transaction(self):
        """
        Commits the current transaction or rolls back
        if an error occurs. Removes the session handle
        from the request's scope.
        """
#        if not hasattr(cherrypy.request, 'db'):
#            return
#        cherrypy.request.db = None
#        cherrypy.engine.publish('commit-session')

        if ((not hasattr(cherrypy.request, 'db_offline')) and (not hasattr(cherrypy.request, 'db_online'))):
            return

        cherrypy.request.db_online = None
        cherrypy.request.db_offline = None
        cherrypy.request.db_cache = None

        cherrypy.engine.publish('commit-online-session')
        cherrypy.engine.publish('commit-offline-session')
        cherrypy.engine.publish('commit-cache-session')


    def cleanup_files(self):
        "Remove the generated file and folder after the download"

        path_info = cherrypy.request.path_info

        if "download" in path_info:
            from LocalConfig import state_dir
            path = state_dir + "/" + cherrypy.request.params['filepath']

            self.log.info('cleanup: %s' % path)
            try:
                os.remove(path)
                self.log.info('cleanup: removed file %s' % path)
            except:
                  pass
            path = os.path.dirname(path)
            try:
                os.rmdir(path)
                self.log.info('cleanup: removed empty directory %s' % path)
            except:
                pass

