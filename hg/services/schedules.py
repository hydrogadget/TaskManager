from flask.views import MethodView
from flask import request, jsonify
import time

# from hg.utils.stores import get_current_backing_store, get_priority_backing_store
from hg.utils.stores import get_hg_db

class API(MethodView):

    def get(self):
        db = get_hg_db()
        cur = db.execute('select label, address, city, state, zip from location')
        location = [dict(label=row[0], address=row[1], city=row[2], state=row[3], zip=row[4]) for row in cur.fetchall()]
        return jsonify(location)

    def post(self):
        pass

    def delete(self):
        p = get_priority_backing_store()
        j = p.popleft(sleep_wait=False)
        return str(j) + " "
