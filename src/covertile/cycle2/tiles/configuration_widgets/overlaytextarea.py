# -*- coding: utf-8 -*-

import zope.component
import zope.interface
import zope.schema.interfaces

from z3c.form import interfaces
from z3c.form.browser.textarea import TextAreaWidget
from z3c.form.browser import widget
from z3c.form.widget import FieldWidget


class IOverlayTextAreaWidget(interfaces.ITextAreaWidget):
    """TextArea widget for Cycle2 Overlay field."""


@zope.interface.implementer_only(IOverlayTextAreaWidget)
class OverlayTextAreaWidget(TextAreaWidget):
    """Textarea widget for Cycle2 Overlay field implementation."""

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(TextAreaWidget, self).update()
        widget.addFieldClass(self)
        self.value = self.context.get('overlay')

@zope.component.adapter(zope.schema.interfaces.IField,
                        zope.interface.Interface, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def OverlayTextAreaFieldWidget(field, source, request=None):
    """IFieldWidget factory for OverlayTextAreaWidget."""
    # BBB: emulate our pre-2.0 signature (field, request)
    if request is None:
        real_request = source
    else:
        real_request = request
    return FieldWidget(field, OverlayTextAreaWidget(real_request))
