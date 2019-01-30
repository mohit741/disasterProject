"""This module is used for automatic posting to facebook page and send emails in case
    of emergency.
    Email Service : SendGrid on Azure """
import os
import urllib.request
import urllib.parse
import facebook
import json
from cope_with_disaster import tweet_analyzer
from cope_with_disaster.models import *
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.core.mail import send_mail
from geopy.geocoders import GoogleV3
from disasterProject.settings import BASE_DIR

DEFAULT_FROM_EMAIL = 'admin@copingwithdisaster.azurewebsites.net'
SMS_API_KEY = ''
page_access_token = ''

# Create scheduler instance and Configure jobstore
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


# Triggered in case of warning
def post_warning():
    msg = str(Variable.objects.filter(name='MSG').first().info)
    sms = str(Variable.objects.filter(name='SMS_MSG').first().info)
    coords = Variable.objects.filter(name='LatLng').first().info
    if coords != 'null' :
        get_tweet_data()
        geolocator = GoogleV3(api_key='AIzaSyCcHofqZ7qVRGDmAOFyJK9ufcjJow6fFEU')
        address = geolocator.reverse(coords)
        place = str(address[2])[:-7]
        msg = msg.format(place)
        sms = sms.format(place)
        mail_list = list()
        nums = ''
        for users in User.objects.all():
            mail_list.append(str(users))
            print(mail_list)
        for rescuer in Rescuer.objects.all():
            nums += '91' + str(rescuer.phone) + ','
        nums = nums[:-1]

        # Send E-mail
        send_mail('Flood Warning : Urgent', msg, DEFAULT_FROM_EMAIL, mail_list, fail_silently=False)

        # Send SMS
        resp = sendsms(SMS_API_KEY, nums, 'TXTLCL', sms)
        print(resp)

        # Post to facebook page
        graph = facebook.GraphAPI(page_access_token)
        graph.put_object(parent_object='me', connection_name="feed", message=msg,
                         link='copingwithdisaster.azurewebsites.net')
        print('Done')


# Code to send sms using TextLocal
def sendsms(apikey, numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': message, 'sender': sender, 'test': 'false'})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return fr


def get_tweet_data():
    lat, lng, num, info = tweet_analyzer.tweet_update()
    lat = lat[:-2]
    lng = lng[:-2]
    if lat == '0' or lng == '0' or num == '0':
        return
    entry = {'lat': lat, 'lon': lng, 'ph': num, 'info': info}
    print(entry)
    fp = os.path.join(BASE_DIR, 'cope_with_disaster/json_data/needs.json')
    d = json.load(open(fp))
    print(d)
    d['food'].append(entry)
    print(d)
    json.dump(d, open(fp,'w'))
    print(d)


@register_job(scheduler, "interval", seconds=60, replace_existing=True)
def fb_job():
    post_warning()


register_events(scheduler)

scheduler.start()
# print("Scheduler started!")
