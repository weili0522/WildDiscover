import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio

# Load multi-species cleaned biological data
birds_gdf = gpd.read_parquet("multispecies_occurrences_clean.parquet")

# Helper function from Iteration 1 to sample rasters efficiently
def sample_raster(raster_path, coordinate_list):
    with rasterio.open(raster_path) as src:
        return [val[0] for val in src.sample(coordinate_list)]

all_species_matrices = []

# Iterate through each species
for species_name, group in birds_gdf.groupby('scientificName'):
    slug = species_name.lower().replace(" ", "_").replace("(", "").replace(")", "")
    print(f"\n--- Processing Matrix for: {species_name} ---")
    
    # Raster paths generated from Phase 2/3
    elev_path = f"species_rasters/{slug}_elevation.tif"
    slope_path = f"species_rasters/{slug}_slope.tif"
    aspect_path = f"species_rasters/{slug}_aspect.tif"
    hcas_path = f"species_rasters/{slug}_hcas.tif"
    
    # Presences (presence = 1)
    pres_coords = [(geom.x, geom.y) for geom in group.geometry]
    
    presence_df = pd.DataFrame({
        'scientificName': species_name,
        'x_coord': [c[0] for c in pres_coords],
        'y_coord': [c[1] for c in pres_coords],
        'presence': 1,
        'elevation': sample_raster(elev_path, pres_coords),
        'slope': sample_raster(slope_path, pres_coords),
        'aspect': sample_raster(aspect_path, pres_coords),
        'hcas': sample_raster(hcas_path, pres_coords)
    })
    
    # Drop nodata / NaNs
    presence_df = presence_df.dropna()
    num_presences = len(presence_df)
    print(f"Valid presences: {num_presences}")
    
    # Pseudo-absences (presence = 0)
    with rasterio.open(elev_path) as src:
        minx, miny, maxx, maxy = src.bounds
        nodata_val = src.nodata
    
    # Generate 3x candidate points to account for ocean/nodata drops
    np.random.seed(42)
    rand_x = np.random.uniform(minx, maxx, num_presences * 3)
    rand_y = np.random.uniform(miny, maxy, num_presences * 3)
    candidate_coords = list(zip(rand_x, rand_y))
    
    absence_df = pd.DataFrame({
        'scientificName': species_name,
        'x_coord': rand_x,
        'y_coord': rand_y,
        'presence': 0,
        'elevation': sample_raster(elev_path, candidate_coords),
        'slope': sample_raster(slope_path, candidate_coords),
        'aspect': sample_raster(aspect_path, candidate_coords),
        'hcas': sample_raster(hcas_path, candidate_coords)
    })
    
    # Filter out nodata pixels and NaNs
    if nodata_val is not None:
        absence_df = absence_df[absence_df['elevation'] != nodata_val]
    absence_df = absence_df.dropna()
    
    # Sample down to match 1:1 balance
    absence_df = absence_df.sample(n=num_presences, random_state=42)
    
    # --- C. Combine & Export ---
    species_matrix = pd.concat([presence_df, absence_df], ignore_index=True)
    
    # Save individual species matrix
    os.makedirs("species_matrices", exist_ok=True)
    species_matrix.to_csv(f"species_matrices/{slug}_training_matrix.csv", index=False)
    print(f"Saved: species_matrices/{slug}_training_matrix.csv ({len(species_matrix)} balanced rows)")
    
    all_species_matrices.append(species_matrix)

# Export Master Consolidated Matrix
master_training_matrix = pd.concat(all_species_matrices, ignore_index=True)
master_training_matrix.to_csv("master_training_matrix_with_absences.csv", index=False)
print(f"\nPipeline complete! Exported {len(master_training_matrix)} total records across 6 species to master_training_matrix_with_absences.csv")