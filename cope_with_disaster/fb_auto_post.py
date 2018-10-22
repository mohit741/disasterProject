import random

import facebook
import time
from cope_with_disaster.models import *
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

x = 'data'
# page_access_token = 'EAAKUSbFF9yMBAGQyRlXdcTokcoORnHu90x1O7SpgsOQiIPZCg8q1afMBmeDEyfhv233yMoOyTwxmgdvScrP3brvlYHZB8klfAZB91t7rsfh7OQH3lhbDspkSqnEoRfZC3gR3IO3tgxKO1xZCqCsEtGK4A1ui6nozZA23zx8QQ9mG1ShZBWMkMKiEATXUjc00MqtNNq4FubBWAZDZD'

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


def post_warning():
    page_access_token = str(Variable.objects.filter(name='FB_KEY').first().name)
    flag = Variable.objects.filter(name='FAKE_WARNING').first().info
    msg = Variable.objects.filter(name='MSG').first().info
    if flag == 'true':
        msg = msg.format('demo', 'high')
        print(msg)
        graph = facebook.GraphAPI(page_access_token)
        graph.put_object(parent_object='me', connection_name="feed", message=msg,
                         link='copingwithdisaster.azurewebsites.net')


@register_job(scheduler, "interval", seconds=60, replace_existing=True)
def fb_job():
    post_warning()


register_events(scheduler)

scheduler.start()
# print("Scheduler started!")
