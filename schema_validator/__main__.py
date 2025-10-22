"""
Main entry point for Schema Validator web application.
Run with: python -m schema_validator or schema-validator command.
"""

import sys
import argparse


def main():
    """Start the web server."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Schema Validator Web Server')
    parser.add_argument('--port', type=int, help='Port to run the server on')
    parser.add_argument('--host', type=str, help='Host to bind the server to')
    args = parser.parse_args()
    
    try:
        from schema_validator.web.app import create_app, socketio
        from schema_validator.config import Config
        
        # Override config with command line arguments
        if args.port:
            Config.PORT = args.port
        if args.host:
            Config.HOST = args.host
        
        print("=" * 60)
        print("Product Schema Validator - Web Interface")
        print("=" * 60)
        print(f"Starting server on http://{Config.HOST}:{Config.PORT}")
        print("Press CTRL+C to stop")
        print("=" * 60)
        
        app = create_app()
        socketio.run(app, host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, allow_unsafe_werkzeug=True)
        
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting server: {e}")
        print("\nMake sure you have installed all dependencies:")
        print("  pip install -e .")
        print("  playwright install chromium")
        sys.exit(1)


if __name__ == '__main__':
    main()

