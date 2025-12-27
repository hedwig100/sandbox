import os
import secrets
import base64

# 32バイトのランダムな鍵を生成（一度生成して保存しておく）
# 実際には OS の環境変数などから読み込むようにします
SECRET_KEY = base64.b64encode(secrets.token_bytes(32)).decode('ascii')

with open("jwe/.env", mode='w') as f:
    f.write(SECRET_KEY)