from pyrogram import Client, filters
from pyrogram.types import Message
import os
import TEL_API
from moviepy.editor import VideoFileClip

proxy = {
    "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
    "hostname": "127.0.0.1",
    "port": 10808
}

app = Client("mehdisticker_bot", api_id=TEL_API.API_ID, api_hash=TEL_API.API_HASH, bot_token=TEL_API.BOT_TOKEN, proxy=proxy)

@app.on_message(filters.command(commands=['start']))
async def start(bot, update):
    await bot.send_message(chat_id=update.chat.id, text="سلام به بات من خوش آمدید لطفا استیکر خود را ارسال کنید.")


@app.on_message(filters.sticker)
async def forward_sticker(client, message: Message):
    try:
        file_id = message.sticker.file_id
        sticker_set_name = message.sticker.set_name

        file_path = await client.download_media(file_id, file_name=f'{sticker_set_name}.webp')
        await client.send_document(chat_id=message.chat.id, document=file_path)

        # تبدیل استیکر به فایل mp4
        video_path = os.path.splitext(file_path)[0] + ".mp4"
        clip = VideoFileClip(file_path)
        
        # تنظیم نرخ فریم (fps)
        clip.set_duration(10)  # مثال: تنظیم نرخ فریم به 10 فریم در ثانیه
        
        clip.write_videofile(video_path)
        
        # ارسال فایل داکیومنت به کاربر
        await client.send_document(chat_id=message.chat.id, document=video_path)

        # حذف فایل‌های موقت
        os.remove(file_path)
        os.remove(video_path)
    except Exception as e:
        print(f'Error: {str(e)}')

# شروع بات
if __name__ == '__main__':
    app.run()
