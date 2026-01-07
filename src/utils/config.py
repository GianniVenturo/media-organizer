"""
Configuration module - Pydantic-based configuration management
"""
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import yaml


class AppConfig(BaseModel):
    """Application settings"""
    name: str = "Media Organizer"
    version: str = "1.0.0"
    log_level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")


class PathsConfig(BaseModel):
    """File paths configuration"""
    input_folder: str
    output_folder: str
    cache_folder: str = "./data/cache"
    models_folder: str = "./data/models"
    queue_folder: str = "./data/queue"
    log_folder: str = "./logs"
    database: str = "./data/media_organizer.db"
    
    @field_validator('input_folder', 'output_folder')
    @classmethod
    def validate_paths(cls, v):
        """Ensure critical paths are set"""
        if not v or v == "/path/to/input" or v == "/path/to/output":
            raise ValueError(f"Path must be configured: {v}")
        return v


class AudioFingerprintConfig(BaseModel):
    """Audio fingerprinting configuration"""
    enabled: bool = True
    use_chromaprint: bool = True
    use_acoustid: bool = True
    extract_features: bool = True


class VideoFingerprintConfig(BaseModel):
    """Video fingerprinting configuration"""
    enabled: bool = True
    extract_scenes: bool = True
    thumbnail_count: int = Field(default=3, ge=1, le=10)


class FingerprintingConfig(BaseModel):
    """Fingerprinting configuration"""
    audio: AudioFingerprintConfig = AudioFingerprintConfig()
    video: VideoFingerprintConfig = VideoFingerprintConfig()


class MusicBrainzConfig(BaseModel):
    """MusicBrainz API configuration"""
    enabled: bool = True
    rate_limit: float = Field(default=1.0, ge=0.5, le=5.0)  # seconds between requests


class TMDBConfig(BaseModel):
    """TMDB API configuration"""
    enabled: bool = True
    api_key: str = ""


class MetadataConfig(BaseModel):
    """Metadata enrichment configuration"""
    musicbrainz: MusicBrainzConfig = MusicBrainzConfig()
    tmdb: TMDBConfig = TMDBConfig()


class MLConfig(BaseModel):
    """Machine learning configuration"""
    enabled: bool = True
    confidence_threshold: float = Field(default=0.75, ge=0.0, le=1.0)
    retrain_interval: int = Field(default=100, ge=10)
    italian_music_boost: float = Field(default=1.2, ge=1.0, le=2.0)


class ReviewConfig(BaseModel):
    """Review system configuration"""
    enabled: bool = True
    confidence_threshold: float = Field(default=0.75, ge=0.0, le=1.0)
    auto_approve_above: float = Field(default=0.95, ge=0.0, le=1.0)


class USBConfig(BaseModel):
    """USB management configuration"""
    enabled: bool = True
    auto_detect: bool = True
    cache_enabled: bool = True
    resume_on_reconnect: bool = True


class BackupConfig(BaseModel):
    """Backup configuration"""
    auto_commit: bool = True
    commit_interval: int = Field(default=10, ge=1)
    auto_push: bool = True
    push_interval: int = Field(default=50, ge=1)


class Config(BaseModel):
    """Main configuration model"""
    app: AppConfig = AppConfig()
    paths: PathsConfig
    fingerprinting: FingerprintingConfig = FingerprintingConfig()
    metadata: MetadataConfig = MetadataConfig()
    ml: MLConfig = MLConfig()
    review: ReviewConfig = ReviewConfig()
    usb: USBConfig = USBConfig()
    backup: BackupConfig = BackupConfig()


class ConfigManager:
    """Configuration file manager"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize configuration manager
        
        Args:
            config_path: Path to main configuration file
        """
        self.config_path = Path(config_path)
        self.secrets_path = Path("config/secrets.yaml")
        self.config: Optional[Config] = None
        
    def load(self) -> Config:
        """
        Load configuration from file
        
        Returns:
            Parsed configuration object
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If configuration is invalid
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        # Load main config
        with open(self.config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        
        # Load secrets if available
        if self.secrets_path.exists():
            with open(self.secrets_path, 'r') as f:
                secrets = yaml.safe_load(f) or {}
            
            # Merge TMDB API key from secrets
            if 'tmdb_api_key' in secrets and secrets['tmdb_api_key']:
                if 'metadata' not in config_dict:
                    config_dict['metadata'] = {}
                if 'tmdb' not in config_dict['metadata']:
                    config_dict['metadata']['tmdb'] = {}
                config_dict['metadata']['tmdb']['api_key'] = secrets['tmdb_api_key']
        
        # Parse and validate
        self.config = Config(**config_dict)
        
        # Create required directories
        self._create_directories()
        
        return self.config
    
    def _create_directories(self):
        """Create all required directories"""
        if self.config is None:
            return
        
        dirs = [
            self.config.paths.cache_folder,
            self.config.paths.models_folder,
            self.config.paths.queue_folder,
            self.config.paths.log_folder
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def get(self) -> Config:
        """
        Get loaded configuration
        
        Returns:
            Configuration object
            
        Raises:
            RuntimeError: If configuration not loaded
        """
        if self.config is None:
            raise RuntimeError("Configuration not loaded. Call load() first.")
        return self.config


# Global configuration instance
_config_manager: Optional[ConfigManager] = None


def load_config(config_path: str = "config/config.yaml") -> Config:
    """
    Load global configuration
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Parsed configuration object
    """
    global _config_manager
    _config_manager = ConfigManager(config_path)
    return _config_manager.load()


def get_config() -> Config:
    """
    Get global configuration
    
    Returns:
        Configuration object
        
    Raises:
        RuntimeError: If configuration not loaded
    """
    if _config_manager is None:
        raise RuntimeError("Configuration not loaded. Call load_config() first.")
    return _config_manager.get()
