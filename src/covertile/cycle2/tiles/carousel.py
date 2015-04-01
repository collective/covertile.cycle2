# -*- coding: utf-8 -*-
from covertile.cycle2 import _
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from collective.cover.widgets.textlinessortable import TextLinesSortableFieldWidget
from plone import api
from plone.autoform import directives as form
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


# Types of Pager style used in Carousel Tiles
PAGER_STYLES = SimpleVocabulary(
                    [SimpleTerm(value='dots', title=_(u'Dots')),
                     SimpleTerm(value='numbers', title=_(u'Numbers')),
                     SimpleTerm(value='thumbnails', title=_(u'Thumbnails'))]
               )

PAGER_TEMPLATES = {
        'dots': "<span>&bull;</span>",
        'numbers': "<strong><a href=#> {{slideNum}} </a></strong>",
        'thumbnails': "<a href='#'><img src='{{thumbnail}}' width=49 height=49></a>"
        }

class ICarouselTile(IListTile):

    """A carousel based on the Cycle2 slideshow plugin for jQuery."""

    form.omitted('autoplay')
    form.no_omit(ITileEditForm, 'autoplay')
    autoplay = schema.Bool(
        title=_(u'Auto play'),
        required=False,
        default=True,
    )

    form.no_omit(ITileEditForm, 'uuids')
    form.widget(uuids=TextLinesSortableFieldWidget)

    pager_style = schema.Choice(
        title=_(u'Pager'),
        vocabulary=PAGER_STYLES,
        required=True,
        default='dots',
    )
    form.omitted('pager_style')
    form.no_omit(IDefaultConfigureForm, 'pager_style')
    form.widget(pager_style='collective.cover.tiles.configuration_widgets.cssclasswidget.CSSClassFieldWidget')

    overlay = schema.SourceText(
        title=_(u'Overlay Template'),
        required=False,
        default=u'<div id="c2-overlay-title">{{title}}</div>'
                u'<div id="c2-overlay-desc">{{desc}}</div>',
    )
    form.omitted('overlay')
    form.no_omit(IDefaultConfigureForm, 'overlay')
    form.widget(overlay='covertile.cycle2.tiles.configuration_widgets.overlaytextarea.OverlayTextAreaFieldWidget')


class CarouselTile(ListTile):

    """A carousel based on the Cycle2 slideshow plugin for jQuery."""

    implements(ICarouselTile)
    index = ViewPageTemplateFile('templates/carousel.pt')
    is_configurable = True
    is_editable = True
    short_name = _(u'msg_short_name_carousel', default=u'C2 Carousel')

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
        """ Return 'true' or 'false' depending on whether the carousel
            will begin in a paused state. Value is intended for Javascript."""
        autoplay = self.data.get('autoplay', None)  # autoplay init'd to None
        autoplay = True if autoplay is None else autoplay  # default to True
        paused_str = str(not autoplay).lower()
        return paused_str

    def pagerclass(self):
        """
        """
        tile_conf = self.get_tile_configuration()
        pager_conf = tile_conf.get('pager_style', None)
        #pager_style = pager_conf.get('', None)
        # stored value could be none - default should be 'dots'
        #return pager_style or 'dots'
        return 'dots'

    def pagerthumbnail(self, item):
        """Return the thumbnail of an image if the item has an image field, the
        pager_style is 'Thumbnails' and the pager is visible.

        :param item: [required]
        :type item: content object
        """
        #pager_style = self.data.get('pager_style', None)
        #if pager_style is None or pager_style != 'Thumbnails':

            #return None  # skip expensive image processing

        #if not (self._has_image_field(item) and
                #self._field_is_visible('pager_style')):
            #return None

        scales = item.restrictedTraverse('@@images')
        return scales.scale('image', width=49, height=49, direction='down')

    def pagertemplate(self):
        #pager_style = self.data.get('pager_style', None)
        #if pager_style is None or pager_style == 'Dots':
            #return "<span>&bull;</span>"
        #elif pager_style == 'Numbers':
            #return "<strong><a href=#> {{slideNum}} </a></strong>"
        #elif pager_style == 'Thumbnails':
            #return "<a href='#'><img src='{{thumbnail}}' width=49 height=49></a>"
        # return "<a href='#'><img src='{{thumbnail}}' width=49 height=49></a>"
        return PAGER_TEMPLATES.get(self.pagerclass())

    def overlaytemplate(self):
        if not self._field_is_visible('overlay'):
            return ''
        else:
            tile_conf = self.get_tile_configuration()
            overlay_conf = tile_conf.get('overlay')
            if overlay_conf is None:
                return ''
            else:
                return overlay_conf.get('template', '')

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
