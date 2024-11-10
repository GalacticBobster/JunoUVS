from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

def plot_photons_by_wavelength(file_path, wavelength_min, wavelength_max):
    """
    Plot photons within a specific wavelength range on a polar plot with latitude and longitude.
    
    Parameters:
    - file_path: str, path to the FITS file
    - wavelength_min: float, minimum wavelength in nm
    - wavelength_max: float, maximum wavelength in nm
    """
    # Open the FITS file and load data
    with fits.open(file_path) as hdulist:
        # Assuming the photon data is in the "Calibrated Photon List" HDU (HDU 2)
        photon_data = hdulist[2].data
        
        # Extract wavelength, latitude, and longitude columns
        wavelengths = photon_data['WAVELENGTH']  # in nanometers (nm)
        latitudes = photon_data['JUPITER_LAT_400km']  # assuming degrees
        longitudes = photon_data['JUPITER_LON_400km']  # assuming degrees
        
        # Filter photons within the desired wavelength range
        mask = (wavelengths >= wavelength_min) & (wavelengths <= wavelength_max)
        filtered_latitudes = latitudes[mask]
        filtered_longitudes = longitudes[mask]
        
        # Convert to radians for polar plot
        theta = np.radians(filtered_longitudes)  # angle in radians
        r = 90 - filtered_latitudes  # distance from the center (latitude)

        # Create the polar plot
        #fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        plt.figure(figsize=(10, 6))
        #sc = ax.scatter(theta, r, c=wavelengths[mask], cmap='viridis', s=1, alpha=0.6)
        sc = plt.scatter(filtered_longitudes, filtered_latitudes, c=wavelengths[mask], 
                         cmap='viridis', s=1, alpha=0.6)
        # Add colorbar for wavelength
        cbar = plt.colorbar(sc, orientation='vertical')
        cbar.set_label('Wavelength (nm)')
        
        # Label and display the plot
        plt.title(f'Photons at {wavelength_min}-{wavelength_max} nm Wavelength')
        plt.xlabel('Longitude (degrees)')
        plt.ylabel('Latitude (degrees)')
        plt.xlim(0, 360)
        plt.ylim(-90, 90)
        
        #ax.set_title(f'Photons at {wavelength_min}-{wavelength_max} nm Wavelength')
        #ax.set_theta_zero_location('N')
        #ax.set_theta_direction(-1)  # Longitude increases counterclockwise
        #ax.set_rlim(0, 180)  # Jupiter's latitude range: 90°N to 90°S

        plt.show()

# Usage example
file_path = 'UVS_S01_738602023_2023149_P51SY3_V01.FIT'  # Replace with your file path
plot_photons_by_wavelength(file_path, wavelength_min=120, wavelength_max=160)

