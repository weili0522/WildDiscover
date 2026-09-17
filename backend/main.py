from pydantic import BaseModel
import json
import os
from functools import lru_cache
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import GeoJSONFeatureCollection
from fastapi.middleware.gzip import GZipMiddleware

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

frontend_url = os.environ.get("FRONTEND_URL")
if frontend_url:
    allowed_origins.append(frontend_url)

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

from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WildDiscover API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins, # Updated for Vercel deployment
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
    valid_species = [
        "night-parrot", "princess-parrot", "plains-wanderer", 
        "rufous-scrub-bird", "malleefowl", "dusky-grasswren",
        "pilot-bird" # Keep pilot-bird for fallback
    ]

    if species_id not in valid_species:
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

    geojson_path = Path(__file__).resolve().parent / "data" / "processed" / f"{species_id}.geojson"
    if not geojson_path.exists():
        # Fallback to pilot-bird or ghost habitat if specific one isn't ready
        geojson_path = Path(__file__).resolve().parent / "data" / "processed" / "ghost_habitat_prediction.geojson"

    with geojson_path.open("r", encoding="utf-8") as f:
        prediction = json.load(f)

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

# --- Phase 1 Placeholder API Endpoints ---

from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class AuthRequest(BaseModel):
    username: str
    password: str

@app.post("/api/v1/auth/register")
async def register(request: AuthRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    hashed_pwd = hash_password(request.password)
    new_user = User(username=request.username, password_hash=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Registration successful", "username": new_user.username}

@app.post("/api/v1/auth/login")
async def login(request: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
        
    if user.password_hash != hash_password(request.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
        
    # In a real app we would generate a proper JWT token here
    return {"access_token": f"token_for_{user.username}", "token_type": "bearer", "username": user.username}



@app.get("/api/v1/map/geojson")
async def get_map_geojson():
    points_path = Path(__file__).resolve().parent / "data" / "raw" / "viewing_points_aus.geojson"
    if points_path.exists():
        with points_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "type": "FeatureCollection",
        "features": []
    }


class JournalRequest(BaseModel):
    username: str
    species_id: str
    exploration_date: str

@app.post("/api/v1/journal")
async def save_journal(request: JournalRequest, db: Session = Depends(get_db)):
    from models import Investigation
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    investigation = Investigation(
        user_id=user.id,
        species_id=request.species_id,
        exploration_date=request.exploration_date
    )
    db.add(investigation)
    user.logged_trips_count = (user.logged_trips_count or 0) + 1
    db.commit()
    db.refresh(investigation)
    
    return {"message": "Journal saved", "id": investigation.id}

@app.get("/api/v1/journal/{username}")
async def get_journal(username: str, db: Session = Depends(get_db)):
    from models import Investigation
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    investigations = db.query(Investigation).filter(Investigation.user_id == user.id).order_by(Investigation.id.desc()).all()
    
    return [
        {
            "id": inv.id,
            "species_id": inv.species_id,
            "exploration_date": inv.exploration_date,
            "created_at": inv.created_at.isoformat()
        }
        for inv in investigations
    ]


class ChallengeSuccessRequest(BaseModel):
    username: str

@app.post("/api/v1/challenge/success")
async def challenge_success(request: ChallengeSuccessRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.bird_calls_identified = (user.bird_calls_identified or 0) + 1
    db.commit()
    
    return {"message": "Success recorded", "bird_calls_identified": user.bird_calls_identified or 0}

@app.get("/api/v1/profile/{username}")
async def get_profile(username: str, db: Session = Depends(get_db)):
    from models import Investigation
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Calculate rank based on points: (logged_trips_count * 20) + (bird_calls_identified * 5)
    all_users = db.query(User).all()
    
    # Create a list of tuples (user_id, points)
    user_points = []
    for u in all_users:
        pts = ((u.logged_trips_count or 0) * 20) + ((u.bird_calls_identified or 0) * 5)
        user_points.append((u.id, pts))
        
    # Sort descending
    user_points.sort(key=lambda x: x[1], reverse=True)
    
    # Find rank
    rank = 1
    for i, up in enumerate(user_points):
        if up[0] == user.id:
            rank = i + 1
            break
            
    # Fetch investigations
    investigations = db.query(Investigation).filter(Investigation.user_id == user.id).order_by(Investigation.id.desc()).all()
    inv_list = [
        {
            "id": inv.id,
            "species_id": inv.species_id,
            "exploration_date": inv.exploration_date,
            "created_at": inv.created_at.isoformat()
        }
        for inv in investigations
    ]
            
    my_points = ((user.logged_trips_count or 0) * 20) + ((user.bird_calls_identified or 0) * 5)
    
    return {
        "username": user.username,
        "points": my_points,
        "logged_trips_count": user.logged_trips_count or 0,
        "bird_calls_identified": user.bird_calls_identified or 0,
        "rank": rank,
        "total_users": len(all_users),
        "investigations": inv_list
    }


@app.get("/api/v1/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    
    leaderboard = []
    for u in all_users:
        pts = ((u.logged_trips_count or 0) * 20) + ((u.bird_calls_identified or 0) * 5)
        leaderboard.append({
            "id": u.id,
            "username": u.username,
            "points": pts
        })
        
    leaderboard.sort(key=lambda x: x["points"], reverse=True)
    
    # Return top 5
    return leaderboard[:5]
