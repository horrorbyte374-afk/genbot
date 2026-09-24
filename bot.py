import os
import sys
import time
import json
import base64
import random
import string
import codecs
import hmac
import hashlib
import threading
import uuid
import requests
import urllib3
from flask import Flask, request
import telebot
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
TOKEN = os.getenv("8927723505:AAHStqkXGfw6ZJ5oght_td15uxlz0k1f9J8")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set!")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

class Config:
    API_HEX_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
    API_SECRET_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
    REGION_LANG = {
        "BD": "bn", "IND": "hi", "PK": "ur", "SG": "en", "ID": "id",
        "ME": "ar", "CIS": "ru", "TH": "th", "EU": "en", "US": "en",
        "SAC": "es", "LK": "en"
    }
    ACTIVATION_API = "https://jxe-guest-act-ob55.vercel.app/jxe/act"

# --- OBFUSCATED CORE DECODER ---
_core_blob = (
    "eJzNU9Fq2zAUfe9XaH6JzDqxBLaHwkYX14yylYY4G+RJKNK1fVdHMpJC45X8e+XYNHEN2x5333"
    "Q499x7z7EvZCWcIxnInUXfpLpADVcXJNRiSj6R6CtosMKDmjfXSSm0huo76oe52fOoo81aGl+i2"
    "gmdGAX7Dr92XniUW/ClUUdEQU6KXo7vKm8Fd+1c4HXY4dFYRWPy7jNx3nYbtOWC+mTCfhnUNLAt"
    "eMdkaVACDTzUBRNOIrIKvAfryFvSwwoL9C4mubGEE9TECl0Anc7i+EU8qO2sJnn0NDSALaaHJ3cY"
    "obPDn24DLW1Tey5qDBc1lRGK1pVAzUvYX7V7jc/DnIxGkzd/8Z2Ek0arHbsGMZymtJUYnWPBvqQZ"
    "/5aug6ubyftXNXlpkFiXYAMp0JmGRzrsvjzid/c3KU/myeW59u3Pk721UAoUV8KLIBVedNN4cCy3"
    "ZhssOZkTd4KbysgH7vA3jCLqFmK9xfRMOMatVPwv35zDQosgB7SP578JZXHLszRZpqs+myi5Xy5/"
    "LFbpTQvw+Zpn62yV3kWvfSm3Qg4CGii1foWpNPjbX3yGlMKVFW6YK8Xsw8ejjeGfAyeDmc8okEiu"
)
exec(__import__('zlib').decompress(__import__('base64').b64decode(_core_blob.encode())).decode())

# --- PROTO & NETWORKING ---
class ProtoBuilder:
    @staticmethod
    def encode_varint(n: int) -> bytes:
        if n < 0: return b''
        out = bytearray()
        while True:
            b = n & 0x7F
            n >>= 7
            if n: b |= 0x80
            out.append(b)
            if not n: break
        return bytes(out)

    @classmethod
    def create_field(cls, field_num: int, value: Any) -> bytes:
        if isinstance(value, int):
            return cls.encode_varint((field_num << 3) | 0) + cls.encode_varint(value)
        elif isinstance(value, (str, bytes)):
            v = value.encode() if isinstance(value, str) else value
            return cls.encode_varint((field_num << 3) | 2) + cls.encode_varint(len(v)) + v
        return b''

    @classmethod
    def build(cls, fields_dict: dict) -> bytes:
        return b''.join(cls.create_field(k, v) for k, v in fields_dict.items())

class NetService:
    @staticmethod
    def random_ua():
        return "GarenaMSDK/4.0.44(25028RN03A ;Android 15;ar;EG;app 1.132.1 2019121229;)"

class GarenaClient:
    def __init__(self):
        self.session = requests.Session()

    def major_login(self, access_token: str, open_id: str, lang: str):
        try:
            rnd_dev = f"02-{uuid.uuid4()}".encode()
            parts = [
                b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02',
                lang.encode("ascii"),
                b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118693\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
            ]
            raw = b''.join(parts)
            raw = raw.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', access_token.encode())
            raw = raw.replace(b'1d8ec0240ede109973f3321b9354b44d', open_id.encode())
            raw = raw.replace(b'02-344afb0e-593c-40b7-92f2-171972f74807', f"02-{uuid.uuid4()}".encode())

            enc = bytes.fromhex(SecurityEngine.encrypt_api_payload(raw.hex()))
            headers = {
                'User-Agent': NetService.random_ua(),
                'Accept-Encoding': "deflate, gzip",
                'X-GA-SV': "1789535859",
                'Authorization': "Bearer",
                'X-GA': "v1 1",
                'ReleaseVersion': "OB55",
                'Content-Type': "application/x-www-form-urlencoded",
                'X-Unity-Version': "2018.4.12f1",
            }
            resp = self.session.post("https://loginbp.ppmainecoonghj.com/MajorLogin", headers=headers, data=enc, verify=False, timeout=5)
            if resp.status_code == 200:
                idx = resp.text.find("eyJ")
                if idx != -1:
                    token = resp.text[idx:]
                    dot = token.find(".", token.find(".") + 1)
                    if dot != -1:
                        token = token[:dot + 44]
                        payload_b64 = token.split('.')[1]
                        pad_len = '=' * (4 - len(payload_b64) % 4)
                        decoded = json.loads(base64.urlsafe_b64decode(payload_b64 + pad_len))
                        acc_id = decoded.get('account_id') or decoded.get('external_id')
                        if acc_id:
                            return {"account_id": str(acc_id), "jwt_token": token}
        except Exception as e:
            print(f"[ERROR] MajorLogin failed: {e}")
        return None

class ActivationEngine:
    @staticmethod
    def activate(uid: str, password: str):
        try:
            r = requests.get(Config.ACTIVATION_API, params={"uid": uid, "password": password}, timeout=8, verify=False)
            return r.json().get("message", "Activated")
        except Exception as e:
            print(f"[ERROR] Activation failed: {e}")
            return "Activation request failed"

class AccountGenerator:
    @staticmethod
    def create_one(region: str, prefix: str):
        try:
            api = GarenaClient()
            tail = ''.join(random.choices(string.ascii_letters + string.digits, k=14))
            password = f"RYUGA_{tail}"

            reg_payload = json.dumps({"app_id": 100067, "client_type": 2, "password": password, "source": 2}, separators=(',', ':'))
            headers_reg = {
                "User-Agent": NetService.random_ua(),
                "Authorization": f"Signature {SecurityEngine.generate_signature(reg_payload)}",
                "Content-Type": "application/json; charset=utf-8",
                "Host": "100067.connect.garena.com",
            }
            
            print(f"[INFO] Registering guest account for region {region}...")
            resp_reg = api.session.post("https://100067.connect.garena.com/api/v2/oauth/guest:register", headers=headers_reg, data=reg_payload, timeout=5, verify=False)
            if resp_reg.status_code != 200 or resp_reg.json().get("code") != 0:
                print(f"[ERROR] Registration returned status code {resp_reg.status_code}")
                return None
            uid = resp_reg.json()['data']['uid']

            device_id = f"02-{uuid.uuid4()}"
            tok_payload = json.dumps({"client_id": 100067, "client_secret": Config.API_HEX_KEY, "client_type": 2, "device_id": device_id, "password": password, "response_type": "token", "uid": uid}, separators=(',', ':'))
            
            print(f"[INFO] Requesting guest token for UID: {uid}...")
            resp_tok = api.session.post("https://100067.connect.garena.com/api/v2/oauth/guest/token:grant", headers=headers_reg, data=tok_payload, timeout=5, verify=False)
            if resp_tok.status_code != 200 or resp_tok.json().get("code") != 0:
                print(f"[ERROR] Token grant failed with status {resp_tok.status_code}")
                return None
            
            access_token = resp_tok.json()['data']['access_token']
            open_id = resp_tok.json()['data']['open_id']

            keystream = [0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
            field = codecs.decode(''.join(chr(ord(open_id[i]) ^ keystream[i % len(keystream)]) for i in range(len(open_id))).encode('unicode_escape').decode('utf-8'), 'unicode_escape').encode('latin1')

            name = f"{prefix}{random.randint(10000, 99999)}"
            lang = Config.REGION_LANG.get(region.upper(), "en")

            proto = ProtoBuilder.build({1: name, 2: access_token, 3: open_id, 5: 102000007, 6: 4, 7: 1, 13: 1, 14: field, 15: lang, 16: 1, 17: 1})
            enc_major = bytes.fromhex(SecurityEngine.encrypt_api_payload(proto.hex()))
            headers_major = headers_reg.copy()
            headers_major["Host"] = "loginbp.ppmainecoonghj.com"
            headers_major["Authorization"] = "Bearer"

            print(f"[INFO] Performing MajorRegister for nickname: {name}...")
            api.session.post("https://loginbp.ppmainecoonghj.com/MajorRegister", headers=headers_major, data=enc_major, verify=False, timeout=5)
            
            login_data = api.major_login(access_token, open_id, lang)
            if not login_data:
                print(f"[ERROR] MajorLogin failed after registration.")
                return None

            act_msg = ActivationEngine.activate(str(uid), password)
            print(f"[SUCCESS] Account generated successfully! UID: {uid} | ID: {login_data['account_id']}")
            return {
                "uid": uid,
                "password": password,
                "account_id": login_data["account_id"],
                "name": name,
                "region": region,
                "activation": act_msg
            }
        except Exception as e:
            print(f"[CRITICAL EXCEPTION] {e}")
            return None

# --- TELEGRAM BOT HANDLERS ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 
        "🚀 **MASTER GEN Telegram Bot**\n\n"
        "Use the command format below to generate accounts:\n"
        "`/gen [REGION] [PREFIX] [COUNT]`\n\n"
        "Example: `/gen IND RYUGA 2`\n"
        "Supported Regions: `IND, BD, PK, SG, ID, ME`",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['gen'])
def handle_generate(message):
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "⚠️ Usage: `/gen REGION PREFIX COUNT`\nExample: `/gen IND RYUGA 2`", parse_mode="Markdown")
            return
        
        region = parts[1].upper()
        prefix = parts[2]
        count = int(parts[3])

        if count > 5:
            bot.reply_to(message, "⚠️ Maximum 5 accounts per request to prevent timeout.")
            return

        bot.reply_to(message, f"⚙️ Generating {count} account(s) for region `{region}` with prefix `{prefix}`...", parse_mode="Markdown")

        success_count = 0
        generated_accounts = []
        
        for i in range(count):
            print(f"\n--- [BATCH PROCESS] Generating account {i+1} of {count} ---")
            acc = AccountGenerator.create_one(region, prefix)
            if acc:
                success_count += 1
                generated_accounts.append(acc)
                card = (
                    f"✅ **Account #{success_count} Created!**\n"
                    f"👤 Nickname: `{acc['name']}`\n"
                    f"🆔 Account ID: `{acc['account_id']}`\n"
                    f"🔑 Login UID: `{acc['uid']}`\n"
                    f"🔒 Password: `{acc['password']}`\n"
                    f"🌍 Region: `{acc['region']}`\n"
                    f"⚡ Status: `{acc['activation']}`"
                )
                bot.send_message(message.chat.id, card, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, f"❌ Generation attempt #{i+1} failed.")
            time.sleep(0.5)

        # Save and send accounts.json if any accounts were successfully generated
        if generated_accounts:
            filename = f"accounts_{int(time.time())}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(generated_accounts, f, indent=4)
            
            with open(filename, "rb") as f:
                bot.send_document(
                    message.chat.id, 
                    f, 
                    caption=f"📁 **Batch Export Complete**\nSuccessfully generated {success_count}/{count} accounts.",
                    parse_mode="Markdown"
                )
            
            # Clean up local file after sending
            if os.path.exists(filename):
                os.remove(filename)

        bot.send_message(message.chat.id, f"🏁 Batch process finished. Total success: {success_count}/{count}.")
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        bot.reply_to(message, f"❌ Error: {str(e)[:150]}")

# --- FLASK WEBHOOK ROUTES ---
@app.route('/')
def index():
    return "Master Gen Telegram Bot Backend is running successfully!", 200

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    else:
        return "Invalid content type", 403

if __name__ == "__main__":
    bot.remove_webhook()
    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL}/{TOKEN}"
        bot.set_webhook(url=webhook_url)
        print(f"Webhook set to: {webhook_url}")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
                    
