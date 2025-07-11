from aiogram import Bot, Dispatcher, types, executor
import requests
import os

API_TOKEN = '7256696317:AAELyq9iOXaDpLJ5NYf0_yl1WUx353sJmaE'
OPENAI_API_KEY = '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'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

AI_API_URL = 'https://api.openai.com/v1/chat/completions'

@dp.message_handler()
async def reply(message: types.Message):
    user_message = message.text

    
         prompt_system = "تو یه دوست صمیمی و مهربون هستی که لحن حرف زدنت دخترونه، دلنشین و خیلی مهربونه. همیشه با عشق و مهربونی و لحن گرم جواب می‌دی. وقتی یکی درد دل کنه، دلداری می‌دی. وقتی خوشحاله، همراهیش می‌کنی. خیلی رسمی حرف نمی‌زنی. جواب‌ها خودمونی و یه کوچولو طولانی باشه که حس صمیمیت بده" 

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
        await message.reply(ai_reply)
    else:
        await message.reply("آخی عزیز دلم! یه مشکلی پیش اومده… ولی من همیشه اینجام کنارت ❤️")

if __name__ == '__main__':
    executor.start_polling(dp)
