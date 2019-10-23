import psycopg2
import config # config file with the database info
from mobalert.models import AccPointsBuffer
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import GEOSGeometry

def buffer(lon, lat, dist):
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
    curs.execute("SELECT ST_AsText(ST_Buffer(ST_GeomFromText('POINT(%s %s)', 4326)::geography, %s));" % (lon, lat, dist))

    res = curs.fetchone()
    
    # Convert unicode string value to Polygon object
    resObj = GEOSGeometry(res[0])
    # convert Polygon to MultiPolygon
    polyGeog = MultiPolygon(resObj)

    # curs.execute(("SELECT ST_Value(crete_elev.rast, 1, ST_SetSRID(ST_Point(%s),4326)) FROM crete_elev" % point))
    conn.close()
    # return only the value from the returned object
    return polyGeog
