from zope.interface import implements
from zope import schema
from wccminisites.policy import MessageFactory as _
from plone.supermodel import model
from zope.component import adapter
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.z3cform.fieldsets import extensible
from z3c.form.field import Fields
from plone.app.users.browser.register import RegistrationForm
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.directives import dexterity, form

# from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget

from plone.app.textfield import RichText
from zope.interface import Interface
#from plone.directives import form
from z3c.form import form
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from wccminisites.policy.interfaces import IProductSpecific


class IEnhancedUserDataSchema(IUserDataSchema):
    # ...
    twitter_username = schema.TextLine(
        title=_(u'label_twitter', default=u'Twitter'),
        description=_(u'desc_twitter_username',
                      default=u"Enter your Twitter Account"),
        required=False,
        )
    #form.widget(user_biography=WysiwygFieldWidget)
    user_biography = schema.Text(
        title=_(u'label_user_biography', default=u'Biography'),
        description=_(u'desc_user_biography',
                      default=u"A short overview of who you are and what you do. Will be displayed on your author page, linked from the items you create."),
        required=False,
        )
    
    # user_biography = RichText(
    #         title=u"Body text",
    #         default_mime_type='text/structured',
    #         output_mime_type='text/html',
    #         allowed_mime_types=('text/structured', 'text/plain',),
    #         default=u"Default value"
    #     )
    

# class ITestSchema(model.Schema):

#     form.widget('body', WysiwygFieldWidget)
#     body = schema.Text(title=u"Body text")


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema
    
    
@adapter(Interface, IProductSpecific, UserDataPanel)
class WCCMinisiteUserDataPanelExtender(extensible.FormExtender):
    
    def update(self):
        fields = Fields(IEnhancedUserDataSchema)
        self.add(fields)
        
@adapter(Interface, IProductSpecific, RegistrationForm)
class WCCMinisiteRegistrationPanelExtender(extensible.FormExtender):
    
    def update(self):
        fields = Fields(IEnhancedUserDataSchema)
        #NB: Not omitting the accept field this time, we want people to check it
        self.add(fields)


class CustomizedUserDataPanel(UserDataPanel):
    def __init__(self, context, request):
        super(CustomizedUserDataPanel, self).__init__(context, request)
        self.form_fields = self.form_fields.omit('description')
        self.form_fields['user_biography'].custom_widget = WYSIWYGWidget
