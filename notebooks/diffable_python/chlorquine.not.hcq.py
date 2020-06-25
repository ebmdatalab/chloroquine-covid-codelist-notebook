# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# This notebook contains dm+d codes medications chloroquine phosphate or chloroquine sulfate. Prescribing of these products in general practice is minimal and you can see current prescribing patterns on OpenPrescribing
# - [Chloroquine phosphate](https://openprescribing.net/chemical/0504010F0/)
# - [Chloroquine with proguanil](https://openprescribing.net/chemical/0504010Z0/)
# - [Chloroquine sulphate](https://openprescribing.net/chemical/0504010G0/)

from ebmdatalab import bq
import pandas as pd
import os

# +
sql = '''WITH bnf_codes AS (
  SELECT bnf_code FROM hscic.presentation WHERE 
    bnf_code LIKE '0504010F0%' OR ## chloroquine phosphate - BNF sect antiprotozoal drugs
    bnf_code LIKE '0504010Z0%'  OR ## chloroquine phosphate with proguanil - BNF sect antiprotozoal drugs
    bnf_code LIKE '0504010G0%' ## chloroquine sulfate - BNF sect antiprotozoal drugs 
  )

SELECT "vmp" AS type, id, bnf_code, nm
FROM dmd.vmp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

UNION ALL

SELECT "amp" AS type, id, bnf_code, descr
FROM dmd.amp
WHERE bnf_code IN (SELECT * FROM bnf_codes)

ORDER BY type, bnf_code, id'''

chloroquine_codelist = bq.cached_read(sql, csv_path=os.path.join('..','data','chloroquine_codelist.csv'))
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
chloroquine_codelist
