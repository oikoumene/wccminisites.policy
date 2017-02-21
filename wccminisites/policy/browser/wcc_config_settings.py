from five import grok
from Products.CMFCore.interfaces import ISiteRoot

grok.templatedir('templates')

class wcc_config_settings(grok.View):
    grok.name('wcc-configuration-settings')
    grok.context(ISiteRoot)