import psycopg2
import config # config file with the database info
from mobalert.models import AccPointsBuffer

def buffer(point):
    dbname = config.DATABASE_CONFIG['dbname']
    user = config.DATABASE_CONFIG['user']
    host = config.DATABASE_CONFIG['host']
    password = config.DATABASE_CONFIG['password']
 
    if dbname != config.DATABASE_CONFIG['dbname']:
        raise ValueError("Couldn't not find DB with given name")

    conn = None
    try:
        db_connection = "dbname = '%s' user = '%s' host = '%s' password = '%s'" % (dbname, user, host, password)
        conn = psycopg2.connect(db_connection)
    except psycopg2.DatabaseError, ex:
        print 'I am unable to connect the database: " + ex'

    curs = conn.cursor()
    curs.execute("SELECT ST_Buffer(ST_GeomFromText('POINT(-71.104 42.315)', 4326)::geography, 500);")

    res = curs.fetchone()
    # curs.execute(("SELECT ST_Value(crete_elev.rast, 1, ST_SetSRID(ST_Point(%s),4326)) FROM crete_elev" % point))
    #conn.close()
    return res
