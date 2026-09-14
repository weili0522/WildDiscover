import os
import rasterio
from rasterio.windows import from_bounds
import xarray as xr
import xrspatial as xrs
import numpy as np
import geopandas as gpd

# 1. Load occurrences and set file paths
ala_gdf = gpd.read_parquet("multispecies_occurrences_clean.parquet")
dem_path = "2026-01-22_Liu_Ning_66355v1/data/90m_EPSG3577/Relief_dems_3s_mosaic1.tif"
hcas_path = "/Users/sunathb/Documents/Sem 4/Industry Experience/Iteration 2/Data/2026-08-18_Valavi_Roozbeh_65549v9/data/1.HABITAT_CONDITION/3yr/HCAS33_AHC_2022_2024.tif"
buffer_dist = 50000  # 50km buffer in meters

os.makedirs("species_rasters", exist_ok=True)

# 2. Open both parent rasters
with rasterio.open(dem_path) as dem_src, rasterio.open(hcas_path) as hcas_src:
    # Verify CRS alignment
    assert dem_src.crs == ala_gdf.crs, f"DEM CRS mismatch: {dem_src.crs}"
    assert hcas_src.crs == ala_gdf.crs, f"HCAS CRS mismatch: {hcas_src.crs}"
    
    for species_name, group in ala_gdf.groupby('scientificName'):
        slug = species_name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        print(f"Generating 4-layer raster stack for: {species_name}...")
        
        # Calculate shared bounding box for this species
        minx, miny, maxx, maxy = group.total_bounds
        bbox = (minx - buffer_dist, miny - buffer_dist, maxx + buffer_dist, maxy + buffer_dist)
        
        # --- A. Process DEM, Slope & Aspect ---
        dem_win = from_bounds(*bbox, transform=dem_src.transform)
        dem_arr = dem_src.read(1, window=dem_win)
        dem_profile = dem_src.profile.copy()
        dem_profile.update({
            "height": dem_arr.shape[0],
            "width": dem_arr.shape[1],
            "transform": dem_src.window_transform(dem_win),
            "nodata": dem_src.nodata,
            "compress": "lzw"
        })
        
        # Save Elevation
        with rasterio.open(f"species_rasters/{slug}_elevation.tif", "w", **dem_profile) as dst:
            dst.write(dem_arr, 1)
            
        # Derive and save Slope & Aspect
        dem_da = xr.DataArray(dem_arr)
        with rasterio.open(f"species_rasters/{slug}_slope.tif", "w", **dem_profile) as dst:
            dst.write(xrs.slope(dem_da).values.astype(np.float32), 1)
            
        with rasterio.open(f"species_rasters/{slug}_aspect.tif", "w", **dem_profile) as dst:
            dst.write(xrs.aspect(dem_da).values.astype(np.float32), 1)
            
        # --- B. Process HCAS Layer ---
        hcas_win = from_bounds(*bbox, transform=hcas_src.transform)
        hcas_arr = hcas_src.read(1, window=hcas_win)
        hcas_profile = hcas_src.profile.copy()
        hcas_profile.update({
            "height": hcas_arr.shape[0],
            "width": hcas_arr.shape[1],
            "transform": hcas_src.window_transform(hcas_win),
            "nodata": hcas_src.nodata,
            "compress": "lzw"
        })
        
        # Save Cropped HCAS
        with rasterio.open(f"species_rasters/{slug}_hcas.tif", "w", **hcas_profile) as dst:
            dst.write(hcas_arr, 1)

print("All species raster stacks complete. 4 layers generated per bird.")