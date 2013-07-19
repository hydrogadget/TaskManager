from flask.views import MethodView
from flask import request, jsonify

from hg.utils.stores import get_hg_db

class API(MethodView):

    # List 
    def get(self):
        db = get_hg_db()

        configuration=[]
        for row in db.execute('select * from configuration'):
            valves.append(dict(id=row[0], label=row[1]))

        db.close()
        
        return jsonify(valves=valves)

    # Add
    def post(self):

        stmt = "update configuration set "
        for x in request.form.keys():
            stmt = stmt + x + "='" + request.form[x] + "', "

        print stmt[:-2]
        return jsonify(status="Yep")

        """
                db = get_hg_db()
                cur = db.execute('insert into valves (label, id) values (?, ?)', self._get_fields())
                db.commit()
                db.close()
                return jsonify(status="Added new valve")
        """

    # Update
    def put(self):
        db = get_hg_db()
        cur = db.execute('update values set label = ? where id = ?', self._get_fields())
        db.commit()
        db.close()
        return jsonify(status="Added new valve")

    # Delete
    def delete(self):
        db = get_hg_db()
        cur = db.execute('delete from valves where id = ?', request.form['id'])
        db.commit()
        db.close()
        return jsonify(status="Valve Deleted")

