from django.test import TestCase
from django.core.mail import send_mail
from cope_with_disaster.models import User, Rescuer
# Create your tests here.
#send_mail('Subject here', 'Hello', 'mohitkv741@gmail.com', ['mohit.verma741@gmail.com'], fail_silently=False)

nums = ''
for users in User.objects.all():
    nums += '91'+str(Rescuer.objects.filter(user=users).first().phone)+','
nums = nums[:-1]
print(nums)