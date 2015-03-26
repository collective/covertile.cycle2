****************
covertile.cycle2
****************

.. contents::

Life, the Universe, and Everything
----------------------------------

A carousel tile for collective.cover_ based on the `Cycle2`_ slideshow plugin for jQuery.

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

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation, first make sure you
have installed collective.cover_. Then:

.. _`collective.cover`: https://pypi.python.org/pypi/collective.cover#installation


1. Edit your buildout.cfg and add ``covertile.cycle2`` to the list of eggs to
   install ::

    [buildout]
    ...
    eggs =
        covertile.cycle2

After updating the configuration you need to run ''bin/buildout'', which will
take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to `covertile.cycle2` and click the 'Activate' button.

Use
^^^

You should read the below in conjunction with the collective.cover_ documentation.

.. _`collective.cover`: https://github.com/collective/collective.cover/blob/master/docs/end-user.rst


Cycle2 Carousel tile
++++++++++++++++++++

A Cycle2 Carousel tile shows a slideshow made with a list of individual items; every
item will show an image, title and description, and will also have a link pointing
back to the original object.  The title, description and link url of individual items
can be changed by configuring the tile in the Compose view; you can also remove or
reorder them.
You can drop any object containing an image into a Carousel tile (though note that
objects without an image will be discarded without any warning).
Cycle2 Carousel tiles are 100% responsive, and support native-like swipe movements.
You can also specify if the carousel will start playing the slideshow
automatically or not.

The Cycle2 Carousel tile is fully responsive, so be sure to configure it to
use the image size that fits best the maximum desired size.
