# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.interface.verify import verifyClass, verifyObject

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from s17.person.employee.content.employee import IEmployee

from s17.content.organizationalunit.content.organizationalunit import IOrganizationalUnit
from s17.content.organizationalunit.content.organizationalunit import OrganizationalUnit
from s17.content.organizationalunit.testing import INTEGRATION_TESTING


class OrganizationalUnitTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('s17.organizationalunit', 'ou1')
        self.ou = self.folder['ou1']

    def test_adding(self):
        self.assertTrue(IOrganizationalUnit.providedBy(self.ou))
        self.assertTrue(verifyClass(IOrganizationalUnit, OrganizationalUnit))

    def test_interface(self):
        self.assertTrue(IOrganizationalUnit.providedBy(self.ou))
        self.assertTrue(verifyObject(IOrganizationalUnit, self.ou))

    def test_add_employee(self):
        self.ou.invokeFactory('s17.employee', 'e1')
        e1 = self.ou['e1']
        self.assertTrue(verifyObject(IEmployee, e1))

    def test_add_ou(self):
        self.ou.invokeFactory('s17.organizationalunit', 'sub_ou')
        sub_ou = self.ou['sub_ou']
        self.assertTrue(verifyObject(IOrganizationalUnit, sub_ou))
