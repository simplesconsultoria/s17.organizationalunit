# -*- coding:utf-8 -*-

from five import grok

from Products.CMFCore.utils import getToolByName

from plone.directives import form
from plone.directives import dexterity

from plone.formwidget.contenttree import ObjPathSourceBinder

from z3c.relationfield.schema import RelationList, RelationChoice

from s17.content.organizationalunit import MessageFactory as _


class IOrganizationalUnit(form.Schema):
    """ A representation of a Content Embedder content type
    """

    area_manager = RelationList(
        title=_(u'Area Manager'),
        default=[],
        value_type=RelationChoice(title=u"Area Manager",
                      source=ObjPathSourceBinder(portal_type='s17.employee')),
        required=False,
        )


class OrganizationalUnit(dexterity.Container):
    """ A Content Embedder
    """
    grok.implements(IOrganizationalUnit)


class View(dexterity.DisplayForm):
    grok.context(IOrganizationalUnit)
    grok.require('zope2.View')
    grok.name('view')

    def get_father_ou(self):
        """ Returns the organizationalunit father if exist.
        """
        result = None
        parent = self.context.__parent__
        is_father = IOrganizationalUnit.providedBy(parent)
        if is_father:
            result = {'title': parent.title,
                      'url': parent.absolute_url()}
        return result

    def has_employees(self):
        """ Tell us if have child employees.
        """
        employees = self.get_child_employees()
        return len(employees) > 1

    def has_ous(self):
        """ Tell us if have child organizationalunits.
        """
        ous = self.get_child_ous()
        return len(ous) > 1

    def get_child_ous(self):
        """ If it have child organizationalunits, then return them.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        query['path'] = '/'.join(self.context.getPhysicalPath()) + '/'
        query['portal_type'] = 's17.organizationalunit'
        content = catalog.searchResults(**query)
        return content

    def get_child_employees(self):
        """ If it have child employees, then return them.
        """
        catalog = getToolByName(self.context, 'portal_personcatalog')
        query = {}
        query['path'] = '/'.join(self.context.getPhysicalPath()) + '/'
        query['portal_type'] = 's17.employee'
        content = catalog.searchResults(**query)
        return content

    def get_employee_batch(self, b_start, first=False, snd=False):
        """ Return a batch of employees for navigation.
        """
        from Products.CMFPlone import Batch
        contents = self.get_child_employees()
        has_employees = self.has_employees()
        if len(contents) < 9 and not snd:
            batch = Batch(contents, len(contents), int(b_start), orphan=0)
            return batch
        if has_employees and (not first) and (not snd):
            batch = Batch(contents, 8, int(b_start), orphan=0)
            return batch
        elif has_employees and first:
            batch = Batch(contents, 4, int(b_start), orphan=0)
            return batch
        elif has_employees and snd:
            b_start = int(b_start) + 4
            if b_start < len(contents):
                batch = Batch(contents, 4, b_start, orphan=0)
                return batch
