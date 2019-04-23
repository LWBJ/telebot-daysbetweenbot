import datetime
import psycopg2
import os
import urllib.parse as urlparse

def prepare_sql_params():
  url = urlparse.urlparse(os.environ['DATABASE_URL'])
  return [url.path[1:], url.username, url.password, url.hostname, url.port]

def create_table():
  params = prepare_sql_params()
  conn = psycopg2.connect(dbname=params[0], user=params[1], password=params[2], host=params[3], port=params[4])
  cur = conn.cursor()
  stmt = """CREATE TABLE IF NOT EXISTS user_tz_table (
user_id INTEGER PRIMARY KEY,
tz INTEGER NOT NULL)"""
  cur.execute(stmt)
  cur.close()
  conn.commit()
  conn.close()

def add_user(user_id, tz_int):
  params = prepare_sql_params()
  conn = psycopg2.connect(dbname=params[0], user=params[1], password=params[2], host=params[3], port=params[4])
  cur = conn.cursor()
  stmt = """INSERT INTO user_tz_table (user_id, tz)
VALUES (%s, %s)"""
  cur.execute(stmt, (user_id, tz_int))
  cur.close()
  conn.commit()
  conn.close()

def update_user(user_id, tz_int):
  params = prepare_sql_params()
  conn = psycopg2.connect(dbname=params[0], user=params[1], password=params[2], host=params[3], port=params[4])
  cur = conn.cursor()
  stmt = """UPDATE user_tz_table
SET tz = %s
WHERE user_id = %s"""
  cur.execute(stmt, (tz_int, user_id))
  cur.close()
  conn.commit()
  conn.close()

def get_user_data(user_id):
  params = prepare_sql_params()
  conn = psycopg2.connect(dbname=params[0], user=params[1], password=params[2], host=params[3], port=params[4])
  cur = conn.cursor()
  stmt = """SELECT * FROM user_tz_table WHERE user_id = %s"""
  cur.execute(stmt, (user_id,))
  rows = cur.fetchone()
  cur.close()
  conn.commit()
  conn.close()
  return rows

def valid_timezone(user_input):
  try:
    intput = int(user_input)
    valid = intput <= 12 and intput >= -12
  except:
    valid = False

  return valid

def add_to_SQL(user_id, tz_int):
  try:
    add_user(user_id, tz_int)
  except: 
    update_user(user_id, tz_int)

def timezone(user_id):
  try:
    tz_int = get_user_data(user_id)[1]
    tz_delta = datetime.timedelta(hours=tz_int)
  except:
    tz_delta = datetime.timedelta(hours=8)

  return tz_delta
