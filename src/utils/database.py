"""
Database module - SQLAlchemy models and database management
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean, 
    DateTime, Text, ForeignKey, JSON, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import enum

Base = declarative_base()


class ProcessingStatus(enum.Enum):
    """File processing status"""
    PENDING = "pending"
    FINGERPRINTING = "fingerprinting"
    METADATA_LOOKUP = "metadata_lookup"
    ML_SCORING = "ml_scoring"
    REVIEW_NEEDED = "review_needed"
    ORGANIZING = "organizing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class MediaType(enum.Enum):
    """Media type classification"""
    AUDIO = "audio"
    VIDEO = "video"
    UNKNOWN = "unknown"


class ReviewStatus(enum.Enum):
    """Review queue status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CORRECTED = "corrected"


class MediaFile(Base):
    """Main table for all media files"""
    __tablename__ = 'media_files'
    
    id = Column(Integer, primary_key=True)
    
    # File information
    original_path = Column(String(1024), nullable=False, unique=True)
    filename = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)  # bytes
    file_hash = Column(String(64), nullable=False, unique=True)  # SHA256
    media_type = Column(SQLEnum(MediaType), nullable=False)
    
    # Processing status
    status = Column(SQLEnum(ProcessingStatus), default=ProcessingStatus.PENDING)
    confidence_score = Column(Float, default=0.0)  # 0.0 to 1.0
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    # Output information (after organization)
    output_path = Column(String(1024), nullable=True)
    
    # USB source tracking
    usb_device_id = Column(String(256), nullable=True)
    is_on_usb = Column(Boolean, default=False)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Relationships - FIXED: renamed 'metadata' to 'media_metadata' (metadata is reserved)
    fingerprint = relationship("Fingerprint", back_populates="media_file", uselist=False)
    media_metadata = relationship("MediaMetadata", back_populates="media_file", uselist=False)
    ml_features = relationship("MLFeatures", back_populates="media_file", uselist=False)
    review = relationship("ReviewQueue", back_populates="media_file", uselist=False)
    processing_logs = relationship("ProcessingLog", back_populates="media_file")


class Fingerprint(Base):
    """Audio/Video fingerprints"""
    __tablename__ = 'fingerprints'
    
    id = Column(Integer, primary_key=True)
    media_file_id = Column(Integer, ForeignKey('media_files.id'), unique=True)
    
    # Audio fingerprinting (Chromaprint)
    chromaprint_fingerprint = Column(Text, nullable=True)
    chromaprint_duration = Column(Float, nullable=True)
    acoustid_id = Column(String(128), nullable=True)
    acoustid_score = Column(Float, nullable=True)
    
    # Video fingerprinting
    video_hash = Column(String(64), nullable=True)  # Perceptual hash
    scene_hashes = Column(JSON, nullable=True)  # List of scene hashes
    
    # Technical metadata
    duration = Column(Float, nullable=True)  # seconds
    bitrate = Column(Integer, nullable=True)
    sample_rate = Column(Integer, nullable=True)  # audio
    channels = Column(Integer, nullable=True)  # audio
    codec = Column(String(64), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    media_file = relationship("MediaFile", back_populates="fingerprint")


class MediaMetadata(Base):
    """Enriched metadata from external sources - RENAMED from Metadata"""
    __tablename__ = 'media_metadata'
    
    id = Column(Integer, primary_key=True)
    media_file_id = Column(Integer, ForeignKey('media_files.id'), unique=True)
    
    # Common metadata
    title = Column(String(512), nullable=True)
    artist = Column(String(512), nullable=True)  # or director for video
    album = Column(String(512), nullable=True)  # or series for video
    year = Column(Integer, nullable=True)
    genre = Column(String(256), nullable=True)
    
    # Audio specific (MusicBrainz)
    musicbrainz_id = Column(String(128), nullable=True)
    musicbrainz_artist_id = Column(String(128), nullable=True)
    musicbrainz_album_id = Column(String(128), nullable=True)
    track_number = Column(Integer, nullable=True)
    disc_number = Column(Integer, nullable=True)
    
    # Video specific (TMDB)
    tmdb_id = Column(Integer, nullable=True)
    imdb_id = Column(String(32), nullable=True)
    season = Column(Integer, nullable=True)
    episode = Column(Integer, nullable=True)
    
    # Additional metadata
    description = Column(Text, nullable=True)
    language = Column(String(8), nullable=True)
    country = Column(String(8), nullable=True)
    
    # Italian music detection
    is_italian = Column(Boolean, default=False)
    italian_confidence = Column(Float, default=0.0)
    
    # Artwork
    artwork_url = Column(String(1024), nullable=True)
    artwork_local_path = Column(String(1024), nullable=True)
    
    # Source and quality
    metadata_source = Column(String(64), nullable=True)  # musicbrainz, tmdb, manual
    metadata_quality = Column(Float, default=0.0)  # 0.0 to 1.0
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    media_file = relationship("MediaFile", back_populates="media_metadata")


class MLFeatures(Base):
    """Extracted features for machine learning"""
    __tablename__ = 'ml_features'
    
    id = Column(Integer, primary_key=True)
    media_file_id = Column(Integer, ForeignKey('media_files.id'), unique=True)
    
    # Audio features (from librosa)
    mfcc = Column(JSON, nullable=True)  # Mel-frequency cepstral coefficients
    spectral_centroid = Column(JSON, nullable=True)
    spectral_rolloff = Column(JSON, nullable=True)
    spectral_contrast = Column(JSON, nullable=True)
    zero_crossing_rate = Column(JSON, nullable=True)
    tempo = Column(Float, nullable=True)
    chroma = Column(JSON, nullable=True)
    
    # Feature summary (for quick ML)
    feature_vector = Column(JSON, nullable=True)  # Compressed feature vector
    
    # Italian music specific features
    italian_language_features = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    media_file = relationship("MediaFile", back_populates="ml_features")


class MLModel(Base):
    """Machine learning model versioning"""
    __tablename__ = 'ml_models'
    
    id = Column(Integer, primary_key=True)
    
    # Model information
    model_name = Column(String(128), nullable=False)
    model_version = Column(String(32), nullable=False)
    model_type = Column(String(64), nullable=False)  # classifier, regressor, etc.
    model_path = Column(String(512), nullable=False)  # file path
    
    # Performance metrics
    accuracy = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    
    # Training information
    training_samples = Column(Integer, default=0)
    features_used = Column(JSON, nullable=True)
    hyperparameters = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    trained_at = Column(DateTime, nullable=True)


class ReviewQueue(Base):
    """Manual review queue for low-confidence items"""
    __tablename__ = 'review_queue'
    
    id = Column(Integer, primary_key=True)
    media_file_id = Column(Integer, ForeignKey('media_files.id'), unique=True)
    
    # Review information
    review_status = Column(SQLEnum(ReviewStatus), default=ReviewStatus.PENDING)
    confidence_score = Column(Float, nullable=False)
    reason = Column(Text, nullable=True)  # Why review is needed
    
    # Suggested metadata (from automated processing)
    suggested_metadata = Column(JSON, nullable=True)
    
    # Manual corrections
    corrected_metadata = Column(JSON, nullable=True)
    reviewer_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    
    # Relationship
    media_file = relationship("MediaFile", back_populates="review")


class MLFeedback(Base):
    """User corrections for ML training"""
    __tablename__ = 'ml_feedback'
    
    id = Column(Integer, primary_key=True)
    media_file_id = Column(Integer, ForeignKey('media_files.id'))
    
    # Original prediction
    predicted_metadata = Column(JSON, nullable=False)
    predicted_confidence = Column(Float, nullable=False)
    
    # Correct metadata (from user)
    correct_metadata = Column(JSON, nullable=False)
    
    # Feedback type
    feedback_type = Column(String(64), nullable=False)  # correction, confirmation, rejection
    
    # ML training usage
    used_for_training = Column(Boolean, default=False)
    training_weight = Column(Float, default=1.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)


class ProcessingLog(Base):
    """Audit trail for all processing steps"""
    __tablename__ = 'processing_logs'
    
    id = Column(Integer, primary_key=True)
    media_file_id = Column(Integer, ForeignKey('media_files.id'), nullable=True)
    
    # Log information
    level = Column(String(16), nullable=False)  # DEBUG, INFO, WARNING, ERROR
    module = Column(String(64), nullable=False)  # ingest, fingerprint, metadata, etc.
    message = Column(Text, nullable=False)
    
    # Additional context
    context = Column(JSON, nullable=True)
    
    # Error information
    exception_type = Column(String(128), nullable=True)
    exception_message = Column(Text, nullable=True)
    stack_trace = Column(Text, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    media_file = relationship("MediaFile", back_populates="processing_logs")


class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self, db_path: str):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.Session = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        """Create all tables if they don't exist"""
        Base.metadata.create_all(self.engine)
        
    def get_session(self):
        """Get a new database session"""
        return self.Session()
    
    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        Base.metadata.drop_all(self.engine)


# Convenience function
def init_database(db_path: str) -> DatabaseManager:
    """
    Initialize database and create tables
    
    Args:
        db_path: Path to SQLite database file
        
    Returns:
        DatabaseManager instance
    """
    db_manager = DatabaseManager(db_path)
    db_manager.create_tables()
    return db_manager
