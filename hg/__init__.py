from flask import Flask

app = Flask(__name__)
app.config.from_object('hg.config')
app.debug = True

from hg.services import schedules
from hg.services import location
from hg.services import valves
from hg.services import water_group
from hg.services import network_settings

from hg.cron import water_scheduler_timer
from hg.utils.stores import purge_backing_stores

#
# API Routes for watering schedule
#
s_view = schedules.API.as_view('schedule_api')
app.add_url_rule('/schedules/', view_func=s_view, methods=['GET','POST','DELETE','PUT'])
app.add_url_rule('/schedules/<day>', view_func=s_view, methods=['GET'])

l_view = location.API.as_view('location_api')
app.add_url_rule('/location/', view_func=l_view, methods=['GET','POST','PUT','DELETE'])

v_view = valves.API.as_view('valves_api')
app.add_url_rule('/valves/', view_func=v_view, methods=['GET','POST','PUT','DELETE'])

w_view = water_group.API.as_view('water_group_api')
app.add_url_rule('/watergroup/', view_func=c_view, methods=['GET','POST','PUT','DELETE'])

n_view = network_settings.API.as_view('network_settings_api')
app.add_url_rule('/network/', view_func=c_view, methods=['GET','POST','PUT','DELETE'])

#
# System Initalization
#
purge_backing_stores()
# water_scheduler_timer().start()

