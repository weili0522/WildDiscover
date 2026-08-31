from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import GeoJSONFeatureCollection

app = FastAPI(
    title="WildDiscover API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "WildDiscover API is running"}

@app.get(
    "/api/v1/predict/{species_id}",
    response_model=GeoJSONFeatureCollection
)
async def predict_habitat(
    species_id: str,
    latitude: float = Query(None, ge=-90, le=90),
    longitude: float = Query(None, ge=-180, le=180)):

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

    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [131.0, -24.0],
                            [134.0, -24.0],
                            [134.0, -21.0],
                            [131.0, -21.0],
                            [131.0, -24.0]
                        ]
                    ]
                },
                "properties": {
                    "species_id": species_id,
                    "species_name": "Night Parrot",
                    "suitability": 0.85
                }
            }
        ]
    }

@app.get(
    "/api/v1/layers/habitat",
    response_model=GeoJSONFeatureCollection
)
async def get_habitat_layer():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [131.0, -24.0],
                            [134.0, -24.0],
                            [134.0, -21.0],
                            [131.0, -21.0],
                            [131.0, -24.0]
                        ]
                    ]
                },
                "properties": {
                    "species_id": "pilot-bird",
                    "species_name": "Night Parrot",
                    "suitability": 0.85
                }
            }
        ]
    }