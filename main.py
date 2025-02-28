import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from database import add_user, add_referral, get_referrals
from config import TOKEN, CHANNEL_LINK

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
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
    
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['check'])
async def check_cmd(message: types.Message):
    count = get_referrals(message.from_user.id)
    if count >= 10:
        await message.answer(f"🎉 Congratulations! Here is your exclusive channel link: {CHANNEL_LINK}")
    else:
        await message.answer(f"👥 You have {count}/10 referrals. Share your link to unlock the channel!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
