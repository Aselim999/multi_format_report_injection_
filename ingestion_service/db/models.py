# implement models.py
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/ingestion_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class IngestionLog(Base):
    __tablename__ = "ingestion_logs"

    file_id = Column(String, primary_key=True, index=True)
    filename = Column(String)
    type = Column(String)
    status = Column(String)
    content = Column(Text)
    error = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class IngestionContent(Base):
    __tablename__ = "ingestion_contents"

    file_id = Column(String, ForeignKey("ingestion_logs.file_id"), primary_key=True)
    full_content = Column(JSON)
    fhir_data = Column(Text) 

    log = relationship("IngestionLog", backref="full_content_entry")    

def init_db():
    Base.metadata.create_all(bind=engine)
