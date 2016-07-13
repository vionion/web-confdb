# -*- coding: utf-8 -*-
import cherrypy
from cherrypy.process import wspbus, plugins
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Sequence
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from confdb_v2.tables import *

__all__ = ['SAEnginePlugin']

class SAEnginePlugin(plugins.SimplePlugin):
    def __init__(self, bus, connection_string):
        """
        The plugin is registered to the CherryPy engine and therefore
        is part of the bus (the engine *is* a bus) registery.

        We use this plugin to create the SA engine. At the same time,
        when the plugin starts we create the tables into the database
        using the mapped class of the global metadata.
        """
        plugins.SimplePlugin.__init__(self, bus)

#        self.sa_engine = None
#        self.connection_string = connection_string
#        self.session = scoped_session(sessionmaker(autoflush=True, autocommit=False))

        self.sa_engine_online = None
        self.connection_string_online = connection_string.connectUrlonline
        self.session_online = scoped_session(sessionmaker(autoflush=True,
                                                   autocommit=False))

        self.sa_engine_offline = None
        self.connection_string_offline = connection_string.connectUrloffline
        self.session_offline = scoped_session(sessionmaker(autoflush=True,
                                                   autocommit=False))

        self.sa_engine_cache = None
        self.connection_string_cache = connection_string.connectUrlcache
        self.session_cache = scoped_session(sessionmaker(autoflush=True,
                                                   autocommit=False))

    def start(self):
        self.bus.log('Starting up DBs access')

#        self.sa_engine = create_engine(self.connection_string, echo=False)
#        self.bus.subscribe("bind-session", self.bind)
#        self.bus.subscribe("commit-session", self.commit)
#        Base.prepare(self.sa_engine, reflect=True)

        self.sa_engine_offline = create_engine(self.connection_string_offline, echo=False)
        self.sa_engine_online = create_engine(self.connection_string_online, echo=False)
        self.sa_engine_cache = create_engine(self.connection_string_cache, echo=False)

        self.bus.subscribe("bind-online-session", self.bind_online)
        self.bus.subscribe("bind-offline-session", self.bind_offline)
        self.bus.subscribe("bind-cache-session", self.bind_cache)

        self.bus.subscribe("commit-online-session", self.commit_online)
        self.bus.subscribe("commit-offline-session", self.commit_offline)
        self.bus.subscribe("commit-cache-session", self.commit_cache)

        self.bus.log('"BASE TO DO')

        Base.prepare(self.sa_engine_offline, reflect=True)

        self.bus.log('"BASE DONE')


    def stop(self):
        self.bus.log('Stopping down DBs access')
#        self.bus.unsubscribe("bind-session", self.bind)
#        self.bus.unsubscribe("commit-session", self.commit)
#        if self.sa_engine:
#            self.sa_engine.dispose()
#            self.sa_engine = None


        self.bus.unsubscribe("bind-online-session", self.bind_online)
        self.bus.unsubscribe("bind-offline-session", self.bind_offline)
        self.bus.unsubscribe("bind-cache-session", self.bind_offline)

        self.bus.unsubscribe("commit-online-session", self.commit_online)
        self.bus.unsubscribe("commit-offline-session", self.commit_offline)
        self.bus.unsubscribe("commit-cache-session", self.commit_cache)


        if self.sa_engine_online:
            self.sa_engine_online.dispose()
            self.sa_engine_online = None

        if self.sa_engine_offline:
            self.sa_engine_offline.dispose()
            self.sa_engine_offline = None

        if self.sa_engine_cache:
            self.sa_engine_cache.dispose()
            self.sa_engine_cache = None

#    def bind(self):
#        """
#        Whenever this plugin receives the 'bind-session' command, it applies
#        this method and to bind the current session to the engine.
#
#        It then returns the session to the caller.
#        """
#        self.session.configure(bind=self.sa_engine)
#        return self.session

    def bind_online(self):
        """
        Whenever this plugin receives the 'bind-online-session' command, it applies
        this method and to bind the current session to the engine.

        It then returns the session to the caller.
        """

        self.session_online.configure(bind=self.sa_engine_online)
        return self.session_online

    def bind_offline(self):
        """
        Whenever this plugin receives the 'bbind-offline-session' command, it applies
        this method and to bind the current session to the engine.

        It then returns the session to the caller.
        """

        self.session_offline.configure(bind=self.sa_engine_offline)
        return self.session_offline


    def bind_cache(self):
        """
        Whenever this plugin receives the 'bind-session' command, it applies
        this method and to bind the current session to the engine.

        It then returns the session to the caller.
        """
        
        self.session_cache.configure(bind=self.sa_engine_cache)
        return self.session_cache

#    def commit(self):
#        """
#        Commits the current transaction or rollbacks if an error occurs.
#
#        In all cases, the current session is unbound and therefore
#        not usable any longer.
#        """
#        try:
#            self.session.commit()
#        except:
#            self.session.rollback()
#            raise
#        finally:
#            self.session.remove()

    def commit_online(self):
        """
        Commits the current transaction or rollbacks if an error occurs.

        In all cases, the current session is unbound and therefore
        not usable any longer.
        """
        try:
            self.session_online.commit()
        except:
            self.session_online.rollback()
            raise
        finally:
            self.session_online.remove()

    def commit_offline(self):
        """
        Commits the current transaction or rollbacks if an error occurs.

        In all cases, the current session is unbound and therefore
        not usable any longer.
        """
        try:
            self.session_offline.commit()
        except:
            self.session_offline.rollback()
            raise
        finally:
            self.session_offline.remove()

    def commit_cache(self):
        """
        Commits the current transaction or rollbacks if an error occurs.

        In all cases, the current session is unbound and therefore
        not usable any longer.
        """
        try:
            self.session_cache.commit()
        except:
            self.session_cache.rollback()  
            raise
        finally:
            self.session_cache.remove()      
            
