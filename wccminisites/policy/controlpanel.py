from plone.app.registry.browser.controlpanel import RegistryEditForm, ControlPanelFormWrapper
from wccminisites.policy.interfaces import IChurchMember, IChurchMemberDGForm
from collective.z3cform.datagridfield import DataGridFieldFactory

class ChurchMemberForm(RegistryEditForm):
    schema = IChurchMemberDGForm
    label = u"Church Member List"
    
    def updateFields(self):
        super(ChurchMemberForm, self).updateFields()
        self.fields['church_member'].widgetFactory = DataGridFieldFactory
    
    def updateWidgets(self):
        super(ChurchMemberForm, self).updateWidgets()
        
    
    
class ChurchMemberFormView(ControlPanelFormWrapper):
    form = ChurchMemberForm