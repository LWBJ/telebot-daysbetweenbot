#Trying SQL code from stack overflow
#bot works. trying 1 line of SQL now
#commented out all TZs, uses TZ = +1h instead
#commented out all add_to_SQL, create_tables()

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from helpers.helpers import *
from helpers.db import *
import datetime
import os
import urllib.parse as urlparse

def days_since(bot, update):
  #tz = timezone(update.message.from_user.id, DATABASE_URL)
  tz = datetime.timedelta(hours=1)
  
  date_str = update.message.text.partition(" ")[2]
  if is_valid_since(date_str, tz):
    date_proper = get_date_proper(date_str)
    days_since = get_days_since(date_proper, tz)
    mess = create_since_message(date_str, days_since)
    
    keyboard = [IKB("Update", callback_data="1"), IKB("Close",callback_data="2")],
    reply_markup = IKM(keyboard)
    
    update.message.reply_text(text=mess, reply_markup= reply_markup)
  else:
    update.message.reply_text(text="Please input a valid date in DD-MM-YYYY format!")

def days_until(bot, update):
  #tz = timezone(update.message.from_user.id, DATABASE_URL)
  tz = datetime.timedelta(hours=1)
  
  date_str = update.message.text.partition(" ")[2]
  if is_valid_until(date_str, tz) == "today":
    update.message.reply_text(text="That date is today!")
  elif is_valid_until(date_str, tz):
    date_proper = get_date_proper(date_str)
    days_until = get_days_until(date_proper, tz)
    mess = create_until_message(date_str, days_until)
    
    keyboard = [IKB("Update", callback_data="3"), IKB("Close",callback_data="4")],
    reply_markup = IKM(keyboard)
    
    update.message.reply_text(text=mess, reply_markup= reply_markup)
  else:
    update.message.reply_text(text="Please input a valid date in DD-MM-YYYY format!")
  
def button(bot, update):
  query = update.callback_query
  #tz = timezone(query.from_user.id, DATABASE_URL)
  tz = datetime.timedelta(hours=1)
  
  date_str = get_date_str_from_message(query.message.text)
  date_proper = get_date_proper(date_str)

  if query.data == "1":
    #updating since messages
    days_since = get_days_since(date_proper, tz)
    mess = create_since_message(date_str, days_since)

    keyboard = [IKB("Update", callback_data="1"), IKB("Close",callback_data="2")],
    reply_markup = IKM(keyboard)

    query.answer(text="Updated!")
    query.edit_message_text(text=mess, reply_markup= reply_markup)

  elif query.data == "2":
    #closing since messages
    days_since = get_days_since(date_proper, tz)
    mess = create_closed_message(date_str, days_since, tz)

    query.answer(text="Closed!")
    query.edit_message_text(text=mess)

  elif query.data == "3" or query.data == "4":
    #updating until messages
    if date_proper.date() == (datetime.datetime.now()+tz).date():
      message = create_until_update_today_message(date_str)

      query.answer(text="Today is the day!")
      query.edit_message_text(text=message)

    elif date_proper.date() < (datetime.datetime.now()+tz).date():
      days_since = get_days_since(date_proper, tz)
      message = create_until_update_passed_message(date_str, days_since, tz)
      
      query.answer(text="Day has already passed!")
      query.edit_message_text(text=message)

    elif query.data == "3":
      days_until = get_days_until(date_proper, tz)
      mess = create_until_message(date_str, days_until)

      keyboard = [IKB("Update", callback_data="3"), IKB("Close",callback_data="4")],
      reply_markup = IKM(keyboard)

      query.answer(text="Updated!")
      query.edit_message_text(text=mess, reply_markup= reply_markup)

    elif query.data == "4":
      days_until = get_days_until(date_proper, tz)
      mess = create_closed_message(date_str, days_until, tz)

      query.answer(text="Closed!")
      query.edit_message_text(text=mess)

def days_between(bot, update):
  user_input = update.message.text.partition(" ")[2]
  if is_valid_between(user_input):
    date_str_1 = user_input.partition(" ")[0]
    date_str_2 = user_input.partition(" ")[2]
  
    date_proper_1 = get_date_proper(date_str_1)
    date_proper_2 = get_date_proper(date_str_2)
  
    days_between = get_days_between(date_proper_1, date_proper_2)
    message = create_days_between_message(date_str_1, date_str_2, days_between)

    update.message.reply_text(text=message)
  else:
    update.message.reply_text(text="Please input valid dates in DD-MM-YYYY format!")

def start(bot, update):
  message = """Hello! This is DaysBetweenBot.

I can track the days since or days until a target date. I can also calculate the days between any 2 dates

Use /help to find out about my commands"""
  update.message.reply_text(text=message)

def help(bot, update):
  message = """/help - This command

/dayssince - input a date in DD-MM-YYYY format after the space. Tracks the days since a target date.

/daysuntil - input a date in DD-MM-YYYY format after the space. Tracks the days until a target date.

/daysbetween - input 2 dates in DD-MM-YYYY format, separated by spaces. For example:
"/daysbetween 01-01-2019 02-01-2019". Calculates the days between 2 dates.

Remember to input dates as DD-MM-YYYY, including the dashes!"""
  update.message.reply_text(text=message)

def set_timezone(bot, update):
  user_input = update.message.text.partition(" ")[2]
  if valid_timezone(user_input):
    tz_int = int(user_input)
    #add_to_SQL(update.message.from_user.id, tz_int, DATABASE_URL)
    update.message.reply_text(text="Timezone set!")
  else:
    update.message.reply_text(text="Please input a valid GMT timezone difference. It should be an integer between -12 and 12")

def main():
  TOKEN = "885176927:AAH-A3nAlzHY0_vEQ0LB4r-zasQO3DO1yLw"
  NAME = "jpdaysbetweenbot"
  PORT = os.environ.get('PORT')
  
  url = urlparse.urlparse(os.environ['DATABASE_URL'])
  dbname = url.path[1:]
  user = url.username
  password = url.password
  host = url.hostname
  port = url.port
  
  create_table(url, dbname, user, password, host, port)
  
  updater = Updater(token=TOKEN)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("dayssince", days_since))
  dp.add_handler(CommandHandler("daysuntil", days_until))
  dp.add_handler(CommandHandler("daysbetween", days_between))
  dp.add_handler(CallbackQueryHandler(button))
  dp.add_handler(CommandHandler("start",start))
  dp.add_handler(CommandHandler("help",help))
  dp.add_handler(CommandHandler("setTZ", set_timezone))

  #updater.start_polling()
  updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
  updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))

if __name__ == "__main__":
  main()
