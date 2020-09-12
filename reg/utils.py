import os
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from reg.models import userModel

pattern='\d'
def validation(myDetails):
    emailContainer = []
    userContainer = []
    uobj=User.objects.all()
    for i in uobj:
        emailContainer.append(i.email)
        userContainer.append(i.username)
    if myDetails['un'] in userContainer:
        return "Username already exists!!"
    elif myDetails['em'] in emailContainer:
        return "Email address already exists!!"
    elif myDetails['pw'] != myDetails['cpw']:
        return "Password Mismatch!!"
    elif re.search(pattern,myDetails['ph'])==False:
        return "Invalid phone number!!"
    elif len(myDetails['ph'])>10 or len(myDetails['ph'])<10:
        return "Invalid phone number length!!"
    else:
        return True

def sendMail(request,teacher,student,message):
    teacher=User.objects.get(email=teacher)
    student=User.objects.get(email=student)
    print(teacher.email)
    print(student.email)
    std=userModel.objects.get(user=student.id)
    subject='EasyEdu'
    greeting=f'Dear {teacher.first_name} {teacher.last_name}!'
    heading=f'{student.first_name} {student.last_name} wants to contact you!'
    emails=student.email
    message=message
    ph=std.ph
    html_content=render_to_string(settings.BASE_DIR+'/templates/webpages/emailMessages.html',{'usage':'msg','heading':heading,'message':message,'ph':ph,'email':emails,'greeting':greeting})
    mail=EmailMessage(subject,html_content,"projectgroups456@gmail.com",[teacher.email])
    mail.content_subtype='html'
    mail.send()