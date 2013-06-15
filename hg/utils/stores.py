from flask import g

def purge_backing_stores():
    try:
        os.remove(app.config['PRIORITY_QUEUE_BACKING_STORE'])
        os.remove(app.config['CURRENT_EVENT_BACKING_STORE'])
    except:
        pass

def get_priority_backing_store():
    db = getattr(g, '_priority_queue', None)
    if db is None:
        db = g._priority_queue = SqliteQueue(app.config['PRIORITY_QUEUE_BACKING_STORE'])
    return db

def get_current_event_backing_store():
    db = getattr(g, '_current_event', None)
    if db is None:
        db = g._current_event = SqliteQueue(app.config['CURRENT_EVENT_BACKING_STORE'])
    return db

def event_queue_backing_store():
    pass


