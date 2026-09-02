import numpy as np
import pandas as pd
import rasterio
import elapid
from sklearn import metrics
from sklearn.model_selection import cross_val_score


# 1. Convert the Aspect Raster into Northness & Eastness Rasters
print("Decomposing Aspect raster into Northness and Eastness...")
with rasterio.open("pilot_dem_aspect.tif") as src:
    aspect_array = src.read(1)
    profile = src.profile
    
    # Ignore NoData values during math if they exist (e.g., -9999)
    valid_mask = aspect_array != src.nodata
    
    # Convert degrees to radians and calculate trig functions
    aspect_rad = np.radians(aspect_array)
    northness = np.where(valid_mask, np.cos(aspect_rad), src.nodata)
    eastness = np.where(valid_mask, np.sin(aspect_rad), src.nodata)

with rasterio.open("pilot_dem_northness.tif", "w", **profile) as dest:
    dest.write(northness.astype(profile['dtype']), 1)
with rasterio.open("pilot_dem_eastness.tif", "w", **profile) as dest:
    dest.write(eastness.astype(profile['dtype']), 1)

# 2. Data Ingestion & New Raster Paths
presence_df = pd.read_csv("training_matrix.csv")

# Convert raw aspect in the presence matrix to Northness/Eastness
if 'aspect' in presence_df.columns:
    presence_rad = np.radians(presence_df['aspect'])
    presence_df['northness'] = np.cos(presence_rad)
    presence_df['eastness'] = np.sin(presence_rad)
    presence_df = presence_df.drop(columns=['aspect'])

raster_paths = [
    "pilot_elevation_cropped.tif",
    "pilot_dem_slope.tif",
    "pilot_dem_northness.tif",
    "pilot_dem_eastness.tif"
]

# 3. Background Point Generation
print("Generating background pseudo-absences...")
bg_points = elapid.sample_raster(raster_paths[0], count=10000)
bg_coords = list(zip(bg_points.geometry.x, bg_points.geometry.y))

def sample_raster(raster_path, coords):
    with rasterio.open(raster_path) as src:
        return [val[0] for val in src.sample(coords)]

bg_df = pd.DataFrame({
    'x_coord': [c[0] for c in bg_coords],
    'y_coord': [c[1] for c in bg_coords],
    'presence': 0,
    'elevation': sample_raster(raster_paths[0], bg_coords),
    'slope': sample_raster(raster_paths[1], bg_coords),
    'northness': sample_raster(raster_paths[2], bg_coords),
    'eastness': sample_raster(raster_paths[3], bg_coords)
}).dropna()

# Add into the final training matrix
model_data = pd.concat([presence_df, bg_df], ignore_index=True)

# 4. Define Updated Feature Matrix
x = model_data[['elevation', 'slope', 'northness', 'eastness']]
y = model_data['presence']
xy = model_data[['x_coord', 'y_coord']] 

# 5. Initialize & Validate the Model
print("Initializing MaxEnt Model...")
model = elapid.MaxentModel(transform="cloglog", beta_multiplier=2)

print("Running Cross-Validation...")
cv_scores = cross_val_score(model, x, y, cv=5, scoring='roc_auc')
print(f"Standard 5-Fold CV ROC-AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

# 6. Finalize Model & Export Prediction Map
print("Fitting final model on all data...")
model.fit(x, y)

print("Generating final prediction map...")
elapid.apply_model_to_rasters(
    model,
    raster_paths,
    "habitat_suitability_maxent.tif"
)
print("Export complete: habitat_suitability_maxent.tif")