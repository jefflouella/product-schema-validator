# Playwright Setup Instructions

## The Issue
Python 3.13 has compatibility issues with greenlet (required by Playwright). This is a known issue with the latest Python version.

## Solutions

### Option 1: Use Python 3.11 or 3.12 (Recommended)

```bash
# Install Python 3.11 or 3.12 using Homebrew
brew install python@3.11

# Create new virtual environment with Python 3.11
python3.11 -m venv venv_playwright
source venv_playwright/bin/activate

# Install dependencies
pip install playwright jsonschema validators jinja2 beautifulsoup4 requests tqdm

# Install Playwright browsers
playwright install chromium

# Run the validator
python3 schema_validator_playwright.py
```

### Option 2: Use Docker (Alternative)

```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install chromium

COPY . .
CMD ["python", "schema_validator_playwright.py"]
EOF

# Build and run
docker build -t schema-validator .
docker run -v $(pwd)/results:/app/results schema-validator
```

### Option 3: Use the Enhanced Requests Version

The current setup already includes an enhanced requests-based validator that works well for most sites. For Cloudflare-protected sites, you may need to:

1. Use residential proxies
2. Implement more sophisticated user-agent rotation
3. Add session management
4. Use different request patterns

## Current Status

✅ **Working Solutions Available:**
- Enhanced requests-based validator (bypasses basic protection)
- Comprehensive schema validation
- Interactive HTML reports
- Rate limiting and stealth features

⚠️ **For Cloudflare Protection:**
- Requires Playwright with Python 3.11/3.12
- Or advanced proxy solutions
- Or manual browser automation

## Quick Test

To test if Playwright works with Python 3.11:

```bash
# Install Python 3.11
brew install python@3.11

# Create test environment
python3.11 -m venv test_env
source test_env/bin/activate

# Install Playwright
pip install playwright
playwright install chromium

# Test
python3.11 -c "from playwright.async_api import async_playwright; print('Playwright works!')"
```

## Recommendation

For immediate use with your 200 URLs:
1. Use the current enhanced requests-based validator
2. Test with a few URLs first
3. If Cloudflare blocks all requests, set up Python 3.11 environment for Playwright
4. The tool is production-ready and will work for most sites
