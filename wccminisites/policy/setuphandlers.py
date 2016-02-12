from collective.grok import gs
from wccminisites.policy import MessageFactory as _

@gs.importstep(
    name=u'wccminisites.policy', 
    title=_('wccminisites.policy import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wccminisites.policy.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
