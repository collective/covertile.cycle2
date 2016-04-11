# -*- coding: utf-8 -*-
from covertile.cycle2.config import PROJECTNAME
from plone import api


def remove_tile(portal):
    tiles = api.portal.get_registry_record('plone.app.tiles')
    if u'covertile.cycle2.carousel' in tiles:
        tiles.remove(u'covertile.cycle2.carousel')


def uninstall(portal, reinstall=False):
    if not reinstall:
        remove_tile(portal)
        profile = 'profile-{0}:uninstall'.format(PROJECTNAME)
        setup_tool = api.portal.get_tool('portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        return 'Ran all uninstall steps.'
