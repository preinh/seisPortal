# -*- coding: utf-8 -*-

"""The base Controller API."""

from tg import TGController, tmpl_context
from tg.render import render
from tg import request
from tg.i18n import ugettext as _, ungettext
import portal.model as model
from tg import url
import tw2.core.core
#import tw2.jquery

__all__ = ['BaseController']


# now dev merge!!


class BaseController(TGController):
    """
    Base class for the controllers in the application.

    Your web application should have one of these. The root of
    your application is used to compute URLs used by your app.

    """

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # TGController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        request.identity = request.environ.get('repoze.who.identity')
        tmpl_context.identity = request.identity

        return TGController.__call__(self, environ, start_response)
#        stream = TGController.__call__(self, environ, start_response)
#         
#        # Disable the injection of tw2.jquery
#        #offending_link = tw2.jquery.jquery_js.req().link
#        local = tw2.core.core.request_local()
#
#        res = []
#        for r in local.get('resources', list()):
#            #if r.link != offending_link:
#            r.link = url(r.link)
#            res.append(r)
#        
#        local['resources'] = res    
#            
#        return stream
