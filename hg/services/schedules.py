from flask.views import MethodView
from flask import request
import time

from hg.utils.stores import get_current_backing_store, get_priority_backing_store

class API(MethodView):

    def get(self, user_id):
        pass

    def post(self):
        p = get_priority_backing_store()
        p.append(time.time())
        return str("add")

    def delete(self):
        p = get_priority_backing_store()
        j = p.popleft(sleep_wait=False)
        return str(j) + " "
