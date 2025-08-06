import telebot
from pyexpat.errors import messages
from telebot import types
import os
import logging
import crud
import weather

# Create the instance of the bot
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Handler of command /start
# @bot.message_handler(commands=['start'])
# def start_command(message):
#     bot.reply_to(message, "Hello! I am your bot. Can I help you?")
#     # Create a keyboard with two inline buttons
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     # Create buttons with callback-data
#     button1 = types.InlineKeyboardButton('Button 1', callback_data='data1')
#     button2 = types.InlineKeyboardButton('Button 2', callback_data='data2')
#     # Add buttons to the keyboard
#     keyboard.add(button1, button2)
#     # Send a message with the keyboard
#     bot.send_message(message.chat.id, 'Select the option:', reply_markup=keyboard)
#
# # Handler for callback-requests
# @bot.callback_query_handler(func=lambda call: True)
# def handle_query(call):
#     if call.data == 'data1':
#         bot.send_message(call.message.chat.id, 'You pressed the button 1')
#     elif call.data == 'data2':
#         bot.send_message(call.message.chat.id, 'You pressed the button 2')

@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        # Logging command /start
        logger.info('Get command /start from user %s', message.chat.id)
        bot.reply_to(message, "Hello! I am your bot. Can I help you?")
        # Create a keyboard with two reply buttons
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        # Create buttons
        button1 = types.KeyboardButton('Харьков')
        button2 = types.KeyboardButton('Никосия')
        # Add buttons to the keyboard
        keyboard.add(button1, button2)
        # Send a message with the keyboard
        bot.send_message(message.chat.id, 'Select the option:', reply_markup=keyboard)
    except telebot.apihelper.ApiException as e:
        # Logging error when interacting with the Telegram API
        logger.error('Error sending the message: %s', e)
        print(f'Error on send the message: {e}')
        bot.send_message(message.chat.id, 'There was an error sending your message. Please try again later.')
    except Exception as e:
        # Logging other errors
        logger.error('Unknown error: %s', e)
        print(f'Unknown error: {e}')
        bot.send_message(message.chat.id, 'An unknown error has occurred. Please contact support.')
    else:
        # Logging successful sending
        logger.info('The message was sending successful to user %s', message.chat.id)
        print('The message was sending successful.')
    finally:
        # Logging finishing command processing /start
        logger.info('Finishing command processing /start for user %s', message.chat.id)
        print('Finishing command processing /start')

# Handler of command /help
@bot.message_handler(commands=['help', 'about'])
def help_command(message):
    bot.reply_to(message, "Help topic. Bot information")

# Handler for send a photo
@bot.message_handler(commands=['send_photo'])
def send_photo(message):
    try:
        with open('d:/Загрузки/photo.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.reply_to(message, 'File not found')

# Handler for send a video
@bot.message_handler(commands=['send_video'])
def send_photo(message):
    try:
        with open('d:/Загрузки/video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
    except FileNotFoundError:
        bot.reply_to(message, 'File not found')

# Handler for send a document
@bot.message_handler(commands=['send_document'])
def send_document(message):
    try:
        with open('d:/Загрузки/document.pdf', 'rb') as document:
            bot.send_document(message.chat.id, document)
    except FileNotFoundError:
        bot.reply_to(message, 'File not found')

# Handler for receive a photo
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.photo:
        downloaded_file_name = message.photo[-1].file_id
        file_info = bot.get_file(downloaded_file_name)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(f"d:/Загрузки/{downloaded_file_name}.jpg", "wb") as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Image received and saved!")

    else:
        bot.reply_to(message, 'Failed to get image.')

# Handler for receive a video
@bot.message_handler(content_types=['video'])
def handle_video(message):
    if message.video:
        downloaded_file_name = message.video.file_id
        file_info = bot.get_file(downloaded_file_name)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(f'd:/Загрузки/{downloaded_file_name}.mp4', "wb") as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, 'Video received and saved!')
    else:
        bot.reply_to(message, 'Failed to get video.')

# Handler for receive a video
@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.document:
        downloaded_file_name = message.document.file_id
        file_info = bot.get_file(downloaded_file_name)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(f'd:/Загрузки/{downloaded_file_name}.pdf', "wb") as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, 'Document received and saved!')
    else:
        bot.reply_to(message, 'Failed to get document.')

# Command for creating record
@bot.message_handler(commands=['create'])
def create_user(message):
    msg = bot.reply_to(message, 'Enter username and age separated by space (e.g. JohnDoe 21)')
    bot.register_next_step_handler(msg, process_create_step)

def process_create_step(message):
    username, age = message.text.split()
    age = int(age)
    msg = crud.create_user(username, age)
    bot.reply_to(message, msg)

# Command for reading record
@bot.message_handler(commands=['read'])
def read_user(message):
    msg = bot.reply_to(message, 'Enter username for searching:')
    bot.register_next_step_handler(msg, process_read_step)

def process_read_step(message):
    username = message.text
    msg = crud.read_user(username)
    bot.reply_to(message, msg)

@bot.message_handler(commands=['read_all'])
def read_users(message):
    msg = crud.read_users()
    bot.reply_to(message, msg)

@bot.message_handler(commands=['update'])
def update_user(message):
    msg = bot.reply_to(message, 'Enter username and a new age separated by space (e.g. JohnDoe 21):')
    bot.register_next_step_handler(msg, process_update_step)

def process_update_step(message):
    username, age = message.text.split()
    age = int(age)
    msg = crud.update_user(username, age)
    bot.reply_to(message, msg)

@bot.message_handler(commands=['delete'])
def delete_user(message):
    msg = bot.reply_to(message, 'Enter username for deleting:')
    bot.register_next_step_handler(msg, process_delete_step)

def process_delete_step(message):
    username = message.text
    msg = crud.delete_user(username)
    bot.reply_to(message, msg)

@bot.message_handler(commands=['weather'])
def get_weather(message):
    msg = bot.reply_to(message, 'Enter the city:')
    bot.register_next_step_handler(msg, process_weather_step)

def process_weather_step(message):
    city=message.text
    msg=weather.process_weather_data(city)
    bot.reply_to(message, msg)

# Handler of your messages
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Харьков':
        bot.reply_to(message, weather.process_weather_data('Харьков'))
    elif message.text == 'Никосия':
        bot.reply_to(message, weather.process_weather_data('Никосия'))
    else:
        response = f"You write: {message.text}"
        bot.send_message(message.chat.id, response)

# Run the bot
try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Error starting polling: {e}")
