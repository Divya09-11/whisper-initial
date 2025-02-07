from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
import services

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sales Conversation Analysis System")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload/")
async def upload_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process audio file
    """
    try:
        result = await services.process_audio_file(file, db)
        return {"message": "File processed successfully", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transcripts/")
def get_transcripts(db: Session = Depends(get_db)):
    """
    Get all transcripts
    """
    return services.get_all_transcripts(db)

@app.get("/transcripts/{transcript_id}")
def get_transcript(transcript_id: int, db: Session = Depends(get_db)):
    """
    Get specific transcript by ID
    """
    transcript = services.get_transcript(db, transcript_id)
    if transcript is None:
        raise HTTPException(status_code=404, detail="Transcript not found")
    return transcript

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sales Conversation Analysis System!"}
