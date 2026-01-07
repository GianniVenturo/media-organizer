#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Testing Phase 2 Components ===${NC}"
echo ""

# Activate venv
if [ -z "$VIRTUAL_ENV" ]; then
    source venv/bin/activate
fi

# Test 1: Database module
echo -e "${BLUE}Test 1: Database Module${NC}"
python << 'PYEOF'
import sys
sys.path.insert(0, 'src')

try:
    from utils.database import init_database, MediaFile, ProcessingStatus
    
    # Initialize test database
    db = init_database('./data/test.db')
    print("✓ Database module imported")
    print("✓ Database initialized")
    print(f"✓ Tables created: MediaFile, Fingerprint, Metadata, MLFeatures, etc.")
    
    # Test creating a session
    session = db.get_session()
    print("✓ Database session created")
    session.close()
    
except Exception as e:
    print(f"✗ Database test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database module OK${NC}\n"
else
    echo -e "${RED}✗ Database module FAILED${NC}\n"
    exit 1
fi

# Test 2: Logger module
echo -e "${BLUE}Test 2: Logger Module${NC}"
python << 'PYEOF'
import sys
sys.path.insert(0, 'src')

try:
    from utils.logger import init_logger, get_logger, audit_log
    
    # Initialize logger
    logger = init_logger(log_dir="./logs/test", log_level="DEBUG")
    print("✓ Logger module imported")
    print("✓ Logger initialized")
    
    # Test logging
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    print("✓ Logging works")
    
    # Test audit log
    audit_log("Test audit message", file_id=123)
    print("✓ Audit logging works")
    
except Exception as e:
    print(f"✗ Logger test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Logger module OK${NC}\n"
else
    echo -e "${RED}✗ Logger module FAILED${NC}\n"
    exit 1
fi

# Test 3: Configuration module
echo -e "${BLUE}Test 3: Configuration Module${NC}"
python << 'PYEOF'
import sys
sys.path.insert(0, 'src')

try:
    from utils.config import load_config, get_config
    
    print("✓ Config module imported")
    
    # Load configuration
    config = load_config('config/config.yaml')
    print("✓ Configuration loaded")
    print(f"✓ App name: {config.app.name}")
    print(f"✓ App version: {config.app.version}")
    print(f"✓ Log level: {config.app.log_level}")
    print(f"✓ ML confidence threshold: {config.ml.confidence_threshold}")
    print(f"✓ Italian music boost: {config.ml.italian_music_boost}")
    
    # Test get_config
    config2 = get_config()
    assert config2.app.name == config.app.name
    print("✓ get_config() works")
    
except Exception as e:
    print(f"✗ Config test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Configuration module OK${NC}\n"
else
    echo -e "${RED}✗ Configuration module FAILED${NC}\n"
    exit 1
fi

# Test 4: Main application
echo -e "${BLUE}Test 4: Main Application${NC}"
python main.py --version
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Main application OK${NC}\n"
else
    echo -e "${RED}✗ Main application FAILED${NC}\n"
    exit 1
fi

# Test 5: Database initialization via CLI
echo -e "${BLUE}Test 5: Database Initialization via CLI${NC}"
python main.py --init-db
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database initialization via CLI OK${NC}\n"
else
    echo -e "${RED}✗ Database initialization via CLI FAILED${NC}\n"
    exit 1
fi

# Cleanup test files
rm -f ./data/test.db
rm -rf ./logs/test

echo -e "${GREEN}=== All Phase 2 Tests Passed! ===${NC}"
