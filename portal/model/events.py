# -*- coding: utf-8 -*-
#import os
#import sys
#
#from datetime import datetime
#from sqlalchemy import Table, ForeignKey, Column
#from sqlalchemy.orm import relation, synonym
#from sqlalchemy.types import Unicode, Integer, DateTime
#
#from portal.model import DeclarativeBase, metadata, DBSession


import psycopg2

import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

#from seiscomp3 import Client, IO, Core, DataModel
import commands

from datetime import datetime, timedelta

class Events(object):

    debug = False

    def __init__(self):
    
        if self.debug:
            self.dbDriverName="postgresql"
            self.dbAddress="sysop:sysop@localhost/seiscomp3"
            self.dbPlugin = "dbpostgresql"
        else:
            self.dbDriverName="postgresql"
            self.dbAddress="sysop:sysop@10.110.0.130/master_sc3"
            self.dbPlugin = "dbpostgresql"
        
        daysBefore = 20
        
        self.e = datetime.utcnow()
        self.b = self.e - timedelta(days=daysBefore)
    
        self.events_list = []


    def getAll(self, filter=""):

        self.events_list = []
        
        # Connect to an existing database
        conn = psycopg2.connect(dbname="master_sc3", user="sysop", password="sysop", host="10.110.0.130")
        
        # Open a cursor to perform database operations
        cur = conn.cursor()
        
        # Query the database and obtain data as Python objects
        cur.execute("""
            SELECT      pevent.m_publicid AS eventid, 
                        eventdescription.m_text AS "desc",
                        event.m_creationinfo_agencyid AS agency,
                        origin.m_time_value AS "time", 
                        origin.m_latitude_value AS lat, 
                        origin.m_longitude_value AS lon, 
                        origin.m_depth_value AS depth,
                        magnitude.m_magnitude_value AS mag, 
                        magnitude.m_type AS mag_type, 
                        coalesce(magnitude.m_stationcount, 0) AS mag_count,
                        case
                            when origin.m_evaluationmode = 'automatic' then 'A'
                            when origin.m_evaluationmode = 'manual' then 'M'
                            else 'U'
                        end AS status,
                        origin.m_creationinfo_author as author
           FROM         event LEFT OUTER JOIN publicobject pmagnitude
                              ON (event.m_preferredmagnitudeid::text = pmagnitude.m_publicid::text),
                        publicobject pevent, 
                        origin, 
                        publicobject porigin, 
                        magnitude, 
                        eventdescription
          WHERE         event._oid = pevent._oid 
          AND           origin._oid = porigin._oid 
          AND           magnitude._oid = pmagnitude._oid 
          AND           event.m_preferredoriginid::text = porigin.m_publicid::text 
          AND           coalesce(event.m_type, '') not in ('not existing', 'outside of network interest')
          AND           eventdescription._parent_oid = pevent._oid
          AND           origin.m_time_value >= '%s'
          AND           origin.m_time_value <= '%s'
          %s
          ORDER BY      time DESC;
          """  % (self.b, self.e, filter))

        for line in cur:
            evt = line[0]
            desc = line[1]
            _time = line[3] 
            lat= ("%.2f") % line[4] 
            lon= ("%.2f") % line[5]
            dep= ("%d") % line[6]
            val = line[7]
            typ = line[8]
            stc = line[9]
            status = line[10]
            author = line[11]
            try:
                _mag = ("%.1f %s (%d)") % (val, typ, stc)
            except:
                _mag = u"--"

            d = dict(id=evt,
                     desc= desc,
                     time= _time, 
                     lat= lat, 
                     lon= lon,
                     dep= dep,
                     mag= _mag,
                     status = status,
                     author = author
                     )        

            self.events_list.append(d)

        
        # Close communication with the database
        cur.close()
        conn.close()

        #return sorted(self.events_list, key=lambda event: event['time'], reverse=True)
        return self.events_list

    def getAllGeoJson(self, limit=None):
        geojson=""
        try:
            for d in self.events_list[0:limit]:
                geojson+= """
                {
                    "type": "Feature",
                    "properties": {
                        "id": "%s",
                        "mag": "%s",
                        "desc": "%s",
                        "time": "%s"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [%f, %f]
                    }
                }, """%(d['id'],  d['mag'], d['desc'],d['time'], float(str(d['lon'])), float(str(d['lat'])))

            geojson = "var geojson = [" + geojson[:] + "];"
        except:
            print geojson
            pass

        return geojson


    def getLastGeoJson(self):
        json=""
        try:
            d = self.events_list[0]
            json = """
                {
                    "type": "Feature",
                    "properties": {
                        "id": "%s",
                        "mag": "%s",
                        "desc": "%s",
                        "time": "%s"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [%f, %f]
                    }
                },
                """%(d['id'],  d['mag'], d['desc'],d['time'], float(str(d['lon'])), float(str(d['lat'])))

            json = "var geojson_l = [" + json[:] + "];"
        except:
            json = "var geojson_l = [ ];"
            print json
            pass

        return json



    def getDetails(self, eid=None):
        r = {}
        
        if not eid:
            r = dict(error="Invalid ID")
            return r

        #evt = self.dbQuery.getEventByPublicID(eid)
#        if not evt:
#            r = dict(error="Event not Found")
#            return r


        cmd = "/home/suporte/seiscomp3/bin/seiscomp exec scbulletin -E %s -3 --extra -d '%s://%s'" % (eid, self.dbDriverName, self.dbAddress)
        out = commands.getstatusoutput(cmd)

        out_lines = out[1]
    
        out_lines = out_lines.split('\n')
    
        r = dict(error="",
                 eid=eid,
                 t = out_lines,
                 )
        return r

#    def _createQuery(self):
#        # Get global plugin registry
#        self.registry = Client.PluginRegistry.Instance()
#        # Add plugin dbmysql
#        self.registry.addPluginName(self.dbPlugin)
#        # Load all added plugins
#        self.registry.loadPlugins()
#        # Create dbDriver
#        self.dbDriver = IO.DatabaseInterface.Create(self.dbDriverName)
#        # Open Connection 
#        #dbDriver.Open(dbAddress)   
#        self.dbDriver.connect(self.dbAddress)
#        # set Query object
#        return DataModel.DatabaseQuery(self.dbDriver)

    
    def __repr__(self):
        return ('<Events: start=%s end=%s>' % str(self.s), str(self.e)).encode('utf-8')

    def __unicode__(self):
        return "Events Model"

