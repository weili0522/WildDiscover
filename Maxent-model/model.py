import pandas as pd
import rasterio
import elapid
from sklearn import metrics
from sklearn.model_selection import cross_val_score

# Data Ingestion
presence_df = pd.read_csv("training_matrix.csv")
raster_paths = [
    "pilot_elevation_cropped.tif",
    "pilot_dem_slope.tif",
    "pilot_dem_aspect.tif"
]

# Background Point Generation
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
    'aspect': sample_raster(raster_paths[2], bg_coords)
}).dropna()

# Add into the final training matrix
model_data = pd.concat([presence_df, bg_df], ignore_index=True)
x = model_data[['elevation', 'slope', 'aspect']]
y = model_data['presence']
xy = model_data[['x_coord', 'y_coord']] # Save coordinates in case you want to use Spatial CV later

# 1. Initialize the Model
print("Initializing MaxEnt Model...")
model = elapid.MaxentModel(transform="cloglog")

# 2. Perform 5-Fold Cross-Validation
print("Running Cross-Validation...")
# This splits the data 5 times, trains on 4/5, and tests on the holdout 1/5
cv_scores = cross_val_score(model, x, y, cv=5, scoring='roc_auc')

print(f"Standard 5-Fold CV ROC-AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

# 3. Finalize Model for Mapping
# Retrain on the entire dataset to generate the most accurate final heatmap
print("Fitting final model on all data...")
model.fit(x, y)

# 4. Spatial Prediction & Export
print("Generating final prediction map...")
elapid.apply_model_to_rasters(
    model,
    raster_paths,
    "habitat_suitability_maxent.tif"
)
print("Export complete: habitat_suitability_maxent.tif")