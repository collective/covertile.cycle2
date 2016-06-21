# -*- coding: utf-8 -*-
from collective.cover.interfaces import ITileEditForm
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.cover.tiles.list import IListTile
from collective.cover.tiles.list import ListTile
from collective.cover.widgets.textlinessortable import TextLinesSortableFieldWidget
from covertile.cycle2 import _
from plone import api
from plone.autoform import directives as form
from plone.namedfile.field import NamedBlobImage
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


# Types of Pager style used in Carousel Tiles
PAGER_STYLES = SimpleVocabulary([
    SimpleTerm(value='dots', title=_(u'Dots')),
    SimpleTerm(value='numbers', title=_(u'Numbers')),
    SimpleTerm(value='thumbnails_square', title=_(u'Square Thumbnails'))
])

PAGER_TEMPLATES = {
    'dots': '<span>&bull;</span>',
    'numbers': '<strong><a href=#> {{slideNum}} </a></strong>',
    'thumbnails_square': '<a href="#"><img src="{{thumbnail}}" width=49 height=49></a>'
}

DEFAULT_PAGER_STYLE = 'dots'
DEFAULT_OVERLAY_TEMPLATE = (u'<div id="c2-overlay-title">{{title}}</div>'
                            u'<div id="c2-overlay-desc">{{desc}}</div>')


class ICarouselTile(IListTile):

    """A carousel based on the Cycle2 slideshow plugin for jQuery."""

    uuids = schema.Dict(
        title=_(u'Elements'),
        key_type=schema.TextLine(),
        value_type=schema.Dict(
            key_type=schema.TextLine(),
            value_type=schema.TextLine(),
        ),
        required=False,
    )
    form.omitted('uuids')
    form.no_omit(ITileEditForm, 'uuids')
    form.widget(uuids=TextLinesSortableFieldWidget)

    # Copied from From IListTile

    image = NamedBlobImage(
        title=_(u'Image'),
        required=False,
    )
    form.omitted('image')
    form.no_omit(IDefaultConfigureForm, 'image')

    tile_title = schema.TextLine(
        title=_(u'Tile Title'),
        required=False,
    )
    form.omitted('tile_title')
    form.no_omit(ITileEditForm, 'tile_title')

    more_link = schema.TextLine(
        title=_('Show more... link'),
        required=False,
    )
    form.omitted('more_link')
    form.no_omit(ITileEditForm, 'more_link')
    form.widget(more_link='collective.cover.tiles.edit_widgets.more_link.MoreLinkFieldWidget')

    more_link_text = schema.TextLine(
        title=_('Show more... link text'),
        required=False,
    )
    form.omitted('more_link_text')
    form.no_omit(ITileEditForm, 'more_link_text')

    form.omitted('autoplay')
    form.no_omit(ITileEditForm, 'autoplay')
    autoplay = schema.Bool(
        title=_(u'Auto play'),
        required=False,
        default=True,
    )

    # Fields specific to Carousel tiles

    pager = schema.Choice(
        title=_(u'Pager'),
        vocabulary=PAGER_STYLES,
        required=True,
        default=DEFAULT_PAGER_STYLE,
    )
    form.omitted('pager')
    form.no_omit(IDefaultConfigureForm, 'pager')
    form.widget(pager='covertile.cycle2.tiles.configuration_widgets.pagerstylewidget.PagerStyleFieldWidget')

    overlay = schema.SourceText(
        title=_(u'Overlay Template'),
        description=_(u'A Mustache-style template string, in which you can use {{title}}, {{desc}} or {{date}}'),
        required=False,
        default=DEFAULT_OVERLAY_TEMPLATE,
    )
    form.omitted('overlay')
    form.no_omit(IDefaultConfigureForm, 'overlay')
    form.widget(overlay='covertile.cycle2.tiles.configuration_widgets.overlaytextarea.OverlayTextAreaFieldWidget')


@implementer(ICarouselTile)
class CarouselTile(ListTile):

    """A carousel based on the Cycle2 slideshow plugin for jQuery."""

    index = ViewPageTemplateFile('templates/carousel.pt')
    is_configurable = True
    is_editable = True
    short_name = _(u'msg_short_name_carousel', default=u'C2 Carousel')
    limit = 100      # Increase hard-coded limit in ListTile

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
        if not self._field_is_visible('pager'):
            return ''
        else:
            tile_conf = self.get_tile_configuration()
            pager_conf = tile_conf.get('pager', None)
            pager_style = pager_conf.get('style', None)
            # stored value could be none - default should be 'dots'
            if not pager_style:
                return DEFAULT_PAGER_STYLE
            else:
                return pager_style[0]

    def pagerthumbnail(self, item):
        """Return the thumbnail of an image if the pager style is Thumbnail
        based (contains {{thumbnail}}) and the pager is visible.

        :param item: [required]
        :type item: content object
        """
        if '{{thumbnail}}' not in self.pagertemplate():
            return None  # skip expensive image processing

        if not self._field_is_visible('pager'):
            return None

        scales = item.restrictedTraverse('@@images')
        return scales.scale('image', width=49, height=49, direction='down')

    def pagertemplate(self):
        if self._field_is_visible('pager'):
            return PAGER_TEMPLATES.get(self.pagerclass(), '')
        else:
            return ''

    def overlaytemplate(self):
        if not self._field_is_visible('overlay'):
            return ''
        else:
            tile_conf = self.get_tile_configuration()
            overlay_conf = tile_conf.get('overlay', None)
            template = overlay_conf.get('template', None)
            # stored value could be none - default should be '...{{title}}...'
            if template is None:
                return DEFAULT_OVERLAY_TEMPLATE
            else:
                return template

    def get_title(self, item):
        """Get the title of the item, or the custom title if set.

        :param item: [required] The item for which we want the title
        :type item: Content object
        :returns: the item title
        :rtype: unicode
        """
        # First we get the title for the item itself
        title = item.Title()
        uuid = self.get_uuid(item)
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
        uuid = self.get_uuid(item)
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
        uuid = self.get_uuid(item)
        data_mgr = ITileDataManager(self)
        data = data_mgr.get()
        uuids = data['uuids']
        if uuid in uuids:
            if uuids[uuid].get('custom_url', u''):
                # If we had a custom url set, then get that
                url = uuids[uuid].get('custom_url')
        return url
