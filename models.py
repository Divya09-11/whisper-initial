from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    duration = Column(Float)
    file_path = Column(String)
    
    # Classification fields
    speaker_type = Column(String)  # Customer/Salesperson
    conversation_phase = Column(String)  # Introduction/Discovery/Pitch/etc
    sentiment = Column(String)  # Positive/Neutral/Negative