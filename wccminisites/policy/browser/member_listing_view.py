from five import grok
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IContentish
from plone.app.discussion.interfaces import IConversation, IComment
from Products.CMFPlone.PloneBatch import Batch
from wccminisites.policy.interfaces import IProductSpecific

grok.templatedir('templates')

# default view for 'the-network' page

class member_listing_view(grok.View):
    grok.context(IContentish)
    grok.require('zope2.View')
    grok.layer(IProductSpecific)
    
    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')
    
    @property
    def portal_groups(self):
        return getToolByName(self.context, 'portal_groups')
    
    def network_group(self):
        results = []
        groups = self.portal_groups.getGroupById('network')
        if groups:
            for gr in groups.getGroupMembers():
                data = {}
                member = self.portal_membership.getMemberById(gr.getUserName())
                data['img'] = self.portal_membership.getPersonalPortrait(gr.getUserName()).absolute_url()
                data['fullname'] = member.getProperty('fullname')
                data['username'] = gr.getUserName()
                results.append(data)
        
        if results:
            results.sort(key = lambda x :x['fullname'])
        return results