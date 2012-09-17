# -*- coding:utf-8 -*-

from five import grok

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
