import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from auto_stretch import apply_stretch

#Change file path as needed
file_path = r"C:\Users\louis\Desktop\20250625\sorted\object\BD+04_3508\B\20250625.0232.fits"
hdulist = fits.open(file_path)

#Access header
image_data = hdulist[0].data
header_info = hdulist[0].header
stretched_data = apply_stretch(image_data) #create a stretched copy to display
min_data = np.min(image_data)
max_data = np.max(image_data)
mean_data = np.mean(image_data)
std_data = np.std(image_data)

#Find object name
if 'OBJECT' in header_info:
    object_name = header_info['OBJECT']
    print(f"Object Name: {object_name}")
else:
     print("The 'OBJECT' keyword was not found in the header.")

#Print basic stats
print("Min:", min_data)
print("Max:", max_data)
print("Mean:", mean_data)
print("Stdev:", std_data)

# Close the FITS file
hdulist.close()

# Create plot
plt.imshow(stretched_data, cmap='gray', origin='lower')
plt.colorbar()
plt.title(object_name)
plt.xlabel("X-axis (pixels)")
plt.ylabel("Y-axis (pixels)")
plt.show()


