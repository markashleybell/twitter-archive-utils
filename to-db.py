import json
import os
import psycopg2
import time
from datetime import date
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.cfg')

params = {
    # Where the downloaded Twitter archive lives
    'data_folder': 'tweets/data/js/tweets/', 
    # Filter out tweets with this such:
    #'filter_text': '#dnd tip:', 
    'filter_text': False
}

# Code from https://github.com/mshea/Parse-Twitter-Archive
def archive_to_db(data_folder):
    json_output = []
    filenames = os.listdir(data_folder)
    for file in filenames:
        if '.js' in file:
            f = open(data_folder + file)
            d = f.readlines()
            d[0] = '' # Twitter's JSON requires we remove the first line
            json_data = json.loads(''.join(d))
            for entry in json_data:
                try:
                    if params['filter_text'] in entry['text']:
                        json_output.append(entry)
                except:
                    json_output.append(entry)

    conn = psycopg2.connect(host=config.get('database', 'host'), 
                            dbname=config.get('database', 'dbname'), 
                            user=config.get('database', 'user'), 
                            password=config.get('database', 'password'))
    c = conn.cursor()

    data_to_write = []
    for item in json_output:
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        data_to_write.append((int(item['id_str']), ts, item['text']))
    c.executemany('INSERT INTO tweets (id, created_at, status) VALUES (%s, %s, %s);', data_to_write)
    conn.commit()
    return True

if archive_to_db(params['data_folder']):
    print 'Insert complete'