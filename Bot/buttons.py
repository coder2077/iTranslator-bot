'''
©️ 2021. Contact(Telegram): @coder2077
'''
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def languages():
	markup = InlineKeyboardMarkup()

	btn = InlineKeyboardButton("🇺🇿 Uzbek", callback_data="uz")
	markup.add(btn)

	markup.row_width = 2
	markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="en"),
	InlineKeyboardButton("🇷🇺 Russian", callback_data="ru"),
	InlineKeyboardButton("🇫🇷 French", callback_data="fr"),
	InlineKeyboardButton("🇩🇪 German", callback_data="de"),
	InlineKeyboardButton("🇸🇦 Arabic", callback_data="ar"),
	InlineKeyboardButton("🇮🇳 Hindi", callback_data="hi"))

	return markup

def settings():
	markup = InlineKeyboardMarkup()

	btn2 = InlineKeyboardButton("⚙️ Change language", callback_data='settings')
	markup.add(btn2)

	return markup

def result():
	markup = InlineKeyboardMarkup()

	btn1 = InlineKeyboardButton("🎧 Pronunciation", callback_data='pronunciation')
	btn2 = InlineKeyboardButton("⚙️ Settings", callback_data='settings')
	btn = InlineKeyboardButton(" ❌ ", callback_data='delete')
	markup.add(btn1, btn2)
	markup.add(btn)

	return markup

def delete():
	markup = InlineKeyboardMarkup()

	btn = InlineKeyboardButton(" ❌ ", callback_data='delete')
	markup.add(btn)

	return markup

def repo():
	markup = InlineKeyboardMarkup()

	btn = InlineKeyboardButton(" Github Repo ", url='https://github.com/coder2077/iTranslator-bot')
	btn1 = InlineKeyboardButton(" ❌ ", callback_data='delete')
	markup.add(btn)
	markup.add(btn1)

	return markup


'''
©️ 2021. Contact(Telegram): @coder2077
'''