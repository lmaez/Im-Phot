# Louis Maez
# Lowell Observatory
# Created: 09/20/2025
# Version: 01/24/226
#
# Need to install CCDProc, Astropy, numpy, matplotlib, auto-stretch
#
# As the final step in reductions, this script takes the
# previously made master flat and master bias frames and
# removes them from the science frames. It also subtracts
# the overscan region from each science frame. 

from pathlib import Path
from astropy import units
from astropy.io import fits
from auto_stretch import apply_stretch
from astropy.nddata import CCDData
from astropy.visualization import hist
import matplotlib.pyplot as plt
import numpy as np
import ccdproc

#Define path to RAW data
image_direct = Path(r"C:\Users\louis\Desktop\20250626")
files = ccdproc.ImageFileCollection(image_direct)

#Define path to reduced data
Path(image_direct, 'reduced').mkdir(exist_ok = True)
calibrated_path = Path(image_direct, 'reduced')
calibrated_data = ccdproc.ImageFileCollection(calibrated_path)

#Create a dictionary of master flats for each filter
master_flats = {ccd.header['filtname']:
                ccd for ccd in calibrated_data.ccds(imagetyp = 'skyflat',
                                                    combined = True)}
#Find master bias frame
master_bias = list(calibrated_data.ccds(combined = True, imagetyp = 'bias'))[0]

print(f"Master Flat Dictionary Created.")

science_imagetyp = 'object'
flat_imagetyp = 'skyflat'
bias_imagetyp = 'bias'

for light, file_name in files.ccds(imagetyp = science_imagetyp,
                                          return_fname = True,
                                          ccd_kwargs = dict(unit = 'adu')):

    #Look at science filter and match it with a master flat
    science_filter = light.header['filtname']
    if science_filter in master_flats:
        master_flat = master_flats[science_filter]

        #Subtract and trim overscan region
        reduced = ccdproc.subtract_overscan(light,
                                            overscan = light[:1370, 1387:1432],
                                            median = True)
        reduced = ccdproc.trim_image(reduced[:1370,17:1382])
        
        # Subtract bias
        reduced = ccdproc.subtract_bias(reduced, master_bias)

        #Calibrate with master flat frame
        reduced = ccdproc.flat_correct(reduced, master_flat)

        
        #Save reduced science image
        reduced.write(calibrated_path / file_name, overwrite = True)
        

        print(f"Reduced", {file_name},"with master flat for filter", {science_filter})
    else:
        print(f"Warning: No master flat found for filter", {science_filter},"in the file", {file_name})

ExampleDir = Path(r"C:\Users\louis\Desktop\20250626\reduced\20250626.0122.fits")
hdulist = fits.open(ExampleDir)
image_data = apply_stretch(hdulist[0].data)
hdulist.close()
plt.imshow(image_data, cmap='gray', origin='lower')
plt.colorbar()
plt.title("Example Image: 20250626.0122")
plt.xlabel("X-axis (pixels)")
plt.ylabel("Y-axis (pixels)")
plt.show()                    
