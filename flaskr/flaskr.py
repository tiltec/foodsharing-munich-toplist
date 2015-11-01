# -*- coding: utf-8 -*-

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
     
DATABASE = '../scraper/foodsharingstats.db'
DEBUG = True
SECRET_KEY = 'devkey'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.route('/')
def show_entries():
    cur = g.db.execute('select id,date,fetchcount,fetchweight,postcount,friends from munichstats order by date desc')
    entries = [dict(userid=row[0], date=row[1], fetchcount=row[2], fetchweight=row[3], postcount=row[4], friends=row[5]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries) 
    
@app.route('/overview', methods=['GET'])
def overview():
    cur = g.db.execute('select id,date,fetchcount,fetchweight,postcount,friends from munichstats order by date desc')
    entries = [dict(userid=row[0], date=row[1], fetchcount=row[2], fetchweight=row[3], postcount=row[4], friends=row[5]) for row in cur.fetchall()]
    userentries = []
    userids = set([_['userid'] for _ in entries])
    for u in userids:
        userentries.append(
            {'userid': u,
             'entries': [e for e in entries if e['userid'] == u]
             })
    return jsonify({'entries': userentries})
    
if __name__ == '__main__':
    app.run()