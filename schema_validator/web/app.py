"""
Flask application for Schema Validator web interface.
"""

import os
from flask import Flask, render_template
from flask_socketio import SocketIO

from ..config import Config
from .database import Database

# Initialize SocketIO
socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')

# Global database instance
db = None


def create_app(config_class=Config):
    """Create and configure Flask application."""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize directories
    config_class.init_app()
    
    # Initialize database
    global db
    db = Database()
    
    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500
    
    return app


def get_db() -> Database:
    """Get database instance."""
    return db

