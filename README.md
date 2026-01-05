# Telegram Support Bot

Professional Support Bot Aiogram 3.x asosida yozilgan. Botning vazifasi - foydalanuvchilar botga yozgan xabarlarni support guruhiga yuborish va operatorlar javob berishini ta'minlash.

## 🚀 O'rnatish

1. **Dependencies o'rnatish:**
```bash
pip install -r requirements.txt
```

2. **Environment variables sozlash:**
`.env` faylini ochib, o'z tokenlaringizni kiriting:
```
BOT_TOKEN=your_bot_token_here
SUPPORT_GROUP_ID=your_support_group_id_here
ADMIN_IDS=123456789,987654321  # ixtiyoriy
```

3. **Botni ishga tushirish:**
```bash
python main.py
```

## 📁 Loyiha Strukturasi

```
Toshkento/
├── config.py                  # Konfiguratsiya moduli
├── main.py                    # Asosiy kirish nuqtasi
├── handlers/                  # Xabarlarni qayta ishlash
│   ├── __init__.py
│   ├── start_handler.py       # /start command handler
│   ├── message_handler.py     # User xabarlarini guruhga yuborish
│   └── reply_handler.py      # Guruhdan javob berish
├── services/                  # Biznes logika
│   ├── __init__.py
│   ├── user_service.py        # User ma'lumotlarini formatlash
│   ├── message_service.py     # Xabar formatlash
│   └── reply_tracker.py      # Reply tracking system
├── .env                       # Environment variables
├── .gitignore
├── requirements.txt           # Dependencies
└── README.md
```

## ⚙️ Sozlash

- **BOT_TOKEN**: Telegram bot token (@BotFather dan olingan)
- **SUPPORT_GROUP_ID**: Support guruh ID si (xabarlar shu guruhga yuboriladi)
- **ADMIN_IDS**: Admin ID lari (vergul bilan ajratilgan, ixtiyoriy)

Guruh ID sini olish uchun:
1. Botni guruhga qo'shing
2. `python get_chat_id.py` ni ishga tushiring
3. Guruhda biror xabar yuboring
4. Bot sizga guruh ID sini ko'rsatadi

## 🎯 Asosiy Funksiyalar

### 1. Avtomatik Xabar Yuborish
- Har qanday foydalanuvchi botga shaxsiy chatda yozsa, xabar avtomatik support guruhga yuboriladi
- Kim yozganidan qat'iy nazar (admin, oddiy user, yangi user) — hammasi bir xil ishlaydi

### 2. To'liq Ma'lumotlar
Guruhga yuborilgan xabarda quyidagi ma'lumotlar ko'rinadi:
- ✅ Foydalanuvchi ismi
- ✅ Username
- ✅ Telefon raqami (agar mavjud bo'lsa)
- ✅ Telegram ID
- ✅ Xabar turi (text / photo / video / audio / voice / document va h.k.)
- ✅ Xabar mazmuni yoki media
- ✅ Yuborilgan vaqt

### 3. Reply orqali Javob Berish
- Operator support guruhida xabarga REPLY qilib javob yozsa
- Bot ushbu javobni FAQAT o'sha foydalanuvchiga shaxsiy chat orqali yuboradi
- Boshqa foydalanuvchilarga ketmaydi
- Reply ↔ user bog'lanishi aniq ishlaydi

### 4. Random Salomlashuv
- `/start` bosilganda foydalanuvchi ISMI bilan salomlashiladi
- Bir nechta turli salomlashuv matnlari mavjud
- Salomlashuvlar RANDOM tanlanadi
- Bir xil xabarlar ketma-ket yuborilib ban bo'lmasligi uchun dinamik matn ishlatiladi

### 5. Barcha Xabar Turlari
Bot quyidagi formatlarni qabul qiladi va guruhga uzatadi:
- ✅ Text
- ✅ Photo
- ✅ Video
- ✅ Audio
- ✅ Voice
- ✅ Document
- ✅ Video Note
- ✅ Sticker
- ✅ Animation
- ✅ Location
- ✅ Contact

### 6. Xavfsizlik
- Agar fayl .apk yoki xavfli / noma'lum format bo'lsa, guruhda ogohlantirish chiqadi
- Spam va flood holatlari hisobga olinadi
- Exception handling to'liq
- Bot xatolik sabab to'xtab qolmaydi
- Loglar yoziladi

## 📝 Qanday Ishlaydi

1. **Foydalanuvchi botga yozadi** → Xabar avtomatik support guruhga boradi
2. **Operator reply qiladi** → Javob faqat o'sha userga qaytadi

## 🔧 Qo'shimcha Scriptlar

- `get_chat_id.py` - Guruh ID sini topish uchun
- `check_group.py` - Guruhni tekshirish uchun

## 📌 Eslatmalar

- Botni support guruhga qo'shing va admin qiling
- Reply tracking system xotirada saqlanadi (bot restart qilinganda yo'qoladi)
- Barcha xabarlar log qilinadi
- Bot professional va ishonchli ishlaydi
