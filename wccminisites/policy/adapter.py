from plone.app.users.browser.account import AccountPanelSchemaAdapter
from wccminisites.policy.userdataschema import IEnhancedUserDataSchema
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class EnhancedUserDataSchemaAdapter(UserDataPanelAdapter):
    #schema = IEnhancedUserDataSchema
    
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
