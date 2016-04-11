# -*- coding: utf-8 -*-

from z3c.form import interfaces
from z3c.form.browser.select import SelectWidget
from z3c.form.widget import FieldWidget

import zope.component
import zope.interface
import zope.schema.interfaces


class IPagerStyleWidget(interfaces.ISelectWidget):
    """TextArea widget for Cycle2 Overlay field."""


@zope.interface.implementer_only(IPagerStyleWidget)
class PagerStyleWidget(SelectWidget):
    """Select widget implementation."""

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(SelectWidget, self).update()
        confvalue = self.context.get('pager', {}).get('style')
        if confvalue is not None:
            self.value = self.context.get('pager').get('style')


@zope.component.adapter(zope.schema.interfaces.IChoice, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def PagerStyleFieldWidget(field, request):
    """IFieldWidget factory for SelectWidget."""
    return FieldWidget(field, PagerStyleWidget(request))
