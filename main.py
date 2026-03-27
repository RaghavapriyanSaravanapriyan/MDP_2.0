from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database
import face_logic
from sqlalchemy.orm import Session
import os

app = FastAPI()

# CORS for external access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
def startup():
    database.init_db()

# Serve Frontend
@app.get("/")
async def get_frontend():
    return FileResponse("index.html")

class RegisterRequest(BaseModel):
    name: str
    images: list[str]

class DetectRequest(BaseModel):
    image: str

@app.post("/register")
async def register(req: RegisterRequest):
    if not req.name or not req.images:
        raise HTTPException(status_code=400, detail="Name and images are required")
    
    embeddings = []
    for img_data in req.images:
        emb = face_logic.get_embedding(img_data)
        if emb:
            embeddings.append(emb)
    
    if not embeddings:
        raise HTTPException(status_code=400, detail="Could not detect any faces in the provided images")
    
    db = database.SessionLocal()
    try:
        user = db.query(database.User).filter(database.User.name == req.name).first()
        if user:
            user.embeddings = embeddings
        else:
            user = database.User(name=req.name, embeddings=embeddings)
            db.add(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
        
    return {"message": f"User {req.name} registered successfully."}

@app.post("/detect")
async def detect(req: DetectRequest):
    if not req.image:
        raise HTTPException(status_code=400, detail="Image is required")
    
    current_emb = face_logic.get_embedding(req.image)
    if not current_emb:
        return {"match": False, "name": "Unknown", "status": "No face detected"}
    
    db = database.SessionLocal()
    try:
        users = db.query(database.User).all()
        user_list = [{"name": u.name, "embeddings": u.embeddings} for u in users]
        
        match_name = face_logic.find_match(current_emb, user_list, threshold=0.3)
        
        if match_name:
            return {"match": True, "name": match_name, "status": "Authorized"}
        else:
            return {"match": False, "name": "Unknown", "status": "Unauthorized"}
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
