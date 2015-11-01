from settings import *

from requests import session
from pyquery import PyQuery as pq
import sqlite3
from datetime import datetime

userids = None
mail = None
password = None

with sqlite3.connect(DBNAME_SETTINGS) as con:    
   userids = [_[0] for _ in con.execute('select userid from munichusers').fetchall()]
   mail, password = con.execute('select mail,password from foodsharinguser').fetchall()[0]

loginurl = 'https://foodsharing.de/?page=login&ref=/?page=dashboard'
payload = {'email_adress': mail, 'password': password}
stats = []

with session() as c:
    c.post(loginurl, data=payload)
    datenow = datetime.now()
    
    for userid in userids:
        userpage = c.get('https://foodsharing.de/profile/{}'.format(userid))
        if userpage.url.find('profile') == -1:
            print('invalid userid:', userid)
            continue
        
        doc = pq(userpage.content)
        
        fetchcount, fetchweight, postcount, friends = (0,0,0,0)
        try:
            fetchcount = int(doc('span.stat_fetchcount > span.val').text().strip('x').replace('.',''))
        except Exception:
            pass
        
        try:
            fetchweight = int(doc('span.stat_fetchweight > span.val').text().strip('kg').replace('.',''))
        except Exception:
            pass
        
        try:
            postcount = int(doc('span.stat_postcount > span.val').text().replace('.',''))
        except Exception:
            pass
        
        try:
            friends = int(doc('div.infos:nth-child(1) > p:nth-child(1)').text().split()[-2].replace('.',''))
        except Exception:
            pass

        stats.append((userid, datenow, fetchcount, fetchweight, postcount, friends))

    
with sqlite3.connect(DBNAME_STATS) as con:
    con.execute('create table if not exists munichstats(id, date, fetchcount, fetchweight, postcount, friends)')
    con.executemany('insert into munichstats(id, date, fetchcount, fetchweight, postcount, friends) values (?, ?, ?, ?, ?, ?)', stats)




