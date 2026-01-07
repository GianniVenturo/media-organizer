#!/usr/bin/env python3
"""
Media Organizer - Main Application Entry Point

Advanced media organization system with ML-powered confidence scoring
and Italian music specialization.
"""
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils import init_logger, get_logger, load_config, get_config, init_database


class MediaOrganizer:
    """Main application orchestrator"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize Media Organizer
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = load_config(config_path)
        
        # Initialize logger
        self.logger = init_logger(
            log_dir=self.config.paths.log_folder,
            log_level=self.config.app.log_level
        )
        
        self.logger.info(f"Starting {self.config.app.name} v{self.config.app.version}")
        
        # Initialize database
        self.db_manager = init_database(self.config.paths.database)
        self.logger.info(f"Database initialized: {self.config.paths.database}")
        
        # Validate configuration
        self._validate_paths()
        
    def _validate_paths(self):
        """Validate that required paths exist"""
        input_path = Path(self.config.paths.input_folder)
        output_path = Path(self.config.paths.output_folder)
        
        if not input_path.exists():
            self.logger.warning(f"Input folder does not exist: {input_path}")
            self.logger.info("Creating input folder...")
            input_path.mkdir(parents=True, exist_ok=True)
        
        if not output_path.exists():
            self.logger.warning(f"Output folder does not exist: {output_path}")
            self.logger.info("Creating output folder...")
            output_path.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Input folder: {input_path}")
        self.logger.info(f"Output folder: {output_path}")
    
    def run(self):
        """Main application loop"""
        self.logger.info("Media Organizer is running...")
        self.logger.info("Press Ctrl+C to stop")
        
        try:
            # TODO: Implement main processing loop
            # This will be implemented in Phase 3
            self.logger.info("Processing pipeline not yet implemented")
            self.logger.info("Ready for Phase 3 implementation")
            
        except KeyboardInterrupt:
            self.logger.info("Shutdown requested by user")
        except Exception as e:
            self.logger.exception(f"Fatal error: {e}")
            raise
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Cleanup and shutdown"""
        self.logger.info("Shutting down Media Organizer...")
        # TODO: Cleanup resources (close DB connections, etc.)
        self.logger.info("Shutdown complete")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Media Organizer - Advanced media management with ML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Run with default config
  %(prog)s --config custom.yaml     # Run with custom config
  %(prog)s --init-db                # Initialize database only
  %(prog)s --version                # Show version
        """
    )
    
    parser.add_argument(
        '--config',
        '-c',
        default='config/config.yaml',
        help='Path to configuration file (default: config/config.yaml)'
    )
    
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize database and exit'
    )
    
    parser.add_argument(
        '--version',
        '-v',
        action='version',
        version='Media Organizer v1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        if args.init_db:
            # Just initialize database and exit
            print("Initializing database...")
            config = load_config(args.config)
            init_database(config.paths.database)
            print(f"Database initialized: {config.paths.database}")
            return 0
        
        # Run main application
        app = MediaOrganizer(config_path=args.config)
        app.run()
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
