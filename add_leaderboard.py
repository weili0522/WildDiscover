with open('backend/main.py', 'r') as f:
    content = f.read()

leaderboard_endpoint = """
@app.get("/api/v1/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    all_users = db.query(User).all()
    
    leaderboard = []
    for u in all_users:
        pts = (u.logged_trips_count * 20) + (u.bird_calls_identified * 5)
        leaderboard.append({
            "id": u.id,
            "username": u.username,
            "points": pts
        })
        
    leaderboard.sort(key=lambda x: x["points"], reverse=True)
    
    # Return top 5
    return leaderboard[:5]
"""

content = content + "\n" + leaderboard_endpoint

with open('backend/main.py', 'w') as f:
    f.write(content)
