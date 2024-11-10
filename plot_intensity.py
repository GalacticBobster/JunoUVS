import numpy as np
from pylab import *
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from astropy.io import fits

def lat_lon_photon_intensity_plot(file_path, wavelength_min, wavelength_max):
    """
    Plot photon intensity on a latitude-longitude map for a specified wavelength range.
    
    Parameters:
    - file_path: str, path to the FITS file
    - wavelength_min: float, minimum wavelength in nm
    - wavelength_max: float, maximum wavelength in nm
    """
    # Open the FITS file and load data
    with fits.open(file_path) as hdulist:
        # Access the "Calibrated Photon List" HDU (HDU 2)
        photon_data = hdulist[2].data
        
        # Extract data fields
        wavelengths = photon_data['WAVELENGTH']        # Wavelength in nm
        latitudes = photon_data['JUPITER_LAT_400km']   # Latitude on Jupiter (assumed)
        longitudes = photon_data['JUPITER_LON_400km']  # Longitude on Jupiter (assumed)
        counts = photon_data['WEIGHTED_COUNT']         # Photon intensity or count
        

        emission_angles = photon_data['EMISSION_ANGLE']    # Emission angle in degrees
        nadir_angle_max=70
        lat_limit = 40
        intensity_threshold = 1e6
        mask = (
            (wavelengths >= wavelength_min) &
            (wavelengths <= wavelength_max) &
            (np.abs(latitudes) >= lat_limit) &  # High latitude for auroras
            (counts >= intensity_threshold)     # High intensity for auroras
        )
        # Filter data for the southern hemisphere, near-nadir emission angles, and specified wavelength range
        #mask = (
        #    (wavelengths >= wavelength_min) &
        #    (wavelengths <= wavelength_max) &
        #    (latitudes < 0) &
        #    (emission_angles <= nadir_angle_max)
        #)
        #filtered_latitudes = latitudes[mask]
        #filtered_longitudes = longitudes[mask]
        #filtered_counts = counts[mask]
        # Filter data based on the wavelength range
        #mask = (wavelengths >= wavelength_min) & (wavelengths <= wavelength_max)
        filtered_latitudes = latitudes[mask]
        filtered_longitudes = longitudes[mask]
        filtered_counts = counts[mask]

    # Create a 2D histogram for latitude and longitude with photon intensity as the color
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.SouthPolarStereo()}, figsize=(10, 10))
    ax.set_extent([0, 360, -90, -45], crs=ccrs.PlateCarree())
    
    # Add gridlines and coastlines for context
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    #ax.coastlines()

    # Plot the data
    sc = ax.scatter(
        filtered_longitudes, filtered_latitudes, c=log10(filtered_counts), s=1, cmap='plasma', 
        alpha=0.75, transform=ccrs.PlateCarree()
    )
    cbar = plt.colorbar(sc, ax=ax, orientation='horizontal', pad=0.05, aspect=50)
    cbar.set_label("Photon Intensity (counts)")

    ax.set_title(f"Southern Hemisphere Photon Intensity (log) for Wavelength {wavelength_min}-{wavelength_max} nm")
    plt.show()
    
    
    #plt.figure(figsize=(12, 8))
    #intensity_map, xedges, yedges = np.histogram2d(filtered_longitudes, filtered_latitudes, bins=1000, weights=filtered_counts)
    #extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    
    # Plotting the 2D histogram
    #plt.imshow(log10(intensity_map.T), extent=extent, origin='lower', aspect='auto', cmap='viridis')
    #plt.colorbar(label="log$_{10}$(Photon Intensity (counts))")
    #plt.xlabel("Longitude (degrees)")
    #plt.ylabel("Latitude (degrees)")
    #plt.title(f"Photon Intensity Map for Wavelength Range {wavelength_min}-{wavelength_max} nm")
    #plt.grid(True)
    #plt.xlim(0, 360)
    #plt.ylim(-90, 90)
    #plt.show()

# Usage example
file_path = 'UVS_S01_738602023_2023149_P51SY3_V01.FIT'  # Replace with your file path
lat_lon_photon_intensity_plot(file_path, wavelength_min=150, wavelength_max=160)

