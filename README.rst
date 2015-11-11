****************
covertile.cycle2
****************

.. contents::

Life, the Universe, and Everything
----------------------------------

A carousel tile for `collective.cover`_ based on the `Cycle2`_ slideshow plugin for jQuery.

.. _`Cycle2`: http://jquery.malsup.com/cycle2/
.. _`collective.cover`: https://pypi.python.org/pypi/collective.cover

Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/covertile.cycle2.png?branch=master
    :alt: Travis CI badge
    :target: http://travis-ci.org/collective/covertile.cycle2

.. image:: https://coveralls.io/repos/collective/covertile.cycle2/badge.png
    :alt: Coveralls badge
    :target: https://coveralls.io/r/collective/covertile.cycle2?branch=master

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/covertile.cycle2/issues

Don't Panic
-----------

The Carousel looks something like the below out the box (shown mid transition).

.. figure:: https://raw.github.com/collective/covertile.cycle2/master/fading-transition.png
    :align: center
    :height: 428px
    :width: 1138px

There are options for choosing different pagers and customizing the overlay,
but for *full* control of all the options provided by Cycle2 you will need to
override the template (easily achievable using technology such as collective.jbot)
and make CSS tweaks.


Installation
^^^^^^^^^^^^

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add ``covertile.cycle2`` to the list of eggs to install::

    [buildout]
    ...
    eggs =
        covertile.cycle2

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to `covertile.cycle2` and click the 'Activate' button.


Uninstallation
^^^^^^^^^^^^^^

This package provides an uninstall Generic Setup profile, however, it will not
deregister the Cycle2 javascripts from the JS registry dependencies as they
could be used by other addons. Feel free to manually uninstall these if you
are sure that you no longer use them.


Use
^^^

You should read the below in conjunction with the `collective.cover documentation`_.

.. _`collective.cover documentation`: https://github.com/collective/collective.cover/blob/master/docs/end-user.rst


Cycle2 Carousel tile
++++++++++++++++++++

A Cycle2 Carousel tile shows a slideshow made with a list of individual items; every
item will show an image, title and description, and will also have a link pointing
back to the original object.  The title, description and link url of individual items
can be changed by configuring the tile in the Compose view; you can also remove or
reorder them.

.. figure:: https://raw.github.com/collective/covertile.cycle2/master/edit-covertile-cycle2.png
    :align: center
    :height: 719px
    :width: 1037px

You can drop any object containing an image into a Carousel tile (though note that
objects without an image will be discarded without any warning).
Cycle2 Carousel tiles are 100% responsive, and support native-like swipe movements.
You can also specify if the carousel will start playing the slideshow
automatically or not. The tile can accept a maximum of 100 slides.

Configuration of the tile allows defining the tile's CSS class, the maximum image size,
the Overlay template and the Pager Style. The Overlay template is a mustache style HTML template
which can show the title, description or date for each tile, with {{title}}, {{desc}} or {{date}} respectively.
The Overlay is the only place the Title & Description of the tiles are shown.

.. figure:: https://raw.github.com/collective/covertile.cycle2/master/configure-covertile-cycle2.png
    :align: center
    :height: 420px
    :width: 565px
