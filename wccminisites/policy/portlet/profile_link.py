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
        
    @property
    def membership(self):
        return getToolByName(self.context, 'portal_membership')
        
    def header_val(self):
        return self.data.header
    
    def logged_user(self):
        context = aq_inner(self.context)
        membership = getToolByName(context, 'portal_membership')
        return membership.getAuthenticatedMember().getUserName()
    
    def is_profile_page(self):
        curr_url = self.request.getURL()
        is_root = self.context.__providedBy__(ISiteRoot)
        
        if 'author_view' in curr_url and is_root:
            return True
        return False
    
    def filter_edit_profile(self):
        current_user = self.context.portal_membership.getAuthenticatedMember().getUserName()
        if 'id' in self.request.form:
            if self.request.form['id'] == current_user:
                return True
        return False
            
    
    def user_info(self):
        membership = self.membership
        request = self.request
        user_id = ''
        result = {'portrait':'#', 'fullname':'', 'email':''}
        if 'id' in request.form:
            user_id = request.form['id']
            user_data = membership.getMemberById(user_id)
            result['portrait'] = membership.getPersonalPortrait(user_id).absolute_url()
            if user_data:
                result['fullname'] = user_data.getProperty('fullname')
                result['email'] = user_data.getProperty('email')
                result['church'] = user_data.getProperty('church')
                result['country'] = user_data.getProperty('location')
                result['homepage'] = user_data.getProperty('home_page')
        return result
        

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
        
