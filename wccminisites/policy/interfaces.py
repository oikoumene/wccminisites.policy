from zope.interface import Interface
from wccminisites.policy import MessageFactory as _
from quintagroup.formlib.captcha import Captcha
from zope import schema
from plone.directives import dexterity, form
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.supermodel import model

class IProductSpecific(Interface):
    pass

class IExtendRegistrationForm(Interface):
    """Marker interface for my custom registration form
    """

class ICaptchaSchema(Interface):
    captcha = Captcha(
        title=_(u'Type the code'),
        description=_(u'Type the code from the picture shown below.'))
    
class IUserApprovedEvent(Interface):
    pass

class IUserRejectedEvent(Interface):
    pass

class IUserRegisteredEvent(Interface):
    pass

class IRegistrationApproval(Interface):

    def get(key):
        pass

    def add(key, data):
        pass

    def approve(key):
        pass

    def reject(key):
        pass
    
    
class IChurchMember(Interface):
    church_member_values = schema.TextLine(
        title = u"Church Member",
    )
    
class IChurchMemberDGForm(Interface):
    
    #form.widget(church_member=DataGridFieldFactory)
    church_member = schema.List(
        title=u"Chuch Member",
        required=False,
        value_type=DictRow(title=u"Value", schema=IChurchMember)
    )
