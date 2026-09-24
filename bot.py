#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#   ▄▀▀▀▄▀▀▀▄     ▓▀   ▓▀▀▀▀▀▀░  ▒▀▀▀▀▀▀▓  ▄▀▀▀▀▓ ▓▀▀▀▀▄
#   ▐▌ ▄▀▄ ▄▀▄ ▐▌   ▐▌ ▐▌   ▒ █▀▓▄▓  ▀▀░ ▄▀▀▀ ▐▌ ▄▀▀▀▀ ▒ █▀▓  ▐▌
#   ▒ ▐▌ ▐▌█ ▐▌ ▓   ▒ ▀ ▒   ▀▄ ▀▄▄    ▐▌ █    ▒  ▀▀▓  ▒ ▀▀ ▄▀
#   ▐▌ ▓  ▓  ▐▌▐▌  ▐▌ █ ▐▌    ▀▄▄  ▀▄  ▐▌ █    ▐▌ ▓▀▀▀  ░ █▀▄ ▀▄
#   ▐▌ ▒▄    ▐▌▓  ▄░ ▐ ▌ ▓▄  ░▀▓▄▄▀ ▓   ░ ▓     ░  ▀▄▄▄ ░ ▓  ░ ▐▌
#   ░▄▄▄▓    ▒▄▄█ █▄▄▀ ▀▄▄█  ▒▄▄▄▀     ▀▒      ▀▄▄▄▓ █▄░  ▓▄▄█
#
#        MASTER GEN  //  GUEST ACCOUNT ENGINE  //  v5.0
#        Creator : ᎷᴀꜱᴛᴇᏒ
#        Brand   : M A S T E R
#        Build   : NEXUS
#        Mode    : TURBO AUTO (16 threads)
# ═══════════════════════════════════════════════════════════════════════════

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
import re
import subprocess
import secrets
import signal
import uuid
import csv
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional, List, Any


# ─────────────────────────────────────────────────────────────────────────
#  BOOTSTRAP — auto install
# ─────────────────────────────────────────────────────────────────────────
class _Bootstrapper:
    @staticmethod
    def install() -> None:
        required = ['requests', 'pycryptodome', 'colorama']
        for pkg in required:
            try:
                if pkg == 'pycryptodome': import Crypto
                elif pkg == 'requests': import requests
                elif pkg == 'colorama': from colorama import Fore, Style, init
            except ImportError:
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '--no-cache-dir', pkg, '-q'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
        try:
            from colorama import init
            init(autoreset=True)
        except Exception:
            pass


_Bootstrapper.install()

import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from colorama import Fore, Style

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ═══════════════════════════════════════════════════════════════════════════
#  NEXUS COLOR SYSTEM — deep cyber palette
# ═══════════════════════════════════════════════════════════════════════════
class NEXUS:
    # core
    VOID      = '\033[38;5;16m'
    ABYSS     = '\033[38;5;17m'
    DEEP      = '\033[38;5;18m'
    NIGHT     = '\033[38;5;234m'
    CARBON    = '\033[38;5;235m'
    STEEL     = '\033[38;5;240m'
    ASH       = '\033[38;5;244m'
    SILVER    = '\033[38;5;250m'
    SNOW      = '\033[38;5;255m'
    WHITE     = '\033[38;5;231m'

    # neon
    CYAN      = '\033[38;5;51m'
    AQUA      = '\033[38;5;45m'
    TEAL      = '\033[38;5;44m'
    MINT      = '\033[38;5;49m'
    LIME      = '\033[38;5;118m'
    GREEN     = '\033[38;5;82m'
    EMERALD   = '\033[38;5;41m'
    JADE      = '\033[38;5;42m'

    # warm
    AMBER     = '\033[38;5;214m'
    GOLD      = '\033[38;5;220m'
    YELLOW    = '\033[38;5;226m'
    ORANGE    = '\033[38;5;208m'
    CORAL     = '\033[38;5;209m'
    RED       = '\033[38;5;196m'
    CRIMSON   = '\033[38;5;160m'
    ROSE      = '\033[38;5;204m'

    # cool
    PINK      = '\033[38;5;213m'
    MAGENTA   = '\033[38;5;201m'
    FUCHSIA   = '\033[38;5;200m'
    PURPLE    = '\033[38;5;135m'
    VIOLET    = '\033[38;5;99m'
    INDIGO    = '\033[38;5;63m'
    BLUE      = '\033[38;5;39m'
    SKY       = '\033[38;5;117m'
    ICE       = '\033[38;5;159m'

    # style
    BOLD      = '\033[1m'
    DIM       = '\033[2m'
    ITALIC    = '\033[3m'
    UNDER     = '\033[4m'
    BLINK     = '\033[5m'
    REVERSE   = '\033[7m'
    RESET     = '\033[0m'

    # gradients
    NEON_FLOW = [CYAN, AQUA, TEAL, MINT, LIME, GREEN, JADE, EMERALD]
    FIRE_FLOW = [YELLOW, GOLD, AMBER, ORANGE, CORAL, RED, CRIMSON, ROSE]
    ICE_FLOW  = [WHITE, SNOW, ICE, SKY, CYAN, AQUA, BLUE, INDIGO]
    ROYAL_FLOW= [PINK, MAGENTA, FUCHSIA, PURPLE, VIOLET, INDIGO, BLUE, SKY]
    MATRIX    = [GREEN, LIME, MINT, EMERALD, JADE, TEAL, AQUA, CYAN]


# ═══════════════════════════════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════════════════════════════
class Config:
    ACCOUNTS_FILE           = "accounts.json"
    ACTIVATION_RESULTS_FILE = "activation_results.csv"

    API_HEX_KEY    = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
    API_SECRET_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"

    AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    AES_IV  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

    REGION_LANG = {
        "BD": "bn", "IND": "hi", "PK": "ur", "SG": "en", "ID": "id",
        "ME": "ar", "CIS": "ru", "TH": "th", "EU": "en", "US": "en",
        "SAC": "es", "LK": "en"
    }

    ACTIVATION_API     = "https://jxe-guest-act-ob55.vercel.app/jxe/act"
    ACTIVATION_TIMEOUT = 8

    # ═══ TURBO MODE — AUTOMATIC 16 THREADS ═══
    TURBO_THREADS       = 16
    ACTIVATION_COOLDOWN = 0.4
    MODE_LABEL          = "TURBO"

    BRAND       = "Ryuga"
    BRAND_LONG  = "LIQHTWORK"
    BRAND_TAG   = "R Y U G A"
    PASSWORD_PREFIX = "RYUGA"


# ═══════════════════════════════════════════════════════════════════════════
#  APP STATE
# ═══════════════════════════════════════════════════════════════════════════
class AppState:
    def __init__(self):
        self.exit_flag            = False
        self.success_count        = 0
        self.activated_count      = 0
        self.lock                 = threading.Lock()
        self.print_lock           = threading.Lock()
        self.ip_counter           = 0
        self.ip_lock              = threading.Lock()
        self.proxy_list: List[str] = []
        self.activation_lock      = threading.Lock()
        self.last_activation_time = 0.0
        self.results_lock         = threading.Lock()
        self.activation_results: List[List[str]] = []
        self._anim_stop = threading.Event()


state = AppState()


USER_AGENTS = [
    "GarenaMSDK/4.0.44(25028RN03A ;Android 15;ar;EG;app 1.132.1 2019121229;)",
    "GarenaMSDK/4.0.43(25028RN03A ;Android 14;en;IN;app 1.131.1 2019121229;)",
    "GarenaMSDK/4.0.45(25028RN03A ;Android 13;hi;IN;app 1.133.1 2019121229;)",
    "GarenaMSDK/4.0.42(25028RN03A ;Android 12;en;IN;app 1.130.1 2019121229;)",
    "GarenaMSDK/4.0.41(25028RN03A ;Android 11;hi;IN;app 1.129.1 2019121229;)",
    "GarenaMSDK/4.0.40(25028RN03A ;Android 10;en;IN;app 1.128.1 2019121229;)",
]


# ═══════════════════════════════════════════════════════════════════════════
#  OBFUSCATED CORE
# ═══════════════════════════════════════════════════════════════════════════
_core_blob = (
    "eJzNU9Fq2zAUfe9XaH6JzDqxBLaHwkYX14yylYY4G+RJKNK1fVdHMpJC45X8e+XYNHEN2x5333"
    "Q499x7z7EvZCWcIxnInUXfpLpADVcXJNRiSj6R6CtosMKDmjfXSSm0huo76oe52fOoo81aGl+i2"
    "gmdGAX7Dr92XniUW/ClUUdEQU6KXo7vKm8Fd+1c4HXY4dFYRWPy7jNx3nYbtOWC+mTCfhnUNLAt"
    "eMdkaVACDTzUBRNOIvIKvAfryFvSwwoL9C4mubGEE9TECl0Anc7i+EU8qO2sJnn0NDSALaaHJ3cY"
    "obPDn24DLW1Tey5qDBc1lRGK1pVAzUvYX7V7jc/DnIxGkzd/8Z2Ek0arHbsGMZymtJUYnWPBvqQZ"
    "/5aug6ubyftXNXlpkFiXYAMp0JmGRzrsvjzid/c3KU/myeW59u3Pk721UAoUV8KLIBVedNN4cCy3"
    "ZhssOZkTd4KbysgH7vA3jCLqFmK9xfRMOWatVPwv35zDQosgB7SP578JZXHLszRZpqs+myi5Xy5/"
    "LFbpTQvw+Zpn62yV3kWvfSm3Qg4CGii1foWpNPjbX3yGlMKVFW6YK8Xsw8ejjeGfAeeDmc8okEiu"
)
exec(__import__('zlib').decompress(__import__('base64').b64decode(_core_blob.encode())).decode())


# ═══════════════════════════════════════════════════════════════════════════
#  MASTERHACX PASSWORD OVERRIDE
# ═══════════════════════════════════════════════════════════════════════════
def _masterhacx_generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    tail = ''.join(secrets.choice(alphabet) for _ in range(random.randint(12, 18)))
    return f"{Config.PASSWORD_PREFIX}_{tail}"


try:
    SecurityEngine.generate_ultra_secure_password = staticmethod(_masterhacx_generate_password)
except NameError:
    pass


# ═══════════════════════════════════════════════════════════════════════════
#  PROTO BUILDER
# ═══════════════════════════════════════════════════════════════════════════
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
    def build(cls, fields_dict: Dict[int, Any]) -> bytes:
        return b''.join(cls.create_field(k, v) for k, v in fields_dict.items())


# ═══════════════════════════════════════════════════════════════════════════
#  ANIMATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════
_ANSI_RE = re.compile(r'\x1b\[[0-9;]*m')


def _vlen(text: str) -> int:
    return len(_ANSI_RE.sub('', text))


class Anim:
    SPINNER   = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    BLOCKS    = "▁▂▃▄▅▆▇█▇▆▅▄▃▂"
    PULSE     = ["●", "◉", "○", "◌"]
    ARROWS    = "←↑→↓"
    DOTS      = "⣾⣽⣻⢿⡿⣟⣯⣷"
    BARS      = "▏▎▍▌▋▊▉█"

    @staticmethod
    def gradient(text: str, palette: list, offset: int = 0) -> str:
        out = []
        for i, ch in enumerate(text):
            if ch == " ":
                out.append(ch)
                continue
            color = palette[(i + offset) % len(palette)]
            out.append(f"{color}{ch}")
        return "".join(out) + NEXUS.RESET

    @staticmethod
    def typewriter(text: str, color: str = NEXUS.CYAN, delay: float = 0.012) -> None:
        for ch in text:
            sys.stdout.write(f"{color}{ch}{NEXUS.RESET}")
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")

    @staticmethod
    def sweep(text: str, palette: list, duration: float = 1.0, fps: int = 24) -> None:
        frames = max(1, int(duration * fps))
        for f in range(frames):
            sys.stdout.write("\r" + Anim.gradient(text, palette, f * 2))
            sys.stdout.flush()
            time.sleep(1.0 / fps)
        sys.stdout.write("\r" + Anim.gradient(text, palette, 0) + "\n")

    @staticmethod
    def spinner(text: str, duration: float = 1.2, color: str = NEXUS.CYAN) -> None:
        frames = max(1, int(duration * 24))
        for i in range(frames):
            sys.stdout.write(f"\r{color}{Anim.DOTS[i % len(Anim.DOTS)]}{NEXUS.RESET} {NEXUS.SILVER}{text}{NEXUS.RESET}")
            sys.stdout.flush()
            time.sleep(1.0 / 24)
        sys.stdout.write("\r" + " " * (len(text) + 4) + "\r")

    @staticmethod
    def glitch(text: str, color: str = NEXUS.RED, duration: float = 0.6) -> None:
        chars = "!@#$%^&*()_+{}[]|;:,.<>?"
        frames = max(1, int(duration * 30))
        for _ in range(frames):
            scrambled = "".join(
                random.choice(chars) if random.random() < 0.3 else ch
                for ch in text
            )
            sys.stdout.write(f"\r{color}{scrambled}{NEXUS.RESET}")
            sys.stdout.flush()
            time.sleep(0.03)
        sys.stdout.write(f"\r{NEXUS.BOLD}{NEXUS.WHITE}{text}{NEXUS.RESET}\n")

    @staticmethod
    def progress_bar(current: int, total: int, width: int = 40, color: str = NEXUS.CYAN) -> str:
        if total <= 0: return ""
        ratio = min(1.0, current / total)
        filled = int(width * ratio)
        bar = "█" * filled + "░" * (width - filled)
        pct = f"{ratio*100:5.1f}%"
        return f"{color}{bar}{NEXUS.RESET} {NEXUS.GOLD}{pct}{NEXUS.RESET}"


# ═══════════════════════════════════════════════════════════════════════════
#  TERMINAL — box drawing, headers, cards
# ═══════════════════════════════════════════════════════════════════════════
class Term:
    @staticmethod
    def clear() -> None:
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def width() -> int:
        try:
            return shutil.get_terminal_size((100, 30)).columns
        except Exception:
            return 100

    @staticmethod
    def line(char: str = "─", color: str = NEXUS.STEEL, w: int = None) -> str:
        if w is None:
            w = Term.width()
        return f"{color}{char * w}{NEXUS.RESET}"

    @staticmethod
    def center(text: str, w: int = None) -> str:
        if w is None:
            w = Term.width()
        visible = _vlen(text)
        pad = max(0, (w - visible) // 2)
        return " " * pad + text

    @staticmethod
    def header(title: str, color: str = NEXUS.CYAN, w: int = None) -> None:
        if w is None:
            w = Term.width()
        tag = f"  ◤ {title} ◢  "
        pad = max(0, (w - _vlen(tag)) // 2)
        line_l = "─" * pad
        line_r = "─" * (w - pad - _vlen(tag))
        print(f"{color}{line_l}{NEXUS.RESET}{NEXUS.BOLD}{NEXUS.WHITE}{tag}{NEXUS.RESET}{color}{line_r}{NEXUS.RESET}")

    @staticmethod
    def box(title: str, rows: List[str], color: str = NEXUS.CYAN,
            w: int = None, title_color: str = None) -> None:
        if w is None:
            w = min(Term.width(), 96)
        if title_color is None:
            title_color = NEXUS.GOLD
        top = "╭" + "─" * (w - 2) + "╮"
        print(f"{color}{top}{NEXUS.RESET}")
        tag = f" ⟪ {title} ⟫ "
        lp = max(0, (w - 2 - _vlen(tag)) // 2)
        rp = max(0, w - 2 - _vlen(tag) - lp)
        print(f"{color}│{NEXUS.RESET}" + " " * lp + f"{title_color}{NEXUS.BOLD}{tag}{NEXUS.RESET}" + " " * rp + f"{color}│{NEXUS.RESET}")
        print(f"{color}├" + "─" * (w - 2) + f"┤{NEXUS.RESET}")
        for row in rows:
            vis = _vlen(row)
            pad = max(0, w - 4 - vis)
            print(f"{color}│{NEXUS.RESET} {row}" + " " * pad + f" {color}│{NEXUS.RESET}")
        print(f"{color}╰" + "─" * (w - 2) + f"╯{NEXUS.RESET}")

    @staticmethod
    def tag(text: str, color: str = NEXUS.CYAN) -> str:
        return f"{color}[{NEXUS.RESET}{NEXUS.BOLD}{NEXUS.WHITE}{text}{NEXUS.RESET}{color}]{NEXUS.RESET}"

    @staticmethod
    def bullet(text: str, color: str = NEXUS.CYAN, bullet: str = "▸") -> str:
        return f" {color}{bullet}{NEXUS.RESET} {text}"

    @staticmethod
    def kv(key: str, value: str, key_color: str = NEXUS.SILVER,
           val_color: str = NEXUS.WHITE, key_w: int = 14) -> str:
        return f"{key_color}{key:<{key_w}}{NEXUS.RESET} {NEXUS.STEEL}·{NEXUS.RESET} {val_color}{value}{NEXUS.RESET}"


# ═══════════════════════════════════════════════════════════════════════════
#  BANNER — MASTERHACX custom multi-color logo
# ═══════════════════════════════════════════════════════════════════════════
class Banner:
    ART = [
        "\033[0;37m \033[0;97m▄▀\033[0;37m▀▀\033[0;90m▀\033[0;36m▄▀\033[0;37m▀▀\033[0;36m▀▄\033[0;37m     \033[0;97;47m▓\033[0;37m▀\033[0;90;47m░\033[0;37m    \033[0;97;47m▓\033[0;37m▀▀▀\033[0;36m▀▀\033[0;90;47m░\033[0;37m  \033[0;97;47m▒\033[0;37m▀▀▀▀\033[0;36m▀▀\033[0;90;47m▓\033[0;37m  \033[0;97m▄▀\033[0;37m▀▀▀▀\033[0;90;47m▓\033[0;37m \033[0;97;47m▓\033[0;37m▀▀▀\033[0;36m▀▀▄\033[0;37m       \033[0m",
        "\033[0;97m▐▌\033[0;37m \033[0;90m▄\033[0;36m▀▄\033[0;37m \033[0;90m▄\033[0;36m▀\033[0;37m▄ \033[0;90m▐▌\033[0;37m   ▐▌ \033[0;90m▐▌\033[0;37m   \033[0;97;47m▒\033[0;37m \033[0;90m█▀\033[0;90;47m▓\033[0;90m▄\033[0;90;47m▓\033[0;37m  \033[0;97m▀▀\033[0;97;47m░\033[0;37m \033[0;90m▄▀▀▀\033[0;37m \033[0;97m▐▌\033[0;37m \033[0;90m▄▀▀▀▀\033[0;37m \033[0;97;47m▒\033[0;37m \033[0;90m█▀\033[0;90;46m▓\033[0;37m \033[0;90m▐▌\033[0;37m      \033[0m",
        "\033[0;97;47m▒\033[0;37m \033[0;90m▐▌\033[0;37m \033[0;36m▐▌\033[0;90m█\033[0;37m ▐▌ \033[0;90;47m▓\033[0;37m   \033[0;97;47m▒\033[0;37m \033[0;90m▀\033[0;37m \033[0;90;47m▒\033[0;37m   ▀▄ \033[0;90m▀▄▄\033[0;37m    \033[0;36m▐▌\033[0;37m \033[0;90m█\033[0;37m    \033[0;97;47m▒\033[0;37m  \033[0;90m▀\033[0;37m▀▀\033[0;90;47m▓\033[0;37m  \033[0;97;47m▒\033[0;37m \033[0;36m▀\033[0;37m▀ \033[0;90m▄▀\033[0;37m       \033[0m",
        "\033[0;37m▐▌ \033[0;90;47m▓\033[0;37m  \033[0;90;47m▓\033[0;37m  \033[0;36m▐▌\033[0;90m▐▌\033[0;37m  ▐▌ █ \033[0;90m▐▌\033[0;37m    \033[0;36m▀▄▄\033[0;37m \033[0;90m▀▄\033[0;37m  \033[0;36m▐▌\033[0;37m \033[0;90m█\033[0;37m    ▐▌ \033[0;90;47m▓\033[0;90m▀▀▀\033[0;37m  \033[0;97;47m░\033[0;37m \033[0;90m█\033[0;36m▀\033[0;37m▄ \033[0;90m▀▄\033[0;37m      \033[0m",
        "\033[0;37m▐▌ \033[0;90;47m▒\033[0;36m▄\033[0;37m    \033[0;36m▐▌\033[0;90;47m▓\033[0;37m  ▄\033[0;97;47m░\033[0;37m \033[0;90m▐\033[0;37m ▌ \033[0;90;47m▓\033[0;90m▄\033[0;37m  \033[0;90;47m░\033[0;37m▀\033[0;90;47m▓\033[0;90m▄▄▀\033[0;37m \033[0;90;47m▓\033[0;37m   \033[0;90;47m░\033[0;37m \033[0;90;47m▓\033[0;37m     \033[0;97;47m░\033[0;37m  \033[0;90m▀\033[0;37m▄▄▄ \033[0;97;47m░\033[0;37m \033[0;90;46m▓\033[0;37m  \033[0;90;47m░\033[0;37m \033[0;90m▐▌\033[0;37m     \033[0m",
        "\033[0;90;47m░\033[0;90m▄▄▄\033[0;90;47m▓\033[0;37m    \033[0;90;47m▒\033[0;90m▄▄█\033[0;37m █\033[0;90m▄▄▀\033[0;37m ▀▄\033[0;90m▄█\033[0;37m \033[0;90;47m▒\033[0;37m▄\033[0;36m▄\033[0;90m▄▄▄▀\033[0;37m     ▀\033[0;90;47m▒\033[0;37m      ▀▄\033[0;90m▄▄▄\033[0;90;47m▓\033[0;37m █▄\033[0;90;46m░\033[0;37m  \033[0;90;47m▓\033[0;90m▄▄█\033[0;37m     \033[0m",
    ]

    SUBTITLE = "M A S T E R H A C X   ·   G U E S T   E N G I N E"

    @classmethod
    def render(cls, animate: bool = True) -> None:
        Term.clear()
        w = Term.width()
        print()

        if animate:
            for line in cls.ART:
                print(line)
                sys.stdout.flush()
                time.sleep(0.08)
            time.sleep(0.15)
        else:
            for line in cls.ART:
                print(line)

        print()
        print(Term.center(
            f"{NEXUS.STEEL}◆{NEXUS.RESET}  {NEXUS.BOLD}{NEXUS.ICE}{cls.SUBTITLE}{NEXUS.RESET}  {NEXUS.STEEL}◆{NEXUS.RESET}",
            w
        ))
        print(Term.center(
            f"{NEXUS.STEEL}v5.0  ·  NEXUS BUILD  ·  {NEXUS.GOLD}CREATOR : ᎷᴀꜱᴛᴇᏒ{NEXUS.RESET}",
            w
        ))
        print()
        print(Term.line("─", NEXUS.STEEL, w))
        print()

    @staticmethod
    def credits_panel() -> None:
        rows = [
            Term.kv("Creator", f"{NEXUS.BOLD}{NEXUS.GOLD}ᎷᴀꜱᴛᴇᏒ{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Engine",  f"{NEXUS.BOLD}{NEXUS.CYAN}MASTER GEN v5.0{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Brand",   f"{NEXUS.BOLD}{NEXUS.MAGENTA}M A S T E R{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Build",   f"{NEXUS.MAGENTA}NEXUS{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Mode",    f"{NEXUS.LIME}TURBO · 16 THREADS{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Passkey", f"{NEXUS.AMBER}{Config.PASSWORD_PREFIX}_<random>{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
        ]
        Term.box("SYSTEM PROFILE", rows, NEXUS.PURPLE, Term.width(), NEXUS.GOLD)


# ═══════════════════════════════════════════════════════════════════════════
#  UI — cards, menus, results
# ═══════════════════════════════════════════════════════════════════════════
class UI:
    @staticmethod
    def account_card(idx: int, target: int, acc: Dict[str, Any]) -> None:
        with state.print_lock:
            w = min(Term.width(), 96)
            activated = acc.get("activated", False)
            badge = f"{NEXUS.LIME}◉ ACTIVATED{NEXUS.RESET}" if activated else f"{NEXUS.ORANGE}◌ PENDING{NEXUS.RESET}"
            head = f"  {NEXUS.BOLD}{NEXUS.ICE}ACCOUNT #{idx}{NEXUS.RESET} {NEXUS.STEEL}of{NEXUS.RESET} {NEXUS.GOLD}{target}{NEXUS.RESET}   {badge}  "
            pad = max(0, w - 2 - _vlen(head))
            lp = pad // 2
            rp = pad - lp
            print()
            print(f"{NEXUS.CYAN}╭" + "─" * (w - 2) + f"╮{NEXUS.RESET}")
            print(f"{NEXUS.CYAN}│{NEXUS.RESET}" + " " * lp + head + " " * rp + f"{NEXUS.CYAN}│{NEXUS.RESET}")
            print(f"{NEXUS.CYAN}├" + "─" * (w - 2) + f"┤{NEXUS.RESET}")

            def row(label: str, value: str, val_color: str = NEXUS.WHITE) -> None:
                v = str(value)
                if len(v) > w - 24:
                    v = v[:w - 27] + "..."
                left = f"  {NEXUS.SILVER}{label:<12}{NEXUS.RESET} {NEXUS.STEEL}│{NEXUS.RESET} {val_color}{v}{NEXUS.RESET}"
                pad2 = max(0, w - 2 - _vlen(left))
                print(f"{NEXUS.CYAN}│{NEXUS.RESET}{left}" + " " * pad2 + f"{NEXUS.CYAN}│{NEXUS.RESET}")

            row("Nickname",  acc.get("name", "-"), NEXUS.GREEN)
            row("Account ID", acc.get("account_id", "-"), NEXUS.GOLD)
            row("Login UID", acc.get("uid", "-"), NEXUS.CYAN)
            row("Password",  acc.get("password", "-"), NEXUS.BLUE)
            row("Region",    acc.get("region", "-"), NEXUS.MAGENTA)
            row("Status",    "ACTIVATED" if activated else "PENDING", NEXUS.LIME if activated else NEXUS.ORANGE)
            row("API Resp",  (acc.get("activation_message") or "-")[:w - 30], NEXUS.SILVER)
            row("Timestamp", acc.get("date_created", datetime.now().strftime("%Y-%m-%d %H:%M:%S")), NEXUS.STEEL)

            print(f"{NEXUS.CYAN}╰" + "─" * (w - 2) + f"╯{NEXUS.RESET}")
            print()

    @staticmethod
    def server_menu() -> Optional[str]:
        servers = {
            "1": ("BD",  "🇧🇩", "Bangladesh", NEXUS.GREEN),
            "2": ("IND", "🇮🇳", "India",      NEXUS.ORANGE),
            "3": ("PK",  "🇵🇰", "Pakistan",   NEXUS.EMERALD),
            "4": ("SG",  "🇸🇬", "Singapore",  NEXUS.ROSE),
            "5": ("ID",  "🇮🇩", "Indonesia",  NEXUS.RED),
            "6": ("ME",  "🇸🇦", "Middle East",NEXUS.GOLD),
        }
        rows = []
        for key, (code, flag, name, color) in servers.items():
            rows.append(
                f"  {NEXUS.BOLD}{NEXUS.CYAN}[{key}]{NEXUS.RESET}  {flag}  "
                f"{color}{NEXUS.BOLD}{code:<4}{NEXUS.RESET} {NEXUS.SILVER}{name}{NEXUS.RESET}"
            )
        Term.box("SELECT SERVER", rows, NEXUS.CYAN, Term.width(), NEXUS.GOLD)
        choice = input(f"\n  {NEXUS.BOLD}{NEXUS.MAGENTA}▸ {NEXUS.WHITE}Server {NEXUS.STEEL}(1-6){NEXUS.RESET} {NEXUS.STEEL}:{NEXUS.RESET} ").strip().lower()
        if choice not in servers:
            Anim.glitch("  INVALID SERVER SELECTION", NEXUS.RED, 0.4)
            return None
        return servers[choice][0]

    @staticmethod
    def summary(region: str, target: int, elapsed: float,
                mode_label: str, threads: int) -> None:
        w = min(Term.width(), 96)
        rows = [
            Term.kv("Target",    f"{NEXUS.GOLD}{target}{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Generated", f"{NEXUS.LIME}{state.success_count}{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Activated", f"{NEXUS.CYAN}{state.activated_count}{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Pending",   f"{NEXUS.ORANGE}{state.success_count - state.activated_count}{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Region",    f"{NEXUS.MAGENTA}{region}{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Mode",      f"{NEXUS.CYAN}{mode_label} · {threads} threads{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Duration",  f"{NEXUS.ICE}{elapsed:.2f}s{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Accounts",  f"{NEXUS.BLUE}{Config.ACCOUNTS_FILE}{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("CSV Log",   f"{NEXUS.BLUE}{Config.ACTIVATION_RESULTS_FILE}{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
            Term.kv("Credit",    f"{NEXUS.BOLD}{NEXUS.GOLD}MASTER OFFICIAL{NEXUS.RESET}", NEXUS.SILVER, NEXUS.WHITE),
        ]
        print()
        Term.box("OPERATION REPORT", rows, NEXUS.GREEN, w, NEXUS.GOLD)
        print()


# ═══════════════════════════════════════════════════════════════════════════
#  NETWORK
# ═══════════════════════════════════════════════════════════════════════════
class NetService:
    @staticmethod
    def random_ua() -> str:
        return random.choice(USER_AGENTS)

    @staticmethod
    def rotated_session() -> requests.Session:
        s = requests.Session()
        ad = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20, max_retries=0)
        s.mount('https://', ad)
        s.mount('http://', ad)
        with state.ip_lock:
            state.ip_counter += 1
            if state.ip_counter >= 20:
                state.ip_counter = 0
                if state.proxy_list:
                    p = random.choice(state.proxy_list)
                    s.proxies = {'http': p, 'https': p}
        return s


# ═══════════════════════════════════════════════════════════════════════════
#  GARENA CLIENT
# ═══════════════════════════════════════════════════════════════════════════
class GarenaClient:
    def __init__(self):
        self.session = NetService.rotated_session()

    def major_login(self, access_token: str, open_id: str, lang: str) -> Optional[Dict[str, str]]:
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
            raw = raw.replace(b'02-344afb0e-593c-40b7-92f2-171972f74807', rnd_dev)

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
            resp = self.session.post(
                "https://loginbp.ppmainecoonghj.com/MajorLogin",
                headers=headers, data=enc, verify=False, timeout=5
            )
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
        except Exception:
            pass
        return None


# ═══════════════════════════════════════════════════════════════════════════
#  ACTIVATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════
class ActivationEngine:
    @staticmethod
    def activate(uid: str, password: str) -> Dict[str, Any]:
        uid = str(uid).strip()
        password = str(password).strip()
        if not uid or not password:
            return {"activated": False, "status": "INVALID_DATA", "message": "UID/Password missing"}
        try:
            with state.activation_lock:
                now = time.time()
                wait = Config.ACTIVATION_COOLDOWN - (now - state.last_activation_time)
                if wait > 0:
                    time.sleep(wait)
                state.last_activation_time = time.time()

            r = requests.get(
                Config.ACTIVATION_API,
                params={"uid": uid, "password": password},
                timeout=Config.ACTIVATION_TIMEOUT, verify=False
            )
            try:
                data = r.json()
                msg = data.get("message", data.get("error", r.text))
            except ValueError:
                msg = r.text
            msg = str(msg).replace("\n", " ")[:300]

            if 200 <= r.status_code < 300:
                low = msg.lower()
                if any(k in low for k in ["success", "activated", "ok", "done", "already", "true"]):
                    return {"activated": True, "status": "SUCCESS", "message": msg}
                return {"activated": True, "status": "SUCCESS", "message": msg or "Activated"}
            return {"activated": False, "status": f"HTTP_{r.status_code}", "message": msg}
        except requests.Timeout:
            return {"activated": False, "status": "TIMEOUT", "message": "Request timed out"}
        except requests.RequestException as e:
            return {"activated": False, "status": "NETWORK_ERROR", "message": str(e)[:200]}
        except Exception as e:
            return {"activated": False, "status": "ERROR", "message": str(e)[:200]}


# ═══════════════════════════════════════════════════════════════════════════
#  ACCOUNT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════
class AccountGenerator:
    @staticmethod
    def save_record(data: Dict[str, Any]) -> None:
        try:
            with state.lock:
                accounts = []
                if os.path.exists(Config.ACCOUNTS_FILE):
                    try:
                        with open(Config.ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
                            file_data = json.load(f)
                            if isinstance(file_data, list):
                                accounts = file_data
                    except Exception:
                        pass
                accounts.append({
                    "uid": data["uid"],
                    "password": data["password"],
                    "account_id": data["account_id"],
                    "name": data["name"],
                    "region": data["region"],
                    "date_created": data["date_created"],
                    "activated": data.get("activated", False),
                    "activation_status": data.get("activation_status", ""),
                    "activation_message": data.get("activation_message", ""),
                    "jwt_token": data.get("jwt_token", ""),
                    "creator": Config.BRAND,
                    "brand": Config.BRAND_TAG,
                })
                with open(Config.ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(accounts, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    @staticmethod
    def save_activation_result(uid: str, status: str, message: str) -> None:
        with state.results_lock:
            state.activation_results.append([uid, status, message])

    @classmethod
    def create_one(cls, region: str, prefix: str) -> Optional[Dict[str, Any]]:
        for _ in range(2):
            if state.exit_flag:
                return None
            try:
                api = GarenaClient()
                password = SecurityEngine.generate_ultra_secure_password()

                reg_payload = json.dumps({
                    "app_id": 100067, "client_type": 2,
                    "password": password, "source": 2,
                }, separators=(',', ':'))
                headers_reg = {
                    "User-Agent": NetService.random_ua(),
                    "Connection": "Keep-Alive",
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "Authorization": f"Signature {SecurityEngine.generate_signature(reg_payload)}",
                    "Content-Type": "application/json; charset=utf-8",
                    "Cookie": "datadome=oYpIhVco_RFvLHe_T9KFd5wuY0gcQuNfrlt4rHJY5QOkwv4TGt8gPMK32MbHuBdzJyfXnXlfzNZT_2tHr2kys8AMYT2~T71QP1S78_7Pdx4JLOXdSrflPT6cOX2vsyJh",
                    "Host": "100067.connect.garena.com",
                }
                resp_reg = api.session.post(
                    "https://100067.connect.garena.com/api/v2/oauth/guest:register",
                    headers=headers_reg, data=reg_payload, timeout=5, verify=False
                )
                if resp_reg.status_code != 200 or resp_reg.json().get("code") != 0:
                    continue
                uid = resp_reg.json()['data']['uid']

                device_id = f"02-{uuid.uuid4()}"
                tok_payload = json.dumps({
                    "client_id": 100067,
                    "client_secret": Config.API_HEX_KEY,
                    "client_type": 2,
                    "device_id": device_id,
                    "password": password,
                    "response_type": "token",
                    "uid": uid,
                }, separators=(',', ':'))
                headers_tok = headers_reg.copy()
                headers_tok["Cookie"] = "datadome=y23Z3X17pgkMHEt5zY8dqxC6BIf7WJMgC0RXNbqifHT7t9zajKe_hegFb1Ie9_7JixXpz7FRGVodOn~mWPk_NrqIIhUOXDYqKOahzoRQcyEy77GWEMcdA9_MqPJeM5qv"
                resp_tok = api.session.post(
                    "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant",
                    headers=headers_tok, data=tok_payload, timeout=5, verify=False
                )
                if resp_tok.status_code != 200 or resp_tok.json().get("code") != 0:
                    continue
                access_token = resp_tok.json()['data']['access_token']
                open_id     = resp_tok.json()['data']['open_id']

                keystream = [0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,
                             0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]
                field = codecs.decode(
                    ''.join(chr(ord(open_id[i]) ^ keystream[i % len(keystream)]) for i in range(len(open_id)))
                    .encode('unicode_escape').decode('utf-8'), 'unicode_escape'
                ).encode('latin1')

                name = f"{prefix}{random.randint(10000, 99999)}"
                lang = Config.REGION_LANG.get(region.upper(), "en")

                proto = ProtoBuilder.build({
                    1: name, 2: access_token, 3: open_id,
                    5: 102000007, 6: 4, 7: 1, 13: 1, 14: field,
                    15: lang, 16: 1, 17: 1,
                })
                enc_major = bytes.fromhex(SecurityEngine.encrypt_api_payload(proto.hex()))
                headers_major = {
                    "User-Agent": NetService.random_ua(),
                    "Accept-Encoding": "deflate, gzip",
                    "X-GA-SV": "1789535859",
                    "Authorization": "Bearer",
                    "X-GA": "v1 1",
                    "ReleaseVersion": "OB55",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Unity-Version": "2018.4.12f1",
                    "Host": "loginbp.ppmainecoonghj.com",
                }
                api.session.post(
                    "https://loginbp.ppmainecoonghj.com/MajorRegister",
                    headers=headers_major, data=enc_major, verify=False, timeout=5
                )

                login_data = api.major_login(access_token, open_id, lang)
                if not login_data:
                    continue

                act = ActivationEngine.activate(str(uid), password)
                cls.save_activation_result(str(uid), act["status"], act["message"])

                record = {
                    "uid": int(uid),
                    "password": password,
                    "account_id": login_data["account_id"],
                    "name": name,
                    "region": region,
                    "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "activated": act["activated"],
                    "activation_status": act["status"],
                    "activation_message": act["message"],
                    "jwt_token": login_data["jwt_token"],
                    "creator": Config.BRAND,
                    "brand": Config.BRAND_TAG,
                }
                cls.save_record(record)
                return record
            except Exception:
                pass
        return None


# ═══════════════════════════════════════════════════════════════════════════
#  WORKER
# ═══════════════════════════════════════════════════════════════════════════
def worker_task(region: str, prefix: str, target: int) -> None:
    while not state.exit_flag:
        with state.lock:
            if state.success_count >= target:
                break
        acc = AccountGenerator.create_one(region, prefix)
        if acc:
            with state.lock:
                if state.success_count >= target:
                    break
                state.success_count += 1
                if acc.get("activated", False):
                    state.activated_count += 1
                curr = state.success_count
            UI.account_card(curr, target, acc)


# ═══════════════════════════════════════════════════════════════════════════
#  SIGNAL / SHUTDOWN
# ═══════════════════════════════════════════════════════════════════════════
def _shutdown(signum, frame):
    print(f"\n{NEXUS.ORANGE}{NEXUS.BOLD}[!] M A S T E R → Stopping gracefully…{NEXUS.RESET}")
    state.exit_flag = True
    sys.exit(0)


signal.signal(signal.SIGINT, _shutdown)
signal.signal(signal.SIGTERM, _shutdown)


def save_csv() -> None:
    try:
        with open(Config.ACTIVATION_RESULTS_FILE, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f)
            w.writerow(["uid", "status", "response"])
            with state.results_lock:
                w.writerows(state.activation_results)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════
def run() -> None:
    Banner.render(animate=True)
    Banner.credits_panel()

    state.proxy_list = []

    # ═══ SERVER SELECTION ═══
    region = UI.server_menu()
    if not region:
        return

    # ═══ INPUT: Prefix + Count ═══
    print()
    Anim.spinner("Initializing input channel…", 0.8, NEXUS.CYAN)
    prefix = input(f"  {NEXUS.BOLD}{NEXUS.MAGENTA}▸ {NEXUS.WHITE}Name Prefix {NEXUS.STEEL}:{NEXUS.RESET} ").strip()
    try:
        target = int(input(f"  {NEXUS.BOLD}{NEXUS.MAGENTA}▸ {NEXUS.WHITE}Generate Count {NEXUS.STEEL}:{NEXUS.RESET} ").strip())
    except ValueError:
        Anim.glitch("  INVALID COUNT", NEXUS.RED, 0.5)
        return

    Term.clear()
    Banner.render(animate=False)
    Banner.credits_panel()

    # ═══ TURBO MODE — AUTOMATIC 16 THREADS ═══
    threads = Config.TURBO_THREADS          # 16
    mode_label = Config.MODE_LABEL          # "TURBO"
    Config.ACTIVATION_COOLDOWN = 0.4

    # ═══ ENGINE ONLINE BOX ═══
    print()
    w = 42
    Term.box("ENGINE ONLINE",
        [
            Term.kv('Region', region, NEXUS.SILVER, NEXUS.GOLD),
            Term.kv('Threads', f'{threads} (Auto)', NEXUS.SILVER, NEXUS.CYAN),
            Term.kv('Mode', mode_label, NEXUS.SILVER, NEXUS.CYAN),
            Term.kv('Cooldown', f'{Config.ACTIVATION_COOLDOWN}s', NEXUS.SILVER, NEXUS.MAGENTA),
            Term.kv('Target', str(target), NEXUS.SILVER, NEXUS.LIME),
            Term.kv('Brand', 'MASTER', NEXUS.SILVER, NEXUS.GOLD),
            Term.kv('Credit', 'MASTER OFFICIAL', NEXUS.SILVER, NEXUS.GOLD),
        ],
        NEXUS.CYAN, w, NEXUS.GOLD
    )
    print()
    Anim.spinner("Igniting worker threads…", 1.0, NEXUS.LIME)

    # ═══ START WORKERS ═══
    start = time.time()
    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = [ex.submit(worker_task, region, prefix, target) for _ in range(threads)]
        try:
            while any(f.running() for f in futures):
                time.sleep(0.05)
                with state.lock:
                    if state.success_count >= target:
                        break
        except KeyboardInterrupt:
            _shutdown(None, None)

    elapsed = time.time() - start
    save_csv()
    UI.summary(region, target, elapsed, mode_label, threads)


if __name__ == "__main__":
    run()