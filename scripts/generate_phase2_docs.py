#!/usr/bin/env python3
"""Generate Phase 2 documentation"""

doc_content = """# Phase 2: Core Architecture Implementation

## Overview

Phase 2 implements the foundational components of the Media Organizer:
- Database schema with SQLAlchemy ORM
- Centralized logging system with loguru
- Configuration management with pydantic
- Base application structure with CLI

## Database Schema

### Main Tables

**media_files** - Main table tracking all media files
**fingerprints** - Audio/video fingerprint data  
**media_metadata** - Enriched metadata (renamed from Metadata to avoid SQLAlchemy conflict)
**ml_features** - Extracted features for ML
**ml_models** - Model versioning and performance
**review_queue** - Manual review queue
**ml_feedback** - User corrections for training
**processing_logs** - Complete audit trail

### Key Design Decisions

1. **MediaMetadata naming**: Renamed from "Metadata" to avoid SQLAlchemy reserved name conflict
2. **Enums for status**: Type-safe status tracking with Python enums
3. **JSON fields**: Flexible storage for features and metadata
4. **Relationships**: Properly configured SQLAlchemy relationships for data integrity

## Database Usage

### Initialize
```python
from utils import init_database
db_manager = init_database('./data/media_organizer.db')
Basic Operations
python
session = db_manager.get_session()
try:
    media_file = MediaFile(
        original_path="/path/to/file.mp3",
        filename="file.mp3",
        file_size=5242880,
        file_hash="abc123...",
        media_type=MediaType.AUDIO
    )
    session.add(media_file)
    session.commit()
finally:
    session.close()
Logging System
Features
3 separate log files (app.log, error.log, audit.log)

Automatic rotation at 10MB

Colorized console output

Thread-safe operation

Usage
python
from utils import init_logger, get_logger, audit_log

logger = init_logger(log_dir="./logs", log_level="INFO")
logger = get_logger()
logger.info("Processing...")
audit_log("File completed", file_id=123)
Configuration Management
Features
YAML-based configuration

Pydantic validation

Secrets management (separate file)

Type safety and range validation

Usage
python
from utils import load_config, get_config

config = load_config('config/config.yaml')
threshold = config.ml.confidence_threshold  # 0.75
boost = config.ml.italian_music_boost  # 1.2
Main Application
CLI Commands
bash
python main.py                    # Run with defaults
python main.py --config custom.yaml
python main.py --init-db          # Initialize DB only
python main.py --version
Application Flow
Parse CLI arguments

Load configuration

Initialize logger

Initialize database

Validate paths

Run processing loop (Phase 3)

Graceful shutdown

Testing
Run all Phase 2 tests:

bash
./scripts/test_phase2.sh
All tests should pass with ✓ marks.

Files Created
text
src/utils/
  ├── __init__.py
  ├── database.py
  ├── logger.py
  └── config.py

main.py
docs/03_phase2_implementation.md
scripts/test_phase2.sh
Known Issues
Issue: SQLAlchemy reserves "metadata" name
Solution: Renamed to MediaMetadata

Next Steps (Phase 3)
Ingest Module - File scanning and queueing

Fingerprinting Audio - Chromaprint + librosa

Fingerprinting Video - ffmpeg + imagehash

Metadata Enrichment - MusicBrainz + TMDB

Last Updated: 2026-01-07
Status: Complete ✅
All Tests: Passing ✅
"""

Write to file
with open('docs/03_phase2_implementation.md', 'w') as f:
f.write(doc_content)

print("✓ Documentation generated: docs/03_phase2_implementation.md")
