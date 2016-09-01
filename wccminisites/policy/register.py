from zope.interface import implements
from plone.app.users.browser.register import RegistrationForm, BaseRegistrationForm
from quintagroup.formlib.captcha import CaptchaWidget
from wccminisites.policy import MessageFactory as _
from wccminisites.policy.interfaces import ICaptchaSchema, IExtendRegistrationForm
from zope.formlib import form
from zope.component import getUtility, getAdapter
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite

class ExtendRegistrationForm(RegistrationForm):
    implements(IExtendRegistrationForm)
    template = ViewPageTemplateFile('registration_form.pt')
    
    @property
    def form_fields(self):
        #my_fields = super(ExtendRegistrationForm, self).form_fields
        my_fields = BaseRegistrationForm(self, self.context).form_fields
        my_fields += form.Fields(ICaptchaSchema)
        
        #my_fields.append(form.Fields(ICaptchaSchema)) --> test
        my_fields['captcha'].custom_widget = CaptchaWidget
        
        #for fld in my_fields:
        #    if fld.__name__ == 'captcha':
        #        
        #        fld.field.custom_widget = CaptchaWidget
        
        return my_fields.omit('password', 'password_ctl', 'mail_me')
    
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
    
    def validate_registration(self, action, data):
        errors = super(ExtendRegistrationForm, self).validate_registration(action,data)

        #if not self.context.restrictedTraverse('@@captcha').verify():
        #    err_str = u'Invalid captcha'
        #    errors.append(ValidationError(err_str))

        portal_props = getToolByName(self.context, 'portal_properties')
        props = portal_props.site_properties
        use_email_as_login = props.getProperty('use_email_as_login')

        error_keys = [error.field_name for error in errors
                      if hasattr(error, 'field_name')]

        username = ''
        email = ''
        try:
            email = self.widgets['email'].getInputValue()
        except InputErrors, exc:
            # WrongType?
            errors.append(exc)
        if use_email_as_login:
            username_field = 'email'
            username = email
        else:
            username_field = 'username'
            try:
                username = self.widgets['username'].getInputValue()
            except InputErrors, exc:
                errors.append(exc)
        
        ratool = getToolByName(self.context, 'wcc_minisites_registration_approval')
    
        # check if username is allowed
        if not username_field in error_keys:
            if not ratool.is_memberid_allowed(username):
                err_str = (u"The login name you selected is already in use "
                            "or is not valid. Please choose another.")
                errors.append(WidgetInputError(
                        username_field, u'label_username', err_str))
                self.widgets[username_field].error = err_str
 
        return errors
    
    def handle_join_success(self, data):
        portal_props = getToolByName(self.context, 'portal_properties')
        props = portal_props.site_properties
        use_email_as_login = props.getProperty('use_email_as_login')

        username = ''
        email = ''
        email = self.widgets['email'].getInputValue()
        if use_email_as_login:
            username = email
            data['username'] = data['email']
        else:
            username = self.widgets['username'].getInputValue()

        ratool = getToolByName(self.context, 'wcc_minisites_registration_approval')

        ratool.add(username, data)

    @form.action(u'Register',
                 validator='validate_registration', name=u'register')
    def action_join(self, action, data):
        self.handle_join_success(data)
        return self.request.response.redirect(getSite().absolute_url() +
                '/registration_success')
    
