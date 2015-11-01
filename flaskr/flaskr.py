# -*- coding: utf-8 -*-

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
     
DATABASE = '../scraper/foodsharingstats.db'
DEBUG = True

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
        
def read_stats():
    cur = g.db.execute('select id,date,fetchcount,fetchweight,postcount,friends from munichstats order by date desc')
    entries = [dict(userid=row[0], date=row[1], fetchcount=row[2], fetchweight=row[3], postcount=row[4], friends=row[5]) for row in cur.fetchall()]
    return entries
        
@app.route('/')
def show_entries():
    entries = read_stats()    
    return render_template('show_entries.html', entries=entries) 
    
@app.route('/overview', methods=['GET'])
def overview():
    entries = read_stats()    
    userentries = []
    userids = set([_['userid'] for _ in entries])
    for u in userids:
        userentries.append(
           )
    userentries.sort(key=lambda e: e['entries'][0]['fetchcount'], reverse=True)
    return jsonify({'entries': userentries})

@app.route('/user/<int:userid>', methods=['GET'])    
def user(userid):
    entries = read_stats()
    userid = str(userid)
    userentries = [{'userid': userid,
             'entries': [e for e in entries if e['userid'] == userid]
             }]
    return jsonify({'entries': userentries})
    
if __name__ == '__main__':
    app.run()