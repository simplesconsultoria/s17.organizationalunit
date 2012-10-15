# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.interface.verify import verifyClass, verifyObject

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from s17.employee.content.employee import IEmployee

from s17.organizationalunit.content.organizationalunit import IOrganizationalUnit
from s17.organizationalunit.content.organizationalunit import OrganizationalUnit
from s17.organizationalunit.testing import INTEGRATION_TESTING


class OrganizationalUnitTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('OrganizationalUnit', 'ou1')
        self.ou = self.folder['ou1']

    def test_adding(self):
        self.assertTrue(IOrganizationalUnit.providedBy(self.ou))
        self.assertTrue(verifyClass(IOrganizationalUnit, OrganizationalUnit))

    def test_interface(self):
        self.assertTrue(IOrganizationalUnit.providedBy(self.ou))
        self.assertTrue(verifyObject(IOrganizationalUnit, self.ou))

    def test_add_employee(self):
        self.ou.invokeFactory('Employee', 'e1')
        e1 = self.ou['e1']
        self.assertTrue(verifyObject(IEmployee, e1))

    def test_add_ou(self):
        self.ou.invokeFactory('OrganizationalUnit', 'sub-ou')
        sub_ou = self.ou['sub-ou']
        self.assertTrue(verifyObject(IOrganizationalUnit, sub_ou))


class OrganizationalUnitViewTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.create_ous()
        self.create_employees()
        self.ou_view = self.ou.unrestrictedTraverse('view')
        self.sub_ou_view = self.sub_ou.unrestrictedTraverse('view')
        self.sub_sub_ou_view = self.sub_sub_ou.unrestrictedTraverse('view')

    def create_ous(self):
        """  Create organizationalunit objects
        """
        self.portal.invokeFactory('OrganizationalUnit', 'ou')
        self.ou = self.portal['ou']
        self.ou.invokeFactory('OrganizationalUnit', 'sub-ou')
        self.sub_ou = self.ou['sub-ou']
        self.sub_ou.invokeFactory('OrganizationalUnit', 'sub-sub-ou')
        self.sub_sub_ou = self.sub_ou['sub-sub-ou']

    def create_employees(self):
        """ Create Employees objects
        """
        index = 1
        while index < 17:
            self.ou.invokeFactory('Employee', 'employee-%s' % index)
            index += 1
        self.sub_ou.invokeFactory('Employee', 'sub-employee')
        self.sub_sub_ou.invokeFactory('Employee', 'sub-sub-employee')

    def test_get_parents(self):
        parent = self.sub_ou_view.get_parents()[0]
        self.assertEqual(parent.absolute_url(), self.ou.absolute_url())

    def test_get_children(self):
        children = self.ou_view.get_children()
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].getId, 'sub-ou')

    def test_get_employees(self):
        children = self.ou_view.get_employees()
        self.assertEqual(len(children), 16)

    def test_get_employee_batch_simple_page(self):
        batch = self.sub_ou_view.get_employee_batch(b_start=0)
        self.assertEqual(len(batch), 1)
        self.assertEqual(batch[0].getObject().getId(), 'sub-employee')

        batch = self.sub_sub_ou_view.get_employee_batch(b_start=0)
        self.assertEqual(len(batch), 1)
        self.assertEqual(batch[0].getObject().getId(), 'sub-sub-employee')

    def test_get_employee_batch_multiple_pages(self):
        # Page 1
        batch = self.ou_view.get_employee_batch(b_start=0)
        self.assertEqual(len(batch), 8)
        self.assertEqual(batch[0].getObject().getId(), 'employee-1')
        self.assertEqual(batch[1].getObject().getId(), 'employee-2')
        self.assertEqual(batch[2].getObject().getId(), 'employee-3')
        self.assertEqual(batch[3].getObject().getId(), 'employee-4')
        self.assertEqual(batch[4].getObject().getId(), 'employee-5')
        self.assertEqual(batch[5].getObject().getId(), 'employee-6')
        self.assertEqual(batch[6].getObject().getId(), 'employee-7')
        self.assertEqual(batch[7].getObject().getId(), 'employee-8')

        # Page 2
        batch = self.ou_view.get_employee_batch(b_start=8)
        self.assertEqual(len(batch), 8)
        self.assertEqual(batch[0].getObject().getId(), 'employee-9')
        self.assertEqual(batch[1].getObject().getId(), 'employee-10')
        self.assertEqual(batch[2].getObject().getId(), 'employee-11')
        self.assertEqual(batch[3].getObject().getId(), 'employee-12')
        self.assertEqual(batch[4].getObject().getId(), 'employee-13')
        self.assertEqual(batch[5].getObject().getId(), 'employee-14')
        self.assertEqual(batch[6].getObject().getId(), 'employee-15')
        self.assertEqual(batch[7].getObject().getId(), 'employee-16')

        # Page 3
        batch = self.ou_view.get_employee_batch(b_start=16)
        self.assertEqual(len(batch), 1)

    def test_get_batch_rows(self):
        batch = self.ou_view.get_employee_batch(b_start=0, first=True)
        self.assertEqual(len(batch), 4)
        self.assertEqual(batch[0].getObject().getId(), 'employee-1')
        self.assertEqual(batch[1].getObject().getId(), 'employee-2')
        self.assertEqual(batch[2].getObject().getId(), 'employee-3')
        self.assertEqual(batch[3].getObject().getId(), 'employee-4')

        batch = self.ou_view.get_employee_batch(b_start=0, snd=True)
        self.assertEqual(len(batch), 4)
        self.assertEqual(batch[0].getObject().getId(), 'employee-5')
        self.assertEqual(batch[1].getObject().getId(), 'employee-6')
        self.assertEqual(batch[2].getObject().getId(), 'employee-7')
        self.assertEqual(batch[3].getObject().getId(), 'employee-8')
