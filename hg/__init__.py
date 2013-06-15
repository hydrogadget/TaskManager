from flask import Flask, g
import sqlite3, os

app = Flask(__name__)
app.config.from_object('hg.config')
app.debug = True

from hg.services import schedules
from hg.utils.queues import SqliteQueue
from hg.utils.stores import purge_backing_stores, get_priority_backing_store
from hg.utils.stores import get_current_backing_store

from hg.cron import water_scheduler_timer

# API Routes for watering schedule
s_view = schedules.API.as_view('schedule_api')
app.add_url_rule('/schedules/<string:user_id>', view_func=s_view, methods=['GET',])
app.add_url_rule('/schedules/', view_func=s_view, methods=['POST','DELETE'])

purge_backing_stores()
x = water_scheduler_timer()
x.start()

