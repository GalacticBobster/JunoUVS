import os
import subprocess
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from astropy.io import fits
import numpy as np
import requests
from bs4 import BeautifulSoup

# The base URL where the FIT files are located
base_url = "https://pds-atmospheres.nmsu.edu/cgi-bin/getdir.pl?volume=jnouvs_5001&dir=DATA/ORBIT-32/"
download_url = "https://pds-atmospheres.nmsu.edu"

# Create a directory to save the downloaded files
os.makedirs("FIT_files", exist_ok=True)

# Send a GET request to the page
response = requests.get(base_url)
response.raise_for_status()  # Check for any request errors

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Find all links to .FIT files
fit_files = []
for link in soup.find_all('a'):
    file_link = link.get('href')
    if file_link and file_link.endswith('.FIT'):  # Check if the link ends with .FIT
        fit_files.append(file_link)

# Download the file
#for fit_file in fit_files:
#  file_url = f"{fit_file}"
#  subprocess.run(["wget", file_url])

# Get the current working directory
current_directory = os.getcwd()

# List all files in the current directory and find those ending with '.FIT'
fit_files = [f for f in os.listdir(current_directory) if f.endswith('.FIT')]

#fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.NorthPolarStereo()})

for fit_file in fit_files:
# Open the FITS file
  hdul = fits.open(fit_file)
  print("Opening file: " + str(fit_file))

# Extract the data
  ratio_map = hdul[4].data  # Ratio map (HDU 4)
  latitude_map = hdul[5].data  # Latitude map (HDU 5)
  longitude_map = hdul[6].data  # Longitude map (HDU 6)

# Replace invalid data with NaN
  ix = np.where(latitude_map == -999.0)
  latitude_map[ix] = np.nan
  ix = np.where(longitude_map == -999.0)
  longitude_map[ix] = np.nan
  ix = np.where(ratio_map <= 0.0)
  ratio_map[ix] = np.nan

# Create a plot
#  fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

# Plot the data as a scatter plot
  sc = ax.scatter(longitude_map, latitude_map, c=ratio_map, cmap='inferno', s=10, transform=ccrs.PlateCarree())

# Remove existing colorbars
#  for cbar in fig.get_children():
#    if isinstance(cbar, plt.colorbar.Colorbar):
#        cbar.remove()

ax.set_extent([-180, 180, 45, 90], ccrs.PlateCarree())
# Add coastlines and gridlines for context
#ax.coastlines()
ax.gridlines(draw_labels=True)

# Add a new colorbar
cbar = plt.colorbar(sc, ax=ax, label='CR')

# Save the plot
#plt.savefig('figs/JunoUVS_CR_PJ32.png')
plt.show()

