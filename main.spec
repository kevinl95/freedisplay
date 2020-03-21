# -*- mode: python -*-
import sys
block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\kevin\\Documents\\freedisplay'],
             binaries=[],
             datas=[],
             hiddenimports=['pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon='images/displayicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='FreeDisplay')


# Build a .app if on OS X
if sys.platform == 'darwin':
  app = BUNDLE(exe,
               name='freedisplay.app',
               icon='images/displayicon.icns')
