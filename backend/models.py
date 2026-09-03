from typing import List, Literal, Optional
from pydantic import BaseModel


class PolygonGeometry(BaseModel):
    """Represent a GeoJSON Polygon geometry."""

    type: Literal["Polygon"] = "Polygon"
    coordinates: List[List[List[float]]]


class FeatureProperties(BaseModel):
    """Store metadata and suitability values for a habitat feature."""

    species_id: str
    species_name: str
    suitability: float


class GeoJSONFeature(BaseModel):
    """Represent one predicted habitat polygon and its properties."""

    type: Literal["Feature"] = "Feature"
    geometry: PolygonGeometry
    properties: FeatureProperties


class GeoJSONFeatureCollection(BaseModel):
    """Represent the GeoJSON response returned by habitat endpoints."""
    
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[GeoJSONFeature]