"""This module is used for automatic posting to facebook page and send emails in case
    of emergency.
    Email Service : SendGrid on Azure """

import facebook
from cope_with_disaster.models import *
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.core.mail import send_mail


DEFAULT_FROM_EMAIL = 'admin@copingwithdisaster.azurewebsites.net'


# Create scheduler instance and Configure jobstore
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


# Triggered in case of warning
def post_warning():
    page_access_token = Variable.objects.filter(name='FB_KEY').first().info
    flag = False # Variable.objects.filter(name='FAKE_WARNING').first().info
    msg = '' # Variable.objects.filter(name='MSG').first().info
    if flag == 'true':
        l = list()
        for users in User.objects.all():
            l.append(str(users))
        msg = msg.format('FAKE AREA', 'high')
        send_mail('Flood Warning : Urgent', msg, DEFAULT_FROM_EMAIL, l, fail_silently=False)
        graph = facebook.GraphAPI(page_access_token)
        graph.put_object(parent_object='me', connection_name="feed", message=msg,
                         link='copingwithdisaster.azurewebsites.net')


@register_job(scheduler, "interval", seconds=60, replace_existing=True)
def fb_job():
    post_warning()


register_events(scheduler)

scheduler.start()
# print("Scheduler started!")
