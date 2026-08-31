import pandas as pd
import rasterio
import elapid
from sklearn import metrics

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

# Model Training
print("Training MaxEnt Model...")
model = elapid.MaxentModel(transform="cloglog")
model.fit(x, y)

y_pred = model.predict(x)
roc_auc = metrics.roc_auc_score(y, y_pred)
print(f"Training ROC-AUC Score: {roc_auc:.3f}")

# Spatial Prediction & Export
print("Generating final prediction map...")
elapid.apply_model_to_rasters(
    model,
    raster_paths,
    "habitat_suitability_maxent.tif"
)

print("Export complete: habitat_suitability_maxent.tif")