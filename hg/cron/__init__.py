import time
from apscheduler.scheduler import Scheduler

from hg.utils.stores import get_hg_db

import logging

logging.basicConfig()

CHECK_INTERVAL = 60

def water_scheduler_timer():
    sched = Scheduler()

    @sched.interval_schedule(seconds=CHECK_INTERVAL)
    def check_for_new_events():

        # Positions: Sun = 0, Sat = 6, start_time = 7
        select_list = [0,0,0,0,0,0,0,0]
        select_list[int(time.strftime("%w"))] = 1
        select_list[7] = int(time.strftime("%H%M"))

        db = get_hg_db()

        cur = db.execute('select valve, duration, start_time from schedule where sun = ? \
                AND mon = ? AND tue = ? AND wed = ? AND thu = ? AND fri = ? \
                AND sat = ? AND start_time = ?', select_list)

        timer_event = [dict(valve=row[0], duration=row[1], start_time=row[2], command=0) for row in cur.fetchall()]
        db.close()

        print timer_event

    return sched
