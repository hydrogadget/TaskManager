from flask.views import MethodView
from flask import request, jsonify
import time

from hg.utils.stores import get_hg_db

class API(MethodView):

    def get(self, day=None):
        db = get_hg_db()

        sql_stmt = 'select id, valve, duration, start_time, sun, mon, tue, wed, thu, fri, sat from schedule'

        if (day != None):
            sql_stmt = sql_stmt + ' where ' + day + ' = 1' 

        schedules = []
        for row in db.execute(sql_stmt):
            schedules.append(dict(id=row[0],valve=row[1],duration=row[2],start_time=row[3],sun=row[4],mon=row[5],tue=row[6],wed=row[7],thu=row[8],fri=row[9],sat=row[10]))
    
        db.close()
        return jsonify(schedules=schedules)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

"""
p = get_priority_backing_store()
j = p.popleft(sleep_wait=False)
return str(j) + " "
"""
