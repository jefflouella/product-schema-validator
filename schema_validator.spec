# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files

# Get the current directory
current_dir = Path.cwd()
schema_validator_dir = current_dir / 'schema_validator'

# Define the main script
main_script = schema_validator_dir / '__main__.py'

# Collect all data files
datas = []

# Add templates
templates_dir = schema_validator_dir / 'web' / 'templates'
if templates_dir.exists():
    datas.append((str(templates_dir), 'schema_validator/web/templates'))

# Add static files
static_dir = schema_validator_dir / 'web' / 'static'
if static_dir.exists():
    datas.append((str(static_dir), 'schema_validator/web/static'))

# Add config files
config_files = [
    'schema_validator/config.py',
    'schema_validator/__init__.py'
]
for config_file in config_files:
    if Path(config_file).exists():
        datas.append((config_file, 'schema_validator'))

# Hidden imports for Flask and related packages
hiddenimports = [
    'flask',
    'flask_socketio',
    'socketio',
    'eventlet',
    'gevent',
    'geventwebsocket',
    'engineio',
    'playwright',
    'playwright._impl',
    'playwright._impl._api_structures',
    'playwright._impl._browser_type',
    'playwright._impl._browser',
    'playwright._impl._browser_context',
    'playwright._impl._page',
    'playwright._impl._element_handle',
    'playwright._impl._locator',
    'playwright._impl._frame',
    'playwright._impl._network',
    'playwright._impl._cdp_session',
    'playwright._impl._connection',
    'playwright._impl._transport',
    'playwright._impl._helper',
    'playwright._impl._errors',
    'playwright._impl._api_types',
    'playwright._impl._generated',
    'playwright._impl._generated.types',
    'playwright._impl._generated.errors',
    'playwright._impl._generated.api_structures',
    'playwright._impl._generated.api_types',
    'playwright._impl._generated.client',
    'playwright._impl._generated.server',
    'playwright._impl._generated.types',
    'playwright._impl._generated.errors',
    'playwright._impl._generated.api_structures',
    'playwright._impl._generated.api_types',
    'playwright._impl._generated.client',
    'playwright._impl._generated.server',
    'jsonschema',
    'validators',
    'beautifulsoup4',
    'requests',
    'tqdm',
    'openpyxl',
    'jinja2',
    'werkzeug',
    'markupsafe',
    'itsdangerous',
    'click',
    'blinker',
    'python-socketio',
    'python-engineio'
]

# Exclude unnecessary modules to reduce size
excludes = [
    'tkinter',
    'matplotlib',
    'numpy',
    'pandas',
    'scipy',
    'PIL',
    'cv2',
    'tensorflow',
    'torch',
    'sklearn'
]

block_cipher = None

a = Analysis(
    [str(main_script)],
    pathex=[str(current_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='schema-validator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
