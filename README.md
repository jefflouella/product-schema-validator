# Product Schema Validator

A comprehensive product schema validation tool with anti-bot bypass capabilities and real-time progress tracking. This tool validates schema.org Product markup across multiple URLs with pause/resume functionality and detailed reporting.

**Available as both a web application and a desktop app for macOS, Windows, and Linux.**

*Built by [Mookee](https://mookee.com)*

## Features

- **Web Interface**: Modern Flask-based web application with real-time updates
- **Desktop App**: Cross-platform Electron app with bundled Python runtime
- **Anti-Bot Bypass**: Uses Playwright with advanced browser automation to bypass bot detection
- **Batch Processing**: Validate multiple URLs simultaneously with progress tracking
- **Pause/Resume**: Control validation processes with pause and resume functionality
- **Real-time Updates**: WebSocket-based live progress updates
- **Comprehensive Reporting**: Detailed validation reports in HTML, Excel, and CSV formats
- **Schema Validation**: Validates against schema.org Product schema with required and recommended fields
- **State Management**: Persistent validation state with database storage
- **Auto-Updates**: Desktop app includes user-prompted update functionality

## How to Run

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Node.js** (for Playwright browser automation)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd schema
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -e .
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

### Running the Application

**Start the web server**:
```bash
python -m schema_validator
```

The application will start on `http://localhost:5000` by default.

**Alternative startup methods**:
```bash
# Using Flask directly
flask run

# With custom port
python -m schema_validator --port 5001
```

## Desktop App

The Schema Validator is also available as a desktop application for macOS, Windows, and Linux. The desktop app bundles Python and all dependencies, so users don't need to install Python separately.

### Building the Desktop App

**Prerequisites for building:**
- Python 3.8+ 
- Node.js 16+
- Platform-specific build tools (Xcode for macOS, Visual Studio for Windows)

**Quick start:**
```bash
# Install all dependencies
npm run install:all

# Build for current platform
npm run build:current

# Build for all platforms (requires platform-specific setup)
npm run build:all
```

**Development mode:**
```bash
# Run in development mode (uses local Python)
npm run electron:dev
```

**Available build commands:**
```bash
# Build Python executables only
npm run build:python

# Build Electron app only
npm run electron:build

# Build for specific platform
npm run electron:build:mac
npm run electron:build:win
npm run electron:build:linux

# Clean build artifacts
npm run clean
```

### Desktop App Features

- **No Python Installation Required**: Bundles Python runtime and all dependencies
- **Cross-Platform**: Works on macOS, Windows, and Linux
- **Auto-Updates**: User-prompted updates with release notes
- **Native Integration**: Uses platform-specific user data directories
- **Offline Capable**: Runs completely offline after installation

### Distribution

The desktop app creates platform-specific installers:
- **macOS**: `.dmg` file (signed and notarized)
- **Windows**: `.exe` installer with NSIS
- **Linux**: `.AppImage` for universal compatibility

**App sizes:**
- macOS: ~400-500 MB
- Windows: ~350-450 MB  
- Linux: ~400-500 MB

## How to Test

### Running Tests

**Run all tests**:
```bash
pytest
```

**Run specific test files**:
```bash
pytest tests/test_validator.py
pytest tests/test_web.py
```

**Run with coverage**:
```bash
pytest --cov=schema_validator
```

### Manual Testing

1. **Start the application** (see How to Run section)
2. **Open your browser** and navigate to `http://localhost:5000`
3. **Test the web interface**:
   - Add URLs to validate
   - Start validation process
   - Test pause/resume functionality
   - Download validation reports

### Testing Validation

**Test with sample URLs**:
```bash
# Test single URL validation
python -c "
from schema_validator.core.validator import ProductValidator
validator = ProductValidator()
result = validator.validate_url('https://example.com/product')
print(result)
"
```

## Project Structure

```
schema/
├── schema_validator/           # Main package
│   ├── core/                  # Core validation logic
│   │   ├── validator.py       # Main validator class
│   │   ├── schemas.py         # Schema definitions
│   │   └── report.py          # Report generation
│   ├── web/                   # Web interface
│   │   ├── app.py            # Flask application
│   │   ├── routes.py         # URL routes
│   │   ├── database.py       # Database operations
│   │   └── templates/        # HTML templates
│   └── config.py             # Configuration
├── requirements.txt           # Python dependencies
├── package.json              # Node.js dependencies
└── setup.py                  # Package setup
```

## Configuration

The application can be configured through environment variables:

- `HOST`: Server host (default: localhost)
- `PORT`: Server port (default: 5000)
- `DEBUG`: Debug mode (default: False)
- `DATABASE_URL`: Database connection string

## Dependencies

### Python Dependencies
- Flask 3.0+ (Web framework)
- Flask-SocketIO 5.3+ (WebSocket support)
- Playwright 1.40+ (Browser automation)
- jsonschema 4.20+ (Schema validation)
- BeautifulSoup4 4.12+ (HTML parsing)
- openpyxl 3.1+ (Excel export)

### Node.js Dependencies
- Playwright 1.40+ (Browser automation)

## Troubleshooting

### Common Issues

1. **Playwright browser not found**:
   ```bash
   playwright install chromium
   ```

2. **Port already in use**:
   ```bash
   python -m schema_validator --port 5001
   ```

3. **Database connection issues**:
   - Check if the database file exists
   - Ensure proper permissions

### Debug Mode

Enable debug mode for detailed logging:
```bash
export DEBUG=True
python -m schema_validator
```

## Troubleshooting

### Desktop App Issues

**App won't start:**
- Check that all dependencies are installed: `npm run install:all`
- Try running in development mode: `npm run electron:dev`
- Check console output for Python server errors

**Python server fails to start:**
- Ensure Python executable is bundled correctly
- Check that Playwright browsers are included
- Verify port availability (app will find alternative ports automatically)

**Build failures:**
- Clean build artifacts: `npm run clean`
- Reinstall dependencies: `npm run install:all`
- Check platform-specific build requirements

**Update issues:**
- Updates are user-prompted, not automatic
- Check GitHub releases for new versions
- Manual download available if auto-update fails

### Web App Issues

**Port already in use:**
```bash
python -m schema_validator --port 5001
```

**Playwright browser not found:**
```bash
playwright install chromium
```

**Database connection issues:**
- Check if the database file exists
- Ensure proper permissions
- Try deleting `data/validator.db` to reset

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.