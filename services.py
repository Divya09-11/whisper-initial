import whisper
from fastapi import UploadFile
from sqlalchemy.orm import Session
import models
import os
import tempfile

# Initialize Whisper model
model = whisper.load_model("large")

async def process_audio_file(file: UploadFile, db: Session):
    """
    Process uploaded audio file using Whisper and store results
    """
    # Validate file
    if not file.filename.endswith(('.wav', '.mp3', '.m4a')):
        raise ValueError("Unsupported file format")

    # Create temp file to store upload
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file.flush()
        
        # Transcribe audio
        result = model.transcribe(temp_file.name)
        
        # Create transcript record
        transcript = models.Transcript(
            filename=file.filename,
            content=result["text"],
            duration=result.get("duration", 0),
            file_path=temp_file.name,
            speaker_type="Unknown",  # To be implemented
            conversation_phase="Unknown",  # To be implemented
            sentiment="Unknown"  # To be implemented
        )
        
        db.add(transcript)
        db.commit()
        db.refresh(transcript)
        
        return {
            "id": transcript.id,
            "filename": transcript.filename,
            "duration": transcript.duration,
            "text": transcript.content
        }

def get_all_transcripts(db: Session):
    """
    Retrieve all transcripts
    """
    return db.query(models.Transcript).all()

def get_transcript(db: Session, transcript_id: int):
    """
    Retrieve specific transcript by ID
    """
    return db.query(models.Transcript).filter(models.Transcript.id == transcript_id).first()