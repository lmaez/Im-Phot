from astropy.io import fits
import numpy as np
from astropy.nddata import CCDData
import astropy.units as u
import matplotlib.pyplot as plt
from auto_stretch import apply_stretch

def calc_percent_diff(arr1, arr2):
    if arr1.shape != arr2.shape:
        raise ValueError("Arrays must have the same shape for element-wise percentage difference.")

    absolute_difference = np.abs(arr1 - arr2)
    average_of_elements = (arr1 + arr2) / 2
    # Handle division by zero: where average_of_elements is zero, set result to NaN
    # Otherwise, calculate the percentage difference
    percent_diff = np.where(average_of_elements == 0, np.nan, (absolute_difference / average_of_elements) * 100)   
    return percent_diff

#Set file path
file_path = r"C:\Users\louis\Desktop\20250626\sorted\object\AP_Lib\B\20250626.0195.fits"
file_path2 = r"C:\Users\louis\Desktop\20250626\sorted\object\AP_Lib\B\20250626.0196.fits"

#Access header and data
hdulist = fits.open(file_path)
image_data = hdulist[0].data
header_info = hdulist[0].header
stretched_data = apply_stretch(image_data) #create a stretched copy to display
min_data = np.min(image_data)
max_data = np.max(image_data)
mean_data = np.mean(image_data)
std_data = np.std(image_data)

hdulist2 = fits.open(file_path2)
image_data2 = hdulist2[0].data
header_info2 = hdulist2[0].header
stretched_data2 = apply_stretch(image_data2) #create a stretched copy to display
min_data2 = np.min(image_data2)
max_data2 = np.max(image_data2)
mean_data2 = np.mean(image_data2)
std_data2 = np.std(image_data2)

#Find object name
if 'OBJECT' in header_info:
    object_name = header_info['OBJECT']
    object_name2 = header_info2['OBJECT']
    print(f"----------------------")
    print(f"Object 1 Name: {object_name}")  #print basic stats
    print("Min:", min_data)
    print("Max:", max_data)
    print("Mean:", mean_data)
    print("Stdev:", std_data)
    print(f"----------------------")
    print(f"Object 2 Name: {object_name2}") #Print stats for object 2
    print("Min:", min_data2)
    print("Max:", max_data2)
    print("Mean:", mean_data2)
    print("Stdev:", std_data2)
    print(f"----------------------")
    
else:
     print("The 'OBJECT' keyword was not found in the header.")

#Print ADU count matrix
try:            
    ccd = CCDData.read(file_path, unit = 'adu')
    ccd2 = CCDData.read(file_path2, unit = 'adu')
    adu_values = ccd.data
    adu_values2 = ccd2.data
    print(f"Unit: {ccd.unit}")
    print(f"----------------------")
    print(f"Image 1:")
    print (adu_values)
    print(f"----------------------")
    print(f"Image 2:")
    print(adu_values2)
    print(f"----------------------")

    diff_image = image_data - image_data2
    # Create a new FITS HDU list
    new_hdul = fits.HDUList([fits.PrimaryHDU(diff_image)])
    # Save the new FITS file
    new_hdul.writeto('difference_image.fits', overwrite=True)
    diff_stretched = apply_stretch(diff_image)

    difference = adu_values - adu_values2
    max_diff = difference.max()
    min_diff = difference.min()
    mean_diff = difference.mean()
    std_diff = difference.std()
    percent_difference = calc_percent_diff(adu_values, adu_values2)
    avg_percent_diff = np.sum(percent_difference)/len(percent_difference)
    
    print("Difference:")
    print(difference)
    print("Min:", min_diff)
    print("Max:", max_diff)
    print("Mean:", mean_diff)
    print("Stdev:", std_diff)
    print("Percent Difference:", avg_percent_diff)
    print(f"----------------------")

except FileNotFoundError:
    print(f"Error: The file '{image_path}' was not found.")
except Exception as e:
    print(f"An error occurred while reading the image: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'hdu_list' in locals() and hdu_list:
        hdu_list.close()




# Create plot
plt.imshow(diff_stretched, cmap='gray', origin='lower')
plt.colorbar()
plt.title("Subtracted Image")
plt.xlabel("X-axis (pixels)")
plt.ylabel("Y-axis (pixels)")
plt.show()
