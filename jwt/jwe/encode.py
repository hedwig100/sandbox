import json
from authlib.jose import JsonWebEncryption
from dotenv import load_dotenv
import os 
import base64

load_dotenv()

SECRET_KEY = base64.b64decode(os.getenv('SECRET_KEY', ''))
jwe = JsonWebEncryption()

# 1. 隠したいデータ（ペイロード）の準備
payload = {
    "user_id": 12345,
    "refresh_token": "abc_secret_refresh_token_xyz",
    "scope": "read write"
}

# 2. ヘッダーの設定
# alg='dir' は共通鍵を直接使用することを示し、enc='A256GCM' はAES-GCMで暗号化することを示します
protected = {'alg': 'dir', 'enc': 'A256GCM'}

# 3. 暗号化の実行
# payloadは文字列またはバイト列である必要があるため json.dumps します
jwe_token = jwe.serialize_compact(protected, json.dumps(payload), SECRET_KEY)

print(f"生成されたJWE:\n{jwe_token.decode('utf-8')}")

# 4. 復号の実行
try:
    data = jwe.deserialize_compact(jwe_token, SECRET_KEY)
    
    # 復号された中身（ヘッダーとペイロード）を確認
    decrypted_payload = json.loads(data['payload'])
    
    print("復号成功！")
    print(f"ユーザーID: {decrypted_payload['user_id']}")
    print(f"リフレッシュトークン: {decrypted_payload['refresh_token']}")

except Exception as e:
    # 鍵が違う、またはデータが改ざんされている場合はここでエラーになる
    print(f"復号失敗または改ざん検知: {e}")