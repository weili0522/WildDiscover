import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

# Check the cropped Elevation map
with rasterio.open("pilot_dem_cropped.tif") as src:
    fig, ax = plt.subplots(figsize=(8, 8))
    show(src, ax=ax, title="Pilot Cropped DEM (Elevation)", cmap="terrain")
    plt.show()

# Check the engineered Slope map
with rasterio.open("pilot_dem_slope.tif") as src:
    fig, ax = plt.subplots(figsize=(8, 8))
    show(src, ax=ax, title="Engineered Slope Feature", cmap="magma")
    plt.show()
