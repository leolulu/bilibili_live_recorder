import arrow
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED, EVENT_JOB_MISSED
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from daily_take_in import daily_take_in
from del_empty_folder import del_empty_folder
from live_video_transform import search_flv_transform
from qbittrent_api import QbittrentClient


class Counter:
    BILIBILI_TAKE_IN_COUNTER = 0

    def __init__(self):
        self.init_minutes = 10
        self.increase_ratio = 1.5131
        self.increase_times = 0
        self.interval_minutes = self.init_minutes

    def time_multiplicate(self):
        if self.increase_times <= 12:
            self.interval_minutes *= self.increase_ratio
            self.increase_times += 1

    def time_reset(self):
        self.interval_minutes = self.init_minutes
        self.increase_times = 0


def test():
    print('test:', arrow.now())
    if arrow.now().format('ss')[-1] == '0':
        raise UserWarning('自定义错误')


def resume_torrent(scheduler, counter: Counter):
    # scheduler.get_jobs()[0].trigger.interval.total_seconds()//60
    api = QbittrentClient()
    print(arrow.now().format(), '登陆了Qbittrent...')
    api.login()
    has_error = api.resume_torrent()
    api.logout()
    if has_error:
        api.sent_to_server_chan()
        counter.time_reset()
    else:
        counter.time_multiplicate()
    # scheduler.modify_job('resume_torrent', minutes=counter.interval_minutes)
    scheduler.reschedule_job('resume_torrent', trigger=IntervalTrigger(minutes=counter.interval_minutes))


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
            Counter.BILIBILI_TAKE_IN_COUNTER += 1
            if Counter.BILIBILI_TAKE_IN_COUNTER % 4 == 0:
                print(arrow.now().format(), '下一次整理录播文件时间：', arrow.get(job_.next_run_time).humanize(locale='zh'))
        if job_.id == 'resume_torrent':
            print(arrow.now().format(), '下一次恢复torrent时间：', arrow.get(job_.next_run_time).humanize(locale='zh'))


# cron_bilibili_take_in = CronTrigger(hour='5')
cron_search_flv_transform = CronTrigger(hour='4')
del_resume_torrent_counter = Counter()
corn_print_job = CronTrigger(hour='*/3')
corn_del_empty_folder = CronTrigger(minute='*/5')
corn_del_resume_torrent = IntervalTrigger(minutes=del_resume_torrent_counter.interval_minutes)


scheduler = BlockingScheduler()
scheduler.add_listener(runtime_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)
# scheduler.add_job(daily_take_in, cron_bilibili_take_in, [r"C:\LiveRecord\22128636", 'metadata'], coalesce=True, misfire_grace_time=60, id='bilibili_take_in')
scheduler.add_job(search_flv_transform, cron_search_flv_transform, ["//192.168.123.44/LiveRecord/22128636-OakNose", "//192.168.123.44/LiveRecord/7969549-暂停实验室", "//192.168.123.44/LiveRecord/12572155-腾讯研究院"], coalesce=True, misfire_grace_time=60)
scheduler.add_job(print_job, corn_print_job, (scheduler,), coalesce=True, misfire_grace_time=60)
# scheduler.add_job(del_empty_folder, corn_del_empty_folder, [r"C:\btdownload"], misfire_grace_time=5)
# scheduler.add_job(resume_torrent, corn_del_resume_torrent, [scheduler, del_resume_torrent_counter], misfire_grace_time=10, id='resume_torrent')

print('begin: ', arrow.now())
scheduler.start()
