from typing import List, Literal, Optional
from pydantic import BaseModel


class PolygonGeometry(BaseModel):
    type: Literal["Polygon"] = "Polygon"
    coordinates: List[List[List[float]]]


class FeatureProperties(BaseModel):
    species_id: str
    species_name: str
    suitability: float


class GeoJSONFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: PolygonGeometry
    properties: FeatureProperties


class GeoJSONFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[GeoJSONFeature]

class Coordinate(BaseModel):
    latitude: float
    longitude: float


class BoundingBox(BaseModel):
    min_latitude: float
    min_longitude: float
    max_latitude: float
    max_longitude: float


class HabitatQuery(BaseModel):
    species_id: str
    coordinates: Optional[Coordinate] = None
    bounding_box: Optional[BoundingBox] = None