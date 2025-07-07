from aiogram import Bot, Dispatcher, types, executor
import requests
import sqlite3
from datetime import datetime, timedelta

API_TOKEN = '7256696317:AAELyq9iOXaDpLJ5NYf0_yl1WUx353sJmaE'
OPENAI_API_KEY = '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'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

AI_API_URL = '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'

def save_message(user_id, message):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO feelings (user_id, message, date) VALUES (?, ?, ?)",
              (user_id, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_last_message(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT message, date FROM feelings WHERE user_id = ? ORDER BY date DESC LIMIT 1", (user_id,))
    result = c.fetchone()
    conn.close()
    return result

@dp.message_handler()
async def reply(message: types.Message):
    user_message = message.text
    user_id = message.from_user.id

    # گرفتن آخرین پیام کاربر
    last = get_last_message(user_id)
    reminder_text = ""

    if last:
        last_msg, last_date = last
        last_time = datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_time) > timedelta(hours=24):
            reminder_text = f"عزیز دلم، دیروز گفتی '{last_msg}'… حالت بهتر شده؟ 🌸"

    # ثبت پیام جدید
    save_message(user_id, user_message)

    # درخواست به OpenAI
    prompt_system = "تو یه دوست صمیمی و مهربون و دخترونه هستی. خیلی دلنشین و دلداری میدی، همیشه لحن دوست داشتنی داری. جواب هات خودمونی، مهربون و یه کوچولو طولانی باشن."

    response = requests.post(
        AI_API_URL,
        headers={
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 600,
            "temperature": 0.8
        }
    )

    if response.status_code == 200:
        ai_reply = response.json()['choices'][0]['message']['content']
        final_reply = f"{reminder_text}\n\n{ai_reply}" if reminder_text else ai_reply
        await message.reply(final_reply)
    else:
        await message.reply("آخی عزیزم، الان مشکلی پیش اومده. ولی بدون من اینجام کنارت ❤️")

if __name__ == '__main__':
    executor.start_polling(dp)
