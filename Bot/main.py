'''
Copyright 2021. Author Tg: @coder2077
'''

import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from googletrans import Translator
from gtts import gTTS
import sqlite3
from buttons import *
from config import *
from languages import Languages
import os

bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')

translator = Translator()

# Text to speech installation
def speak(text, lang):
	try:
		tts = gTTS(text=text, lang=lang, slow=False)
		filename = 'speech.mp3'
		tts.save(filename)
	except:
		print('Error in speak() function!')

# Handling /start command
@bot.message_handler(commands=['start'])
def start_command(message):
	firstname = message.from_user.first_name
	username = message.from_user.username
	chat_id = message.chat.id
	try:
		answer = f'🔥 *Xush kelibsiz {firstname}!\n\n⚙️ Hoziroq tilni tanlang va matn yoki rasm yuboring.\n\n🆘 Barcha buyruqlarni ko\'rish uchun /help*'
		lang = bot.send_message(chat_id, answer, reply_markup=languages())

		conn = sqlite3.connect('users.db')
		cursor = conn.cursor()

		cursor.execute(f"SELECT user_id FROM users WHERE user_id = ?", (chat_id,))
		data = cursor.fetchone()
		if data is None:
			cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", (firstname, username, chat_id, 'None', 'None',))
			conn.commit()
		else:
			pass
	except:
		pass

	conn.close()


# Handling /help command
@bot.message_handler(commands=['help'])
def help_command(message):
	first_name = message.from_user.first_name
	msg_text = '*Iltimos, botdan xato topsangiz @coder_0006 ga xabar bering.'
	msg_text += '\nBiz xatoni tuzatamiz va sizga tezkorlik va qulaylikni taqdim etamiz!*'
	msg_text += '\n\n*Mavjud Buyruqlar:*\n'
	msg_text += '*/language* - _Tilni o\'zgartirish_\n'
	msg_text += '*/help* - _Mavjud buyruqlar_\n'
	msg_text += '*/about* - _Bot haqida_\n'
	msg_text += '*/developer* - _@iTarjimonBot dasturchisi_\n'
	msg_text += '*/partner* - _Reklama va Hamkorlik_\n'
	msg_text += '*/statistika* - _Bot statistikasi_'
	bot.reply_to(message, msg_text, reply_markup=delete())

# Handling /developer command
@bot.message_handler(commands=['developer'])
def developer_command(message):
	first_name = message.from_user.first_name
	msg_text = f'<b>Dasturchi: <i> @coder_0006\n\nReklama va hamkorlik uchun <a href="https://t.me/coder_0006">admin</a>ga xabar yozishingiz mumkin.</i></b>'
	bot.reply_to(message, msg_text, parse_mode='html', reply_markup=delete())

# Handling /donate command
@bot.message_handler(commands=['partner'])
def donate_command(message):
	first_name = message.from_user.first_name
	msg_text = f'<b>Reklama va Hamkorlik uchun @coder_0006 ga yozing!</b>'
	bot.reply_to(message, msg_text, parse_mode='html', reply_markup=delete())


# Handling /about command
@bot.message_handler(commands=['about'])
def about_command(message):
	first_name = message.from_user.first_name
	msg_text = f'<b>@iTarjimonBot matn yoki rasmdagi matnlarni tilini avtomatik aniqlab tanlangan tilga tarjima qiladigan professional bot.'
	msg_text += f'\n\n<a href="https://t.me/iTarjimonBot">iTarimonBot</a>ga qo\'shilgan yangi funksiyalardan birinchilardan'
	msg_text += f' bo\'lib xabardor bo\'lishni istasangiz @iTarjimonNews kanaliga obuna bo\'lib qo\'ying.</b>'
	bot.reply_to(message, msg_text, parse_mode='html', reply_markup=delete())

# Handling /statistika command
@bot.message_handler(commands=['statistika'])
def stat_command(message):
	first_name = message.from_user.first_name
	chat_id = message.chat.id

	conn = sqlite3.connect('users.db')
	cur = conn.cursor()
	num = cur.execute("SELECT COUNT(*) FROM users")
	for n in num:
		for i in n:
			msg_text = f'<b>💹 STATISTIKA:\n\n<i>Foydalanuvchilar soni</i> - {i} <i>ta</i></b>'

	conn.commit()
	conn.close()
	
	bot.send_message(chat_id, msg_text, parse_mode='html', reply_markup=delete())


# Handling /lang command
@bot.message_handler(commands=['language'])
def lang_command(message):
	chat_id = message.chat.id
	try:
		conn = sqlite3.connect('users.db')
		cur = conn.cursor()
		cur.execute("SELECT lang FROM users WHERE user_id = (?);", (chat_id,))
		data_lang = cur.fetchone()
		for lang in data_lang:
			answer = f'<b>Siz <i>{Languages[lang]}</i> tilini tanlagansiz.\n\n'
			answer += f'Yuborgan matnlaringiz yoki rasmdan aniqlangan matnlar <i>{Languages[lang]}</i> tiliga tarjima qilinadi.\n\nTilni o\'zgartirish uchun pastdagi tugmalardan birini tanlang.</b>'
			bot.send_message(chat_id, answer, parse_mode='html', reply_markup=languages())
		conn.close()
	except:
		answer = f'Siz tarjima uchun til tanlamagansiz, hoziroq tilni tanlang!'
		bot.send_message(chat_id, answer, parse_mode='html', reply_markup=languages())

# Callback Query Handler
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
	chat_id = call.message.chat.id
	firstname = call.message.chat.first_name
	conn = sqlite3.connect('users.db')
	cursor = conn.cursor()
	if call.data == 'page2':
		try:
			text = f'🔥 *Xush kelibsiz {firstname}!\n\n⚙️ Hoziroq tilni tanlang va matn yuboring.\n\nP.S:* _2 - sahifa_.'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=page2())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')
	elif call.data == 'page1':
		try:
			text = f'🔥 *Xush kelibsiz {firstname}!\n\n⚙️ Hoziroq tilni tanlang va matn yuboring.\n\n🆘 Barcha buyruqlarni ko\'rish uchun /help*'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=languages())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')
	
	elif call.data == 'delete':
		try:
			bot.delete_message(chat_id, call.message.id)
			bot.delete_message(chat_id, call.message.id-1)
		except:
			pass

	elif call.data == 'uz':
		try:
			bot.answer_callback_query(call.id, '☑️ O\'zbek tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('uz', chat_id))
			conn.commit()
			text = f'✅* O\'zbek tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'en':
		try:
			bot.answer_callback_query(call.id, '☑️ Ingliz tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('en', chat_id))
			conn.commit()
			text = f'✅* Ingliz tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')		

	elif call.data == 'fr':
		try:
			bot.answer_callback_query(call.id, '☑️ Fransuz tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('fr', chat_id))
			conn.commit()
			text = f'✅* Fransuz tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')	

	elif call.data == 'de':
		try:
			bot.answer_callback_query(call.id, '☑️ Nemis tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('de', chat_id))
			conn.commit()
			text = f'✅* Nemis tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')	

	elif call.data == 'ar':
		try:
			bot.answer_callback_query(call.id, '☑️ Arab tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('ar', chat_id))
			conn.commit()
			text = f'✅* Arab tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')	

	elif call.data == 'hi':
		try:
			bot.answer_callback_query(call.id, '☑️ Hind tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('hi', chat_id))
			conn.commit()
			text = f'✅* Hind tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')	


	elif call.data == 'ru':
		try:
			bot.answer_callback_query(call.id, '☑️ Rus tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('ru', chat_id))
			conn.commit()
			text = f'✅* Rus tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'tr':
		try:
			bot.answer_callback_query(call.id, '☑️ Turk tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('tr', chat_id))
			conn.commit()
			text = f'✅* Turk tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'fa':
		try:
			bot.answer_callback_query(call.id, '☑️ Fors tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('fa', chat_id))
			conn.commit()
			text = f'✅* Fors tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'tg':
		try:
			bot.answer_callback_query(call.id, '☑️ Tojik tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('tg', chat_id))
			conn.commit()
			text = f'✅* Tojik tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'kk':
		try:
			bot.answer_callback_query(call.id, '☑️ Qozoq tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('kk', chat_id))
			conn.commit()
			text = f'✅* Qozoq tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'ky':
		try:
			bot.answer_callback_query(call.id, '☑️ Qirgiz tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('ky', chat_id))
			conn.commit()
			text = f'✅* Qirgiz tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'zh-tw':
		try:
			bot.answer_callback_query(call.id, '☑️ Xitoy tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('zh-tw', chat_id))
			conn.commit()
			text = f'✅* Xitoy tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'ko':
		try:
			bot.answer_callback_query(call.id, '☑️ Koreys tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('ko', chat_id))
			conn.commit()
			text = f'✅* Koreys tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'ja':
		try:
			bot.answer_callback_query(call.id, '☑️ Yapon tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('ja', chat_id))
			conn.commit()
			text = f'✅* Yapon tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'es':
		try:
			bot.answer_callback_query(call.id, '☑️ Ispan tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('es', chat_id))
			conn.commit()
			text = f'✅* Ispan tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')
	elif call.data == 'it':
		try:
			bot.answer_callback_query(call.id, '☑️ Italyan tili tanlandi! Matn yuboring.')
			cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', ('it', chat_id))
			conn.commit()
			text = f'✅* Italyan tili tanlandi!* Matn kiriting:'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=settings())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')
	elif call.data == 'settings':
		try:
			bot.answer_callback_query(call.id, '⚙️ Sozlamalar!')
			text = f'*⚙️ Sozlamalar:\n\nTilni tanlang va matn kiriting.*'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=set1())
			bot.answer_callback_query(call.id, '⚙️ Sozlamalar!')
		except:
			try:
				bot.delete_message(chat_id, call.message.id)
				bot.send_message(chat_id, text, reply_markup=set1())
			except:
				print('Error in 247 line')

	elif call.data == 'set2':
		try:
			bot.answer_callback_query(call.id, '⚙️ 2 - Sahifa!')
			text = f'*Sozlamalar:*\n\n*Tilni tanlang va matn kiriting.*'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=set2())
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'speech':
		try:
			cursor.execute(f"SELECT lang FROM users WHERE user_id = ?", (chat_id,))
			data = cursor.fetchone()
			cursor.execute(f"SELECT result FROM users WHERE user_id = ?", (chat_id,))
			data_text = cursor.fetchone()
			for x in data_text:
				text = x
			for lang in data:
				result = translator.translate(text, dest=lang).text
				detect = translator.detect(text).lang
				# try:
				try:
					tts = gTTS(text=result, lang=lang, slow=False)
					tts.save(f'{chat_id}.mp3')
					bot.delete_message(chat_id, call.message.id)
					bot.send_audio(chat_id, open(f'{chat_id}.mp3', 'rb'), caption=f'*Natija: 👇*\n\n`{result.title()}`\n\n*Aniqlandi: *__{Languages[detect]}__', reply_markup=result_uz())
				except:
					bot.answer_callback_query(call.id, '😔 Bu til qo\'llab quvvatlanmaydi!')

		except:
			pass
		try:
			os.remove(f'{chat_id}.mp3')
		except:
			pass

	conn.close()


# Choose Language message
@bot.message_handler(content_types=['text', 'photo'])
def response(message):
	chat_id = message.chat.id
	conn = sqlite3.connect('users.db')
	cursor = conn.cursor()
	if message.content_type == 'text':
		text = message.text
		if chat_id == 1737755392:
			if '#post' in text:
				cursor.execute("SELECT * FROM users")
				items = cursor.fetchall()
				for item in items:
					try:
						caption = text.replace('#post', '')
						bot.send_message(item[2], caption)
					except:
						pass
			else:
				pass
	

		cursor.execute('UPDATE users SET result = (?) WHERE user_id = (?)', (text, chat_id))
		conn.commit()

		cursor.execute(f"SELECT lang FROM users WHERE user_id = ?", (chat_id,))
		data = cursor.fetchone()
		cursor.execute(f"SELECT result FROM users WHERE user_id = ?", (chat_id,))
		data_text = cursor.fetchone()
		try:
			for x in data_text:
				text = x
			for lang in data:
				try:
					if '\'' in text:
						result = translator.translate(text, dest=lang, src='uz').text
					elif '`' in text:
						result = translator.translate(text, dest=lang, src='uz').text
					else:
						result = translator.translate(text, dest=lang).text
					detect = translator.detect(text).lang
					if 'uz' in lang:
						l = '🇺🇿 o\'zbekcha'
					elif 'en' in lang:
						l = '🇬🇧 inglizcha'
					elif 'ru' in lang:
						l = '🇷🇺 ruscha'
					elif 'fr' in lang:
						l = '🇫🇷 fransuzcha'
					elif 'de' in lang:
						l = '🇩🇪 nemischa'
					elif 'ar' in lang:
						l = '🇸🇦 arabcha'
					elif 'in' in lang:
						l = '🇮🇳 hindcha'
					elif 'tr' in lang:
						l = '🇹🇷 turkcha'
					elif 'fa' in lang:
						l = '🇮🇷 forcha'
					elif 'tg' in lang:
						l = '🇹🇯 tojikcha'
					elif 'kk' in lang:
						l = '🇰🇿 qozoqcha' 
					elif 'ky' in lang:
						l = '🇰🇬 qirgizcha' 
					elif 'zh-tw' in lang:
						l = '🇨🇳 xitoycha' 
					elif 'ko' in lang:
						l = '🇰🇷 koreyscha' 
					elif 'ja' in lang:
						l = '🇯🇵 yaponcha' 
					elif 'es' in lang:
						l = '🇪🇸 ispancha' 
					elif 'it' in lang:
						l = '🇮🇹 italyancha' 
					else:
						l = lang

					bot.send_message(chat_id, f'*Natija: 👇*\n\n`{result.title()}`\n\n*P.S: *__{Languages[detect]} --> {l}__', reply_markup=result_uz())
				except:
					result = f'*Siz hali tilni tanlamadingiz iltimos avval tilni tanlang keyin matn yuboring.*'
					bot.send_message(chat_id, result, reply_markup=languages())
		except:
			pass

		# content type = text:
	elif message.content_type == 'photo':
		if chat_id == 1737755392:
			try:
				if '#post' in message.caption:
					file_info = bot.get_file(message.photo[-1].file_id)
					downloaded_file = bot.download_file(file_info.file_path)
					src = 'result.jpg'
					with open(src, 'wb') as new_file:
						new_file.write(downloaded_file)
						new_file.close()

					conn = sqlite3.connect('users.db')
					cursor = conn.cursor()
					cursor.execute("SELECT * FROM users")
					items = cursor.fetchall()
					for item in items:
						try:
							caption = message.caption.replace('#post', '')
							bot.send_photo(item[2], open('result.jpg', 'rb'), caption=caption)
						except:
							pass
			except:
				pass

				conn.commit()
				conn.close()
			else:
				pass

'''
Copyright 2021. Author Tg: @coder2077
'''

bot.polling(none_stop=True)