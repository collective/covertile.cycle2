# -*- coding: utf-8 -*-
from collective.cover.testing import generate_jpeg
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.cover
        self.loadZCML(package=collective.cover)
        import covertile.cycle2
        self.loadZCML(package=covertile.cycle2)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.cover:default')
        self.applyProfile(portal, 'collective.cover:testfixture')
        self.applyProfile(portal, 'covertile.cycle2:default')
        portal['my-image1'].setImage(generate_jpeg(900, 400))
        portal['my-image1'].reindexObject()
        portal['my-image2'].setImage(generate_jpeg(900, 400))
        portal['my-image2'].reindexObject()


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='covertile.cycle2:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='covertile.cycle2:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='covertile.cycle2:Robot')
