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


@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def OverlayTextAreaFieldWidget(field, request):
    """IFieldWidget factory for OverlayTextWidget."""
    return FieldWidget(field, OverlayTextAreaWidget(request))
