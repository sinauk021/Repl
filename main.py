from telethon import TelegramClient, events, functions, types, Button
import asyncio
from datetime import datetime, timedelta
import pytz
import requests
import random
import os
import time
from math import ceil
from bs4 import BeautifulSoup

# اطلاعات API تلگرام (حساب کاربری)
api_id = 26499348
api_hash = '0bb16692fda21e16c2f132ad57573709'
phone = '+989960544616'
admin_user_id = 7602039005  # آیدی عددی شما (با @userinfobot چک کنید)

# ساخت کلاینت بدون پروکسی
client = TelegramClient('selfbot_session', api_id, api_hash)

# تنظیم منطقه زمانی
timezone = pytz.timezone('Asia/Tehran')

# متغیرهای وضعیت (تعریف به‌عنوان سراسری)
weather_active = False
auto_msg_active = False
spam_active = False

# لیست‌های محتوا
jokes = [
    "چرا برنامه‌نویسا شب کار می‌کنن؟ چون باگ‌ها توی نور غیبشون می‌زنه!",
    "یه روز اومدم باگ رو فیکس کنم، حالا برنامه‌نویسم گمم!",
    "زندگی مثل کد زدنه، یه خط اشتباه همه‌چیو خراب می‌کنه!"
]
quotes = [
    "زندگی کوتاهه، کد بزن!",
    "هر چی که می‌تونی تصور کنی، شدنیه.",
    "تنها راه انجام کار بزرگ، شروع کردنشه."
]

# تابع گرفتن آب‌وهوا از Open-Meteo
def get_weather(city_name="Tehran"):
    lat, lon = 35.6892, 51.3890  # مختصات تهران
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}¤t_weather=true"
    try:
        response = requests.get(url)
        data = response.json()
        temp = data['current_weather']['temperature']
        wind = data['current_weather']['windspeed']
        return f"{temp}°C, باد: {wind} km/h"
    except:
        return "خطا توی گرفتن آب‌وهوا!"

# تابع گرفتن بیو کاربر
def get_user_bio():
    try:
        with open('settings/bio.txt', 'r') as f:
            return f.read().strip()
    except:
        return "بیو تنظیم نشده!"

# آپدیت نام خانوادگی (Last Name)
async def update_last_name():
    global current_time_str
    while True:
        try:
            with open('settings/time.txt', 'r') as f:
                option_enabled = f.read().strip() == 'True'
            with open('settings/heart.txt', 'r') as f:
                heart_enabled = f.read().strip() == 'True'
            with open('settings/mode.txt', 'r') as f:
                mode = f.read().strip()

            if option_enabled:
                current_time = datetime.now(timezone)
                rounded_time = current_time.replace(second=0, microsecond=0) + timedelta(minutes=ceil(current_time.second/60))
                current_time_str = rounded_time.strftime("%H:%M")
                
                if mode == 'Bold':
                    current_time_str = current_time_str.replace("0", "𝟎").replace("1", "𝟏").replace("2", "𝟂").replace("3", "𝟃").replace("4", "𝟄").replace("5", "𝟅").replace("6", "𝟆").replace("7", "𝟇").replace("8", "𝟈").replace("9", "𝟉")
                elif mode == 'Mono':
                    current_time_str = current_time_str.replace("0", "０").replace("1", "１").replace("2", "２").replace("3", "３").replace("4", "４").replace("5", "５").replace("6", "６").replace("7", "７").replace("8", "８").replace("9", "９")
                elif mode == 'Mini':
                    current_time_str = current_time_str.replace("0", "⁰").replace("1", "¹").replace("2", "²").replace("3", "³").replace("4", "⁴").replace("5", "⁵").replace("6", "⁶").replace("7", "⁷").replace("8", "⁸").replace("9", "⁹")
                elif mode == 'rnd':
                    font_options = [
                        ["𝟶", "𝟷", "𝟸", "𝟹", "𝟺", "𝟻", "𝟆", "𝟇", "𝟈", "𝟿"],
                        ["⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨"],
                        ["⓿", "❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽", "❾"],
                        ["0", "𝟙", "ϩ", "Ӡ", "５", "Ϭ", "Ϭ", "7", "𝟠", "۹"],
                        ["⁰", "₁", "²", "₃", "⁴", "₅", "⁶", "₇", "⁸", "₉"],
                        ["０", "１", "２", "３", "４", "５", "６", "７", "８", "９"],
                        ["𝟬", "𝟭", "𝟮", "𝟯", "𝟴", "𝟱", "𝟲", "𝟳", "𝟴", "𝟵"],
                        ["𝟎", "𝟏", "𝟂", "𝟃", "𝟄", "𝟅", "𝟆", "𝟇", "𝟈", "𝟉"],
                        ["𝟶", "𝟷", "𝟸", "𝟹", "𝟺", "𝟻", "𝟆", "𝟇", "𝟈", "𝟿"]
                    ]
                    random_font = random.choice(font_options)
                    current_time_str = current_time_str.translate(str.maketrans("0123456789", "".join(random_font)))
                
                heart_list = ['❤️', '💛', '💚', '💙', '💜', '🖤', '🤍', '🧡', '💖', '💗', '💓', '💞', '💕', '💘', '💝', '💟', '🩵']
                heart = random.choice(heart_list) if heart_enabled else ""

                with open('settings/nameinfo.txt', 'r') as f:
                    user_lname = f.read()
                user_lname = user_lname.replace("time", current_time_str).replace("heart", heart)
                await client(functions.account.UpdateProfileRequest(last_name=user_lname))
        
        except Exception as e:
            print(f"خطا توی آپدیت نام خانوادگی: {e}")
            await asyncio.sleep(300)
        
        await asyncio.sleep(60)

# آپدیت بیو
async def update_about():
    while True:
        try:
            with open('settings/bioinfo.txt', 'r') as f:
                bio_info_enabled = f.read().strip() == 'True'
            with open('settings/mode.txt', 'r') as f:
                mode = f.read().strip()

            if bio_info_enabled:
                current_time = datetime.now(timezone)
                current_time_str = current_time.strftime("%H:%M")
                current_date = current_time.strftime("%Y/%m/%d")

                if mode == 'Bold':
                    current_time_str = current_time_str.replace("0", "𝟎").replace("1", "𝟏").replace("2", "𝟂").replace("3", "𝟃").replace("4", "𝟄").replace("5", "𝟅").replace("6", "𝟆").replace("7", "𝟇").replace("8", "𝟈").replace("9", "𝟉")
                    current_date = current_date.replace("0", "𝟎").replace("1", "𝟏").replace("2", "𝟂").replace("3", "𝟃").replace("4", "𝟄").replace("5", "𝟅").replace("6", "𝟆").replace("7", "𝟇").replace("8", "𝟈").replace("9", "𝟉")
                elif mode == 'Mono':
                    current_time_str = current_time_str.replace("0", "０").replace("1", "１").replace("2", "２").replace("3", "３").replace("4", "４").replace("5", "５").replace("6", "６").replace("7", "７").replace("8", "８").replace("9", "９")
                    current_date = current_date.replace("0", "０").replace("1", "１").replace("2", "２").replace("3", "３").replace("4", "４").replace("5", "５").replace("6", "６").replace("7", "７").replace("8", "８").replace("9", "９")
                elif mode == 'Mini':
                    current_time_str = current_time_str.replace("0", "⁰").replace("1", "¹").replace("2", "²").replace("3", "³").replace("4", "⁴").replace("5", "⁵").replace("6", "⁶").replace("7", "⁷").replace("8", "⁸").replace("9", "⁹")
                    current_date = current_date.replace("0", "⁰").replace("1", "¹").replace("2", "²").replace("3", "³").replace("4", "⁴").replace("5", "⁵").replace("6", "⁶").replace("7", "⁷").replace("8", "⁸").replace("9", "⁹")
                elif mode == 'rnd':
                    font_options = [
                        ["𝟶", "𝟷", "𝟸", "𝟹", "𝟺", "𝟻", "𝟆", "𝟇", "𝟈", "𝟿"],
                        ["⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨"],
                        ["⓿", "❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽", "❾"],
                        ["0", "𝟙", "ϩ", "Ӡ", "５", "Ϭ", "Ϭ", "7", "𝟠", "９"],
                        ["⁰", "₁", "²", "₃", "⁴", "₅", "⁶", "₇", "⁸", "₉"],
                        ["０", "１", "２", "３", "４", "５", "６", "７", "８", "９"],
                        ["𝟬", "𝟭", "𝟮", "𝟯", "𝟴", "𝟱", "𝟲", "𝟳", "𝟴", "𝟵"],
                        ["𝟎", "𝟏", "𝟂", "𝟃", "𝟄", "𝟅", "𝟆", "𝟇", "𝟈", "𝟉"],
                        ["𝟶", "𝟷", "𝟸", "𝟹", "𝟺", "𝟻", "𝟆", "𝟇", "𝟈", "𝟿"]
                    ]
                    random_font = random.choice(font_options)
                    current_time_str = current_time_str.translate(str.maketrans("0123456789", "".join(random_font)))
                    current_date = current_date.translate(str.maketrans("0123456789", "".join(random_font)))
                
                heart_list = ['❤️', '💛', '💚', '💙', '💜', '🖤', '🤍', '🧡', '💖', '💗', '💓', '💞', '💕', '💘', '💝', '💟', '🩵']
                heart = random.choice(heart_list)

                bio = get_user_bio().replace("time", current_time_str).replace("heart", heart).replace("DATE", current_date)
                await client(functions.account.UpdateProfileRequest(about=bio))
        
        except Exception as e:
            print(f"خطا توی آپدیت بیو: {e}")
            await asyncio.sleep(300)
        
        await asyncio.sleep(60)

# آپدیت اسم (First Name)
async def update_first_name():
    prev_name = ''
    while True:
        try:
            with open('settings/rnamest.txt', 'r') as f:
                rname_enabled = f.read().strip() == 'True'
            if rname_enabled:
                with open('settings/rname.txt', 'r') as f:
                    names = f.read().strip().split(',')
                if len(names) >= 1:
                    first_name = random.choice(names).strip()
                    while first_name == prev_name:
                        first_name = random.choice(names).strip()
                    await client(functions.account.UpdateProfileRequest(first_name=first_name))
                    prev_name = first_name
            
            current_time = datetime.now(timezone)
            rounded_time = current_time.replace(second=0, microsecond=0) + timedelta(minutes=ceil(current_time.second/60))
            next_minute = (rounded_time + timedelta(minutes=1)).replace(second=0, microsecond=0)
            time_until_next_minute = (next_minute - current_time).total_seconds()
            await asyncio.sleep(time_until_next_minute)
        
        except Exception as e:
            print(f"خطا توی آپدیت اسم: {e}")
            await asyncio.sleep(300)

# تایپر جدید (برای سلف‌بات)
@client.on(events.NewMessage())
async def typer_handler(event):
    me = await client.get_me()
    chatid = int(me.id)
    if event.sender_id == chatid and str(event.raw_text).startswith("."):
        msg = event.raw_text
        await event.delete()
        msg = msg.replace(".", "")
        txt = ""
        mess = None
        for i in range(len(msg)):
            txt += msg[i]
            if i == 0:
                mess = await client.send_message(entity=event.chat_id, message=msg[0])
            elif msg[i] not in [" ", "\n"]:
                await client.edit_message(entity=event.chat_id, message=mess.id, text=txt)
            time.sleep(0.001)

# دستورات متنی برای سلف‌بات (توی Saved Messages)
@client.on(events.NewMessage(chats='me'))
async def handle_self_commands(event):
    global weather_active, auto_msg_active, spam_active  # اعلام همه متغیرهای سراسری در ابتدای تابع
    text = event.message.text.strip()
    print(f"دستور سلف‌بات دریافت شد: {text}")  # دیباگ
    
    if text == '/info':
        me = await client.get_me()
        about = getattr(me, 'about', 'نداره')
        await event.respond(f"اسم: {me.first_name}\nآیدی عددی: {me.id}\nآیدی متنی: @{me.username or 'نداره'}\nبیو: {about}")
    
    elif text == '/test':
        await event.respond("تست سلف‌بات موفقیت‌آمیز بود!")

    elif text == '/weather':
        weather_active = True
        await event.respond("آب‌وهوا توی اسم و بیو روشن شد!")
    
    elif text == '/weatheroff':
        weather_active = False
        await event.respond("آب‌وهوا خاموش شد!")
    
    elif text == '/auto':
        auto_msg_active = True
        await event.respond("پیام خودکار فعال شد!")
        while auto_msg_active:
            await event.respond(f"پیام خودکار | زمان: {datetime.now(timezone).strftime('%H:%M:%S')}")
            await asyncio.sleep(300)
    
    elif text == '/autooff':
        auto_msg_active = False
        await event.respond("پیام خودکار غیرفعال شد!")
    
    elif text.startswith('/spam'):
        args = text.split()
        if len(args) >= 3:
            count = int(args[1])
            message = " ".join(args[2:])
            spam_active = True
            await event.respond(f"اسپم شروع شد! {count} پیام...")
            for _ in range(count):
                if not spam_active:
                    break
                await event.respond(message)
                await asyncio.sleep(1)
            await event.respond("اسپم تموم شد!")
        else:
            await event.respond("فرمت: /spam <تعداد> <پیام>")
    
    elif text == '/spamoff':
        spam_active = False
        await event.respond("اسپم متوقف شد!")
    
    elif text == '/joke':
        await event.respond(random.choice(jokes))
    
    elif text == '/quote':
        await event.respond(random.choice(quotes))
    
    elif text == '/ping':
        start = datetime.now()
        msg = await event.respond("پینگ...")
        ping_time = (datetime.now() - start).total_seconds() * 1000
        await msg.edit(f"پینگ: {ping_time:.0f} میلی‌ثانیه")
    
    elif text == '/panel':
        print("درخواست پنل دریافت شد!")  # دیباگ
        try:
            buttons = [[Button.inline("فارسی 🇮🇷", b"langfa")]]
            await event.respond("سلام ادمین عزیز، لطفاً زبان هلپر را انتخاب کنید", buttons=buttons)
            print("پنل با موفقیت ارسال شد!")  # دیباگ
        except Exception as e:
            print(f"خطا در ارسال پنل: {e}")  # دیباگ

# Inline Query برای پنل (برای سلف‌بات)
@client.on(events.InlineQuery)
async def inline_handler(event):
    print(f"Inline Query از {event.sender_id}: {event.text}")  # دیباگ
    if event.sender_id == admin_user_id and event.text == "/panel":
        try:
            text = "سلام، پنل سلف‌بات شما"
            buttons = [[Button.inline("فعال کردن زمان", b"turn_on"), Button.inline("خاموش کردن زمان", b"turn_off")],
                       [Button.inline("فعال کردن بیو", b"turn_on_bio"), Button.inline("خاموش کردن بیو", b"turn_off_bio")],
                       [Button.inline("مشاهده بیو", b"bio")],
                       [Button.inline("بستن", b"close_panel")]]
            builder = event.builder
            result = builder.article(
                title="پنل سلف‌بات",
                description="مدیریت پروفایل",
                text=text,
                buttons=buttons
            )
            await event.answer([result])
            print("پنل با موفقیت ارسال شد!")  # دیباگ
        except Exception as e:
            print(f"خطا توی Inline Query: {e}")  # دیباگ
    else:
        print(f"دسترسی رد شد برای {event.sender_id} - آیدی ادمین: {admin_user_id}")  # دیباگ

# Callback Query برای دکمه‌ها
@client.on(events.CallbackQuery)
async def callback(event):
    print(f"Callback از {event.sender_id}: {event.data}")  # دیباگ
    if event.sender_id != admin_user_id:
        print(f"دسترسی رد شد برای {event.sender_id} - آیدی ادمین: {admin_user_id}")  # دیباگ
        return
    
    try:
        if event.data == b"turn_on":
            with open('settings/time.txt', 'w') as f:
                f.write('True')
            await event.edit("زمان فعال شد!")
        elif event.data == b"turn_off":
            with open('settings/time.txt', 'w') as f:
                f.write('False')
            await event.edit("زمان غیرفعال شد!")
        elif event.data == b"turn_on_bio":
            with open('settings/bioinfo.txt', 'w') as f:
                f.write('True')
            await event.edit("بیو فعال شد!")
        elif event.data == b"turn_off_bio":
            with open('settings/bioinfo.txt', 'w') as f:
                f.write('False')
            await event.edit("بیو غیرفعال شد!")
        elif event.data == b"bio":
            bio = get_user_bio()
            await event.edit(f"بیو فعلی: {bio}")
        elif event.data == b"close_panel":
            await event.edit("پنل بسته شد!")
        print("دکمه با موفقیت پردازش شد!")  # دیباگ
    except Exception as e:
        print(f"خطا توی Callback: {e}")  # دیباگ

# راه‌اندازی سلف‌بات
async def main():
    if not os.path.exists('settings'):
        os.makedirs('settings')
    for file in ['time.txt', 'heart.txt', 'mode.txt', 'bioinfo.txt', 'rnamest.txt', 'nameinfo.txt', 'rname.txt', 'bio.txt']:
        if not os.path.exists(f'settings/{file}'):
            with open(f'settings/{file}', 'w') as f:
                if file == 'mode.txt':
                    f.write('Default')
                elif file == 'nameinfo.txt':
                    f.write('time heart')
                elif file == 'rname.txt':
                    f.write('Name1,Name2,Name3')
                elif file == 'bio.txt':
                    f.write('Bio time DATE heart')
                else:
                    f.write('False')
    
    await client.start(phone)
    print("سلف‌بات شروع شد!")
    await asyncio.gather(
        update_last_name(),
        update_about(),
        update_first_name(),
        client.run_until_disconnected()
    )

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except Exception as e:
        print(f"خطای اصلی: {e}")