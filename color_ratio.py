import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import numpy as np
import cartopy.crs as ccrs
from astropy.io import fits
from collections import defaultdict

# Open the FITS file and load photon data
file_path = 'UVS_S01_737487019_2023136_P51OBS_V01.FIT'
with fits.open(file_path) as hdul:
    data = hdul[2].data  # Assuming HDU 2 contains the calibrated photon list
    wavelength = data['WAVELENGTH']  # Wavelengths in nm
    latitude = data['JUPITER_LAT_400km']  # Latitude data in degrees
    longitude = data['JUPITER_LON_400km']  # Longitude data in degrees
    intensity = data['WEIGHTED_COUNT']  # Photon intensity or count
    emission_angle = data['EMISSION_ANGLE']  # Emission angle in degrees

nadir_range = 30

# Define wavelength bands in nm
band1_min, band1_max = 155, 162  # Adjust based on your bands of interest
band2_min, band2_max = 123, 130  # Adjust based on your bands of interest

# Separate photons into band 1 and band 2 based on wavelength
band1_mask = (wavelength >= band1_min) & (wavelength <= band1_max) & (emission_angle <= nadir_range)
band2_mask = (wavelength >= band2_min) & (wavelength <= band2_max) & (emission_angle <= nadir_range)



# Create dictionaries to sum intensities for each (lat, lon) point
band1_sums = defaultdict(float)
band2_sums = defaultdict(float)

# Sum intensities for each band at each lat-lon point
for lat, lon, inten, in_band1, in_band2 in zip(latitude, longitude, intensity, band1_mask, band2_mask):
    key = (lat, lon)
    if in_band1:
        band1_sums[key] += inten
    if in_band2:
        band2_sums[key] += inten

# Calculate color ratio for each unique lat-lon point
latitudes, longitudes, color_ratios = [], [], []
for (lat, lon) in band1_sums.keys():
    if band2_sums[(lat, lon)] > 0:  # Avoid division by zero
        color_ratio = band1_sums[(lat, lon)] / band2_sums[(lat, lon)]
        latitudes.append(lat)
        longitudes.append(lon)
        if (color_ratio < 1):
          color_ratios.append(np.nan)
        else:
          color_ratios.append(color_ratio)


# Convert to arrays for plotting
latitudes = np.array(latitudes)
longitudes = np.array(longitudes)
color_ratios = np.array(color_ratios)

# Set up a grid for contouring
grid_lat, grid_lon = np.linspace(0, 90, 100), np.linspace(0, 366, 100)
lon_grid, lat_grid = np.meshgrid(grid_lon, grid_lat)
color_ratio_grid = griddata((longitudes, latitudes), color_ratios, (lon_grid, lat_grid), method='linear')

# Set color ratios < 1 to NaN in the grid
#color_ratio_grid[(color_ratio_grid > 0) & (color_ratio_grid < 1)] = np.nan

# Plot the color ratio on a lat-lon map

fig, ax = plt.subplots(subplot_kw={'projection': ccrs.NorthPolarStereo()}, figsize=(10, 10))
#ax.set_extent([0, 360, 90, 45], crs=ccrs.PlateCarree())

contour = ax.contourf(lon_grid, lat_grid, color_ratio_grid, levels=30, cmap='plasma', transform=ccrs.PlateCarree())
plt.colorbar(contour, label="Color Ratio (Unabsorbed / Absorbed)")
gl = ax.gridlines(draw_labels=True, linestyle="--", linewidth=0.5)
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}
#fig = plt.figure(figsize=(10, 5))
#ax = plt.axes(projection=ccrs.PlateCarree())
#sc = ax.scatter(longitudes, latitudes, c=color_ratios, cmap='viridis', marker='.', transform=ccrs.PlateCarree())
#plt.colorbar(sc,ax = ax, label="Photon Color Ratio (Band 1 / Band 2)")

# Set map attributes
#ax.coastlines()
ax.set_title("Photon Color Ratio (UV Emissions) - Summed Intensity per Point")
#ax.set_extent([-180, 180, -90, 0], ccrs.PlateCarree())  # Adjust to southern hemisphere extent if needed

plt.show()

