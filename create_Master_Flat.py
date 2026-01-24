# Louis Maez
# Lowell Observatory
# Created: 09/11/2025
# Version: 01/24/2026
# Subtracts and Trims overscan from Flat Frames
# Removes bias and creates master_flat frame

from astropy.nddata import CCDData
from pathlib import Path
from astropy.io import fits
from astropy.stats import mad_std
from auto_stretch import apply_stretch
from astropy.visualization import hist
import numpy as np
import matplotlib.pyplot as plt
import ccdproc
import warnings
from astropy.wcs import FITSFixedWarning
import os

# Define the inverse median of value a, for Flat scaling
def inv_median(a):
    return 1 / np.median(a)

# Create image file collection leading to RAW data
image_direct = Path(r"C:\Users\louis\Desktop\20250626")
files = ccdproc.ImageFileCollection(image_direct)

# Create subfolder for reduced images
Path(image_direct, 'reduced').mkdir(exist_ok = True)
calibrated_path = Path(image_direct, 'reduced')
calibrated_data = ccdproc.ImageFileCollection(calibrated_path)

#Find master bias frame
master_bias = list(calibrated_data.ccds(combined = True, imagetyp = 'bias'))[0]

#Subtract and trim overscan, subtract master bias for all FLAT frames 
for ccd, file_name in files.ccds(imagetyp = 'FLAT',
                                 ccd_kwargs = {'unit':'adu'},
                                 return_fname = True
                                 ):
    ccd = ccdproc.subtract_overscan(ccd,
                                    overscan = ccd[:1370, 1387:1432],
                                    median = True)
    ccd = ccdproc.trim_image(ccd[:1370,17:1382])
    ccd = ccdproc.subtract_bias(ccd, master_bias)
    ccd.write(calibrated_path / ('flat_' + file_name), overwrite = True)
    warnings.simplefilter('ignore', category = FITSFixedWarning)    #Ignore those pesky datFix warnings
    print(f"Bias and Overscan Subtracted, Image Trimmed:", {file_name})

# Create Master Flats for each filter
flat_filters = set(h['filtname'] for h in files.headers(imagetyp = 'skyflat'))

#Create a master flat for each filter and save it
for filt in flat_filters:
    warnings.simplefilter('ignore', category = FITSFixedWarning)
    to_combine = files.files_filtered(imagetyp = 'skyflat',
                                      filtname = filt,
                                      include_path = True)
    
    combined_flat = ccdproc.combine(to_combine,
                                    method = 'average',
                                    scale = inv_median,
                                    sigma_clip = True,
                                    sigma_clip_low_thresh = 3,
                                    sigma_clip_high_thresh = 3,
                                    sigma_clip_func = np.ma.median,
                                    sigma_clip_dec_func = mad_std,
                                    mem_limit = 350e6)
    combined_flat = ccdproc.trim_image(combined_flat[:1370,17:1382])
    combined_flat.meta['combined'] = True
    new_file_name = '{}_master_flat.fits'.format(filt.replace("''", "p"))
    combined_flat.write(calibrated_path / new_file_name, overwrite = True)

print(f"Master Flats Saved")

hdulist = fits.open(calibrated_path / 'v_master_flat.fits')
image_data = apply_stretch(hdulist[0].data)
hdulist.close()
plt.imshow(image_data, cmap='gray', origin='lower')
plt.colorbar()
plt.title("Master Flat")
plt.xlabel("X-axis (pixels)")
plt.ylabel("Y-axis (pixels)")
plt.show()
    
                            
