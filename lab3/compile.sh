#!/bin/bash

xsltproc --xinclude --stringparam profile.role html /usr/share/xml/docbook/xsl-stylesheets-1.79.2/xhtml/profile-docbook.xsl user.xml > user.html
xsltproc --xinclude --stringparam profile.role html /usr/share/xml/docbook/xsl-stylesheets-1.79.2/xhtml/profile-docbook.xsl develop.xml > develop.html

xsltproc --xinclude --stringparam profile.role fo --stringparam ulink.footnotes 0 --stringparam body.font.family 'DejaVu Serif' --stringparam title.font.family 'DejaVu Sans' --stringparam sans.font.family 'DejaVu Sans' --stringparam monospace.font.family 'DejaVu Sans Mono' /usr/share/xml/docbook/xsl-stylesheets-1.79.2/fo/profile-docbook.xsl user.xml > user.fo
xsltproc --xinclude --stringparam profile.role fo --stringparam ulink.footnotes 0 --stringparam body.font.family 'DejaVu Serif' --stringparam title.font.family 'DejaVu Sans' --stringparam sans.font.family 'DejaVu Sans' --stringparam monospace.font.family 'DejaVu Sans Mono' /usr/share/xml/docbook/xsl-stylesheets-1.79.2/fo/profile-docbook.xsl develop.xml > develop.fo

dblatex -b xetex user.xml
dblatex -b xetex develop.xml

fop -c fop.xconf user.fo user_fo.pdf
fop -c fop.xconf develop.fo develop_fo.pdf
