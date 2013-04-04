import os
import psycopg2
import time
from datetime import date
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

def load_from_db(where = ''):
    tweets = []
    conn = psycopg2.connect(host=config.get('database', 'host'), 
                            dbname=config.get('database', 'dbname'), 
                            user=config.get('database', 'user'), 
                            password=config.get('database', 'password'))
    c = conn.cursor()
    c.execute('SELECT id, created_at, status FROM tweets ' + where + ' ORDER BY id DESC;')
    db_object = c.fetchall()
    for item in db_object:
        tweets.append(item)
    return tweets

def output_text(tweets):
    text_output = ''
    for item in tweets:
        id, created_at, text = item
        # text_output += str(id)+'\n'+created_at.strftime("%b %d %Y %H:%M")+'\n'+text+'\n\n'
        text_output += created_at.strftime("%b %d %Y %H:%M") +'\n' + text + '\n\n'
    f = open('tweets.txt', "w")
    f.write(text_output.encode('utf-8'))
    f.close()

# l = load_from_db()
l = load_from_db("WHERE status NOT LIKE '@%' AND status NOT LIKE 'RT%' AND status NOT LIKE '%http://%'")
# l = load_from_db("WHERE status LIKE '%rule of%'")
output_text(l)
print 'Export Complete'