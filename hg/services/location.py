from flask.views import MethodView
from flask import request, jsonify

from hg.utils.stores import get_hg_db

class API(MethodView):

    def _get_fields(self):
        location_list = []
        location_list.append(request.form['label'])
        location_list.append(request.form['street'])
        location_list.append(request.form['city'])
        location_list.append(request.form['state'])
        location_list.append(request.form['zip'])
        return location_list

    # List 
    def get(self):
        db = get_hg_db()
        cur = db.execute('select label, street, city, state, zip from location')
        row = cur.fetchone()
        db.close()
        location = dict(label=row[0], street=row[1], city=row[2], state=row[3], zip=row[4])
        return jsonify(location)

    # Add new
    def post(self):
        db = get_hg_db()
        cur = db.execute('insert into location values(null, ?, ?, ?, ?, ?)', self._get_fields())
        db.commit()
        db.close()
        return jsonify(status="Added New Location")
    
    # Update
    def put(self):
        db = get_hg_db()
        cur = db.execute('delete from location')
        cur = db.execute('insert into location values(null, ?, ?, ?, ?, ?)', self._get_fields())
        # cur = db.execute('update location set label=?, street=?, city=?, state=?, zip=?', self._get_fields())
        db.commit()
        db.close()
        return jsonify(status="Updated Location")

    # Delete
    def delete(self):
        db = get_hg_db()
        cur = db.execute('delete from location')
        db.commit()
        db.close()
        return jsonify(status="Location Deleted")

