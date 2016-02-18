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
from Acquisition import aq_inner
from wccminisites.policy import MessageFactory as _


class IProfileLink(IPortletDataProvider):
    
    header = schema.TextLine(title=_(u"Link Title"),
                             required=True,
                             default=_(u"My Profile"),)

class Assignment(base.Assignment):
    implements(IProfileLink)
    
    def __init__(self, header):
        self.header = header
    
    title = _(u"Profile Link Portlet")

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/profile_link.pt')
    
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        
    def header_val(self):
        return self.data.header
    
    def logged_user(self):
        context = aq_inner(self.context)
        membership = getToolByName(context, 'portal_membership')
        return membership.getAuthenticatedMember().getUserName()

class AddForm(base.AddForm):
    form_fields = form.Fields(IProfileLink)
    label = u"Add Profile Link Portlet"
    description = ''
    
    def create(self, data):
        return Assignment(**data)
    

class EditForm(base.EditForm):
    form_fields = form.Fields(IProfileLink)
    label = u"Edit Profile Link Portlet"
    description = ''
        
