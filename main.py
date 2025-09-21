import asyncio
import logging
import os
import json
from pathlib import Path
from typing import List
from aiogram.types import FSInputFile, Document, Video
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InputFile
from dotenv import load_dotenv


# Load environment
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS_RAW = os.getenv("ADMIN_IDS", "")  # comma separated ids

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN .env faylda topilmadi!")


# Parse admin ids into list[int]
def parse_admins(raw: str) -> List[int]:
    ids = []
    for part in (raw or "").split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            logging.warning("ADMIN_IDS ichida noto'g'ri ID: %s", part)
    return ids


ADMIN_IDS = parse_admins(ADMIN_IDS_RAW)

# Paths
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data.json"
SAMPLES_DIR = BASE_DIR / "samples"
SAMPLES_DIR.mkdir(exist_ok=True)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- Data helpers ---
def load_data():
    if not DATA_FILE.exists():
        # create empty list
        DATA_FILE.write_text("[]", encoding="utf-8")
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        logger.exception("data.json o'qishda xato: %s", e)
        return []


def save_data(movies):
    try:
        DATA_FILE.write_text(
            json.dumps(movies, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True
    except Exception as e:
        logger.exception("data.json yozishda xato: %s", e)
        return False


movies = load_data()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# --- Commands ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Assalomu alaykum! 👋\n"
        "Kino botiga xush kelibsiz.\n"
        "Kino kodini yuboring (masalan: 1 yoki 2).\n\n"
        "Adminlar uchun buyruqlar:\n"
        "/addlink <title>|<genre>|<description>|<url> - link bilan kino qo'shadi\n"
        "Yoki fayl yuboring (document) va captionga: title|genre|description yozing.\n"
        "/movies - kinolar ro'yxati\n"
        "/deletemovie <raqam> - kino o'chirish (admin)\n"
        "/upload - fayl yuklash bo'yicha ko'rsatma (admin)"
    )


@dp.message(Command("movies"))
async def cmd_movies(message: Message):
    movies_local = load_data()
    if not movies_local:
        await message.answer("Hozircha kinolar roʻyxati boʻsh.")
        return

    lines = []
    for i, m in enumerate(movies_local, start=1):
        lines.append(f"{i}. {m.get('title','(No title)')} — {m.get('genre','-')}")
    await message.answer("Mavjud kinolar:\n" + "\n".join(lines))


# --- Admin: add link ---
@dp.message(Command("addlink"))
async def cmd_addlink(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("Bu buyruq faqat adminlarga mavjud.")
        return

    rest = message.text.partition(" ")[2].strip()
    if not rest:
        await message.answer(
            "Foydalanish: /addlink <title>|<genre>|<description>|<url>"
        )
        return

    parts = [p.strip() for p in rest.split("|")]
    if len(parts) != 4:
        await message.answer(
            "Xato format. Kerak: title|genre|description|url (4 qism, '|' bilan ajrating)."
        )
        return

    title, genre, description, url = parts
    new_movie = {
        "title": title,
        "genre": genre,
        "description": description,
        "url": url,
    }

    movies_local = load_data()
    movies_local.append(new_movie)

    if save_data(movies_local):
        await message.answer(f"✅ Kino qo'shildi. Kod: {len(movies_local)}\n{title}")
    else:
        await message.answer(
            "Xatolik: Kino saqlandi, lekin faylga yozishda muammo yuz berdi."
        )


# --- Admin: delete movie ---
@dp.message(Command("deletemovie"))
async def cmd_delete_movie(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("Bu buyruq faqat adminlarga mavjud.")
        return

    rest = message.text.partition(" ")[2].strip()
    if not rest or not rest.isdigit():
        await message.answer("Foydalanish: /deletemovie <raqam>")
        return

    idx = int(rest) - 1
    movies_local = load_data()

    if 0 <= idx < len(movies_local):
        removed = movies_local.pop(idx)
        if save_data(movies_local):
            await message.answer(f"✅ O'chirildi: {removed.get('title')}")
        else:
            await message.answer(
                "Xatolik: o'chirish amalga oshirildi, lekin faylga yozishda muammo yuz berdi."
            )
    else:
        await message.answer("Bunday raqamdagi kino topilmadi.")


# --- Admin: upload command ---
@dp.message(Command("upload"))
async def cmd_upload(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("Bu buyruq faqat adminlarga mavjud.")
        return

    await message.answer(
        "Fayl yuboring va captionga `title|genre|description` yozing."
    )

# --- Admin: fayl qabul qilish (document yoki video) ---
@dp.message(F.document | F.video)
async def handle_file(message: Message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("Bu funksiyani faqat adminlar ishlatadi.")
        return

    caption = (message.caption or "").strip()
    if not caption:
        await message.answer("Fayl uchun caption kerak: title|genre|description")
        return

    parts = [p.strip() for p in caption.split("|")]
    if len(parts) != 3:
        await message.answer(
            "Caption formati: title|genre|description (3 qism, '|' bilan ajrating)."
        )
        return

    title, genre, description = parts

    # Fayl nomini olish
    if message.document:
        file_name = message.document.file_name or f"{message.document.file_unique_id}.bin"
        file_id = message.document.file_id
    else:
        file_name = f"{message.video.file_unique_id}.mp4"
        file_id = message.video.file_id

    safe_filename = file_name.replace(" ", "_")
    dest_path = SAMPLES_DIR / safe_filename

    try:
        await bot.download(file_id, destination=dest_path)
    except Exception as e:
        logger.exception("Faylni yuklashda xato: %s", e)
        await message.answer("❌ Fayl yuklashda xato yuz berdi.")
        return

    rel_path = f"samples/{safe_filename}"
    new_movie = {
        "title": title,
        "genre": genre,
        "description": description,
        "url": rel_path,
    }

    movies_local = load_data()
    movies_local.append(new_movie)

    if save_data(movies_local):
        await message.answer(
            f"✅ Fayl yuklandi va kino qo'shildi.\nKod: {len(movies_local)}\n🎬 {title}"
        )
    else:
        await message.answer(
            "⚠️ Fayl yuklandi, lekin data.json yozishda xato bo'ldi."
        )

# --- User: send number ---
@dp.message(F.text)
async def movie_handler(message: Message):
    text = message.text.strip()
    if not text.isdigit():
        await message.answer("Iltimos, faqat raqam yuboring. Masalan: 1 yoki 2.")
        return

    idx = int(text) - 1
    movies_local = load_data()

    if 0 <= idx < len(movies_local):
        movie = movies_local[idx]
        url = movie.get("url", "")
        title = movie.get("title", "No title")
        genre = movie.get("genre", "")
        description = movie.get("description", "")

        if isinstance(url, str) and (
            url.startswith("http://") or url.startswith("https://")
        ):
            response = (
                f"🎬 <b>{title}</b>\n"
                f"📂 Janr: {genre}\n"
                f"📝 {description}\n\n"
                f"🔗 <a href='{url}'>Kino linki</a>"
            )
            await message.answer(response, parse_mode="HTML")
            return

        local_path = BASE_DIR / str(url)
        if local_path.exists():
            try:
                file = FSInputFile(str(local_path))
                await message.answer_document(
                    document=file,
                    caption=f"{title}\n{genre}\n{description}",
                )
            except Exception as e:
                logger.exception("Fayl yuborishda xato: %s", e)
                await message.answer("Faylni yuborishda xatolik yuz berdi.")
                return
        else:
            await message.answer(
                "Kodni topdim, lekin fayl serverda mavjud emas. Admin bilan bog'laning."
            )
    else:
        await message.answer("Bunday kodli kino topilmadi. ❌")

# Main
async def main():
    logger.info("Bot ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
