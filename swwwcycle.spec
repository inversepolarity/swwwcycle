# -*- mode: python ; coding: utf-8 -*-
import os
import glob

block_cipher = None

# Find OpenGL library
libgl_path = '/usr/lib/x86_64-linux-gnu/libGL.so.1'
binaries = [(libgl_path, '.')] if os.path.exists(libgl_path) else []

# Add other necessary libraries
extra_libs = [
    '/usr/lib/x86_64-linux-gnu/libEGL.so.1',
    '/usr/lib/x86_64-linux-gnu/libGLX.so.0',
    '/usr/lib/x86_64-linux-gnu/libGLdispatch.so.0',
]

for lib in extra_libs:
    if os.path.exists(lib):
        binaries.append((lib, '.'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=[],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='swwwcycle',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)