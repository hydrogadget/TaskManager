from flask.views import MethodView
from flask import request, jsonify
import time

from hg.utils.stores import get_hg_db

class API(MethodView):

    def _get_fields(self):
        s_list = []
        s_list.append(request.form['valve'])
        s_list.append(request.form['duration'])
        s_list.append(request.form['start_time'])
        s_list.append(request.form['sun'])
        s_list.append(request.form['mon'])
        s_list.append(request.form['tue'])
        s_list.append(request.form['wed'])
        s_list.append(request.form['thu'])
        s_list.append(request.form['fri'])
        s_list.append(request.form['sat'])
        return s_list

    # list
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

    # Add new
    def post(self):
        db = get_hg_db()
        cur = db.execute('insert into schedule values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', self._get_fields())
        db.commit()
        db.close()
        return jsonify(status="Added new schedule")

    # Update
    def put(self):
        db = get_hg_db()

        sql_stmt = 'update schedule set valve = ?, duration = ?, start_time = ?, sun = ?, mon = ?, tue = ?, wed = ?, thu = ?, fri = ?, sat = ? where id = ?'

        fields = self._get_fields()
        fields.append(request.form['id'])
        cur = db.execute(sql_stmt, fields)
        db.commit()
        db.close()

        return jsonify(status="Updated schedule")

    # Delete
    def delete(self):
        db = get_hg_db()

        sql_stmt = 'delete from schedule where id=?'

        sid = [request.form["id"],]
        cur = db.execute(sql_stmt,sid)
        db.commit()
        db.close()
        return jsonify(status="Schedule deleted")

"""
p = get_priority_backing_store()
j = p.popleft(sleep_wait=False)
return str(j) + " "
"""
