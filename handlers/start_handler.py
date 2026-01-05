"""
Start command handler with random greetings.
"""
import random
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


# Random greeting messages
GREETINGS = [
    "👋 Salom, {name}! Xush kelibsiz! Qanday yordam bera olaman?",
    "🎉 Assalomu alaykum, {name}! Sizga qanday yordam kerak?",
    "✨ Salom, {name}! Yordam kerakmi? Men sizga yordam berishga tayyorman!",
    "🌟 Xush kelibsiz, {name}! Savollaringiz bo'lsa, yozing!",
    "💫 Salom, {name}! Qanday muammo bor? Men yechishga yordam beraman!",
    "🎯 Assalomu alaykum, {name}! Qanday yordam kerak?",
    "🚀 Salom, {name}! Sizga qanday yordam bera olaman?",
    "⭐ Xush kelibsiz, {name}! Savollaringiz bo'lsa, yozing!",
]


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Handle /start command with random greeting."""
    user_name = message.from_user.first_name or "Foydalanuvchi"
    
    # Select random greeting
    greeting_template = random.choice(GREETINGS)
    greeting = greeting_template.format(name=user_name)
    
    # Add help text
    help_text = """
    
📝 **Qanday ishlaydi:**
• Sizga yordam kerak bo'lsa, shunchaki xabar yuboring
• Xabaringiz support guruhiga yuboriladi
• Operatorlar tez orada javob beradi

💡 **Eslatma:** Barcha xabarlaringiz support guruhiga yuboriladi.
"""
    
    await message.answer(greeting + help_text)

