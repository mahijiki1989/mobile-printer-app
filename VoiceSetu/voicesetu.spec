# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for VoiceSetu.
Uses onedir mode for reliability with large model files and DLLs.
The output directory is then packaged with Inno Setup into a single installer.
"""

import os
import sys
from pathlib import Path

block_cipher = None

# Get the project root
spec_dir = os.path.dirname(os.path.abspath(SPEC))

# Collect data files
datas = [
    (os.path.join(spec_dir, 'locales'), 'locales'),
    (os.path.join(spec_dir, 'assets'), 'assets'),
]

# Collect hidden imports needed by faster-whisper and dependencies
hiddenimports = [
    'faster_whisper',
    'ctranslate2',
    'huggingface_hub',
    'tokenizers',
    'sounddevice',
    'numpy',
    'keyboard',
    'pyperclip',
    'pystray',
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'customtkinter',
    'pkg_resources.extern',
]

a = Analysis(
    [os.path.join(spec_dir, 'main.py')],
    pathex=[spec_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'pandas', 'pytest', 'IPython'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VoiceSetu',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(spec_dir, 'assets', 'icon.ico') if os.path.exists(os.path.join(spec_dir, 'assets', 'icon.ico')) else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VoiceSetu',
)
