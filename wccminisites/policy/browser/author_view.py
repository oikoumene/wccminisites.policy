from five import grok
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.discussion.interfaces import IConversation, IComment
from Products.CMFCore.interfaces import IContentish
from plone.i18n.normalizer import idnormalizer
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from wccminisites.policy.interfaces import IChurchMemberDGForm

grok.templatedir('templates')

class author_view(grok.View):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    @property
    def membership(self):
        return getToolByName(self.context, 'portal_membership')
    
    def churchValues(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IChurchMemberDGForm, check=False)
        contents = {}
        if settings.church_member:
            for val in settings.church_member:
                cmv = unicode(idnormalizer.normalize(val['church_member_values']))
                if cmv not in contents.keys():
                    contents[cmv] = val['church_member_values']
        return contents
    
    def author_data(self):
        membership = self.membership
        request = self.request
        if request.form:
            if 'id' in request.form:
                author = membership.getMemberById(request.form['id'])
                if author:
                    return True
        return False
    
    def author_info(self):
        membership = self.membership
        request = self.request
        results = {'fullname':'', 'portrait':'', 'user_biography':'', 'id':'', 'location':'', 'language':'', 'twitter':''}
        churches  = self.churchValues()
        if request.form:
            if 'id' in request.form:
                author = membership.getMemberById(request.form['id'])
                if author:
                    results['fullname'] = author.getProperty('fullname')
                    results['portrait'] = membership.getPersonalPortrait(request.form['id'])
                    results['user_biography'] = author.getProperty('user_biography')
                    results['id'] = request.form['id']
                    results['location'] = author.getProperty('location')
                    results['language'] = author.getProperty('language')
                    results['email'] = author.getProperty('email')
                    results['twitter'] = author.getProperty('twitter_username')
                    if author.getProperty('church') in churches.keys():
                        results['church'] = churches[author.getProperty('church')]
                    else:
                        results['church'] = ''
                    
                    results['homepage'] = author.getProperty('home_page')
        return results
                
    def posts(self, author=None):
        catalog = self.catalog
        brains = catalog.unrestrictedSearchResults(dict(sort_on='created', sort_order='reverse', portal_type=('News Item', 'Document', 'Event'), review_state=('shared_intranet')))
        
        results = []
        for brain in brains:
            
            if author in brain.listCreators:
                obj = brain._unrestrictedGetObject()
                data = {}
                data['creator'] = brain.listCreators
                data['modified'] = brain.modified
                data['title'] = brain.Title
                data['description'] = brain.description
                data['path'] = brain.getPath()
                data['obj'] = obj
                results.append(data)
                if len(results) ==4:
                    break;
        return results
    
    def totalComments(self, context=None):
        comments = IConversation(context)
        return len(comments)
    
    def filter_edit_profile(self):
        current_user = self.context.portal_membership.getAuthenticatedMember().getUserName()
        if 'id' in self.request.form:
            if self.request.form['id'] == current_user:
                return True
        return False
        
                
