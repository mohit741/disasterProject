from django.test import TestCase
from django.core.mail import send_mail

# Create your tests here.
send_mail('Subject here', 'Hello', 'mohitkv741@gmail.com', ['mohit.verma741@gmail.com'], fail_silently=False)
