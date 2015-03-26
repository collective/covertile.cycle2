#!/bin/bash
# i18ndude should be available in your buildout's bin directory
I18NDUDE=../../../../../../bin/i18ndude

$I18NDUDE rebuild-pot --pot covertile.cycle2.pot --merge manual.pot --create covertile.cycle2 ../
$I18NDUDE sync --pot covertile.cycle2.pot */LC_MESSAGES/covertile.cycle2.po
