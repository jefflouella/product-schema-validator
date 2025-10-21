"""
Configuration settings for Schema Validator application.
"""

import os
from pathlib import Path


class Config:
    """Application configuration with sensible defaults."""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    RESULTS_DIR = DATA_DIR / "results"
    
    # Database
    DATABASE_PATH = DATA_DIR / "validator.db"
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Validation defaults
    DEFAULT_HEADLESS = True
    DEFAULT_TIMEOUT = 30000  # milliseconds
    DEFAULT_DELAY_MIN = 2  # seconds
    DEFAULT_DELAY_MAX = 5  # seconds
    DEFAULT_MAX_RETRIES = 1
    DEFAULT_CONCURRENT_LIMIT = 3
    
    # User agents for rotation
    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
    ]
    
    @classmethod
    def init_app(cls):
        """Initialize application directories."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.RESULTS_DIR.mkdir(exist_ok=True)
        
        # Create .gitkeep files to ensure directories exist in git
        (cls.DATA_DIR / '.gitkeep').touch()
        (cls.RESULTS_DIR / '.gitkeep').touch()

