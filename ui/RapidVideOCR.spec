# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

import rapidocr_onnxruntime

block_cipher = None

package_name = 'rapidocr_onnxruntime'
install_dir = Path(rapidocr_onnxruntime.__file__).resolve().parent
model_dir_map = (str(install_dir / 'models'), f'{package_name}/models')
yaml_path_map = (str(install_dir / '*.yaml'), package_name)


a = Analysis(
    ['RapidVideOCR.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='RapidVideOCR',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['rapid_videocr.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='RapidVideOCR',
)
