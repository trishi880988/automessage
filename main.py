import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from database import add_user, add_referral, get_referrals
from config import TOKEN, CHANNEL_LINK

# लॉगिंग सेटअप
logging.basicConfig(level=logging.INFO)

# बॉट और डिस्पैचर इनिशियलाइज़ करना
bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()

# /start कमांड हैंडलर
@dp.message(Command("start"))
async def start_cmd(message: Message):
    referrer_id = None
    if " " in message.text:
        referrer_id = message.text.split()[1]
        if referrer_id.isdigit() and int(referrer_id) != message.from_user.id:
            add_referral(int(referrer_id))

    add_user(message.from_user.id, referrer_id)

    referral_link = f"https://t.me/{(await bot.get_me()).username}?start={message.from_user.id}"
    text = (f"👋 *Welcome!* Share your referral link with 10 friends to unlock the secret channel!\n\n"
            f"🔗 Your referral link:\n{referral_link}\n\n"
            f"✅ You have {get_referrals(message.from_user.id)} referrals so far.")

    await message.answer(text)

# /check कमांड हैंडलर
@dp.message(Command("check"))
async def check_cmd(message: Message):
    count = get_referrals(message.from_user.id)
    if count >= 10:
        await message.answer(f"🎉 Congratulations! Here is your exclusive channel link: {CHANNEL_LINK}")
    else:
        await message.answer(f"👥 You have {count}/10 referrals. Share your link to unlock the channel!")

# बॉट स्टार्ट करने का फंक्शन
async def main():
    await dp.start_polling(bot)

# अगर फ़ाइल डायरेक्ट रन हो रही है तो बॉट स्टार्ट करो
if __name__ == "__main__":
    asyncio.run(main())
