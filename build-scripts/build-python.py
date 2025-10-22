#!/usr/bin/env python3
"""
Build script to create Python executables for all platforms using PyInstaller.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, env=None):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def install_playwright_browsers():
    """Install Playwright browsers for the current platform."""
    print("Installing Playwright browsers...")
    run_command([sys.executable, "-m", "playwright", "install", "chromium"])
    run_command([sys.executable, "-m", "playwright", "install-deps"])

def build_for_platform(target_platform):
    """Build Python executable for a specific platform."""
    print(f"\nBuilding for {target_platform}...")
    
    # Set up environment variables for cross-platform building
    env = os.environ.copy()
    
    if target_platform == "win":
        env["PYINSTALLER_TARGET_OS"] = "windows"
    elif target_platform == "mac":
        env["PYINSTALLER_TARGET_OS"] = "darwin"
    elif target_platform == "linux":
        env["PYINSTALLER_TARGET_OS"] = "linux"
    
    # Build with PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--distpath", f"python-dist/{target_platform}",
        "schema_validator.spec"
    ]
    
    run_command(cmd, env=env)
    
    # Copy Playwright browsers to the dist directory
    playwright_browsers = Path.home() / ".cache" / "ms-playwright"
    if playwright_browsers.exists():
        dest_browsers = Path(f"python-dist/{target_platform}/playwright-browsers")
        dest_browsers.mkdir(parents=True, exist_ok=True)
        
        print(f"Copying Playwright browsers from {playwright_browsers} to {dest_browsers}")
        if target_platform == "win":
            shutil.copytree(playwright_browsers, dest_browsers, dirs_exist_ok=True)
        else:
            shutil.copytree(playwright_browsers, dest_browsers, dirs_exist_ok=True)
    
    print(f"Build completed for {target_platform}")

def main():
    """Main build function."""
    print("Schema Validator - Python Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("schema_validator").exists():
        print("Error: schema_validator directory not found. Run this script from the project root.")
        sys.exit(1)
    
    # Install PyInstaller if not already installed
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("Installing PyInstaller...")
        run_command([sys.executable, "-m", "pip", "install", "pyinstaller>=6.3.0"])
    
    # Install Playwright browsers
    install_playwright_browsers()
    
    # Build for current platform
    current_platform = platform.system().lower()
    if current_platform == "darwin":
        target_platform = "mac"
    elif current_platform == "windows":
        target_platform = "win"
    else:
        target_platform = "linux"
    
    build_for_platform(target_platform)
    
    print(f"\nBuild completed successfully!")
    print(f"Executable created at: python-dist/{target_platform}/schema-validator")
    if target_platform == "win":
        print(f"Executable created at: python-dist/{target_platform}/schema-validator.exe")

if __name__ == "__main__":
    main()
