# -*- coding:utf-8 -*-

from five import grok

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch

from plone.directives import form
from plone.directives import dexterity

from zope.component import getMultiAdapter
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
#from plone.formwidget.contenttree import ObjPathSourceBinder
#from plone.formwidget.autocomplete import AutocompleteFieldWidget

from z3c.relationfield.schema import Choice

from plone.app.layout.navigation.interfaces import INavigationRoot

from s17.organizationalunit import MessageFactory as _


@grok.provider(IContextSourceBinder)
def vocab_employees(context):
    ct = getToolByName(context, 'portal_catalog')
    query = {}
    query['path'] = {'query': '/'.join(context.getPhysicalPath()),
                     'depth': 2}
    query['portal_type'] = 'Employee'
    query['sort_on'] = 'sortable_title'
    employees = [SimpleTerm(b.UID, b.UID, b.Title) for b in ct.searchResults(**query)]
    return SimpleVocabulary(employees)


class IOrganizationalUnit(form.Schema):
    """ A representation of a Organizational Unit content type
    """

    # TODO: AutocompleteFieldWidget
    # form.widget()
    area_manager = Choice(
        title=_(u'Area Manager'),
        description=_(u'Assign one employee as manager for this area.'),
        source=vocab_employees,
        required=False,
    )

    # area_manager = RelationList(
    #     title=_(u'Area Manager'),
    #     default=[],
    #     value_type=RelationChoice(
    #         title=u"Area Manager",
    #         source=ObjPathSourceBinder(portal_type='Employee')),
    #     required=False,
    # )


class OrganizationalUnit(dexterity.Container):
    """ A Organizational Unit
    """
    grok.implements(IOrganizationalUnit)


class View(dexterity.DisplayForm):
    grok.context(IOrganizationalUnit)
    grok.require('zope2.View')
    grok.name('view')

    def portal_state(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        return portal_state

    def get_parents(self):
        """ Return the organizational unit parent's breadcrumbs
            if those parents are organizational units themselves.
        """
        parents = []
        obj = self.context
        while not INavigationRoot.providedBy(obj):
            obj = obj.__parent__
            if IOrganizationalUnit.providedBy(obj):
                parents.insert(0, obj)
        return parents

    def get_children(self):
        """ Return child organizational units
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {}
        query['path'] = {'query': '/'.join(self.context.getPhysicalPath()),
                         'depth': 1}
        query['portal_type'] = 'OrganizationalUnit'
        query['sort_on'] = 'sortable_title'
        content = catalog.searchResults(**query)
        return content

    def get_employees(self):
        """ Return organizational unit child employees
        """
        catalog = getToolByName(self.context, 'portal_personcatalog')
        query = {}
        query['path'] = {'query': '/'.join(self.context.getPhysicalPath()),
                         'depth': 1}
        query['portal_type'] = 'Employee'
        content = catalog.searchResults(**query)
        return content

    def get_employee_batch(self, b_start, first=False, snd=False):
        """ Return a batch of employees for navigation
        """
        contents = self.get_employees()
        has_employees = len(contents)
        if has_employees < 9 and not snd:
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
