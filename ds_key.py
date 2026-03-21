import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

dir_path = "/home/tns0/service/sec/"

# 鍵を生成して保存（初回だけ）
def generate_and_save_key(key_file="key.bin"):
    key_path = os.path.join(dir_path, key_file)
    if not os.path.exists(key_path):
        key = AESGCM.generate_key(bit_length=256)
        with open(key_path, "wb") as f:
            f.write(key)
        print("鍵を生成して保存しました:", key_path)
    else:
        print("鍵は既に存在します:", key_path)

# 鍵を読み込む
def load_key(key_file="key.bin"):
    key_path = os.path.join(dir_path, key_file)
    with open(key_path, "rb") as f:
        return f.read()

# トークンを暗号化してテキストファイルに保存
def encrypt_and_save_token(token: str, outfile="token.enc", key_file="key.bin"):
    key = load_key(key_file)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # GCM用のランダムnonce
    ciphertext = aesgcm.encrypt(nonce, token.encode(), None)

    # Base64でまとめて保存
    with open(os.path.join(dir_path, outfile), "w") as f:
        f.write(base64.b64encode(nonce).decode() + "\n")
        f.write(base64.b64encode(ciphertext).decode())
    print("トークンを暗号化して保存しました:", outfile)

# 暗号化したトークンを復号
def load_and_decrypt_token(infile="token.enc", key_file="key.bin"):
    key = load_key(key_file)
    aesgcm = AESGCM(key)

    with open(os.path.join(dir_path, infile), "r") as f:
        nonce_b64, ct_b64 = f.read().splitlines()

    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ct_b64)

    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()
