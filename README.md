🎬 Telegram Kino Bot

Telegram orqali foydalanuvchi yuborgan kod asosida kinoni qaytaruvchi bot.

📌 Maqsad

Foydalanuvchi botga kino kodini yuboradi (masalan, 2).

Bot shu kodga mos keladigan kino faylini yoki linkini yuboradi.

⚙️ Texnologiyalar

Python 3.10+

aiogram (Telegram bot uchun kutubxona)

SQLite / JSON (ma’lumotlarni vaqtincha saqlash uchun)

🚀 O‘rnatish va ishga tushirish

Loyihani yuklab oling:

git clone https://github.com/username/kino-bot.git
cd kino-bot


Virtual muhit yarating va faollashtiring:

python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Kerakli kutubxonalarni o‘rnating:

pip install -r requirements.txt


.env fayl yarating va BotFather dan olingan tokenni yozing:

BOT_TOKEN=your_telegram_bot_token


Botni ishga tushiring:

python main.py

📂 Loyihaning tuzilishi
kino-bot/
│── main.py            # Botning asosiy fayli
│── data.json          # Kod ↔ Kino ma’lumotlari
│── requirements.txt   # Kutubxonalar ro‘yxati
│── README.md          # Loyihaning hujjati
│── .env               # Maxfiy tokenlar

🗂 Ma’lumotlar bazasi

Oddiy test uchun data.json fayl ishlatiladi:

{
  "1": "kino1.mp4",
  "2": "kino2.mp4",
  "3": "kino3.mp4"
}

🔮 Keyingi rejalar

Kino haqida qisqa ma’lumot qaytarish.

Kod emas, balki kino nomi bo‘yicha ham qidirish.

Admin panel orqali kinolarni qo‘shish/o‘chirish.

Serverga joylash (Render / PythonAnywhere).