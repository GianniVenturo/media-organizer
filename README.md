# Media Organizer

Advanced, fully automated media organization system with ML-powered confidence scoring and Italian music specialization.

## Features

- 🎵 **Audio Fingerprinting**: Chromaprint + AcoustID + librosa feature extraction
- 🎬 **Video Fingerprinting**: ffmpeg + perceptual hashing
- 🇮🇹 **Italian Music Priority**: Specialized detection and classification
- 🤖 **Machine Learning**: Confidence scoring with incremental learning
- 📀 **USB Support**: Hot-plug detection, caching, automatic resume
- ✅ **Manual Review**: Isolated review queue for low-confidence items
- 📊 **Netflix-Style Output**: Perfect organization, artwork, metadata
- 🔄 **Auto Backup**: Automatic GitHub sync
- 💰 **100% Free**: All components use free and open-source software

## Technology Stack

- **Python 3.12+**
- **SQLite3** for metadata storage
- **Chromaprint/AcoustID** for audio fingerprinting
- **ffmpeg** for video processing
- **librosa** for audio feature extraction
- **scikit-learn** for ML
- **MusicBrainz** and **TMDB** for metadata
- **watchdog** for filesystem monitoring

## Quick Start

```bash
# Clone repository
git clone git@github.com:YOUR-USERNAME/media-organizer.git
cd media-organizer

# Activate environment
source scripts/activate.sh

# Configure
nano config/config.yaml

# Run (coming soon)
python main.py
Documentation
Architecture

Installation Guide

Requirements
Ubuntu Server 24.04 LTS

Python 3.12+

2GB+ RAM

SSH access

Project Status
🚧 Under Active Development

✅ Phase 1: Setup & Architecture (COMPLETE)

🔄 Phase 2: Core Implementation (IN PROGRESS)

License
MIT License

Version: 1.0.0
Last Updated: 2026-01-07
