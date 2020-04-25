# coding: UTF-8
from copy import deepcopy
from pyrogram import Client, Filters, KeyboardButton, ReplyKeyboardMarkup, Message
import json
import datetime as dt
import requests
from math import *
from random import choice

xizmat_narxi = {}
time = dt.datetime.now()
info = {}
komment = {}
bot_token = "961191162:AAFCjhCFTcA2ZQir7fjqggDGk20esrV3v9Y"
api_hash = "9f8cd674a86791512c2baebef59a3a09"
api_id = 394876
phone_numbers = {}
buyurtmalar = {}
manzil = {}
geolokatsiya = {}
fakt_kanal_id = -1001354904206
guruh_id = -1001229948049
# komandalar

qoidalar = "📑 Qoidalar"
ortga = "🔙 Ortga"
menu = "🏠 Asosiy menyu"
buyurtma = "🛵 Buyurtma Berish"
korzina = "🛒 Savat"
ha = "✅ Ha, buyurtma beraman"
yuq = "❌ Yo'q, tozalansin"
qol = "🛒 Savatda qolsin"
tozalash = "🔄 Tozalash"
boglanish = "👨‍💻 Bog'lanish"
manzil_ = "📍 Manzil"
shikoyat = "🖍 Shikoyat qilmoqchiman"
taklif = "✏️ Taklifim bor"
xatolik = "⚠️ Botda hatolik topdim"
shunchaki = "🔖 Shunchaki..."
sozlamalar = "⚙ Sozlamalar"
telefon = "🔘 Telefon raqamni almashtirish"
fikr = {}
# bo'limlar
taomlar = {
    "1⃣ Suyuq Taomlar": [],
    "2⃣ Quyuq Taomlar": [],
    "🍜 Uyg'ur Taomlar": [],
    "🍢 Kaboblar": [],
    "🥗 Salatlar": [],
    "🍻 BAR": [],

}
faktlar = deepcopy(taomlar)
tezt = deepcopy(taomlar)

bosh_shablon = """<b>{} {}  {}° {}</b>

🔴 Yangiyo'l Shahar va Tuman  

<i>👇 Kerakli taomlar bo'limni tanlang:</i>
"""
bosh = ""
ob_havo = "", ""
hafta = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
icon = {
    "01d": "☀️",
    "01n": "🌑",
    "02d": "🌤",
    "02n": "☁️",
    "03d": "⛅️",
    "03n": "☁️",
    "04d": "☁️",
    "04n": "☁️",
    "09d": "🌧",
    "09n": "🌧",
    "10d": "🌦",
    "10n": "🌧",
    "11d": "⛈",
    "11n": "⛈",
    "13d": "❄️",
    "13n": "❄️",
    "50d": "🌫",
    "50n": "🌫",
}

# bo'lim nomi #taom nomi #soni
temp = {}
bot = Client("EZAZ", bot_token=bot_token, api_hash=api_hash, api_id=api_id)


def distance(lat1,long1, lat2,  long2):
    lat1 = lat1 / 180 * pi
    lat2 = lat2 / 180 * pi
    long1 = long1 / 180 * pi
    long2 = long2 / 180 * pi
    r = 6371
    dlon = long1 - long2
    dlat = lat1 - lat2
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return c * r


def save():
    f = open("phone_number.json", "w")
    f.write(json.dumps(phone_numbers))
    f.close()


def load():
    global phone_numbers
    try:
        f = open("phone_number.json", 'r')
    except:
        return
    phone_numbers = json.loads(f.read())


def rasmlilar(m_list):
    n_list = []
    for x in m_list:
        try:
            a = x.caption
            if a:
                n_list.append(x)
        except:
            continue
    return n_list


def fakt(m_list):
    global faktlar
    for x in m_list:
        try:
            if x.text:  # and not faktlar.get(x.text.split('\n')[0].strip(), 0):
                faktlar[x.text.split('\n')[0].strip()].append('\n'.join(x.text.split('\n')[1:]))
        except:
            pass


def yangilash():
    global taomlar
    taomlar = deepcopy(tezt)
    taom = rasmlilar(bot.get_messages(-1001149535338, range(337, 437)))
    fakt(bot.get_messages(fakt_kanal_id, range(100)))
    #    taom += rasmlilar(bot.get_messages(-1001149535338, range(337, 437)))
    for t in taom:
        x = t.caption.split('\n')
        x = [i for i in x if i]
        bolim = x[0].strip()

        nomi = ''
        try:
            nomi = x[1].strip()

            narxi = float(x[2])
        except:
            narxi = 0
        rasm = t.photo.file_id
        if len(x) >= 5:
            variant1 = x[3]
            variant2 = x[4]
            if len(x) > 5:
                description = '\n'.join(x[5:])
            else:
                description = ""
        else:
            variant1 = variant2 = None
            description = ''
        taomlar[bolim].append([rasm, nomi, narxi, variant1, variant2, description])


def get_weather():
    try:
        a = requests.get(
            "http://api.openweathermap.org/data/2.5/weather?lat=41.35&lon=69.29&appid=9993d5f60ccd41752f2ba809ea2682b3")
        x = json.loads(a.text)
        return "{0:+}".format(x["main"]["temp"] - 273.15), icon[x["weather"][0]["icon"]]
    except:
        return


def edit_home():
    global bosh, ob_havo
    if time.minute == dt.datetime.now().minute:
        ob_havo = get_weather() or ob_havo
        bosh = bosh_shablon.format(hafta[dt.date.today().weekday()], dt.date.today(), *ob_havo)


edit_home()
bolimlar = ReplyKeyboardMarkup([
    ["1⃣ Suyuq Taomlar", "2⃣ Quyuq Taomlar"],
    ["🍜 Uyg'ur Taomlar", "🍢 Kaboblar", ],
    ["🍻 BAR", "🥗 Salatlar"],
    [korzina,  # tayyor
     buyurtma],
    [sozlamalar, qoidalar ],
    [boglanish,  # tayyor
     manzil_  # tayyor
     ],

], resize_keyboard=True)
raqamlar = ReplyKeyboardMarkup([
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    [ortga, menu],
    [korzina, ]
], resize_keyboard=True)


@bot.on_message(Filters.command(["start"]))
def handle_start(c, m):
    edit_home()
    yangilash()
    buyurtmalar[m.chat.id] = []
    bot.send_message(m.chat.id,"""Assalomu Alaykum,

EZAZ | Milliy Taomlar botimizga xush kelibsiz.

Iltimos, avval siz bilan bog'lanishimiz uchun o'z raqamingizni 👤 Kontakt ko'rinishda jo'nating yoki pastdagi "📲 Telefon raqamni jo'natish" tugmasini bosing:""",
                     reply_markup=ReplyKeyboardMarkup(
                         [[KeyboardButton("📱 Telefon raqamni jo'natish", request_contact=True), ]],
                         resize_keyboard=True))


@bot.on_message(Filters.contact)
def handle_contact(c, m):
    edit_home()
    phone_numbers[m.chat.id] = m.contact.phone_number
    save()
    bot.send_message(m.chat.id, """
<b>BOT V2.1.0 TEST</b>

Rahmat!
Eslatib o'tamiz: BOT test rejimida qayta ishlanmoqda.Yangi o'zgarishlarga o'tish uchun iltimos /start kommandasini tez-tez jo'natib turing ana shunda o'zgarishlar sizda paydo bo'ladi.
""")
    bot.send_message(m.chat.id, bosh, reply_markup=bolimlar)


@bot.on_message(Filters.text)
def handle_text(c, m: Message):
    edit_home()
    global buyurtmalar, temp, info
    if m.text.lower() == "yangila":
        yangilash()
        return
    if m.chat.id == -1001149535338:
        yangilash()
        return
    if m.chat.id == guruh_id:
        if m.text.lower().startswith("info"):
            text = "Bugun:\n"
            for k, v in info.items():
                text += "{}ta {};\n".format(v, k)
            text += "sotildi"
            bot.send_message(m.chat.id, text)
            return
        elif m.text.lower().startswith("tozala"):
            info = {}
            m.reply("Ma'lumotlar to'liq tozalandi!")
            return
        elif m.text.lower().startswith("javob"):
            if m.text.split("\n")[1] == "hammaga":
                for i in phone_numbers.keys():
                    try:
                        bot.send_message(i, '\n'.join(m.text.split('\n')[2:]))
                    except:
                        pass
            else:
                try:
                    bot.send_message(m.text.split('\n')[1], '\n'.join(m.text.split('\n')[2:]))
                except:
                    pass
            return
    elif m.text == ortga:
        fikr[m.chat.id] = None
        if not temp.get(m.chat.id) or len(temp.get(m.chat.id, [])) <= 1:
            temp[m.chat.id] = None
            bot.send_message(m.chat.id, bosh, reply_markup=bolimlar)
            return
        else:
            # print(1)
            temp[m.chat.id] = [temp[m.chat.id][0]]
            x = []
            try:
                bot.send_message(m.chat.id, choice(faktlar[temp[m.chat.id][0]]))
            except:
                pass
            for i, t in enumerate(taomlar[temp[m.chat.id][0]]):
                a, b = i // 2, i % 2
                if b == 0:
                    x.append([])
                x[a].append(t[1])
            x.append([ortga, korzina])
            x.append([buyurtma])
            # print(2)
            x = ReplyKeyboardMarkup(x, resize_keyboard=True)
            bot.send_message(m.chat.id, "{} :".format(temp[m.chat.id][0]), reply_markup=x)
            return
    elif fikr.get(m.chat.id, 0):
        text = "{} `{}` mavzu: {}\n\n".format(m.from_user.first_name, m.from_user.id, fikr[m.chat.id])
        text += m.text
        bot.send_message(guruh_id, text)
        bot.send_message(m.chat.id, "Rahmat adminstratorlar albatta siz bilan bo'glanadi.", reply_markup=bolimlar)
        fikr[m.chat.id] = None
    elif m.text == manzil_:
        bot.send_location(m.chat.id, 41.120233069494155, 69.07184731700151)
        bot.send_message(m.chat.id, """🍴 Ezaz Milliy Taomlar:

🇺🇿 Toshkent viloyati,Yangiyo'l shahar,Toshkent shox. 34-uy.  
""")
        return
    elif m.text == menu:
        bot.send_message(m.chat.id, bosh, reply_markup=bolimlar)
        temp[m.chat.id] = None
        return
    elif m.text == boglanish:
        x = ReplyKeyboardMarkup([[shikoyat],
                                 [taklif],
                                 [xatolik],
                                 [shunchaki],
                                 [ortga, ]], resize_keyboard=True)
        bot.send_message(m.chat.id, """✉️ Telegram orqali: @EzazAdmin 

📞 Telefon orqali: +998951466616

📧 Elektron Pochta: 
ezazsprt@gmail.com

📷 Instagram: 
http://instagram.com/ezazmilliytaomlar

<b>✍ Marhamat: qay tarzda bog'lanmoqchisiz ?</b>""", reply_markup=x)
        return
    elif m.text == qoidalar:
        bot.send_message(m.chat.id, """
        👤 <b>Hurmatli mijoz,</b>siz tanlagan taomlar uchun doimiy ravishda "Bir martalik" idish qo'shib oboriladi.
shuning uchun BOT avtomatik tarzda Quyuq taom uchun: quyuq idish(1000so'm) suyuq taom uchun: suyuq idish(1500so'm) hisoblaydi.

🛵 Yetkazib berish xizmatimiz Yangiyo'l shahar va Tumanida amal qiladi.Yetkazib berish xizmatimiz 3kmdan uzoq masofaga km hisobida 1000so'mdan qo'shib boriladi.Bu ishni BOTning o'zi avtomatik tarzda bajaradi.

⚠️Bundan tashqari albatta mahsulot yetkazib berilgandan so'ng siz mahsulotlar nomi yozilgan mahsus chekni talab qilishingiz mumkun bo'ladi.

👨‍💻Shikoyat yoki qandaydir taklif murojaatlar bo'lsa "Bog'lanish" bo'limiga o'tishingiz mumkin,Adminstratorlar albatta siz bilan bog'lanadi.

👤 KONTAKTLAR:
@EZAZSUPPORTBOT
+998951466616
+998903366807
""")
    elif m.text == korzina:
        try:
            if not buyurtmalar[m.chat.id]:
                bot.send_message(m.chat.id,
                                 "🧐 Siz hali taom tanlamadingiz \"🔙 Ortga\" qaytib taom tanlang va Savatga yig'ib "
                                 "boring.🛒", reply_markup=ReplyKeyboardMarkup([[ortga]], resize_keyboard=True))
                return
        except KeyError:
            buyurtmalar[m.chat.id] = []
            bot.send_message(m.chat.id,
                             '🧐 Siz hali taom tanlamadingiz "🔙 Ortga" qaytib taom tanlang va Savatga yig\'ib boring.🛒',
                             reply_markup=ReplyKeyboardMarkup([[ortga]], resize_keyboard=True))
            return
        else:
            x = []
            text = "👇 Siz tanlagan taomlar:\n\n"
            for i in buyurtmalar[m.chat.id]:
                # print(i)
                text += "{}x{}: {}00\n".format(i[2], i[0], i[1] * i[2])
                x.append([KeyboardButton("❌ {}ni bekor qilish".format(i[0]), request_contact=False)])
            x.append([buyurtma])
            x.append([tozalash])
            x.append([ortga])
            x = ReplyKeyboardMarkup(x, resize_keyboard=True)
            bot.send_message(m.chat.id, text, reply_markup=x)
            return
    elif m.text == sozlamalar:
        bot.send_message(m.chat.id,
                         "Sozlamalar orqali siz bilan bog'lanishimiz mumkin bo'lgan raqamingizni o'zgartirishingiz mumkin:",
                         reply_markup=ReplyKeyboardMarkup(
                             [[KeyboardButton(telefon, request_contact=True)], [ortga]], resize_keyboard=True))
        return
    elif m.text == tozalash:
        buyurtmalar[m.chat.id] = []
        bot.send_message(m.chat.id, """Siz tanlagan barcha taomlar to'liq tozalandi.
       
        👇 Kerakli taomlar bo'limni tanlang:""",
                         reply_markup=ReplyKeyboardMarkup([[ortga, menu]], resize_keyboard=True))
        return
    elif m.text == shikoyat:
        fikr[m.chat.id] = 'shikoyat'
        bot.send_message(m.chat.id, """<b>Qanday shikoyat qilmoqchisiz ?</b>

🔸 O'z fikringizni yozib qoldiring albatta inobatga olamiz:""",
                         reply_markup=ReplyKeyboardMarkup([[ortga]], resize_keyboard=True))
        return
    elif m.text == taklif:
        fikr[m.chat.id] = 'taklif'
        bot.send_message(m.chat.id, """<b>Qanday taklifingiz bor ?</b>

🔸 O'z fikringizni yozib qoldiring albatta inobatga olamiz:""",
                         reply_markup=ReplyKeyboardMarkup([[ortga]], resize_keyboard=True))
        return
    elif m.text == xatolik:
        fikr[m.chat.id] = 'xatolik'
        bot.send_message(m.chat.id, """<b>Qanday xatolik topdingiz ?</b>

🔸 O'z fikringizni yozib qoldiring albatta inobatga olamiz:""",
                         reply_markup=ReplyKeyboardMarkup([[ortga]], resize_keyboard=True))
        return
    elif m.text == shunchaki:
        fikr[m.chat.id] = 'shunchaki'
        bot.send_message(m.chat.id, """🔸 O'z fikringizni yozib qoldiring albatta inobatga olamiz:""",
                         reply_markup=ReplyKeyboardMarkup([[ortga]], resize_keyboard=True))
        return

    elif m.text == buyurtma:
        x = buyurtmalar.get(m.chat.id, None)
        if x is None:
            buyurtmalar[m.chat.id] = []
        if not x:
            bot.send_message(m.chat.id,
                             '🧐 Siz hali taom tanlamadingiz "🔙 Ortga" qaytib taom tanlang va Savatga yig\'ib boring.🛒',
                             reply_markup=ReplyKeyboardMarkup([[ortga, menu]], resize_keyboard=True))
            return

        jami = 0.0
        text = "👇 Siz tanlagan taomlar: \n\n"
        for i in buyurtmalar[m.chat.id]:
            # print(i)
            text += "{} x {}: {}00\n".format(i[2], i[0], i[1]*i[2])
            jami += i[1] * i[2]
        bot.send_message(m.chat.id, text)
        x = ReplyKeyboardMarkup([[ha], [yuq], [qol]], resize_keyboard=True)
        bot.send_message(m.chat.id, "Tasdiqlaysizmi ❓", reply_markup=x)
        return
    elif m.text == ha and not xizmat_narxi.get(m.chat.id, 0):
        manzil[m.chat.id] = True
        bot.send_message(m.chat.id, """Iltimos oldin manzilni aniqlash uchun "📍<b>Geolokatsiya</b>" tugmasini bosib manzilni jo'nating:""",
                         reply_markup=ReplyKeyboardMarkup([[KeyboardButton("📍 Geolokatsiya", request_location=True)]],
                                                          resize_keyboard=True))

        return
    elif m.text == ha:
        komment[m.chat.id] = True
        bot.send_message(m.chat.id, "💬 Istasangiz, buyurtmangiz haqida izoh kommentariya yozib qoldirishingiz mumkin.Biz uni albatta inobatga olamiz.",
                         reply_markup= ReplyKeyboardMarkup([["Shart emas"]], resize_keyboard=True))
        return
    elif m.text == yuq:
        buyurtmalar[m.chat.id] = []
        bot.send_message(m.chat.id, """Siz tanlagan taomlaringiz to'liq tozalandi 
        
        👇 Kerakli taomlar bo'limni tanlang:""",
                         reply_markup=ReplyKeyboardMarkup([[ortga, menu]], resize_keyboard=True))
        return
    elif m.text == qol:
        bot.send_message(m.chat.id, """Taomlaringiz savatda saqlandi 
        
        👇 Kerakli taomlar bo'limni tanlang:""", reply_markup=ReplyKeyboardMarkup([[ortga, menu]],
                                                                                  resize_keyboard=True))
    elif m.text in taomlar.keys():
        x = []
        try:
            bot.send_message(m.chat.id, choice(faktlar[m.text]))
        except:
            pass
        for i, t in enumerate(taomlar[m.text]):
            a, b = i // 2, i % 2
            if b == 0:
                x.append([])
            x[a].append(t[1])
        x.append([ortga, korzina])
        x = ReplyKeyboardMarkup(x, resize_keyboard=True)
        temp[m.chat.id] = [m.text]
        bot.send_message(m.chat.id, "{} :".format(m.text), reply_markup=x)
        return
    elif manzil.get(m.chat.id, 0) and komment.get(m.chat.id, 0):

        text = "{} (`{}`) {} buyurtma berdi:\n".format(m.from_user.first_name, m.chat.id,
                                                       m.from_user.last_name or "")
        idishlar = 0.0
        jami = 0.0
        for n, i in enumerate(buyurtmalar[m.chat.id]):
            text += "{}) {} x {} {}00\n".format(n+1, i[0], i[2], i[1] * i[2])
            jami += i[1] * i[2]
            if "suyuq" in i[-1].lower() or "uyg'ur" in i[-1].lower():
                idishlar += 1.5*i[2]
            if "quyuq" in i[-1].lower() or "salatlar" in i[-1].lower():
                idishlar += 1.0*i[2]
        if idishlar:
            text += "🍽 Bir martalik idishlar: {}00\n".format(idishlar)
        text += "🛵 Yetkazib berish hizmati: {}00\n".format(xizmat_narxi[m.chat.id])
        jami += xizmat_narxi[m.chat.id]
        text += "🔖 Jami: {0}00\n\n".format(jami+idishlar)
        text += "📞 Tel: {}\n📍 Manzil: {}".format(phone_numbers[m.chat.id], manzil[m.chat.id])
        text += "\n💬 Komment: {}".format(m.text)
        bot.send_message(guruh_id, text)
        bot.send_location(guruh_id, *geolokatsiya[m.chat.id])
        for i in buyurtmalar[m.chat.id]:
            a = info.get(i[-1], 0) + i[2]
            info[i[-1]] = a
        temp[m.chat.id] = None
        manzil[m.chat.id] = None
        komment[m.chat.id] = None
        buyurtmalar[m.chat.id] = []
        bot.send_message(m.chat.id, "Rahmat,tez orada adminstratorlarimiz albatta siz bilan bog'lanishadi "


                                    "👇 Kerakli taomlar bo'limini tanlang:", reply_markup=bolimlar)
        return
    elif "bekor qilish" in m.text:
        import re
        s = re.search(r"(\w*) bekor", m.text)
        s = s.groups()[0][:-2]
        # print(s)
        for i in buyurtmalar[m.chat.id]:
            if s in i[0]:
                buyurtmalar[m.chat.id].remove(i)
                break
        x = []
        jami = 6.0
        text = "👇 Siz tanlagan taomlar:\n\n"
        for i in buyurtmalar[m.chat.id]:
            # print(i)
            text += "{}x{}: {}00\n".format(i[2], i[0], i[1] * i[2])
            jami += i[1] * i[2]
            x.append([KeyboardButton("❌ {}ni bekor qilish".format(i[0]), request_contact=False)])
        x.append([buyurtma])
        x.append([tozalash])
        x.append([ortga])
        text += "\nYetkazib berish: 6.000\n\nJami: {}00".format(jami)
        x = ReplyKeyboardMarkup(x, resize_keyboard=True)
        bot.send_message(m.chat.id, text, reply_markup=x)
        return

    elif temp.get(m.chat.id, 0) and len(temp[m.chat.id]) == 1:
        bol = temp[m.chat.id][0]
        x = None
        for i in taomlar[bol]:
            if m.text in i:
                x = i
                break
        if x is None:
            return
        # print(x)
        if "ro'yxat" in m.text.lower():
            bot.send_photo(m.chat.id, x[0])
            return
        temp[m.chat.id].append(m.text)
        temp[m.chat.id].append(x[2])

        if x[3]:
            bot.send_photo(m.chat.id, x[0], caption="""{}\nNarxi: {}00so'm""".format(x[1], x[2]),
                           reply_markup=ReplyKeyboardMarkup([[x[3]], [x[4]]], resize_keyboard=True))
            if x[-1]:
                bot.send_message(m.chat.id, x[-1])
        else:
            bot.send_photo(m.chat.id, x[0], caption="""{}\nNarxi: {}00so'm""".format(x[1], x[2]), reply_markup=raqamlar)
            if x[-1]:
                bot.send_message(m.chat.id, x[-1])
            bot.send_message(m.chat.id, "👇 Miqdorni kiriting yoki o'zingiz yozing:")

        return
    elif temp.get(m.chat.id, 0) and len(temp[m.chat.id]) == 3:
        if len(m.text) <= 2:
            soni = int(m.text)
            temp[m.chat.id].append(soni)

            try:  # nomi     #narxi         #soni
                buyurtmalar[m.chat.id].append((temp[m.chat.id][1], temp[m.chat.id][2], soni, temp[m.chat.id][0]))
            except KeyError:
                buyurtmalar[m.chat.id] = []
                buyurtmalar[m.chat.id].append((temp[m.chat.id][1], temp[m.chat.id][2], soni, temp[m.chat.id][0]))
            bot.send_message(m.chat.id,
                             "🛒 Siz tanlagan taomlar savatga qo'shildi  Buyurtma Berish bo'limiga kirib buyurtma qilishingiz mumkin!"
                             "", reply_markup=bolimlar)
            return
        else:
            temp[m.chat.id][1] += "  {}".format(m.text)
            bot.send_message(m.chat.id, "👇 Miqdorni kiriting yoki o'zingiz yozing:", reply_markup=raqamlar)
    elif m.text == "🔙 Ortga":
        bot.send_message(m.chat.id, "👇 Kerakli taomlar bo'limini tanlang:", reply_markup=bolimlar)
        temp[m.chat.id] = None
        return
    elif m.text == "👨‍💻 Bog'lanish":
        bot.send_message(m.chat.id, """✉️ Telegram orqali: @EzazAdmin 

📞 Telefon orqali: +998951466616

📧 Elektron Pochta: 
ezazsprt@gmail.com

📷 Instagram: 
http://instagram.com/ezazmilliytaomlar """)
        return


@bot.on_message(Filters.location)
def handle_location(c, m: Message):
    if manzil.get(m.chat.id, None):
        manzil[m.chat.id] = "Geolokatsiya"
        geolokatsiya[m.chat.id] = (m.location.latitude, m.location.longitude)
        a = distance( 41.120233069494155, 69.07184731700151, m.location.latitude, m.location.longitude)
        xizmat_narxi[m.chat.id] = 6.0
        if a>=3:
            xizmat_narxi[m.chat.id] += ceil(a-3)
        jami = 0.0
        text = """👤 <b>Hurmatli mijoz,</b>siz tanlagan taomlar uchun doimiy ravishda "Bir martalik" idish qo'shib oboriladi.
shuning uchun BOT avtomatik tarzda Quyuq taom uchun: quyuq idish(1000so'm) suyuq taom uchun: suyuq idish(1500so'm) hisoblaydi.

🛵 Yetkazib berish xizmatimiz Yangiyo'l shahar va Tumanida amal qiladi.Yetkazib berish xizmatimiz 3kmdan uzoq masofaga km hisobida 1000so'mdan qo'shib boriladi.Bu ishni BOTning o'zi avtomatik tarzda bajaradi.

👇 Siz tanlagan taomlar:\n
--------------"""
        idishlar = 0.0
        for i in buyurtmalar[m.chat.id]:
            if "suyuq" in i[-1].lower() or "uyg'ur" in i[-1].lower():
                idishlar += 1.5*i[2]
            if "quyuq" in i[-1].lower() or "salatlar" in i[-1].lower():
                idishlar += 1.0*i[2]
            text += "{} x {}: {}00\n".format(i[2], i[0], i[1]*i[2])
            jami += i[1] * i[2]
        if idishlar:
            text += "🍽 Bir martalik idishlar: {}00\n".format(idishlar)
            jami += idishlar
        text += "🛵 Yetkazib berish hizmati: {}00\n".format(xizmat_narxi[m.chat.id])
        jami += xizmat_narxi[m.chat.id]
        text += "<b>📋 Jami: {}00</b>\n" \
                "--------------".format(jami)
        bot.send_message(m.chat.id, text, reply_markup=ReplyKeyboardMarkup(
            [[ha], [yuq], [qol]], resize_keyboard=True
        ))
        return


@bot.on_message(Filters.media)
def ls(c, m: Message):
    if m.chat.id == guruh_id:
        for i in phone_numbers.keys():
            try:
                m.forward(i, as_copy=True)
            except:
                pass


@bot.on_message()
def handle_default(c, m):
    print(m)


load()
if __name__ == '__main__':
    bot.run()
