import json
import os
import psycopg2
import time
from datetime import date
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')

params = {
    'data_file': 'tweets/tweets-bydate.txt', 
}

# Code from https://github.com/mshea/Parse-Twitter-Archive
def archive_to_db(data_file):
    f = open(data_file)
    lines = f.readlines()
    tweets = [(time.strptime(s[:17].strip(), '%b %d %Y %H:%M'), s[:17].strip(), s[19:].strip()) for s in lines]

    # conn = psycopg2.connect(host=config.get('database', 'host'), 
    #                         dbname=config.get('database', 'dbname'), 
    #                         user=config.get('database', 'user'), 
    #                         password=config.get('database', 'password'))
    # c = conn.cursor()

    tweets.sort()

    data_to_write = []
    text_output = ''
    for item in tweets:
        # data_to_write.append((int(item['id_str']), ts, item['text']))
        text_output += item[1] + ': ' + item[2] + '\n'

    f = open('tweets-sorted.txt', "w")
    f.write(text_output)
    f.close()

    # c.executemany('INSERT INTO tweets (id, created_at, status) VALUES (%s, %s, %s);', data_to_write)
    # conn.commit()
    return True

if archive_to_db(params['data_file']):
    print 'Insert complete'