from plone.app.users.browser.account import AccountPanelSchemaAdapter
from wccminisites.policy.userdataschema import IEnhancedUserDataSchema
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class EnhancedUserDataSchemaAdapter(UserDataPanelAdapter):
    #schema = IEnhancedUserDataSchema
    
    def get_church(self):
        return self.context.getProperty('church', '')
    def set_church(self, value):
        return self.context.setMemberProperties({'church': value})
    church = property(get_church, set_church)
    
    def get_region(self):
        return self.context.getProperty('region', '')
    def set_region(self, value):
        return self.context.setMemberProperties({'region': value})
    region = property(get_region, set_region)
    
    def get_wcc_commission(self):
        return self.context.getProperty('wcc_commission', '')
    def set_wcc_commission(self, value):
        return self.context.setMemberProperties({'wcc_commission': value})
    wcc_commission = property(get_wcc_commission, set_wcc_commission)
    
    def get_twitter_username(self):
        return self.context.getProperty('twitter_username', '')
    def set_twitter_username(self, value):
        return self.context.setMemberProperties({'twitter_username': value})
    twitter_username = property(get_twitter_username, set_twitter_username)

    def get_user_biography(self):
        return self.context.getProperty('user_biography', '')
    def set_user_biography(self, value):
        return self.context.setMemberProperties({'user_biography': value})
    user_biography = property(get_user_biography, set_user_biography)
