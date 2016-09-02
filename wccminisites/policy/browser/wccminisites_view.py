from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class WccminisitesView(BrowserView):
    
    @property
    def membership(self):
        return getToolByName(self.context, 'portal_membership')
    
    def creators_emails(self):
        context = self.context
        creators = context.listCreators()
        membership = self.membership
        emails = []
        for creator in creators:
            member = membership.getMemberById(creator)
            if member and member.getProperty('email'):
                emails.append(member.getProperty('email'))
        if emails:
            return ','.join(emails)
        return ''
    
    def site_admins_emails(self):
        membership = self.membership
        emails = []
        for member in membership.listMembers() or []:
            if member.has_role('Site Administrator'):
                emails.append(member.getProperty('email'))
        if emails:
            return ','.join(emails)
        return ''
                
        
        