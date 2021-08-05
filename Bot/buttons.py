'''
Copyright 2021. Author Tg: @coder2077
'''

from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def languages():
	markup = InlineKeyboardMarkup()
	btn = InlineKeyboardButton("🇺🇿 O\'zbekcha", callback_data="uz")
	markup.add(btn)

	markup.row_width = 2
	markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="en"),
	InlineKeyboardButton("🇷🇺 Russian", callback_data="ru"),

	InlineKeyboardButton("🇫🇷 France", callback_data="fr"),

	InlineKeyboardButton("🇩🇪 Germany", callback_data="de"),

	InlineKeyboardButton("🇸🇦 Arabian", callback_data="ar"),
	InlineKeyboardButton("🇮🇳 Indian", callback_data="hi"))

	return markup

def page2():
	markup = InlineKeyboardMarkup()

	markup.row_width = 2
	markup.add(InlineKeyboardButton("🇹🇷 Turkish", callback_data="tr"),
	InlineKeyboardButton("🇮🇷 Fors", callback_data="fa"),
	InlineKeyboardButton("🇹🇯 Tajik", callback_data="tg"),
	InlineKeyboardButton("🇰🇿 Qozoq", callback_data="kk"),
	InlineKeyboardButton("🇰🇬 Qirgiz", callback_data="ky"),
	InlineKeyboardButton("🇨🇳 Xitoy", callback_data="zh-tw"),
	InlineKeyboardButton("🇰🇷 Koreya", callback_data="ko"),
	InlineKeyboardButton("🇯🇵 Yapon", callback_data="ja"),
	InlineKeyboardButton("🇪🇸 Ispan", callback_data="es"),
	InlineKeyboardButton("🇮🇹 Italya", callback_data="it"))

	return markup

def settings():
	markup = InlineKeyboardMarkup()

	btn2 = InlineKeyboardButton("⚙️ Tilni o\'zgartirish", callback_data='settings')
	markup.add(btn2)

	return markup

def set1():
	markup = InlineKeyboardMarkup()

	btn = InlineKeyboardButton("🇺🇿 O\'zbekcha", callback_data="uz")
	markup.add(btn)
	markup.row_width = 2
	markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="en"),
	InlineKeyboardButton("🇷🇺 Russian", callback_data="ru"),
	InlineKeyboardButton("🇫🇷 France", callback_data="fr"),
	InlineKeyboardButton("🇩🇪 Germany", callback_data="de"),
	InlineKeyboardButton("🇸🇦 Arabian", callback_data="ar"),
	InlineKeyboardButton("🇮🇳 Indian", callback_data="hi"))

	btn2 = InlineKeyboardButton("▶️ Boshqa til", callback_data='set2')
	markup.add(btn2)

	return markup

def set2():
	markup = InlineKeyboardMarkup()

	markup.row_width = 2
	markup.add(InlineKeyboardButton("🇹🇷 Turkish", callback_data="tr"),
	InlineKeyboardButton("🇮🇷 Fors", callback_data="fa"),
	InlineKeyboardButton("🇹🇯 Tajik", callback_data="tg"),
	InlineKeyboardButton("🇰🇿 Qozoq", callback_data="kk"),
	InlineKeyboardButton("🇰🇬 Qirgiz", callback_data="ky"),
	InlineKeyboardButton("🇨🇳 Xitoy", callback_data="zh-tw"),
	InlineKeyboardButton("🇰🇷 Koreya", callback_data="ko"),
	InlineKeyboardButton("🇯🇵 Yapon", callback_data="ja"),
	InlineKeyboardButton("🇪🇸 Ispan", callback_data="es"),
	InlineKeyboardButton("🇮🇹 Italya", callback_data="it"))

	return markup


def result_uz():
	markup = InlineKeyboardMarkup()

	btn1 = InlineKeyboardButton("🎧 Talaffuzi", callback_data='speech')
	btn2 = InlineKeyboardButton("⚙️ Til sozlamalari", callback_data='settings')
	btn = InlineKeyboardButton(" 🗑 ", callback_data='delete')
	markup.add(btn1, btn2)
	markup.add(btn)

	return markup

def delete():
	markup = InlineKeyboardMarkup()

	btn = InlineKeyboardButton(" 🗑 ", callback_data='delete')
	markup.add(btn)

	return markup

'''
Copyright 2021. Author Tg: @coder2077
'''
