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
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from wccminisites.policy.interfaces import IChurchMemberDGForm
from five import grok

@grok.provider(IContextSourceBinder)
def church_member_val(context):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IChurchMemberDGForm, check=False)
    values = []
    result = []
    if settings.church_member:
        for val in settings.church_member:
            values.append({'value':unicode(val['church_member_values']), 'title':val['church_member_values']})
            #values.append(SimpleTerm(value=unicode(val['church_member_values']), token=unicode(val['church_member_values']), title=val['church_member_values']))
    if values:
        values.sort(key=lambda k:k['title'])
        result = [SimpleTerm(value=v['value'], token=v['value'], title=v['value']) for v in values]
    return SimpleVocabulary(result)

regions_val = SimpleVocabulary([SimpleTerm(value=u'Africa', title=_(u'Africa')),
                            SimpleTerm(value=u'Asia', title=_(u'Asia')),
                            SimpleTerm(value=u'Caribbean', title=_(u'Caribbean')),
                            SimpleTerm(value=u'Europe', title=_(u'Europe')),
                            SimpleTerm(value=u'Latin America', title=_(u'Latin America')),
                            SimpleTerm(value=u'Middle East', title=_(u'Middle East')),
                            SimpleTerm(value=u'North America', title=_(u'North America')),
                            SimpleTerm(value=u'Pacific', title=_(u'Pacific'))])

wcc_commission_val = SimpleVocabulary([SimpleTerm(value='Commission of the Churches on International Affairs', title=_(u'Commission of the Churches on International Affairs')),
                                       SimpleTerm(value='Commission on Education and Ecumenical Formation', title=_(u'Commission on Education and Ecumenical Formation')),
                                       SimpleTerm(value='Commission on Faith and Order', title=_(u'Commission on Faith and Order')),
                                       SimpleTerm(value='Commission on World Mission and Evangelism', title=_(u'Commission on World Mission and Evangelism')),
                                       SimpleTerm(value='ECHOS Commission on Youth in the Ecumenical Movement', title=_(u'ECHOS Commission on Youth in the Ecumenical Movement')),
                                       SimpleTerm(value='Joint Consultative Commission with Christian World Communions', title=_(u'Joint Consultative Commission with Christian World Communions')),
                                       SimpleTerm(value='Joint Consultative Group between the WCC and Pentecostals', title=_(u'Joint Consultative Group between the WCC and Pentecostals')),
                                       SimpleTerm(value='Joint Working Group with the Roman Catholic Church', title=_(u'Joint Working Group with the Roman Catholic Church'))])

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
    
    church = schema.Choice(
        title = _(u'Church'),
        required = True,
        source = church_member_val,
    )
    
    region = schema.Choice(
        title = _(u"Region"),
        required = True,
        vocabulary = regions_val,
    )
    
    wcc_commission = schema.List(
        title = _(u'WCC Commission or Governing Body'),
        required = True,
        value_type = schema.Choice(
            vocabulary = wcc_commission_val,
        )
    )
    
    # user_biography = RichText(
    #         title=u"Body text",
    #         default_mime_type='text/structured',
    #         output_mime_type='text/html',
    #         allowed_mime_types=('text/structured', 'text/plain',),
    #         default=u"Default value"
    #     )
    

#class IExtendedSchema(IEnhancedUserDataSchema):

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
        #self.add(fields)
        self.form_fields = self.form_fields.omit('description')
        self.form_fields['user_biography'].custom_widget = WYSIWYGWidget
        self.form_fields['location'].field.title = u"Country"
        self.form_fields['location'].field.description = u"(Country of origin and/or country of residence)"
        
