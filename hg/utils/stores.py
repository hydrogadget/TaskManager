from flask import g
from contextlib import closing
import sqlite3

import hg
from hg.utils.queues import SqliteQueue

def purge_backing_stores():
    try:
        os.remove(hg.app.config['PRIORITY_QUEUE_BACKING_STORE'])
        os.remove(hg.app.config['CURRENT_EVENT_BACKING_STORE'])
    except:
        pass

def get_priority_backing_store():
    db = getattr(g, '_priority_queue', None)
    if db is None:
        db = g._priority_queue = SqliteQueue(hg.app.config['PRIORITY_QUEUE_BACKING_STORE'])
    return db

def get_current_backing_store():
    db = getattr(g, '_current_event', None)
    if db is None:
        db = g._current_event = SqliteQueue(hg.app.config['CURRENT_EVENT_BACKING_STORE'])
    return db

def get_hg_db():
    with hg.app.app_context():
        db = getattr(g, '_hg_db', None)
        if db is None:
            db = g._hg_db = sqlite3.connect(hg.app.config['HYDROGADGET_DB'])
        return db

def init_hg_db():

    try:
        os.remove(hg.app.config['HYDROGADGET_DB'])
    except:
        pass

    with hg.app.app_context():
        with closing(get_hg_db()) as db:
            with hg.app.open_resource('../schema.sql') as f:
                db.cursor().executescript(f.read())
            db.commit()

