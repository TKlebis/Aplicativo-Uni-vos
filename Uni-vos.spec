# -*- mode: python ; coding: utf-8 -*-

import os
import subprocess
import sys
from pathlib import Path

# Instala o MapView diretamente do GitHub se não estiver instalado
try:
    import kivy_garden.mapview
except ImportError:
    print("Instalando kivy_garden.mapview...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "https://github.com/kivy-garden/mapview/archive/master.zip"])
    # Força o recarregamento dos módulos
    import importlib
    import kivy_garden
    importlib.reload(kivy_garden)

block_cipher = None

# Caminhos base
base_dir = 'D:\\Desktop\\Aplicativoo\\frontend'
layout_dir = os.path.join(base_dir, 'layout')

a = Analysis(
    ['uni-vos.py'],
    pathex=['D:\\Desktop\\Aplicativoo\\frontend'],
    binaries=[],
    datas=[
        ('D:\\Desktop\\Aplicativoo\\frontend\\layout\\*', 'layout'),
        ('D:\\Desktop\\Aplicativoo\\frontend\\service-account-key.json', '.'),
        (str(Path(sys.prefix)/'Lib'/'site-packages'/'kivy_garden'), 'kivy_garden'),
        # Inclui todo o diretório kivy_garden
        (str(Path(sys.prefix)/'Lib'/'site-packages'/'kivy_garden'), 'kivy_garden'),
 
    ],
    hiddenimports=[
        'kivy',
        'kivy_garden',
        'kivy_garden.mapview',
        'kivymd',
        'firebase_admin',
        'google.cloud.firestore',
        'google.auth',
        'google.api_core',
        'grpc',
        'pytz',
        'cachetools',
        'urllib3',
        'protobuf',
        'six',
        'setuptools'
        'matplotlib',
        'matplotlib.backends.backend_agg',
        'numpy',
        'requests',
        'pkg_resources.py2_warn',
        'openssl',
    ],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Uni-vos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='D:\\Desktop\\Aplicativoo\\frontend\\layout\\Univos.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Uni-vos',
)