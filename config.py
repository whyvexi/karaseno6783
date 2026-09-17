import os

from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int = 0) -> int:
    raw = os.getenv(name, "").strip()
    return int(raw) if raw.lstrip("-").isdigit() else default


def _ids(name: str) -> set[int]:
    return {
        int(x)
        for x in os.getenv(name, "").replace(" ", "").split(",")
        if x.strip().isdigit()
    }


# ─── Telegram Bot ───
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS = _ids("ADMIN_IDS")

# ─── Database ───
DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite+aiosqlite:///./exam_bot.db"
).strip()

# ─── Platega.io ───
PLATEGA_MERCHANT_ID = os.getenv("PLATEGA_MERCHANT_ID", "").strip()
PLATEGA_SECRET = os.getenv("PLATEGA_SECRET", "").strip()
PLATEGA_BASE_URL = os.getenv("PLATEGA_BASE_URL", "https://app.platega.io").strip().rstrip("/")
PLATEGA_METHOD_CARD = _int("PLATEGA_METHOD_CARD", 11)
PLATEGA_METHOD_SBP = _int("PLATEGA_METHOD_SBP", 2)
PLATEGA_RETURN_URL = os.getenv("PLATEGA_RETURN_URL", "https://t.me").strip()

PLATEGA_ENABLED = bool(PLATEGA_MERCHANT_ID and PLATEGA_SECRET)

# ─── CryptoBot / Crypto Pay API ───
CRYPTO_PAY_TOKEN = os.getenv("CRYPTO_PAY_TOKEN", "").strip()
CRYPTO_ASSET = os.getenv("CRYPTO_ASSET", "USDT").strip()
CRYPTO_ENABLED = bool(CRYPTO_PAY_TOKEN)

# ─── Webhook сервер ───
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "").strip()
WEBHOOK_PORT = _int("WEBHOOK_PORT", 8080)
WEBHOOK_PATH_PLATEGA = os.getenv(
    "WEBHOOK_PATH_PLATEGA", "/webhook/platega"
).strip()
WEBHOOK_PATH_CRYPTO = os.getenv(
    "WEBHOOK_PATH_CRYPTO", "/webhook/crypto"
).strip()

# ─── Feature-флаги ───
STARS_ENABLED = os.getenv("STARS_ENABLED", "1") == "1"

FREE_DAILY_LIMIT = 3

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN не задан. Скопируйте .env.example в .env и заполните."
    )
