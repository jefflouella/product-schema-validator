# Schema Validator - Web Interface

A comprehensive web-based tool for validating schema.org Product markup across multiple URLs with anti-bot bypass capabilities. Features a modern browser interface for managing URLs, running validations, and viewing results in real-time.

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

### 🚀 Web Interface
- **Modern Dashboard**: Intuitive browser-based control panel
- **Project Management**: Organize URLs by client or website
- **Real-time Progress**: Live updates via WebSockets during validation
- **Results Viewer**: Interactive results with filtering and sorting
- **Bulk Operations**: Add, edit, and delete multiple URLs at once

### 🔒 Anti-Bot Protection
- **Playwright Integration**: Browser automation with stealth mode
- **User Agent Rotation**: Multiple browser fingerprints
- **Rate Limiting**: Configurable delays to avoid detection
- **Cookie Handling**: Session management like real browsers

### 📊 Validation Features
- **Comprehensive Validation**: Full schema.org Product specification
- **Required Fields**: name, image, offers validation
- **Recommended Fields**: brand, SKU, ratings, reviews
- **Scoring System**: 0-100% quality score for each URL
- **Multiple Formats**: JSON-LD and microdata extraction

### 📈 Reporting
- **Export Options**: CSV, JSON, Excel formats
- **Interactive Reports**: Filter, sort, and search results
- **Detailed Analysis**: Error and warning breakdowns
- **Historical Data**: Track validation runs over time

## Installation

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/schema-validator.git
   cd schema-validator
   ```

2. **Install the package:**
   ```bash
   pip install -e .
   ```

3. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

4. **Start the web server:**
   ```bash
   schema-validator
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5000`

That's it! You're ready to start validating schemas.

### Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install package
pip install -e .
playwright install chromium
```

## Usage

### Starting the Server

```bash
schema-validator
```

The server will start on `http://localhost:5000` by default.

### Configuration

Set environment variables to customize:

```bash
export HOST=0.0.0.0          # Listen on all interfaces
export PORT=8080             # Custom port
export DEBUG=true            # Enable debug mode
```

Or use a `.env` file in the project root.

### Using the Web Interface

#### 1. Create a Project

- Navigate to **Projects** in the sidebar
- Click **New Project**
- Enter project name and description
- Projects help organize URLs by client or website

#### 2. Add URLs

- Navigate to **URLs** in the sidebar
- Click **Add URL** for single URL
- Or click **Bulk Add** to import multiple URLs (one per line)
- Select the project and set status (active/inactive)

#### 3. Start Validation

- Go to **Dashboard**
- Click **Start Validation**
- Select project and configure settings:
  - Headless mode (run browser in background)
  - Concurrent limit (parallel validations)
  - Timeout and delay settings
- Click **Start Validation**

#### 4. Monitor Progress

- Real-time progress bar shows current status
- See which URL is being processed
- Pause, resume, or stop validation at any time

#### 5. View Results

- Navigate to **Results** in the sidebar
- Select a validation run from the list
- View summary statistics
- Filter results by status
- Click **Details** to see full validation report
- Export results as CSV or JSON

### Settings

Configure default validation parameters in **Settings**:

- **Browser Configuration**: Headless mode on/off
- **Timeout Settings**: Page load timeout
- **Rate Limiting**: Delay between requests
- **Concurrency**: Number of parallel browsers
- **Retry Settings**: Maximum retry attempts

#### Recommended Presets

**Conservative (Slow but Safe)**
- Concurrent Limit: 1
- Delay: 5-10 seconds
- Timeout: 45 seconds
- Best for: Sites with strict anti-bot protection

**Balanced (Recommended)**
- Concurrent Limit: 3
- Delay: 2-5 seconds
- Timeout: 30 seconds
- Best for: Most websites

**Aggressive (Fast but Risky)**
- Concurrent Limit: 5-10
- Delay: 1-2 seconds
- Timeout: 20 seconds
- Best for: Your own websites or testing

## Validation Levels

### Required Fields (Critical)
- `name`: Product name
- `image`: Product image(s)
- `offers`: Pricing and availability information
  - `price`: Product price
  - `priceCurrency`: Currency code (e.g., USD)
  - `availability`: Stock status

### Recommended Fields (SEO)
- `description`: Product description
- `brand`: Product brand
- `sku`: Stock keeping unit
- `gtin`: Global Trade Item Number
- `aggregateRating`: Average customer rating
- `review`: Customer reviews

## Data Storage

All data is stored locally in SQLite database:

- **Location**: `data/validator.db`
- **Projects**: Organization structure
- **URLs**: All tracked URLs
- **Validation Runs**: Historical validation sessions
- **Results**: Individual URL validation results

### Database Schema

```
projects
  ├── id
  ├── name
  ├── description
  ├── created_date
  └── settings_json

urls
  ├── id
  ├── project_id (FK)
  ├── url
  ├── added_date
  ├── status
  ├── tags
  └── notes

validation_runs
  ├── id
  ├── project_id (FK)
  ├── start_time
  ├── end_time
  ├── status
  ├── total_urls
  ├── processed_urls
  └── settings_snapshot

validation_results
  ├── id
  ├── run_id (FK)
  ├── url_id (FK)
  ├── status
  ├── schema_data
  ├── errors
  ├── score
  ├── validated_at
  └── response_time
```

## API Endpoints

The web interface uses a RESTful API:

### Projects
- `GET /api/projects` - List all projects
- `POST /api/projects` - Create project
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project

### URLs
- `GET /api/urls` - List URLs (with filters)
- `POST /api/urls` - Add single URL
- `POST /api/urls/bulk` - Add multiple URLs
- `PUT /api/urls/<id>` - Update URL
- `DELETE /api/urls/<id>` - Delete URL
- `POST /api/urls/bulk-delete` - Delete multiple URLs

### Validation
- `POST /api/validation/start` - Start validation
- `GET /api/validation/runs` - List validation runs
- `GET /api/validation/runs/<id>` - Get specific run
- `GET /api/validation/results/<id>` - Get results for run
- `GET /api/validation/results/<id>/download/<format>` - Download results

### Settings
- `GET /api/settings` - Get current settings

## WebSocket Events

Real-time updates via Socket.IO:

**Client → Server**
- `pause_validation` - Pause current validation
- `resume_validation` - Resume paused validation
- `stop_validation` - Stop current validation
- `get_validation_state` - Get current state

**Server → Client**
- `validation_progress` - Progress update with current URL
- `validation_complete` - Validation finished
- `validation_error` - Error occurred
- `validation_paused` - Validation paused
- `validation_resumed` - Validation resumed
- `validation_stopped` - Validation stopped

## Troubleshooting

### Browser Installation Issues

If Playwright browsers fail to install:

```bash
# Reinstall Playwright browsers
playwright install --force chromium
```

### Port Already in Use

Change the port:

```bash
PORT=8080 schema-validator
```

### Database Locked

If you get "database is locked" errors:

1. Ensure only one instance is running
2. Delete `data/validator.db-journal` if it exists
3. Restart the application

### Import Errors

If you get import errors:

```bash
# Reinstall in development mode
pip uninstall schema-validator-web
pip install -e .
```

## Development

### Project Structure

```
schema-validator/
├── schema_validator/
│   ├── __init__.py
│   ├── __main__.py              # Entry point
│   ├── config.py                # Configuration
│   ├── models.py                # Data models
│   ├── core/
│   │   ├── validator.py         # Validation engine
│   │   ├── report.py            # Report generation
│   │   └── schemas.py           # Schema definitions
│   └── web/
│       ├── app.py               # Flask application
│       ├── routes.py            # API routes
│       ├── database.py          # Database operations
│       ├── socketio_events.py   # WebSocket handlers
│       ├── templates/           # HTML templates
│       └── static/              # CSS, JavaScript
├── data/                        # SQLite database & results
├── setup.py                     # Package installation
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

### Running in Development Mode

```bash
# Enable debug mode
DEBUG=true schema-validator
```

### Technology Stack

- **Backend**: Flask 3.0+
- **Database**: SQLite3
- **Real-time**: Flask-SocketIO
- **Browser**: Playwright (Chromium)
- **Frontend**: Bootstrap 5, Alpine.js, HTMX
- **Validation**: jsonschema

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues, questions, or contributions:

- **Issues**: https://github.com/yourusername/schema-validator/issues
- **Documentation**: https://github.com/yourusername/schema-validator
- **Email**: support@example.com

## Changelog

### Version 2.0.0 (Current)
- ✨ Complete web interface with dashboard
- 🗂️ Project-based URL organization
- 📊 Real-time validation progress
- 💾 SQLite database for persistent storage
- 🔄 Pause/resume/stop validation controls
- 📤 Export results in CSV/JSON formats
- 🎨 Modern responsive UI with Bootstrap 5

### Version 1.0.0
- ✅ CLI-based schema validation
- ✅ Playwright browser automation
- ✅ Anti-bot bypass capabilities
- ✅ HTML report generation

## Acknowledgments

- Built with [Playwright](https://playwright.dev/) for browser automation
- Powered by [Flask](https://flask.palletsprojects.com/) web framework
- UI components from [Bootstrap](https://getbootstrap.com/)
- Real-time updates via [Socket.IO](https://socket.io/)
