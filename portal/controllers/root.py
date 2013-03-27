# -*- coding: utf-8 -*-
"""Main Controller"""
from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from itertools import cycle

from portal import model

from repoze.what import predicates
from portal.controllers.secure import SecureController

from portal.model import DBSession, metadata

from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController

from portal.lib.base import BaseController
from portal.controllers.error import ErrorController

from portal.controllers.events import EventsController
from portal.controllers.stations import StationsController
from portal.controllers.bsb import BsbController

import urllib2
from json import loads


import psycopg2
import psycopg2.extras
import json
import collections
from datetime import datetime, timedelta
import calendar

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the portal application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()
    events = EventsController()
    bsb = BsbController()
    stations = StationsController()

    @expose('portal.templates.index')
    def index(self):

        e = model.events.Events()
        event_list = e.getAll()
        geojson = e.getAllGeoJson(8)

        b = model.bsb.BoletimSismico()
        bsb_list = b.getAll()
        geojson_l = b.getAllGeoJson(20)


        return dict(page='index',
            filterForm = "",
            events = event_list[:8],
            bsb = bsb_list[:20],
            cycle = cycle,
            geojson = geojson,
            geojson_l = geojson_l,
            evt_png = url("/images/event.png"),
            last_evt_png = url("/images/event.png"),
        )

#        """Handle the front-page."""
#        return dict(page='index')


    @expose('portal.templates.waveform')
    def waveform(self):
        """Handle the waveform page."""
        event_list = model.events.Events().getAll()
        return dict(page='waveform', events=event_list)


    @expose('portal.templates.inform')
    def inform(self):
        """Handle the waveform page."""
        return dict(page='inform')

    @expose('portal.templates.download')
    def download(self, *args, **kw):

        import downloadForms as df
        from datetime import datetime

        filter = ""
        dat = {}
        if kw != {}:
            for k, v in kw.iteritems():
                dat[k]=v
                if v != '':
                    if k == "network":
                        filter += " network  %s " % v
                    elif k == "station":
                        filter += " station  %s " % v
                    elif k == "channel":
                        filter += " channel  %s " % v
                    elif k == "onehour":
                        filter += " onehour  %s " % v
                    elif k == "type":
                        filter += " type  %s " % v
                    elif k == "outfile":
                        filter += " outfile  %s " % v
                    elif k == "type":
                        filter += " network  %s " % v
                    elif k == "date_f":
                        filter += " start " + str(datetime.strptime(v, "%d-%m-%Y %H:%M"))
                    elif k == "date_t":
                        filter += " end " + str(datetime.strptime(v, "%d-%m-%Y %H:%M"))

        print dat

        f = df.DownloadForm().req()

        """Handle the waveform page."""
#        event_list = model.events.Events().getAll()
        return dict(page='download',
                    downloadForm = f,
                    data = dat,
        )


    #@expose('portal.templates.data')
    @expose('json')
    def getStations(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        seishub_stations = "http://seishub.iag.usp.br/seismology/station/getList?format=json&network_id=BL"
        req = urllib2.Request(seishub_stations)
        opener = urllib2.build_opener()
        f = opener.open(req)
        json = loads(f.read())
        #return dict(params=kw)
        return dict(stations=dict(args=kw, json=json))

    #@expose('portal.templates.data')
    @expose('json')
    def getGaps(self, **kw):
        #gaps("2010-01-01T00:00:00Z", "2013-12-31T00:00:00Z", 1, "%s"%sta, "HHZ")

        j = None
        con = None

        try:

            t0 = datetime.strptime(kw["t0"], '%Y-%m-%dT%H:%M:%SZ')
            tf = datetime.strptime(kw["tf"], '%Y-%m-%dT%H:%M:%SZ')
            d = int(kw["d"])
            #delta = timedelta(days=)
            station = kw["s"]
            dt = kw["dt"]
            channel = kw["c"]

            con = psycopg2.connect(host="10.110.0.134", database='seishub', user='seishub', password="seishub")

            cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            query = """
                select t0, percent
                from mv_gaps_weekly
                where sta = '%s'
                and cha = '%s'
                and t0 > '%s'
                and tf < '%s'
                """%(station, channel,t0, tf)
            #print query
            cursor.execute(query)

            #print json.dumps(cursor.fetchall(), default=date_handler)

            rows = cursor.fetchall()
            l = []
            for r in rows:
                l.append([calendar.timegm(r['t0'].timetuple()),r['percent']])

            #print l
            #print json.dumps(dict(l))
            j = json.dumps(dict(l))
            #print l
            #file = 'month_hour_%s.%s.js'%(station,channel)
            #f = open(file,'w')
            #print >> f, j

            con.close()

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            pass

        finally:
            if con:
                con.close()

        #sta = station["code"]

        """This method showcases how you can use the same controller for a data page and a display page"""
        #seishub_stations = "http://seishub.iag.usp.br/seismology/station/getList?format=json&network_id=BL"
        #req = urllib2.Request(seishub_stations)
        #opener = urllib2.build_opener()
        #f = opener.open(req)
        #json = loads(f.read())
        #return dict(params=kw)
        return dict(gaps=j)

    #@expose('portal.templates.data')
    @expose('json')
    def getGapsDaily(self, **kw):
        #gaps("2010-01-01T00:00:00Z", "2013-12-31T00:00:00Z", 1, "%s"%sta, "HHZ")

        j = None
        con = None

        try:

            t0 = datetime.strptime(kw["t0"], '%Y-%m-%dT%H:%M:%SZ')
            tf = datetime.strptime(kw["tf"], '%Y-%m-%dT%H:%M:%SZ')
            d = int(kw["d"])
            #delta = timedelta(days=)
            station = kw["s"]
            dt = kw["dt"]
            channel = kw["c"]

            con = psycopg2.connect(host="10.110.0.134", database='seishub', user='seishub', password="seishub")

            cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
            query = """
                select t0, percent
                from mv_gaps_daily
                where sta = '%s'
                and cha = '%s'
                and t0 > '%s'
                and tf < '%s'
                """%(station, channel,t0, tf)

            query = """
                select t0, percent from get_gaps( '%s', '%s',
                            '1 day'::interval,
                            '%s'::text, '%s'::text )
                """%(t0, tf, station, channel)

            #print query
            cursor.execute(query)

            #print json.dumps(cursor.fetchall(), default=date_handler)

            rows = cursor.fetchall()
            l = []
            for r in rows:
                l.append([calendar.timegm(r['t0'].timetuple()),r['percent']])
#                  l.append(dict(date=calendar.timegm(r['t0'].timetuple()),
#                                gaps = r['percent']))
            #print l
            #print json.dumps(dict(l))
            j = json.dumps(dict(l))
            #j = json.dumps(l)
            #print j
            #file = 'month_hour_%s.%s.js'%(station,channel)
            #f = open(file,'w')
            #print >> f, j

            con.close()

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            pass

        finally:
            if con:
                con.close()

        #sta = station["code"]

        """This method showcases how you can use the same controller for a data page and a display page"""
        #seishub_stations = "http://seishub.iag.usp.br/seismology/station/getList?format=json&network_id=BL"
        #req = urllib2.Request(seishub_stations)
        #opener = urllib2.build_opener()
        #f = opener.open(req)
        #json = loads(f.read())
        #return dict(params=kw)
        return dict(gaps=j)


    @expose('portal.templates.google')
    def google(self):
        """Handle the 'about' page."""
        return dict(page='google')


    @expose('portal.templates.about')
    def about(self, *args, **kw):
        return dict(page='about')


    @expose('portal.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)


    @expose('portal.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        seishub_stations = "http://seishub.iag.usp.br/seismology/station/getList?format=json&network_id=BL"
        req = urllib2.Request(seishub_stations)
        opener = urllib2.build_opener()
        f = opener.open(req)
        json = loads(f.read())
        #return dict(params=kw)
        return dict(params=dict(args=kw, json=json))

    @expose('portal.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('portal.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Permitido apenas para funcionários')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('portal.templates.index')
    @require(predicates.is_user('editor', msg=l_('Permitido apenas para editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('portal.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Usuario|Senha invalidos'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect(url('/login'),
                params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Bem vindo novamente, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('Esperamos ve-lo novamente em breve!'))
        redirect(came_from)
