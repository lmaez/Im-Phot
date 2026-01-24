# Louis Maez
# Lowell Observatory
# Created: 09/11/2025
# Version: 01/24/2026
#
# Subtracts and Trims overscan from Bias Images.
# Creates a master_bias frame

from astropy.nddata import CCDData
from pathlib import Path
from astropy.stats import mad_std
from astropy.io import fits
from auto_stretch import apply_stretch
import ccdproc
import numpy as np
import warnings
from astropy.wcs import FITSFixedWarning
import matplotlib.pyplot as plt

#Create image file collection leading to RAW data
# Replace path with actual image file path
image_direct = Path(r"C:\Users\louis\Desktop\20250626")
files = ccdproc.ImageFileCollection(image_direct)
files.summary['file', 'imagetyp', 'filtname', 'exptime', 'naxis1', 'naxis2']

#Create a path for only darks, if there are darks. (make into if statement)
#darks_only = ccdproc.ImageFileCollection(image_direct / 'darks')
#darks_only.summary['file','OBJECT','EXPTIME']

files.summary['file', 'imagetyp', 'biassec', 'trimsec'][0]

#Create path for reduced data
Path(image_direct, 'reduced').mkdir(exist_ok=True)
calibrated_path = Path(image_direct, 'reduced')
calibrated_data = ccdproc.ImageFileCollection(calibrated_path)

#Subtract and Trim overscan for all BIAS frames
for ccd, file_name in files.ccds(imagetyp = 'BIAS',
                                 ccd_kwargs = {'unit':'adu'},
                                 return_fname = True
                                 ):
    ccd = ccdproc.subtract_overscan(ccd,
                                    overscan = ccd[:1370, 1387:1432],
                                    median = True)
    ccd = ccdproc.trim_image(ccd[:1370,17:1382])
    ccd.write(calibrated_path / ('bias_' + file_name), overwrite = True)
    warnings.simplefilter('ignore', category = FITSFixedWarning) #Ignore warnings
    print(f"Subtracted and Trimmed", {file_name})

#calibrated_path = ccdproc.ImageFileCollection(image_direct / calibrated_data)
calibrated_biases =  calibrated_data.files_filtered(imagetyp = 'bias',
                                                    include_path = True)
#calibrated_biases = calibrated_path.ccds(imagetyp = 'bias')

combined_bias = ccdproc.combine(
    calibrated_biases,
    method='average',
    sigma_clip = True,
    sigma_clip_low_thresh = 3,
    sigma_clip_high_thresh = 3,
    sigma_clip_func=np.ma.median,
    sigma_clip_dev_func = mad_std, # `mad_std` calculates the median absolute deviation
    mem_limit = 350e6
    )

combined_bias.meta['combined'] = True

combined_bias.write(calibrated_path / 'master_bias.fits', overwrite = True)

print(f"Master Bias Saved as master_bias.fits")

hdulist = fits.open(calibrated_path / 'master_bias.fits')
image_data = apply_stretch(hdulist[0].data)
hdulist.close()
plt.imshow(image_data, cmap='gray', origin='lower')
plt.colorbar()
plt.title("Master Bias")
plt.xlabel("X-axis (pixels)")
plt.ylabel("Y-axis (pixels)")
plt.show()


