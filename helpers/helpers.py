import datetime

#----------------------------------------Getting dates---------------------------------------------------------------
def get_date_str_from_message(text):
  #gets a date string from existing message
  remove_front = text.partition("Target date: ")[2]
  date_str = remove_front.partition("\n")[0]
  return date_str

def get_date_proper(date_str):
  #gets a datetime object from a date string
  day = int(date_str[:2])
  month = int(date_str[3:5])
  year = int(date_str[6:])
  date_proper = datetime.datetime(year, month, day)
  
  return date_proper

def get_days_since(date_proper, tz):
  #get days since from a datetime object using datetime.now()
  days_since = (datetime.datetime.now()+tz - date_proper).days
  return days_since

def get_days_until(date_proper, tz):
  #get days until from a datetime object using datetime.now()
  days_until = (date_proper + datetime.timedelta(days=1) - (datetime.datetime.now()+tz)).days
  return days_until

def get_days_between(date_proper_1, date_proper_2):
  days_between_timedelta = (date_proper_1 - date_proper_2).days
  days_between = abs(int(days_between_timedelta))
  return days_between
#--------------------------------------------------------------------------------------------------------------------

#------------------------------------------Checks for validity-------------------------------------------------------
def is_valid_since(date_str, tz):
  #checks validity of date_str for since command
  try:
    target_date = get_date_proper(date_str)
    valid = target_date <= (datetime.datetime.now()+tz) and date_str[2]=="-" and date_str[5]=="-"
  except:
    valid = False

  return valid

def is_valid_until(date_str, tz):
  #checks validity of date string and returns true or false. If input date is today, returns "today"
  try:
    target_date = get_date_proper(date_str)
    valid = target_date + datetime.timedelta(days=1)> (datetime.datetime.now()+tz) and date_str[2]=="-" and date_str[5]=="-"
  except:
    valid = False

  if valid and target_date.date() == (datetime.datetime.now()+tz).date():
    valid = "today"

  return valid

def is_valid_between(user_input):
  try:
    date_str_1 = user_input.partition(" ")[0]
    date_str_2 = user_input.partition(" ")[2]
  
    date_proper_1 = get_date_proper(date_str_1)
    date_proper_2 = get_date_proper(date_str_2)

    valid = date_str_1[2]=="-" and date_str_1[5]=="-" and date_str_2[2]=="-" and date_str_2[5]=="-"
  except:
    valid = False

  return valid
    
#--------------------------------------------------------------------------------------------------------------------

#----------------------------------Creating messages-----------------------------------------------------------------
def create_since_message(date_str, days_since):
  #creates message to be sent / edited for since command
  message = """Target date: %s
Days since target date: %s""" % (date_str, days_since)
  return message

def create_until_message(date_str, days_until):
  #creates message to be sent / edited for until command
  message = """Target date: %s
Days until target date: %s""" % (date_str, days_until)
  return message

def create_closed_message(date_str, days_between, tz):
  #creates message to be edited to for closing since commands
  today = (datetime.datetime.now()+tz).date().strftime("%d-%m-%Y")
  message = """Closed on %s
Target date: %s
Days between target and closing: %s""" % (today, date_str, days_between)
  return message

def create_until_update_today_message(date_str):
  message = """Target date: %s
Today is the day!""" % (date_str)
  return message

def create_until_update_passed_message(date_str, days_since, tz):
  today = (datetime.datetime.now()+tz).date().strftime("%d-%m-%Y")
  message = """Target date: %s
Today's date: %s
Day has passed!
It has been %s days since target date""" % (date_str, today, days_since)
  return message

def create_days_between_message(date_str_1, date_str_2, days_between):
  message = "Days between %s and %s: %s" % (date_str_1, date_str_2, days_between)
  return message

