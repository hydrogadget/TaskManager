import sqlite3, logging, time, json
from contextlib import closing
from apscheduler.scheduler import Scheduler
from collections import deque

from flask import Flask, request, session, g, Response, jsonify

DATABASE = '/tmp/hydrogadget.db'
DEBUG = True
SECRET_KEY = 'the key'
# USERNAME = 'admin'
# PASSWORD = 'default'
CHECK_FOR_NEW_EVENTS_INTERVAL = 60
LOG_FILE_LOCATION="/tmp/hydrogadget.log"

app = Flask(__name__)
app.config.from_object(__name__)

TASK_QUEUE = deque()
PRIORITY_TASK_QUEUE = deque()
CURRENTLY_RUNNING_QUEUE = []

task_queue_log = logging.FileHandler(LOG_FILE_LOCATION)
task_queue_log.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

task_queue_log.setLevel(logging.INFO)
app.logger.addHandler(task_queue_log)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

logging.basicConfig()
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

    timer_event = [dict(valve=row[0], duration=row[1], start_time=row[2]) for row in cur.fetchall()]
    db.close()
    
    if len(timer_event) > 0:
        app.logger.info("adding event")
        TASK_QUEUE.append(json.dumps(timer_event[0]))

sched.start()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

# pt-bare@zappos.com / Goldbull13

@app.route('/next/event', methods=['GET'])
def next_event():

    if len(TASK_QUEUE) > 0:
        js = json.dumps(TASK_QUEUE.popleft())
    else:
        js = json.dumps({'valve':0,'duration':0,'start_time':0})

    return Response(js, status=200, mimetype='application/json')

@app.route('/list/queue', methods=['GET'])
def list_queue():
    j = []
    for x in TASK_QUEUE:
        j.append(x)

    return json.dumps(j,sort_keys=True, indent=2)

if __name__ == '__main__':
    app.run()

