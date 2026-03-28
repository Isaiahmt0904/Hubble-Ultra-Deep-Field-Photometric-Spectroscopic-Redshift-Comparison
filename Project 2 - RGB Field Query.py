
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
from astroquery.mast import Observations
from pprint import pprint
from astropy.table import Table
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


# Get Center of Hubble UDF
hudf = SkyCoord("03h32m39.0s -27d47m29.0s", frame="icrs")

# use the synchronous query_region (it accepts obs_collection)
obs = Observations.query_criteria(coordinates = hudf, radius=3 * u.arcmin, obs_collection='HST', instrument_name='ACS/WFC', dataproduct_type='image', filters = ['F606W', 'F775W', 'F435W'])


# Grab Products
products = Observations.get_product_list(obs)
type(products)


#Filter only Science Images, AND those of the same obs id (for a matched mosaic)
science_images = Observations.filter_products(products, productType="SCIENCE",
    mrp_only=False,  
) 

# Filter for a 3D Image Mosaic 
psg = science_images['productSubGroupDescription']
arr = np.array(psg.filled('')).astype(str)
is_drz = np.char.find(np.char.upper(arr), 'DRZ') != -1
science_images = science_images[is_drz]


#pprint(science_images)

#Put in pandas DF to select one of the Products 
image_df = science_images.to_pandas()
image_df.sort_values('productFilename') 
image_df = image_df.groupby('parent_obsid', as_index = False).tail(1)
#pprint(image_df)

image_table = Table.from_pandas(image_df)
image_table = image_table[image_table['obs_collection'] == 'HST']
#pprint(image_table)


##########################################################################################
"""This section downloads one fits file for each filter (first entry in the table)"""
filters = ['F606W', 'F775W', 'F435W']

for filter in filters: 
    try: 
            cur_filter_table = image_table[image_table['filters'] == filter]
            object = Observations.download_products(cur_filter_table[0], extension = 'fits', download_dir = '.') 
            print(f"Successfully Downloaded data for {filter}")
    except Exception as e: 
          print(f"Failed to get data for {filter} due to {e}")

# """"""
##########################################################################################


