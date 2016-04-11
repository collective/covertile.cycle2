# -*- coding: utf-8 -*-

from z3c.form import interfaces
from z3c.form.browser.textarea import TextAreaWidget
from z3c.form.widget import FieldWidget

import zope.component
import zope.interface
import zope.schema.interfaces


class IOverlayTextAreaWidget(interfaces.ITextAreaWidget):
    """TextArea widget for Cycle2 Overlay field."""


@zope.interface.implementer_only(IOverlayTextAreaWidget)
class OverlayTextAreaWidget(TextAreaWidget):
    """Textarea widget for Cycle2 Overlay field implementation."""

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(TextAreaWidget, self).update()
        confvalue = self.context.get('overlay', {}).get('template')
        if confvalue is not None:
            self.value = self.context.get('overlay').get('template')


@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def OverlayTextAreaFieldWidget(field, request):
    """IFieldWidget factory for OverlayTextWidget."""
    return FieldWidget(field, OverlayTextAreaWidget(request))
