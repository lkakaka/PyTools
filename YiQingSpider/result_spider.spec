# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src\\result_spider.py', 'src\\spider_base.py'],
             pathex=['E:\\project\\PyTools\\YiQingSpider'],
             binaries=[],
             datas=[('chromedriver.exe', '.'),
			 ('template\\模板.docx', '.\\template')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='疫情扫描',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None, icon='Porsche.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='疫情扫描')
