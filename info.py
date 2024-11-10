from astropy.io import fits
from pylab import *

file_path = 'UVS_S01_736023703_2023119_P50CA1_V01.FIT'

with fits.open(file_path) as hdulist:
            # Print the overall file information
            print(f"\nFITS file: {file_path}")
            print("=" * 50)
            hdulist.info()  # Summary of the file's HDU list

            # Loop through each Header/Data Unit (HDU) in the FITS file
            for i, hdu in enumerate(hdulist):
                print(f"\nHDU {i} Information:")
                print("-" * 50)
                
                # Print header details
                print("Header:")
                print(repr(hdu.header))

                if hdu.data is not None:
                    print("\nData:")
                    print(f"Data shape: {hdu.data.shape}")
                    print(f"Data type: {hdu.data.dtype}")
                else:
                    print("No data found in this HDU.")

