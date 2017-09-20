# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['E:\\Project\\PyQt\\MqttClientAssistant'],
             binaries=[('mqttclientassistant.ui','.')],
             datas=[],
             hiddenimports=["PyQt5.QtWidgets","paho.mqtt.client"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=True,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MqttClientAssistant',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=False )
