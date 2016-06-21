# -*- coding: utf-8 -*-
"""Setup test fixtures.

We have to set different test fixtures depending on features we want:

plone.app.contenttypes:
    installed under Plone 4.3, if requested
"""
from collective.cover.testing import generate_jpeg
from collective.cover.tests.utils import create_standard_content_for_tests
from collective.cover.tests.utils import set_image_field
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


import os
import pkg_resources

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    DEXTERITY_ONLY = False
else:
    # this environment variable is set in .travis.yml test matrix
    DEXTERITY_ONLY = os.environ.get('DEXTERITY_ONLY') is not None


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if DEXTERITY_ONLY:
            import plone.app.contenttypes
            self.loadZCML(package=plone.app.contenttypes)
            z2.installProduct(app, 'Products.DateRecurringIndex')

        import collective.cover
        self.loadZCML(package=collective.cover)
        import covertile.cycle2
        self.loadZCML(package=covertile.cycle2)

    def setUpPloneSite(self, portal):
        if DEXTERITY_ONLY:
            self.applyProfile(portal, 'plone.app.contenttypes:default')

        self.applyProfile(portal, 'collective.cover:default')
        self.applyProfile(portal, 'collective.cover:testfixture')
        self.applyProfile(portal, 'covertile.cycle2:default')

        # setup test content
        create_standard_content_for_tests(portal)
        set_image_field(portal['my-image1'], generate_jpeg(900, 400))
        set_image_field(portal['my-image2'], generate_jpeg(900, 400))


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='covertile.cycle2:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='covertile.cycle2:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='covertile.cycle2:Robot',
)
