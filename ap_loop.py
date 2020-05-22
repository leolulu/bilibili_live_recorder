from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
import arrow
from daily_take_in import daily_take_in


def test():
    print('test:', arrow.now())
    if arrow.now().format('ss')[-1] == '0':
        raise UserWarning('自定义错误')


def my_event(event):
    if event.code == EVENT_JOB_EXECUTED:
        print(arrow.now().format(), '任务运行成功...')
    elif event.code == EVENT_JOB_ERROR:
        print(arrow.now().format(), '出错了，原因如下：')
        print(event.exception)
    elif event.code == EVENT_JOB_MISSED:
        print(arrow.now().format(), '任务错过了...')


#cron_convert = CronTrigger(hour='5')
cron_convert = CronTrigger(hour='11')
# cron_test = CronTrigger(second='*/5')

scheduler = BlockingScheduler()
scheduler.add_listener(my_event, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)
scheduler.add_job(daily_take_in, cron_convert, [r"C:\LiveRecord\22128636", 'metadata'], coalesce=True, misfire_grace_time=60)
# scheduler.add_job(test, cron_test)

print('begin: ', arrow.now())
scheduler.start()
