# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.browserlayer.utils import registered_layers

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from s17.content.organizationalunit.config import PROJECTNAME
from s17.content.organizationalunit.testing import INTEGRATION_TESTING

CSS = [
    "organizationalunit.css",
    ]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertTrue(id in resource_ids, '%s not installed' % id)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertTrue(id not in resource_ids, '%s not removed' % id)
