import sqlite3, logging, time, json
from contextlib import closing
from apscheduler.scheduler import Scheduler
from collections import deque

from logging.handlers import RotatingFileHandler
from logging import Formatter

from flask import Flask, request, session, g, Response, jsonify

DATABASE = '/tmp/hydrogadget.db'
DEBUG = True

SECRET_KEY = 'the key'
# USERNAME = 'admin'
# PASSWORD = 'default'

CHECK_FOR_NEW_EVENTS_INTERVAL = 60
LOG_FILE_LOCATION="/tmp/hydrogadget.log"
NULL_EVENT = {"valve":None,"duration":None,"start_time":None,"command":None}

EVENT_QUEUE = deque()
PRIORITY_EVENT = [NULL_EVENT,]
CURRENT_EVENT = [NULL_EVENT,]

app = Flask(__name__)
app.config.from_object(__name__)

file_handler = RotatingFileHandler('/tmp/hydrogadget.log')

file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

# logging.basicConfig()
sched = Scheduler()

@sched.interval_schedule(seconds=CHECK_FOR_NEW_EVENTS_INTERVAL)
def check_for_new_events():

    # Positions: Sun = 0, Sat = 6, time = 7
    select_list = [0,0,0,0,0,0,0,0]
    select_list[int(time.strftime("%w"))] = 1
    select_list[7] = int(time.strftime("%H%M"))
    db = connect_db()
    cur = db.execute('select valve, duration, start_time from schedule where mon = ? \
            AND tue = ? AND wed = ? AND thu = ? AND fri = ? AND sat = ? \
            AND sun = ? AND start_time = ?', select_list)

    timer_event = [dict(valve=row[0], duration=row[1], start_time=row[2], command=0) for row in cur.fetchall()]
    db.close()
    
    if len(timer_event) > 0:
        app.logger.info("adding event " + repr(timer_event[0]))
        EVENT_QUEUE.append(timer_event[0])

sched.start()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/list/events', methods=['GET'])
def list_queue():

    j = []
    for x in EVENT_QUEUE:
        j.append(x)

    js = json.dumps(j,sort_keys=True, indent=2)
    return Response(js, status=200, mimetype='application/json')

@app.route('/next/event', methods=['POST'])
def next_event():

    if len(EVENT_QUEUE) > 0:
        js = json.dumps(EVENT_QUEUE.popleft())
    else:
        js = json.dumps(NULL_EVENT)

    CURRENT_EVENT[0] = js
    return Response(js, status=200, mimetype='application/json')

@app.route('/current/event', methods=['GET'])
def current_event():

    return Response(CURRENT_EVENT, status=200, mimetype='application/json')

@app.route('/list/priority', methods=['GET'])
def check_priority():

    return Response(json.dumps(PRIORITY_EVENT), status=200, mimetype='application/json')

@app.route('/add/priority', methods=['POST'])
def add_priority():

    event = {'valve': int(request.form['valve']),
             'command': int(request.form['command']),
             'duration': int(request.form['duration']),
             'start_time': int(request.form['start_time'])
             }

    PRIORITY_EVENT[0] = event
    return Response(json.dumps(PRIORITY_EVENT), status=200, mimetype='application/json')

@app.route('/next/priority', methods=['POST'])
def next_priority():

    js = json.dumps(PRIORITY_EVENT)
    PRIORITY_EVENT = NULL_EVENT

    return Response(js, status=200, mimetype='application/json')

@app.route('/', methods=['GET','POST'])
def index():
    return Response(json.dumps(NULL_EVENT), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run()

