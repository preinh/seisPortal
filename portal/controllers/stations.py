#from tg import expose, request

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from portal.lib.base import BaseController
from portal import model

from itertools import cycle
import datetime

import tw2.core as twc
import tw2.forms as twf
import tw2.dynforms as twd
import tw2.jqplugins.ui as jqui

import stationsForms as sf


__all__ = ['StationsController']



class Station_Page(twc.Page):
    title = "page"
    child = sf.StationFilterForm()
    




class StationsController(BaseController):
    
    #_s = model.stations.Stations()

    @expose('portal.templates.stations')
    def index(self, *args, **kw):
        """Handle the stations page."""
        
        filter = ""
        dat = {}
        if kw != {}:
            for k, v in kw.iteritems():
                dat[k]=v
                if v != '':
                    if k == "cod":
                        filter += " AND     lower(station.m_code) LIKE lower('%s') " % ("%"+str(v)+"%")
                    elif k == "loc":
                        filter += " AND     lower(station.m_description) LIKE lower('%s')  " % ("%"+str(v)+"%")
                    
                    elif k == "dep_f":
                        filter += " AND     station.m_elevation >= %f  " % (float(v))
                    elif k == "dep_t":
                        filter += " AND     station.m_elevation <= %f  " % (float(v))

                    elif k == "lat_f":
                        filter += " AND     station.m_latitude <= %f  " % (float(v))
                    elif k == "lat_t":
                        filter += " AND     station.m_latitude <= %f  " % (float(v))
                
                    elif k == "lon_f":
                        filter += " AND     station.m_longitude <= %f  " % (float(v))
                    elif k == "lon_t":
                        filter += " AND     station.m_longitude <= %f  " % (float(v))
                

        _s = model.stations.Stations()
        
        stations_list = _s.getAll(filter=filter)
        
        json = _s.getAllJson()
       
        f = sf.StationFilterForm().req()
        
        return dict(page = 'stations',
                    filterForm=f, 
                    data = dat,
                    stations = stations_list,
                    cycle = cycle,
                    json = json)



    
    @expose('portal.templates.stations')
    def stations(self):
        """Handle the events page."""
        #s = model.stations.Stations()

        f = sf.StationFilterForm().req()

        _s = model.stations.Stations()
        
        stations_list = _s.getAll()
        json = _s.getAllJson()
        return dict(page='stations', 
                    filterForm=f,
                    data = {},
                    stations = stations_list,
                    cycle = cycle,
                    json = json)


    @expose('portal.templates.station')
    def _default(self, came_from=url('/')):
        id = came_from
        _s = model.stations.Stations()
        station_details = _s.getDetails(id)

        return dict(page='station',
                    d = station_details)
        