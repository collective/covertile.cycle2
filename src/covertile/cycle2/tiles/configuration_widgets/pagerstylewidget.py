# -*- coding: utf-8 -*-

import zope.interface
import zope.schema
from z3c.form.widget import FieldWidget
from z3c.form.browser.select import SelectWidget
from z3c.form import interfaces
from z3c.form.browser import widget


class IPagerStyleWidget(interfaces.ISelectWidget):
    """TextArea widget for Cycle2 Overlay field."""


@zope.interface.implementer_only(IPagerStyleWidget)
class PagerStyleWidget(SelectWidget):
    """Select widget implementation."""

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(SelectWidget, self).update()
        widget.addFieldClass(self)
        confvalue = self.context.get('pager_style').get('style')
        if confvalue is not None:
            self.value = self.context.get('pager_style').get('style')


@zope.component.adapter(zope.schema.interfaces.IChoice,
                        zope.interface.Interface,
                        interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def PagerStyleFieldWidget(field, source, request=None):
    """IFieldWidget factory for SelectWidget."""
    # BBB: emulate our pre-2.0 signature (field, request)
    if request is None:
        real_request = source
    else:
        real_request = request
    return FieldWidget(field, PagerStyleWidget(real_request))
