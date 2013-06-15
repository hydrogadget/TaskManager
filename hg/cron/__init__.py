from apscheduler.scheduler import Scheduler

def water_scheduler_timer():
    sched = Scheduler()

    @sched.interval_schedule(seconds=5)
    def check_for_new_events():
        print "hello, timer"

    return sched
