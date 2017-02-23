from five import grok
from zope.formlib import form
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.portlets.portlets import base
from Acquisition import aq_inner, aq_parent
from wccminisites.policy import MessageFactory as _
from zope.component import getUtility, getAdapter, getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot

class INetworkSearchPortlet(IPortletDataProvider):
    
    pass

class Assignment(base.Assignment):
    implements(INetworkSearchPortlet)

    @property
    def title(self):
        return _('Search Network Members')
    
class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/networksearchportlet.pt')
    
    def search_params(self):
        return ('Name', 'Church', 'Country', 'Region', 'WCC Commission')
    
    def search_values(self, val):
        if self.request.form:
            if val in self.request.form:
                return self.request.form[val]
        return ''
    

class AddForm(base.NullAddForm):
    form_fields = form.Fields(INetworkSearchPortlet)
    label = _(u"Add Network Search Facility")
    #description = _(u"Display upcoming prayer cycle")

    def create(self):
        return Assignment()
    
    