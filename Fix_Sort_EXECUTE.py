# updated folder paths to avoid extra folders in folders!
import os
from astropy.io import fits
import shutil
from astropy.time import Time
import numpy as np

input_folder = "TEST"
output_folder = "TEST"
latitude = 35.09675
longitude = -111.5355
altitude = 2206

def sortType(input_folder):
    
    append = "sorted"
    os.makedirs(os.path.join(input_folder, append), exist_ok=True)
    output_folder = os.path.join(input_folder, append)

    # subdirectories
    for subdir in ['bias', 'flat', 'object', 'unknown']:
        os.makedirs(os.path.join(output_folder, subdir), exist_ok=True)

    # Loop through fits
    for fname in os.listdir(input_folder):
        if not fname.lower().endswith('.fits'):
            continue

        fpath = os.path.join(input_folder, fname)

        try:
            hdr = fits.getheader(fpath)

            #extract image type from FITS header
            img_type = hdr.get('IMAGETYP', '').strip().lower()

            #Categorize based on IMAGETYP
            if 'bias' in img_type:
                category = 'bias'
            elif 'flat' in img_type or 'skyflat' in img_type:
                category = 'flat'
            elif 'object' in img_type or 'light' in img_type:
                category = 'object'
            elif 'dark' in img_type or 'skydark' in img_type:
                category = 'unknown'
            else:
                # backup guess 
                object_name = hdr.get('OBJECT', '').strip().lower()
                if 'flat' in object_name:
                    category = 'flat'
                elif 'bias' in object_name:
                    category = 'bias'
                elif 'dark' in object_name:
                    category = 'unknown'
                elif object_name:
                    category = 'object'
                else:
                    category = 'unknown'

            # Copy to subfolder
            out_path = os.path.join(output_folder, category, fname)
            shutil.copyfile(fpath, out_path)
            print(f"✅ Sorted {fname} → {category}")

        except Exception as e:
            print(f"❌ Error reading {fname}: {e}")

def sortTrimFix(output_folder):

    # get trimsec value
    def parse_section(section_str):
        section_str = section_str.strip().strip('[]')
        x_range, y_range = section_str.split(',')
        x1, x2 = [int(val) - 1 for val in x_range.split(':')]
        y1, y2 = [int(val) - 1 for val in y_range.split(':')]
        return slice(y1, y2 + 1), slice(x1, x2 + 1)

    # ✅ this is now correctly outside the parse_section function
    for subdir, _, files in os.walk(output_folder):
        for fname in files:
            if not fname.lower().endswith('.fits'):
                continue

            path = os.path.join(subdir, fname)
            try:
                with fits.open(path, mode='update') as hdul:
                    hdr = hdul[0].header
                    data = hdul[0].data.astype(float)

                    # Trim
                    trimsec = hdr.get('TRIMSEC') or hdr.get('TRIM01')
                    biassec = hdr.get('BIASSEC') or hdr.get('BIAS01')
                    if trimsec:
                        y_slice, x_slice = parse_section(trimsec)
                        data = data[y_slice, x_slice]
                    if biassec:
                        yb_slice, xb_slice = parse_section(biassec)
                        overscan = data[yb_slice, xb_slice]
                        if overscan.size > 0:
                            data -= np.median(overscan)

                    hdul[0].data = data

                    # JD
                    date_obs = hdr.get('DATE-OBS')
                    time_obs = hdr.get('UTSTART') or hdr.get('TIME-OBS')
                    if date_obs and time_obs:
                        t = Time(f"{date_obs}T{time_obs}", format='isot', scale='utc')
                        hdr['JD'] = (t.jd, 'Julian Date')

                    if 'OBJCTRA' not in hdr and 'RA' in hdr:
                        hdr['OBJCTRA'] = (hdr['RA'], 'Copied from RA')
                    if 'OBJCTDEC' not in hdr and 'DEC' in hdr:
                        hdr['OBJCTDEC'] = (hdr['DEC'], 'Copied from DEC')

                    hdr['SITELAT'] = (latitude, 'Observatory latitude')
                    hdr['SITELONG'] = (longitude, 'Observatory longitude')
                    hdr['SITEALT'] = (altitude, 'Observatory altitude in meters')

                    hdul.flush()
                print(f"✅ Processed: {fname}")
            except Exception as e:
                print(f"❌ Failed {fname}: {e}")

    # sort by target name (only for object frames)
    print("Sorting by target name (only for object frames)...")
    for root, dirs, files in os.walk(output_folder):
        if 'object' not in root.lower():
            continue
        for fname in files:
            if not fname.endswith('.fits'):
                continue
            fpath = os.path.join(root, fname)
            try:
                hdr = fits.getheader(fpath)
                target = hdr.get('OBJECT', 'UNKNOWN').replace(' ', '_')
                dest_dir = os.path.join(root, target)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(fpath, os.path.join(dest_dir, fname))
            except Exception as e:
                print(f"Could not sort {fname} by OBJECT: {e}")

    # sort by filter (for flats and objects only)
    print("Sorting by filter (flats and objects)...")
    for root, dirs, files in os.walk(output_folder):
        if not any(ftype in root.lower() for ftype in ['flat', 'object']):
            continue  # skip bias and unknown folders
        for fname in files:
            if not fname.endswith('.fits'):
                continue
            fpath = os.path.join(root, fname)
            try:
                hdr = fits.getheader(fpath)
                filt = hdr.get('FILTNAME', 'UNKNOWN').strip().replace(' ', '_')
                dest_dir = os.path.join(root, filt)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.move(fpath, os.path.join(dest_dir, fname))
            except Exception as e:
                print(f"⚠️ Could not sort {fname} by FILTNAME: {e}")

    print("\n✅ Done! FITS files trimmed, headers updated, and sorted by target and filter.")


