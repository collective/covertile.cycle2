# -*- coding: utf-8 -*-
from covertile.cycle2 import _
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from collective.cover.widgets.textlinessortable import TextLinesSortableFieldWidget
from plone import api
from plone.autoform import directives as form
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implements


class ICarouselTile(IListTile):

    """A carousel based on the Cycle2 slideshow plugin for jQuery."""

    #form.omitted('autoplay')
    #form.no_omit(ITileEditForm, 'autoplay')
    autoplay = schema.Bool(
        title=_(u'Auto play'),
        default=False,
        required=False,
    )

    form.no_omit(ITileEditForm, 'uuids')
    form.widget(uuids=TextLinesSortableFieldWidget)


class CarouselTile(ListTile):

    """A carousel based on the Cycle2 slideshow plugin for jQuery."""

    implements(ICarouselTile)
    index = ViewPageTemplateFile('templates/carousel.pt')
    is_configurable = True
    is_editable = True
    short_name = _(u'msg_short_name_carousel', default=u'Carousel')

    def populate_with_object(self, obj):
        """Add an object to the carousel. This method will append new
        elements to the already existing list of items. If the object
        does not have an image associated, it will not be included and
        silently ignored.

        :param uuids: The list of objects' UUIDs to be used
        :type uuids: List of strings
        """
        if not self._has_image_field(obj):
            return
        super(CarouselTile, self).populate_with_object(obj)

    @property
    def paused(self):
        """Return True if the carousel will begin in a paused state."""
        paused = not self.data.get('autoplay', False)
        return str(paused).lower()

    def get_title(self, item):
        """Get the title of the item, or the custom title if set.

        :param item: [required] The item for which we want the title
        :type item: Content object
        :returns: the item title
        :rtype: unicode
        """
        # First we get the title for the item itself
        title = item.Title()
        uuid = self.get_uid(item)
        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        uuids = data['uuids']
        if uuid in uuids:
            if uuids[uuid].get('custom_title', u''):
                # If we had a custom title set, then get that
                title = uuids[uuid].get('custom_title')
        return title

    def get_description(self, item):
        """Get the description of the item, or the custom description
        if set.

        :param item: [required] The item for which we want the description
        :type item: Content object
        :returns: the item description
        :rtype: unicode
        """
        # First we get the url for the item itself
        description = item.Description()
        uuid = self.get_uid(item)
        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        uuids = data['uuids']
        if uuid in uuids:
            if uuids[uuid].get('custom_description', u''):
                # If we had a custom description set, then get that
                description = uuids[uuid].get('custom_description')
        return description

    def _get_types_that_use_view_action(self):
        """Return a list of types that use the view action in listings.

        :returns: a list of content types
        :rtype: tuple
        """
        portal_properties = api.portal.get_tool('portal_properties')
        return portal_properties.site_properties.getProperty(
            'typesUseViewActionInListings', ())

    def get_url(self, item):
        """Get the URL of the item, or the custom URL if set.

        :param item: [required] The item for which we want the URL
        :type item: Content object
        :returns: the item URL
        :rtype: str
        """
        # First we get the url for the item itself
        url = item.absolute_url()
        if item.portal_type in self._get_types_that_use_view_action():
            url = url + '/view'
        uuid = self.get_uid(item)
        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        uuids = data['uuids']
        if uuid in uuids:
            if uuids[uuid].get('custom_url', u''):
                # If we had a custom url set, then get that
                url = uuids[uuid].get('custom_url')
        return url
