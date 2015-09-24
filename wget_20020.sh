#!/bin/sh
## NOTE: The 'wget' executable must be in your path
## for this script to function without edits.

WGET='wget --no-cookies --header=Cookie:KOA80=anon|anon|TMP_pVqAHR_18942'
$WGET "http://koa.ipac.caltech.edu/cgi-bin/KOADownload/nph-KOADownload?ref=\ISIS_WORKDIR\/TMP_pVqAHR_18942/KOA/NIRC2_sci_20020_1.tar" -O NIRC2_sci_20020_1.tar
