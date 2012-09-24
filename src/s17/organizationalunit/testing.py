# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import s17.organizationalunit
        self.loadZCML(package=s17.organizationalunit)
        z2.installProduct(app, 's17.organizationalunit')
        z2.installProduct(app, 's17.person.employee')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 's17.organizationalunit:default')
        self.applyProfile(portal, 's17.person.employee:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 's17.person.employee')
        z2.uninstallProduct(app, 's17.organizationalunit')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='s17.organizationalunit:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='s17.organizationalunit:Functional',
    )