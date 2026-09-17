with open('backend/main.py', 'r') as f:
    content = f.read()

profile_code = """
class ChallengeSuccessRequest(BaseModel):
    username: str

@app.post("/api/v1/challenge/success")
async def challenge_success(request: ChallengeSuccessRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.bird_calls_identified += 1
    db.commit()
    
    return {"message": "Success recorded", "bird_calls_identified": user.bird_calls_identified}

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
        pts = (u.logged_trips_count * 20) + (u.bird_calls_identified * 5)
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
            
    my_points = (user.logged_trips_count * 20) + (user.bird_calls_identified * 5)
    
    return {
        "username": user.username,
        "points": my_points,
        "logged_trips_count": user.logged_trips_count,
        "bird_calls_identified": user.bird_calls_identified,
        "rank": rank,
        "total_users": len(all_users),
        "investigations": inv_list
    }
"""

content = content + "\n" + profile_code

with open('backend/main.py', 'w') as f:
    f.write(content)
