from five import grok
from plone.app.layout.viewlets.interfaces import IBelowContentTitle
from Products.CMFCore.interfaces import IContentish
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from AccessControl import getSecurityManager
from zope.component import getMultiAdapter, queryMultiAdapter
from plone.app.layout.globals.interfaces import IViewView
from plone.app.content.browser.interfaces import IFolderContentsView
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr

grok.templatedir('templates')

class document_byline(grok.Viewlet):
    grok.name('plone.belowcontenttitle.documentbyline')
    grok.require('zope2.View')
    grok.viewletmanager(IBelowContentTitle)
    grok.context(IContentish)
    
    def show_history(self):
        if not _checkPermission('CMFEditions: Access previous versions', self.context):
            return False
        if IViewView.providedBy(self.__parent__):
            return True
        if IFolderContentsView.providedBy(self.__parent__):
            return True
        return False
    
    def locked_icon(self):
        if not getSecurityManager().checkPermission('Modify portal content',
                                                    self.context):
            return ""

        locked = False
        lock_info = queryMultiAdapter((self.context, self.request),
                                      name='plone_lock_info')
        if lock_info is not None:
            locked = lock_info.is_locked()
        else:
            context = aq_inner(self.context)
            lockable = getattr(context.aq_explicit, 'wl_isLocked', None) is not None
            locked = lockable and context.wl_isLocked()

        if not locked:
            return ""

        portal = self.portal_state.portal()
        icon = portal.restrictedTraverse('lock_icon.png')
        return icon.tag(title='Locked')
    
    def creator(self):
        return self.context.Creator()
    
    def authorname(self):
        author = self.author()
        return author and author['fullname'] or self.creator()
    
    def author(self):
        membership = getToolByName(self.context, 'portal_membership')
        return membership.getMemberInfo(self.creator())
    
    def isExpired(self):
        if base_hasattr(self.context, 'expires'):
            return self.context.expires().isPast()
        return False
    
    def pub_date(self):
        """Return object effective date.

        Return None if publication date is switched off in global site settings
        or if Effective Date is not set on object.
        """
        # check if we are allowed to display publication date
        properties = getToolByName(self.context, 'portal_properties')
        site_properties = getattr(properties, 'site_properties')
        if not site_properties.getProperty('displayPublicationDateInByline',
           False):
            return None

        # check if we have Effective Date set
        date = self.context.EffectiveDate()
        if not date or date == 'None':
            return None

        return DateTime(date)
    
    def toLocalizedTime(self, time, long_format=None, time_only = None):
        """Convert time to localized time
        """
        util = getToolByName(self.context, 'translation_service')
        return util.ulocalized_time(time, long_format, time_only, self.context,
                                    domain='plonelocales')
