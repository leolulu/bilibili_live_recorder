from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
import arrow
from daily_take_in import daily_take_in
from del_empty_folder import del_empty_folder


def test():
    print('test:', arrow.now())
    if arrow.now().format('ss')[-1] == '0':
        raise UserWarning('自定义错误')


def runtime_listener(event):
    if event.code == EVENT_JOB_EXECUTED:
        if event.job_id == 'bilibili_take_in':
            print(arrow.now().format(), f'{event.job_id} 任务运行成功...')
    elif event.code == EVENT_JOB_ERROR:
        print(arrow.now().format(), '出错了，原因如下：')
        print(event.exception)
    elif event.code == EVENT_JOB_MISSED:
        print(arrow.now().format(), '任务错过了...')


def print_job(scheduler):
    for job_ in scheduler.get_jobs():
        # print(job_)
        if job_.id == 'bilibili_take_in':
            print('下一次整理时间：', arrow.get(job_.next_run_time).humanize(locale='zh'))


cron_bilibili_take_in = CronTrigger(hour='5')
corn_print_job = CronTrigger(hour='*/17', jitter=3600)
corn_del_empty_folder = CronTrigger(minute='*/5')

scheduler = BlockingScheduler()
scheduler.add_listener(runtime_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)
scheduler.add_job(daily_take_in, cron_bilibili_take_in, [r"C:\LiveRecord\22128636", 'metadata'], coalesce=True, misfire_grace_time=60, id='bilibili_take_in')
scheduler.add_job(print_job, corn_print_job, (scheduler,), misfire_grace_time=60)
scheduler.add_job(del_empty_folder, corn_del_empty_folder, [r"C:\BaiduNetdiskDownload"], misfire_grace_time=5)

print('begin: ', arrow.now())
scheduler.start()
