#from tg import expose, request

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from portal.lib.base import BaseController
from portal import model

from itertools import cycle

__all__ = ['EventsController']

import tw2.core as twc
#import tw2.forms as twf
#import tw2.dynforms as twd
#import tw2.jqplugins.ui as jqui
from datetime import datetime

#from eventsForms import EventFilterForm
import eventsForms as ef
import bsbForms as bf

#class Event_Page(twc.Page):
#    title = "page"
#    child = ef.EventFilterForm()    

class EventsController(BaseController):

    @expose('portal.templates.events')
    def index(self, *args, **kw):
        """Handle the events page."""

        e = model.events.Events()
        
        filter = ""
        dat = {}
        if kw != {}:
            for k, v in kw.iteritems():
                dat[k]=v
                if v != '':
                    if k == "mag_f":
                        filter += " AND     magnitude.m_magnitude_value >= %f  " % (float(v))
                    elif k == "mag_t":
                        filter += " AND     magnitude.m_magnitude_value <= %f  " % (float(v))
                    
                    elif k == "dep_f":
                        filter += " AND     origin.m_depth_value >= %f  " % (float(v))
                    elif k == "dep_t":
                        filter += " AND     origin.m_depth_value <= %f  " % (float(v))

                    elif k == "lat_f":
                        filter += " AND     origin.m_latitude_value <= %f  " % (float(v))
                    elif k == "lat_t":
                        filter += " AND     origin.m_latitude_value <= %f  " % (float(v))
                
                    elif k == "lon_f":
                        filter += " AND     origin.m_longitude_value <= %f  " % (float(v))
                    elif k == "lon_t":
                        filter += " AND     origin.m_longitude_value <= %f  " % (float(v))
                
                    elif k == "date_f":
                        e.b = datetime.strptime(v, "%d-%m-%Y %H:%M")
                    elif k == "date_t":
                        e.e = datetime.strptime(v, "%d-%m-%Y %H:%M")
                
        event_list = e.getAll(filter=filter)
        json = e.getAllJson()
        #json_l = e.getLastJson()
        f = ef.EventFilterForm().req()

        b = model.bsb.BoletimSismico()

        bsb_filter = ""
        bsb_dat = {}
        if kw != {}:
            for k, v in kw.iteritems():
                bsb_dat[k]=v
                if v != '':
                    if k == "bsb_mag_f":
                        bsb_filter += " AND    m_magnitude_value >= %f  " % (float(v))
                    elif k == "bsb_mag_t":
                        bsb_filter += " AND    m_magnitude_value <= %f  " % (float(v))

                    elif k == "bsb_dep_f":
                        bsb_filter += " AND    m_depth_value >= %f  " % (float(v))
                    elif k == "bsb_dep_t":
                        bsb_filter += " AND    m_depth_value <= %f  " % (float(v))

                    elif k == "bsb_lat_f":
                        bsb_filter += " AND    m_latitude_value <= %f  " % (float(v))
                    elif k == "bsb_lat_t":
                        bsb_filter += " AND    m_latitude_value <= %f  " % (float(v))

                    elif k == "bsb_lon_f":
                        bsb_filter += " AND    m_longitude_value <= %f  " % (float(v))
                    elif k == "bsb_lon_t":
                        bsb_filter += " AND    m_longitude_value <= %f  " % (float(v))

                    elif k == "bsb_date_f":
                        b.b = datetime.strptime(v, "%d-%m-%Y %H:%M")
                    elif k == "bsb_date_t":
                        b.e = datetime.strptime(v, "%d-%m-%Y %H:%M")


        bsb_list = b.getAll(limit=60, filter=bsb_filter)
        json_l = b.getAllJson(limit=60)

        bsb_f = bf.BsbFilterForm().req()

        return dict(page = 'events',
                    filterForm = f,
                    bsbFilterForm = bsb_f,
                    data = dat,
                    bsb_data = bsb_dat,
                    events = event_list,
                    bsb = bsb_list,
                    cycle = cycle,
                    json = json,
                    json_l = json_l,
                    evt_png = url("/images/event.png"),
                    last_evt_png = url("/images/star2.png"),
                    )
    
    @expose('portal.templates.events')
    def events(self, *args, **kw):
        """Handle the events page."""
        e = model.events.Events()
        event_list = e.getAll()
        json = e.getAllJson()
        #json_l = e.getLastJson()

        b = model.bsb.BoletimSismico()
        bsb_list = b.getAll()
        json_l = b.getAllJson()

        f = ef.EventFilterForm().req()
        bsb_f = bf.BsbFilterForm().req()

        return dict(page='events',
                    filterForm = f,
                    bsbFilterForm = bsb_f,
                    events = event_list,
                    bsb = bsb_list,
                    cycle = cycle,
                    json = json,
                    json_l = json_l,
                    evt_png = url("/images/event.png"),
                    last_evt_png = url("/images/star2.png"),
                    )

    @expose('portal.templates.event')
    def _default(self, came_from=url('/'), *args, **kw):
        id = came_from
        event_details = model.events.Events().getDetails(id)

        f = ef.EventFilterForm().req()
        bsb_f = bf.BsbFilterForm().req()

        return dict(page='event',
                    filterForm=f,
                    bsbFilterForm= bsb_f,
                    d = event_details)
        
