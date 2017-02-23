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
            if self.request.form:
                search_by = self.request.form['search_by']
                keyword = self.request.form['keyword'].lower() or ''
                
                if keyword:
                    
                    if search_by == 'Name':
                        for gr in groups.getGroupMembers():
                        
                            member = self.portal_membership.getMemberById(gr.getUserName())
                            if member and member.getProperty('fullname'):
                                
                                if keyword in member.getProperty('fullname').lower():
                                    data = {}
                                    data['img'] = self.portal_membership.getPersonalPortrait(gr.getUserName()).absolute_url()
                                    data['fullname'] = member.getProperty('fullname')
                                    data['username'] = gr.getUserName()
                                    results.append(data)
                                        
                    elif search_by == 'Church':
                        for gr in groups.getGroupMembers():
                        
                            member = self.portal_membership.getMemberById(gr.getUserName())
                            if member and member.getProperty('church'):
                                
                                if keyword in member.getProperty('church').lower():
                                    data = {}
                                    data['img'] = self.portal_membership.getPersonalPortrait(gr.getUserName()).absolute_url()
                                    data['fullname'] = member.getProperty('fullname')
                                    data['username'] = gr.getUserName()
                                    results.append(data)
                    elif search_by == 'Region':
                        for gr in groups.getGroupMembers():
                        
                            member = self.portal_membership.getMemberById(gr.getUserName())
                            if member and member.getProperty('region'):
                                
                                if keyword in member.getProperty('region'):
                                    data = {}
                                    data['img'] = self.portal_membership.getPersonalPortrait(gr.getUserName()).absolute_url()
                                    data['fullname'] = member.getProperty('fullname')
                                    data['username'] = gr.getUserName()
                                    results.append(data)
                    elif search_by == 'Country':
                        for gr in groups.getGroupMembers():
                        
                            member = self.portal_membership.getMemberById(gr.getUserName())
                            if member and member.getProperty('location'):
                                
                                if keyword in member.getProperty('location'):
                                    data = {}
                                    data['img'] = self.portal_membership.getPersonalPortrait(gr.getUserName()).absolute_url()
                                    data['fullname'] = member.getProperty('fullname')
                                    data['username'] = gr.getUserName()
                                    results.append(data)
                    elif search_by == 'WCC Commission':
                        for gr in groups.getGroupMembers():
                        
                            member = self.portal_membership.getMemberById(gr.getUserName())
                            if member and member.getProperty('wcc_commission'):
                                
                                if keyword in (','.join(member.getProperty('wcc_commission'))).lower():
                                    data = {}
                                    data['img'] = self.portal_membership.getPersonalPortrait(gr.getUserName()).absolute_url()
                                    data['fullname'] = member.getProperty('fullname')
                                    data['username'] = gr.getUserName()
                                    results.append(data)
                                    
                            
                            
                                    
            
            else:
            
                for gr in groups.getGroupMembers():
                    
                    member = self.portal_membership.getMemberById(gr.getUserName())
                    if member:
                        data = {}
                        data['img'] = self.portal_membership.getPersonalPortrait(gr.getUserName()).absolute_url()
                        data['fullname'] = member.getProperty('fullname')
                        data['username'] = gr.getUserName()
                        results.append(data)
        
        if results:
            results.sort(key = lambda x :x['fullname'])
        return results