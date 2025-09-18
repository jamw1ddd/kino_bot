### FILE: README.md
# 🎬 Telegram Kino Bot


Oddiy Telegram-bot: foydalanuvchi yuborgan **kod** asosida kinoni yuboradi (fayl yoki link).


## Tez boshlash
1. Klonlang:
```bash
git clone https://github.com/username/kino-bot.git
cd kino-bot
```
2. Virtual muhit va kutubxonalarni o'rnating:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. `.env` faylni yarating va BotFather tokenni joylang (`BOT_TOKEN`):
```env
BOT_TOKEN=123456:ABC-DEF
```
4. Test uchun `data.json` ichidagi mapping va sample fayllarni tekshiring.
5. Botni ishga tushiring:
```bash
python main.py
```


## Tuzilishi
- `main.py` — botning asosiy kodi
- `data.json` — kod -> kino (fayl yoki link) mapping
- `requirements.txt` — kerakli kutubxonalar
- `.env.example` — atrof-muhit namunasi


## Ishlash mantig'i
- Foydalanuvchi 1 ta so'z yuboradi (odatda raqam yoki kod).
- Agar kod `data.json` dan topilsa, qiymat kino fayli (local path) yoki URL bo'lishi mumkin.
- Agar qiymat `http` bilan boshlasa, bot link yuboradi; aks holda fayl yuboradi (agar mavjud bo'lsa).


## Eslatma
- Hozircha test uchun local fayl yoki URL ishlatish qulay. Serverga deploy qilinganda fayllarni serverga joylash yoki CDN ishlatish tavsiya etiladi.
"""


"""
### FILE: requirements.txt
python-telegram-bot==20.5
python-dotenv==1.0.0
# agar faylni streaming yuborishni xohlasangiz:
# aiofiles==23.1.0
"""


"""
### FILE: .env.example
# .env faylni .env deb nomlab ichiga quyidagilarni yozing:
BOT_TOKEN=your_telegram_bot_token_here
# Bu loyihada boshqa maxfiy sozlamalar yo'q. Agar kerak bo'lsa, KEY=VALUE tarzida qo'shing.
"""


### FILE: main.py