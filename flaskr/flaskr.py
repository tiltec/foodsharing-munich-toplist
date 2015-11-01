# -*- coding: utf-8 -*-

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
     
DATABASE = '../scraper/foodsharingstats.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

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
@crossdomain(origin='*')
def overview():
    entries = read_stats()    
    userentries = []
    userids = set([_['userid'] for _ in entries])
    for u in userids:
        userentries.append( {'userid': u,
             'entries': [e for e in entries if e['userid'] == u]
             })
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