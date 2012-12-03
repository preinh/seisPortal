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
        json = e.getAllJson(8)

        b = model.bsb.BoletimSismico()
        bsb_list = b.getAll()
        json_l = b.getAllJson(20)


        return dict(page='index',
            filterForm = "",
            events = event_list[:8],
            bsb = bsb_list[:20],
            cycle = cycle,
            json = json,
            json_l = json_l,
            evt_png = url("/images/event.png"),
            last_evt_png = url("/images/event.png"),
        )

        """Handle the front-page."""
        return dict(page='index')





    @expose('portal.templates.waveform')
    def waveform(self):
        """Handle the waveform page."""
        event_list = model.events.Events().getAll()
        return dict(page='waveform', events=event_list)




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
        return dict(params=kw)

    @expose('portal.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('portal.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Permitido apenas para managers')))
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
