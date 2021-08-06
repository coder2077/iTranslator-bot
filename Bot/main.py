'''
©️ 2021. Contact(Telegram): @coder2077
Official bot of repo: @iTarjimonBot
'''

import telebot
from googletrans import Translator
from gtts import gTTS
import sqlite3
import buttons
import config
from languages import Languages
import os

bot = telebot.TeleBot(config.TOKEN, parse_mode='Markdown')

translator = Translator()

# Function for pronunciation
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
		answer = f'🔥 *Welcome {firstname} !\n\n⚙️ Select language and send me text\n\n🆘 Available commands: /help*'
		lang = bot.send_message(chat_id, answer, reply_markup=buttons.languages())

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
	msg_text = '\n\n*Available commands:*\n'
	msg_text += '*/language* - _Change language_\n'
	msg_text += '*/help* - _Available commands_\n'
	msg_text += '*/about* - _About bot_\n'
	msg_text += '*/statistics* - _Number of users_'
	bot.reply_to(message, msg_text, reply_markup=buttons.delete())

# Handling /about command
@bot.message_handler(commands=['about'])
def about_command(message):
	msg_text = f'*A bot is a professional bot that automatically detects a language in texts and translates it into the selected language.'
	msg_text += '\n\nBot is open source. Github repo 👇*'

	bot.reply_to(message, msg_text, reply_markup=buttons.repo())

# Handling /statistics command
@bot.message_handler(commands=['statistics'])
def stat_command(message):
	first_name = message.from_user.first_name
	chat_id = message.chat.id

	conn = sqlite3.connect('users.db')
	cur = conn.cursor()
	num = cur.execute("SELECT COUNT(*) FROM users")
	for n in num:
		for i in n:
			msg_text = f'<b><i>Number of users</i> - {i}</b>'

	conn.commit()
	conn.close()
	
	bot.send_message(chat_id, msg_text, parse_mode='html', reply_markup=buttons.delete())


# Handling /language command
@bot.message_handler(commands=['language'])
def lang_command(message):
	chat_id = message.chat.id
	try:
		conn = sqlite3.connect('users.db')
		cur = conn.cursor()
		cur.execute("SELECT lang FROM users WHERE user_id = (?);", (chat_id,))
		data_lang = cur.fetchone()
		for lang in data_lang:
			answer = f'<b>You selected <i>{Languages[lang]}</i> language.\n\n'
			answer += f'For change it, select new language 👇</b>'
			bot.send_message(chat_id, answer, parse_mode='html', reply_markup=buttons.languages())
		conn.close()
	except:
		answer = f'Please select language.'
		bot.send_message(chat_id, answer, parse_mode='html', reply_markup=buttons.languages())

# Callback Query Handler
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
	chat_id = call.message.chat.id
	firstname = call.message.chat.first_name
	conn = sqlite3.connect('users.db')
	cursor = conn.cursor()

	def save_language(short):
		bot.answer_callback_query(call.id, f'{Languages[call.data]} language selected. Send me a text')
		cursor.execute('UPDATE users SET lang = (?) WHERE user_id = (?)', (call.data, chat_id,))
		conn.commit()
		text = f'✅* {Languages[call.data]} language selected.* Send me a text'
		bot.edit_message_text(text, chat_id, call.message.id, reply_markup=buttons.settings())

	if call.data in ['uz', 'en', 'ru', 'fr', 'de', 'ar', 'hi']:
		save_language(call.data)

	elif call.data == 'delete':
		try:
			bot.delete_message(chat_id, call.message.id)
			bot.delete_message(chat_id, call.message.id-1)
		except:
			bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'settings':
		try:
			text = f'*⚙️ Select new language*'
			bot.edit_message_text(text, chat_id, call.message.id, reply_markup=buttons.languages())
			bot.answer_callback_query(call.id, '⚙️ Settings')
		except:
			try:
				# If message is audio, edit_message_text() function don't work.
				bot.delete_message(chat_id, call.message.id)
				bot.send_message(chat_id, text, reply_markup=buttons.settings())
			except:
				bot.answer_callback_query(call.id, '😞 oops!')

	elif call.data == 'pronunciation':
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
				try:
					tts = gTTS(text=result, lang=lang, slow=False)
					tts.save(f'{chat_id}.mp3')
					bot.delete_message(chat_id, call.message.id)
					caption = f'*Result: 👇*\n`{result.capitalize()}` \n\n*Detected:* __{detect}__ *to* __{lang}__'
					bot.send_audio(chat_id, open(f'{chat_id}.mp3', 'rb'), caption=caption, reply_markup=buttons.result())
					os.remove(f'{chat_id}.mp3')
				except:
					bot.answer_callback_query(call.id, '😔 Unsupported language!')
		except:
			pass

	conn.close()


# Message handler
@bot.message_handler(content_types=['text', 'photo'])
def response(message):
	chat_id = message.chat.id
	conn = sqlite3.connect('users.db')
	cursor = conn.cursor()

	if message.content_type == 'text':
		text = message.text

	elif message.content_type == 'photo':
		text = message.caption
	
	# Save a text to db
	cursor.execute('UPDATE users SET result = (?) WHERE user_id = (?)', (text, chat_id,))
	conn.commit()

	cursor.execute(f"SELECT lang FROM users WHERE user_id = ?", (chat_id,))
	data = cursor.fetchone()
	cursor.execute(f"SELECT result FROM users WHERE user_id = ?", (chat_id,))
	data_text = cursor.fetchone()

	for x in data_text:
		text = x
	for lang in data:
		# There are (', `) notations in uzbek language
		if '\'' in text:
			result = translator.translate(text, dest=lang, src='uz').text
		elif '`' in text:
			result = translator.translate(text, dest=lang, src='uz').text
		else:
			result = translator.translate(text, dest=lang).text

		detect = translator.detect(text).lang
		result = f'*Result: 👇*\n`{result.capitalize()}` \n\n*Detected:* __{detect}__ *to* __{lang}__'
		bot.send_message(chat_id, result, reply_markup=buttons.result())


bot.polling(none_stop=True)

'''
©️ 2021. Contact(Telegram): @coder2077
'''