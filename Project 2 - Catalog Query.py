import numpy as np
from astropy.io import fits
from astropy.wcs import WCS 
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import visualization
import astropy.constants as const
from astropy.table import Table, QTable
from astropy.time import Time, TimeDelta
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, FK5, Galactic
from astropy.visualization import quantity_support, time_support
import matplotlib.pyplot as plt
import numpy as np
from astroquery.mast import Observations, Catalogs
from pprint import pprint
from astropy.table import Table
import pandas as pd
from astroquery.simbad import Simbad
from astroquery.vizier import Vizier
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

vizier = Vizier(row_limit = -1)

# Identify Literature Paper with Photo-Z data in Hubble UDF
catalog_list = vizier.find_catalogs('The MUSE Hubble Ultra Deep Field surveys: Data release II')
for k, v in catalog_list.items(): 
    print(k, ':', v.description)

#pprint(catalog_list)
spec_catalog_key = 'J/A+A/608/A2'
phot_catalog_key = 'J/AJ/150/31'

spec_cat = vizier.get_catalogs(spec_catalog_key)
phot_cat = vizier.get_catalogs(phot_catalog_key)


pprint(phot_cat)
spec_cat_table = spec_cat[0] #Get the combined table (not mosaic or udf10)

#print(len(spec_cat_table))
#pprint(spec_cat_table)

# Iterate directly over the list of photometric catalog tables to identify which to save
for tbl in phot_cat:
    pprint(tbl[0])
    print(tbl[0].columns)

phot_cat_table = phot_cat[0] #Store the table with only the necessary columns. 

#Save the Tables
#First clear UNC ahh Metadata
phot_cat_table.meta.clear()
spec_cat_table.meta.clear()

phot_cat_table.write('Photoz_catalog.fits', overwrite = True)
spec_cat_table.write('Spec_catalog.fits', overwrite = True)