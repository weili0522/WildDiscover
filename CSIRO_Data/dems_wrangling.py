import rasterio
from rasterio.windows import from_bounds
import xarray as xr
import xrspatial as xrs
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from rasterio.plot import show

# Load Parquet and Calculate Bounding Box
ala_gdf = gpd.read_parquet("pilot_bird_occurrences_clean.parquet")
minx, miny, maxx, maxy = ala_gdf.total_bounds
buffer_dist = 50000  # 50km buffer in meters
pilot_bbox = (minx - buffer_dist, miny - buffer_dist, maxx + buffer_dist, maxy + buffer_dist)

print("Cropping 8GB DEM to Pilot Bounding Box...")

# Extract window and handle NoData
with rasterio.open("2026-01-22_Liu_Ning_66355v1/data/90m_EPSG3577/Relief_dems_3s_mosaic1.tif") as src:
    # Explicitly verify Coordinate Reference Systems match
    assert src.crs == ala_gdf.crs, f"CRS Mismatch! Raster is {src.crs}, Vector is {ala_gdf.crs}"
    print(f"CRS verified: {src.crs}")
    
    # Identify nodata value to prevent math errors
    nodata_val = src.nodata
    print(f"NoData value identified as: {nodata_val}")

    window = from_bounds(*pilot_bbox, transform=src.transform)
    dem_array = src.read(1, window=window)
    dem_transform = src.window_transform(window)
    dem_profile = src.profile

dem_profile.update({
    "height": dem_array.shape[0],
    "width": dem_array.shape[1],
    "transform": dem_transform,
    "nodata": nodata_val,
    "compress": "lzw"
})

# Save with the required file name
with rasterio.open("pilot_elevation_cropped.tif", "w", **dem_profile) as dest:
    dest.write(dem_array, 1)
print("Saved: pilot_elevation_cropped.tif")

# Generate Spatial Features for the ML Model
print("Engineering Slope and Aspect features...")
dem_da = xr.DataArray(dem_array)

slope_da = xrs.slope(dem_da)
slope_array = slope_da.values.astype(np.float32)

aspect_da = xrs.aspect(dem_da)
aspect_array = aspect_da.values.astype(np.float32)

with rasterio.open("pilot_dem_slope.tif", "w", **dem_profile) as dest:
    dest.write(slope_array, 1)
print("Saved: pilot_dem_slope.tif")

with rasterio.open("pilot_dem_aspect.tif", "w", **dem_profile) as dest:
    dest.write(aspect_array, 1)
print("Saved: pilot_dem_aspect.tif")

# Visual Quality Check
print("Generating visual quality check plot...")
with rasterio.open("pilot_elevation_cropped.tif") as src:
    fig, ax = plt.subplots(figsize=(10, 8))
    show(src, ax=ax, cmap='terrain', title="Quality Check: Cropped Elevation Map")
    plt.show()

print("Pipeline Phase 1 & 2 Complete! Ready for the ALA spatial join.")