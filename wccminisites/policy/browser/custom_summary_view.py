from five import grok
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.PloneBatch import Batch



grok.templatedir('templates')

class CustomSummaryView(BrowserView):
    
    def folder_contents(self):
        context = self.context
        brains = context.portal_catalog.unrestrictedSearchResults(path={'query':'/'.join(context.getPhysicalPath()),
                                                                        'depth':1},
                                                                  sort_order='reverse',
                                                                  sort_on='created')
        
        contents = [b.getObject() for b in brains]
        #if contents:
        #    b_start = self.context.REQUEST.get('b_start', 0)
        #    batch = Batch(contents, b_size, int(b_start), orphan=0)
        #    return batch
        return brains
    
