# -*- mode: python ; coding: utf-8 -*-
import os
from cells import utility

block_cipher = None

resources = utility.viewResourcesDir()

a = Analysis(['../cells/__main__.py'],
             pathex=['/Users/alestsurko/Desktop/cells'],
             binaries=[],
             datas=[(resources, "resources")],
             hiddenimports=["PySide2.QtPrintSupport"],
             hookspath=["hooks"],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts, [],
          exclude_binaries=True,
          name='Cells',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Cells')
app = BUNDLE(coll,
             name='Cells.app',
             icon=None,
             bundle_identifier='by.alestsurko.cells',
             info_plist={
                'NSPrincipalClass': 'NSApplication',
                'NSAppleScriptEnabled': False,
                'CFBundleDocumentTypes': [
                        {
                            'CFBundleTypeName': 'Cells Document Format',
                            'CFBundleTypeRole': 'Editor',
                            # 'CFBundleTypeIconFile': 'MyFileIcon.icns',
                            'LSItemContentTypes': ['by.alestsurko.cells'],
                            'LSHandlerRank': 'Owner'
                        },
                        {
                            'CFBundleTypeName': 'Cells Track Template Format',
                            'CFBundleTypeRole': 'Editor',
                            # 'CFBundleTypeIconFile': 'MyFileIcon.icns',
                            'LSItemContentTypes': ['by.alestsurko.ctt'],
                            'LSHandlerRank': 'Owner'
                        },
                    ]
                })
