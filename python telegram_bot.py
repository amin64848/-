from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import instaloader
import requests
import os

# توکن ربات تلگرام (از BotFather دریافت کنید)
TELEGRAM_TOKEN = '8000392501:AAGc6_lZGpK2noDl4is13TrokjH-WBSYmyU'

# تابع برای دانلود محتوای اینستاگرام
def download_instagram_media(url):
    L = instaloader.Instaloader()
    try:
        shortcode = url.split("/")[-2]  # استخراج shortcode از لینک
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        if post.is_video:
            media_url = post.video_url
            media_type = 'video'
        else:
            media_url = post.url
            media_type = 'photo'
        
        # دانلود محتوا
        response = requests.get(media_url)
        if response.status_code == 200:
            file_name = f"{post.shortcode}.mp4" if post.is_video else f"{post.shortcode}.jpg"
            with open(file_name, 'wb') as file:
                file.write(response.content)
            return file_name, media_type
        else:
            return None, None
    except Exception as e:
        print(f"خطا در دانلود: {e}")
        return None, None

# تابع شروع
async def start(update: Update, context):
    await update.message.reply_text('سلام! لینک پست اینستاگرام را برای من بفرستید.')

# تابع مدیریت پیام‌ها
async def handle_message(update: Update, context):
    user_message = update.message.text
    if "instagram.com" in user_message:
        await update.message.reply_text("در حال دانلود محتوا... لطفاً صبر کنید.")
        file_name, media_type = download_instagram_media(user_message)
        if file_name:
            if media_type == 'video':
                await update.message.reply_video(video=open(file_name, 'rb'))
            else:
                await update.message.reply_photo(photo=open(file_name, 'rb'))
            os.remove(file_name)  # حذف فایل پس از ارسال
        else:
            await update.message.reply_text("خطا در دانلود محتوا. لطفاً لینک را بررسی کنید.")
    else:
        await update.message.reply_text("لطفاً یک لینک معتبر اینستاگرام ارسال کنید.")

# تابع اصلی
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # افزودن دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()
