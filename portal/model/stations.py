# -*- coding: utf-8 -*-
from portal.lib import app_globals as appg

import psycopg2

import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

from datetime import datetime
#from seiscomp3 import Client, IO, Core, DataModel

class Stations(object):

    def __init__(self):
        self.details = [] 
        self.stations_list = []


    def getAll(self, filter=""):
        self.stations_list = []
        
        # Connect to an existing database
        conn = psycopg2.connect(dbname="seisrequest_v7", user="sysop", password="sysop", host="10.110.0.130")
        
        # Open a cursor to perform database operations
        cur = conn.cursor()
        
        # Query the database and obtain data as Python objects
        cur.execute("""
                    SELECT          net.m_code as net,
                                    station.m_code as sta,
                                    station.m_description as desc,
                                    station.m_latitude as lat,
                                    station.m_longitude as lon,
                                    station.m_elevation as elev,
                                    count(stream.m_code) as channels
                    FROM            station,
                                    network as net,
                                    sensorlocation as sl LEFT OUTER JOIN stream ON (stream._parent_oid = sl._oid )
                    WHERE           sl._parent_oid = station._oid
                    AND             station._parent_oid = net._oid
                                    %s
                    /* AND          net.m_code = 'BL'
                    AND             station.m_code = 'APOB'
                    */
                    GROUP BY    net.m_code, 
                                    station.m_code, 
                                    station.m_description, 
                                    station.m_longitude, 
                                    station.m_latitude, 
                                    station.m_elevation
                    ORDER BY        net, sta;
                    """ % (filter))

        for line in cur:
            self.stations_list.append(dict(
                NN = line[0],
                SSSSS = line[1],
                desc = line[2],
                lat = ("%.2f") % line[3], 
                lon = ("%.2f") % line[4],
                ele = ("%.1f") % line[5],
                n_ch = line[6],
            ))
        # Close communication with the database
        cur.close()
        conn.close()
        return self.stations_list



    def getAllJson(self):
        json = ""                                             
        for sta in self.stations_list:
            element = """
             {
                "type": "Feature",
                "properties": {
                    "net":    "%s",
                    "sta":    "%s",
                    "desc":   "%s"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [%.4f , %.4f ]
                }
            }
            """ % (sta['NN'], sta['SSSSS'], sta['desc'], float(sta['lon']), float(sta['lat']))
            json += element + ","

        json = "var stations_gj = [" + json[ : -1] + "];"
        return json


    def getDetails(self, sid=None):
        r = {}
        try:
            ss = sid.split('_')[-1]
            nn = (sid.split('_')[-2]).split('/')[-1]
            if not nn or not ss:
                r = dict(error="Station Not Found",
                         details = [],
                         )
                return r
        except:
            r = dict(error="Out of pattern NN_SSSSS " + str(sid),
                     details = [],
                     )
            return r

        # Connect to an existing database
        conn = psycopg2.connect(dbname="seisrequest_v7", user="sysop", password="sysop", host="10.110.0.130")
        
        # Open a cursor to perform database operations
        cur = conn.cursor()
        
        # Query the database and obtain data as Python objects
        query = """
                SELECT          net.m_code as net,
                                station.m_code as sta,
                                sl.m_code as loc,
                                stream.m_code as cha,
                                stream.m_start as cha_sta,
                                coalesce(stream.m_end, date_trunc('seconds', now()::timestamp)) as cha_end,
                                station.m_description as desc,
                                station.m_latitude as lat,
                                station.m_longitude as lon,
                                station.m_elevation as elev
                FROM            station,
                                network as net,
                                sensorlocation as sl,
                                stream
                WHERE           stream._parent_oid = sl._oid
                AND             sl._parent_oid = station._oid
                AND             station._parent_oid = net._oid
                AND             net.m_code = '%s'
                AND             station.m_code = '%s'
                ORDER BY        station.m_code;
                """  % (nn, ss)

        print query
        cur.execute(query)

        self.details = []
        for line in cur:
            png = "%s.%s.%s.%s.ALL.png" % (line[0], line[1], line[2].replace("","--"), line[3])
            self.details.append(dict(NN=line[0],
                                     SSSSS=line[1],
                                     LL=line[2],
                                     CCC=line[3],
                                     desc = line[6],
                                     lat = ("%.4f") % line[7],
                                     lon = ("%.4f") % line[8],
                                     ele = ("%.1f") % line[9], 
                                     png = "%s.%s/%s"% (line[0], line[1], png),
                                     t0 = ("%sZ"%(line[4])).replace(" ", "T"),
                                     tf = ("%sZ"%(line[5])).replace(" ", "T"),
                                     ))
        
        # Close communication with the database
        cur.close()
        conn.close()

        if self.details == []:
            return dict(error="unable to get streams",
                        details=[],
                        )
        
        return dict(error="",
                    details=self.details,
                    )

    def __repr__(self):
        return ('<Stations>').encode('utf-8')

    def __unicode__(self):
        return "Stations"


#"""
#scheli capture -I "combined://seisrequest.iag.usp.br:18000;seisrequest.iag.usp.br:18001" 
#                --offline --amp-range=1E3 --stream BL.AQDB..HHZ -N -o saida.png
#"""

# scxmldump $D -E iag-usp2012ioiu | scmapcut --ep - -E iag-usp2012ioiu -d 1024x768 -m 5 --layers -o evt.png

