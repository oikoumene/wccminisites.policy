from zope.interface import implements
from plone.app.users.browser.register import RegistrationForm
from quintagroup.formlib.captcha import CaptchaWidget
from wccminisites.policy import MessageFactory as _
from wccminisites.policy.interfaces import ICaptchaSchema, IExtendRegistrationForm
from zope.formlib import form
from zope.component import getUtility, getAdapter
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ExtendRegistrationForm(RegistrationForm):
    implements(IExtendRegistrationForm)
    template = ViewPageTemplateFile('registration_form.pt')
    
    @property
    def form_fields(self):
        my_fields = super(ExtendRegistrationForm, self).form_fields
        my_fields += form.Fields(ICaptchaSchema)
        
        #my_fields.append(form.Fields(ICaptchaSchema)) --> test
        #my_fields['captcha'].custom_widget = CaptchaWidget
        
        for fld in my_fields:
            if fld.__name__ == 'captcha':
                
                fld.field.custom_widget = CaptchaWidget
        return my_fields
    
    @property
    def showForm(self):
        """The form should not be displayed to the user if the system is
           incapable of sending emails and email validation is switched on
           (users are not allowed to select their own passwords).
        """
        portal = getUtility(ISiteRoot)
        ctrlOverview = getMultiAdapter((portal, self.request),
                                       name='overview-controlpanel')

        # hide form iff mailhost_warning == True and validate_email == True
        return not (ctrlOverview.mailhost_warning() and
                    portal.getProperty('validate_email', True))
    
    
