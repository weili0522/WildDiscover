from typing import List, Literal, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    logged_trips_count = Column(Integer, default=0)
    bird_calls_identified = Column(Integer, default=0)
    
    investigations = relationship("Investigation", back_populates="owner")

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    species_id = Column(String)
    exploration_date = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="investigations")
