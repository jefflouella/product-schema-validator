#!/bin/bash

# Schema Validator - Master Build Script
# Builds Python executables and Electron apps for all platforms

set -e  # Exit on any error

echo "Schema Validator - Master Build Script"
echo "======================================"

# Check if we're in the right directory
if [ ! -d "schema_validator" ]; then
    echo "Error: schema_validator directory not found. Run this script from the project root."
    exit 1
fi

# Create necessary directories
mkdir -p python-dist
mkdir -p dist
mkdir -p build-resources

# Function to build Python for a specific platform
build_python() {
    local platform=$1
    echo "Building Python executable for $platform..."
    
    # Install dependencies
    pip install -r requirements.txt
    pip install pyinstaller>=6.3.0
    
    # Install Playwright browsers
    python -m playwright install chromium
    python -m playwright install-deps
    
    # Build with PyInstaller
    python -m PyInstaller --clean --onefile --windowed \
        --name schema-validator \
        --distpath python-dist/$platform \
        schema_validator.spec
    
    echo "Python build completed for $platform"
}

# Function to build Electron app
build_electron() {
    local platform=$1
    echo "Building Electron app for $platform..."
    
    cd electron
    
    # Install Electron dependencies
    npm install
    
    # Build Electron app
    if [ "$platform" = "all" ]; then
        npm run build
    else
        npm run build:$platform
    fi
    
    cd ..
    echo "Electron build completed for $platform"
}

# Parse command line arguments
PLATFORM=${1:-"current"}

case $PLATFORM in
    "current")
        # Build for current platform only
        CURRENT_OS=$(uname -s | tr '[:upper:]' '[:lower:]')
        if [[ "$CURRENT_OS" == "darwin" ]]; then
            PLATFORM="mac"
        elif [[ "$CURRENT_OS" == "linux" ]]; then
            PLATFORM="linux"
        else
            echo "Unsupported platform: $CURRENT_OS"
            exit 1
        fi
        
        echo "Building for current platform: $PLATFORM"
        build_python $PLATFORM
        build_electron $PLATFORM
        ;;
    
    "all")
        echo "Building for all platforms..."
        echo "Note: This requires platform-specific build environments"
        
        # Build Python for all platforms
        for platform in mac win linux; do
            build_python $platform
        done
        
        # Build Electron for all platforms
        build_electron all
        ;;
    
    "mac"|"win"|"linux")
        echo "Building for $PLATFORM..."
        build_python $PLATFORM
        build_electron $PLATFORM
        ;;
    
    "python-only")
        echo "Building Python executables only..."
        CURRENT_OS=$(uname -s | tr '[:upper:]' '[:lower:]')
        if [[ "$CURRENT_OS" == "darwin" ]]; then
            PLATFORM="mac"
        elif [[ "$CURRENT_OS" == "linux" ]]; then
            PLATFORM="linux"
        else
            echo "Unsupported platform: $CURRENT_OS"
            exit 1
        fi
        build_python $PLATFORM
        ;;
    
    "electron-only")
        echo "Building Electron app only..."
        CURRENT_OS=$(uname -s | tr '[:upper:]' '[:lower:]')
        if [[ "$CURRENT_OS" == "darwin" ]]; then
            PLATFORM="mac"
        elif [[ "$CURRENT_OS" == "linux" ]]; then
            PLATFORM="linux"
        else
            echo "Unsupported platform: $CURRENT_OS"
            exit 1
        fi
        build_electron $PLATFORM
        ;;
    
    *)
        echo "Usage: $0 [current|all|mac|win|linux|python-only|electron-only]"
        echo ""
        echo "Options:"
        echo "  current      - Build for current platform (default)"
        echo "  all          - Build for all platforms"
        echo "  mac          - Build for macOS"
        echo "  win          - Build for Windows"
        echo "  linux        - Build for Linux"
        echo "  python-only  - Build Python executables only"
        echo "  electron-only - Build Electron app only"
        exit 1
        ;;
esac

echo ""
echo "Build completed successfully!"
echo "Output directory: dist/"
echo ""
echo "Generated files:"
ls -la dist/ 2>/dev/null || echo "No dist directory found"
