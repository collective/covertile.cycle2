# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

PROJECTNAME = 'covertile.cycle2'


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            u'covertile.cycle2:uninstall',
        ]
