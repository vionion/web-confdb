from Config import Config
from Config.ConfDBAuth.ConfDBAuth import ConnectionString
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from confdb_tables.confdb_tables import Base
from data_builder import DataBuilder
from utils import Timer

logger      = None
databuilder = None


def initialize(online, version, use_cherrypy):
    # configure the logger
    global logger
    if use_cherrypy:
        import cherrypy
        logger = cherrypy.log
    else:
        import multiprocessing
        logger = multiprocessing.get_logger()

    # create a database session
    connectionString = ConnectionString()
    engine = None

    if online == 'True':
        engine = create_engine(connectionString.connectUrlonline)
    else:
        engine = create_engine(connectionString.connectUrloffline)

    Base.prepare(engine, reflect=True)
    session = scoped_session(sessionmaker(engine))

    # store the version id
    global databuilder
    databuilder = DataBuilder(session, version, logger)


def worker(args):
    label, method = args

    # call the requested method
    try:
        logger.info('%s: call to DataBuilder.%s' % (label, method))
        t = Timer()
        data = getattr(databuilder, method)()
        t.stop()
        logger.info('%s: done [%.1fs]' % (label, t.elapsed))
        return label, data, None

    except:
        import StringIO
        import traceback
        buffer = StringIO.StringIO()
        traceback.print_exc(file = buffer)
        return label, None, buffer.getvalue()

