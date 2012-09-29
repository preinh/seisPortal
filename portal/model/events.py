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
#            self.dbDriverName="mysql"
#            self.dbAddress="sysop:sysop@localhost/seiscomp3"
#            self.dbPlugin = "dbmysql"
        else:
            self.dbDriverName="postgresql"
            self.dbAddress="sysop:sysop@10.110.0.130/sc_master"
            self.dbPlugin = "dbpostgresql"
        
        #self.dbQuery = self._createQuery()        
        
        daysBefore = 20
        
        self.e = datetime.utcnow()
        self.b = self.e - timedelta(days=daysBefore)
        
        #self.e = Core.Time.GMT()
        #self.s = self.e - Core.TimeSpan(daysBefore*24*60*60)
        
#        self.s = Core.Time_FromString("2012-01-01 00:00:00", "%F %T")
#        self.e = Core.Time_FromString("2012-02-01 00:00:00", "%F %T")
    
        self.events_list = []


    def getAll(self, filter=""):

        self.events_list = []
        
        # Connect to an existing database
        conn = psycopg2.connect(dbname="sc_master", user="sysop", password="sysop", host="10.110.0.130")
        
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
                        magnitude.m_stationcount AS mag_count 
           FROM         event, 
                        publicobject pevent, 
                        origin, 
                        publicobject porigin, 
                        magnitude, 
                        publicobject pmagnitude, 
                        eventdescription
          WHERE         event._oid = pevent._oid 
          AND           origin._oid = porigin._oid 
          AND           magnitude._oid = pmagnitude._oid 
          AND           event.m_preferredoriginid::text = porigin.m_publicid::text 
          AND           event.m_preferredmagnitudeid::text = pmagnitude.m_publicid::text 
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
            _mag = ("%.1f %s (%d)") % (val, typ, stc)

            d = dict(id=evt,
                     desc= desc,
                     time= _time, 
                     lat= lat, 
                     lon= lon,
                     dep= dep,
                     mag= _mag
                     )        

            self.events_list.append(d)

        
        # Close communication with the database
        cur.close()
        conn.close()

        #return sorted(self.events_list, key=lambda event: event['time'], reverse=True)

        return self.events_list


    def getAllJson(self):
        json=""
        try:
            
            for d in self.events_list[1:]:
                json += """
                    {
                        id:     '%s',
                        desc:   '%s',
                        time:   '%s',
                        lat:    %f,
                        lng:    %f,
                        dep:    %f,
                        mag:    '%s'
                    },
                """ % (d['id'], d['desc'], d['time'], float(str(d['lat'])), float(str(d['lon'])), float(str(d['dep'])), d['mag'] )
    
            json = "var businesses = [" + json[ : -1] + "];"
        except:
            pass
        
        return json
    
    
    def getLastJson(self):
        json=""
        
        try:
            #print self.events_list
            d = self.events_list[0]
        
            json = """
                {
                    id:     '%s',
                    desc:   '%s',
                    time:   '%s',
                    lat:    %f,
                    lng:    %f,
                    dep:    %f,
                    mag:    '%s'
                },
            """ % (d['id'], d['desc'], d['time'], float(str(d['lat'])), float(str(d['lon'])), float(str(d['dep'])), d['mag'] )
    
            json = "var last = [" + json[ : -1] + "];"
        except:
            pass
        
        return json



    def getDetails(self, eid=None):
        r = {}
        
        if not eid:
            r = dict(error="Invalid ID")
            return r

        evt = self.dbQuery.getEventByPublicID(eid)
        if not evt:
            r = dict(error="Event not Found")
            return r


        cmd = "/home/pirchiner/bin/scbulletin -E %s -3 --extra -d '%s://%s'" % (eid, self.dbDriverName, self.dbAddress)
        out = commands.getstatusoutput(cmd)

        out_lines = out[1]
#        out_lines = out_lines.replace("automatic", "<span style='font-color: red;'>automatic</span>")
#        out_lines = out_lines.replace("manual", "<span color='green'>manual</span>")
    
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
        return "Events bla bla"


class EventCatalog:
    IAG = 1
    QED = 2
    ISC = 3


class EventFilter(object):

    def __init__(self, 
                start_time = 0, 
                end_time = 0,
        
                min_mag = 0,
                max_mag = 10,
        
                min_dep = 0,
                max_dep = 6300,
        
                min_lat = -90,
                max_lat = +90,
                
                min_lon = -180,
                max_lon = +180,
                
                catalogs = [EventCatalog.IAG]
                ):
        
        self.start_time = start_time 
        self.end_time = end_time

        self.min_mag = min_mag
        self.max_mag = max_mag

        self.min_dep = min_dep
        self.max_dep = max_dep

        self.min_lat = min_lat
        self.max_lat = max_lat
        
        self.min_lon = min_lon
        self.max_lon = max_lon
        
        self.catalogs = catalogs

        