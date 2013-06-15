from flask.views import MethodView
from flask import request
import time

import hg

class API(MethodView):

    def get(self, user_id):
        pass

    def post(self):
        p = hg.get_priority_backing_store()
        p.append(time.time())
        return str("add")

    def delete(self):
        p = hg.get_priority_backing_store()
        j = p.popleft(sleep_wait=False)
        return str(j) + " "
