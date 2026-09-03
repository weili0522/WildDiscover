import json
import os
from functools import lru_cache
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import GeoJSONFeatureCollection
from fastapi.middleware.gzip import GZipMiddleware

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173"
    ).split(",")
    if origin.strip()
]

HABITAT_GEOJSON_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "processed"
    / "ghost_habitat_prediction.geojson"
)

@lru_cache(maxsize=1)
def load_habitat_geojson():
    """Load and cache the live Night Parrot habitat GeoJSON file."""
    with HABITAT_GEOJSON_PATH.open(
        mode="r",
        encoding="utf-8",
    ) as geojson_file:
        return json.load(geojson_file)

app = FastAPI(
    title="WildDiscover API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)

@app.get("/")
async def root():
    """Return the operational status of the WildDiscover API.

    Returns:
        dict: A JSON object containing a message confirming that the API
        is running.
    """
    return {"message": "WildDiscover API is running"}

def apply_location_blurring(geojson_data):
    """
    Placeholder for location masking.

    In Iteration 1, the GeoJSON is returned unchanged.
    In future iterations, exact coordinates will be blurred
    to help protect vulnerable species from poaching risks.
    """
    return geojson_data

@app.get(
    "/api/v1/predict/{species_id}",
    response_model=GeoJSONFeatureCollection
)
async def predict_habitat(
    species_id: str,
    latitude: float = Query(None, ge=-90, le=90),
    longitude: float = Query(None, ge=-180, le=180)
):
    """Return predicted habitat suitability for a selected species.

    The endpoint currently supports the pilot species identified by
    ``pilot-bird``. Optional coordinates are first constrained to valid
    global latitude and longitude ranges by FastAPI. When supplied, they
    are also checked against the supported Australian bounds: latitude
    from -44 to -10 degrees and longitude from 112 to 154 degrees.

    Args:
        species_id: Identifier of the species for which habitat suitability
            is requested.
        latitude: Optional latitude in decimal degrees. The global valid
            range is -90 to 90, while the supported Australian range is
            -44 to -10.
        longitude: Optional longitude in decimal degrees. The global valid
            range is -180 to 180, while the supported Australian range is
            112 to 154.

    Returns:
        GeoJSONFeatureCollection: A GeoJSON FeatureCollection containing a
        habitat polygon and properties including the species identifier,
        species name, and suitability score.

    Raises:
        HTTPException: A 404 error if the species identifier is unsupported.
        HTTPException: A 400 error if the supplied coordinates fall outside
            the supported Australian bounds.
    """

    if species_id != "pilot-bird":
        raise HTTPException(
            status_code=404,
            detail="Species not found"
        )

    if latitude is not None and not (-44 <= latitude <= -10):
        raise HTTPException(
            status_code=400,
            detail="Latitude is outside the supported Australian bounds"
        )

    if longitude is not None and not (112 <= longitude <= 154):
        raise HTTPException(
            status_code=400,
            detail="Longitude is outside the supported Australian bounds"
        )

    
    prediction = load_habitat_geojson()
    return apply_location_blurring(prediction)

@app.get(
    "/api/v1/layers/habitat",
    response_model=GeoJSONFeatureCollection
)
async def get_habitat_layer():
    """Return the live Night Parrot habitat suitability layer.

    Returns:
        GeoJSONFeatureCollection: A GeoJSON FeatureCollection generated
        from the live model suitability raster.
    """
    return load_habitat_geojson()