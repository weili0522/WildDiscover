# WildDiscover Backend

The WildDiscover backend is a FastAPI service that provides processed Night Parrot habitat suitability data to the frontend as GeoJSON.

## Run the Backend Locally

Open a terminal and enter the backend directory:

```bash
cd backend
```

Activate the virtual environment on macOS:

```bash
source venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

The backend will be available at:

- API: `http://127.0.0.1:8000`
- Swagger documentation: `http://127.0.0.1:8000/docs`

## API Endpoints

### `GET /`

Returns the operational status of the WildDiscover API.

Example response:

```json
{
  "message": "WildDiscover API is running"
}
```

### `GET /api/v1/predict/{species_id}`

Returns the predicted habitat suitability layer for the selected species as a GeoJSON `FeatureCollection`.

The current pilot species identifier is:

```text
pilot-bird
```

Example request:

```text
http://127.0.0.1:8000/api/v1/predict/pilot-bird
```

The endpoint also accepts optional coordinates:

- `latitude`: valid global range is `-90` to `90`
- `longitude`: valid global range is `-180` to `180`

For the currently supported Australian area:

- Latitude must be between `-44` and `-10`
- Longitude must be between `112` and `154`

Example request with coordinates:

```text
http://127.0.0.1:8000/api/v1/predict/pilot-bird?latitude=-25&longitude=130
```

### `GET /api/v1/layers/habitat`

Returns the processed Night Parrot habitat suitability layer as a GeoJSON `FeatureCollection`.

Example request:

```text
http://127.0.0.1:8000/api/v1/layers/habitat
```

## GeoJSON Response Models

The Pydantic models in `models.py` validate the GeoJSON returned by the habitat endpoints.

The response uses the following structure:

```text
GeoJSONFeatureCollection
└── GeoJSONFeature
    ├── PolygonGeometry
    └── FeatureProperties
```

Each feature contains:

- `species_id`: internal species identifier
- `species_name`: displayed name of the species
- `suitability`: classified habitat suitability value
- `geometry`: polygon coordinates using EPSG:4326

The stored suitability value is a representative value for a classification range. It is not the exact probability value of every original raster pixel.

## Source Data

The habitat suitability data is provided as a GeoTIFF raster:

```text
data/raw/habitat_suitability_maxent.tif
```

The supplied model file is stored at:

```text
data/raw/night_parrot_maxent_beta_2.joblib
```

The GeoTIFF:

- Uses the EPSG:3577 coordinate reference system
- Contains one raster band
- Uses the `float32` data type
- Stores suitability values between approximately 0 and 1
- Uses `-9999` as the NoData value

The `.joblib` file is retained as supplied source material but is not required by the current raster-to-GeoJSON processing pipeline.

## Inspecting the Raster

Run the raster inspection script from the `backend` directory:

```bash
python inspect_raster.py
```

The script reports information such as:

- Coordinate reference system
- Rasterlk
- Raster dimensions
- Number of bands
- Data type
- NoData value
- Geographic bounds
- Sample minimum and maximum
- Suitability percentiles

## Generating the Processed GeoJSON

Run the processing script from the `backend` directory:

```bash
python vectorize_raster.py
```

The generated file is saved to:

```text
data/processed/ghost_habitat_prediction.geojson
```

The processing pipeline:

1. Reads the original GeoTIFF raster.
2. Downsamples the raster to reduce processing and response size.
3. Classifies the continuous suitability values into five ranges.
4. Removes very small isolated raster regions.
5. Converts classified raster regions into vector polygons.
6. Simplifies the polygon boundaries.
7. Reprojects the polygons from EPSG:3577 to EPSG:4326.
8. Saves the result as GeoJSON.

The current processed output contains approximately 4,229 polygons and has a file size of approximately 5.48 MB. These values may change if the processing settings are adjusted.

## Suitability Classification

The Iteration 1 visualisation uses the following classes:

| Original suitability range | Stored value | Map colour |
| --- | ---: | --- |
| 0.50–0.60 | 0.55 | Green |
| 0.60–0.70 | 0.65 | Yellow-green |
| 0.70–0.80 | 0.75 | Yellow |
| 0.80–0.90 | 0.85 | Orange |
| 0.90–1.00 | 0.95 | Red |

These ranges are visualisation choices for Iteration 1. They should not be interpreted as scientifically validated habitat thresholds.

The map legend represents suitability from low to high:

```text
Green → Yellow-green → Yellow → Orange → Red
```

## API Performance

The processed GeoJSON is loaded and cached by the backend using `lru_cache`.

FastAPI's `GZipMiddleware` compresses large API responses during network transfer:

```python
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)
```

GZip reduces the amount of data transferred to the browser. It does not change the size of the GeoJSON file stored on disk.

After regenerating the GeoJSON, restart the backend so the cached data is reloaded:

```bash
uvicorn main:app --reload
```

## Location Protection

The backend currently contains an `apply_location_blurring()` placeholder.

In Iteration 1, it returns the GeoJSON unchanged. A future iteration can implement coordinate masking or location generalisation to reduce poaching risks for vulnerable species.

## Testing

Run the backend tests from the `backend` directory:

```bash
pytest
```

All tests should pass before committing and deploying backend changes.

## Git and Large Files

Do not commit the raw GeoTIFF or model file:

```text
data/raw/habitat_suitability_maxent.tif
data/raw/night_parrot_maxent_beta_2.joblib
```

These files should be excluded using `.gitignore` and `.dockerignore`.

The processed GeoJSON should be committed because it is required by the deployed backend:

```text
data/processed/ghost_habitat_prediction.geojson
```

## Deployment

The backend is deployed as a Render Web Service.

Production API:

```text
https://wilddiscover-api.onrender.com
```

Production habitat endpoint:

```text
https://wilddiscover-api.onrender.com/api/v1/predict/pilot-bird
```

The frontend should use the following environment variable:

```text
VITE_API_BASE_URL=https://wilddiscover-api.onrender.com
```