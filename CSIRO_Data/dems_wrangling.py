import rasterio
from rasterio.windows import from_bounds
import xarray as xr
import xrspatial as xrs
import numpy as np

# 1. Define a Pilot Bounding Box in EPSG:3577 (Australian Albers)
# This mock box covers a section of the arid zone out West
pilot_bbox = (-1500000.0, -2500000.0, -1000000.0, -2000000.0) # (min_x, min_y, max_x, max_y)

print("Cropping 8GB DEM to Pilot Bounding Box...")

# 2. Extract only the required window from the raw CSIRO DEM
with rasterio.open("2026-01-22_Liu_Ning_66355v1/data/90m_EPSG3577/Relief_dems_3s_mosaic1.tif") as src:
    window = from_bounds(*pilot_bbox, transform=src.transform)
    dem_array = src.read(1, window=window)
    dem_transform = src.window_transform(window)
    dem_profile = src.profile

# Update the metadata profile for the new, smaller rasters
dem_profile.update({
    "height": dem_array.shape[0],
    "width": dem_array.shape[1],
    "transform": dem_transform
})

# Save the cropped baseline DEM
with rasterio.open("pilot_dem_cropped.tif", "w", **dem_profile) as dest:
    dest.write(dem_array, 1)
print("Saved: pilot_dem_cropped.tif")

# 3. Generate Spatial Features for the ML Model
print("Engineering Slope and Aspect features...")

# xarray-spatial requires an xarray DataArray
dem_da = xr.DataArray(dem_array)

# Calculate Slope (steepness of the terrain)
slope_da = xrs.slope(dem_da)
slope_array = slope_da.values.astype(np.float32)

# Calculate Aspect (compass direction the slope faces)
aspect_da = xrs.aspect(dem_da)
aspect_array = aspect_da.values.astype(np.float32)

# Save the new engineered feature rasters
with rasterio.open("pilot_dem_slope.tif", "w", **dem_profile) as dest:
    dest.write(slope_array, 1)
print("Saved: pilot_dem_slope.tif")

with rasterio.open("pilot_dem_aspect.tif", "w", **dem_profile) as dest:
    dest.write(aspect_array, 1)
print("Saved: pilot_dem_aspect.tif")

print("Pipeline Phase 1 & 2 Complete! Ready for the ALA spatial join.")
