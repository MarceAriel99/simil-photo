# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.pyw'],
    pathex=[],
    binaries=[],
    datas=[('E:\\Mis_Archivos\\Proyects\\Programs\\SimilPhoto\\Program\\venv\\lib\\site-packages\\tensorflow\\python\\_pywrap_tensorflow_internal.pyd', 'tensorflow\python'),
    ('E:\\Mis_Archivos\\Proyects\\Programs\\SimilPhoto\\Program\\resources\\logo.png', 'resources'),
    ('E:\\Mis_Archivos\\Proyects\\Programs\\SimilPhoto\\Program\\resources\\logo_greyscale.png', 'resources'),
    ('E:\\Mis_Archivos\\Proyects\\Programs\\SimilPhoto\\Program\\feature_extraction_methods_descriptions.json', '.')],
    hiddenimports=['sklearn.neighbors.typedefs', 
    'tensorflow', 
    'numpy', 
    'tensorflow.compiler.tf2tensorrt.ops', 
    'sklearn.metrics._pairwise_distances_reduction._datasets_pair', 
    'sklearn.metrics._pairwise_distances_reduction._middle_term_computer'],
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
    name='main',
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
    icon='E:\\Mis_Archivos\\Proyects\\Programs\\SimilPhoto\\Program\\resources\\logo.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
