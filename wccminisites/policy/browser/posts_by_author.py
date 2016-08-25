from five import grok
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATFolder
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.discussion.interfaces import IConversation, IComment
from Products.CMFPlone.PloneBatch import Batch
from wccminisites.policy.interfaces import IProductSpecific

grok.templatedir('templates')

class posts_by_author(grok.View):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.layer(IProductSpecific)

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    def contents(self):
        results = []
        author = self.authorValue()
        brains = self.catalog.searchResults(portal_type=('News Item', 'Page', 'Event'),
                                                  sort_on='created',
                                                  sort_order='reverse',
                                                  review_state='shared_intranet')
        for brain in brains:
            if author in brain.listCreators or author == '':
                results.append(brain)
        #b_start = self.context.REQUEST.get('b_start',0)
        #b_size = 1
        #batch = Batch(results, b_size, int(b_start), orphan=0)
        return results
    
    def authorValue(self):
        tag = ''
        request = self.request
        if request.form:
            if 'name' in request.form:
                tag = request.form['name']
        return tag
    
    def totalComments(self, context=None):
        comments = IConversation(context)
        return len(comments)
    
