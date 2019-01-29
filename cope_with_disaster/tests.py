from django.test import TestCase
from django.core.mail import send_mail
from cope_with_disaster.models import Rescuer, Variable
from cope_with_disaster.fb_auto_post import sendsms, SMS_API_KEY, DEFAULT_FROM_EMAIL
# Create your tests here.


"""print('testing')
msg = Variable.objects.filter(name='MSG').first().info
k = send_mail('Subject here', msg, DEFAULT_FROM_EMAIL, ['mohit.verma741@gmail.com','maqbool.dhn2011@gmail.com'], fail_silently=False)
print(k)
resp = sendsms(SMS_API_KEY, '918102071481', 'TXTLCL', 'Hello there')"""