from flask import Flask

app = Flask(__name__)
app.config.from_object('hg.config')
app.debug = True

from hg.services import schedules
from hg.cron import water_scheduler_timer
from hg.utils.stores import purge_backing_stores

#
# API Routes for watering schedule
#
s_view = schedules.API.as_view('schedule_api')
app.add_url_rule('/schedules/<string:user_id>', view_func=s_view, methods=['GET',])
app.add_url_rule('/schedules/', view_func=s_view, methods=['POST','DELETE'])

#
# System Initalization
#
purge_backing_stores()
water_scheduler_timer().start()

