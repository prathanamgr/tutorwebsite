from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone

from reg.models import *
from reg.utils import sendMail


@login_required(login_url='/reg')
def show(request):
    um = userModel.objects.get(user=request.user)
    if request.method == 'POST':
        if request.POST.get('search'):
            search=request.POST['subject']
            umObjs=[]
            uobj=User.objects.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search) | Q(email__icontains=search))
            ums=userModel.objects.filter(Q(subject__icontains=search))
            for i in uobj:
                try:
                    umObjs.append(userModel.objects.get(status='Teacher',user=i.id))
                except Exception as e:
                    print(e)
            for i in ums:
                umObjs.append(i)
            content = {
                'um': um,
                'ums': umObjs
            }
            return render(request, 'webpages/book.html', content)


    content={
        'um':um
    }
    return render(request,'webpages/index.html',content)
@login_required(login_url='/reg')
def contact(request):
    um = userModel.objects.get(user=request.user)
    content = {
        'um': um
    }
    return render(request,'webpages/contact.html',content)
@login_required(login_url='/reg')
def about(request):
    um = userModel.objects.get(user=request.user)
    content = {
        'um': um
    }
    return render(request,'webpages/about.html',content)
@login_required(login_url='/reg')
def tutors(request):
    um = userModel.objects.get(user=request.user)
    if request.method == 'POST':
        if request.POST.get('msgs'):
            teacher=User.objects.get(id=request.POST['id'])
            student=request.user
            message=request.POST['msg']
            date1=datetime.now()
            date2=timezone.now()
            if um.status=='Student':
                mObj=meetings(student=student,teacher=teacher,message=message,date=date1,date2=date2)
                mObj.save()
                sendMail(request,teacher.email,student.email,message)
                messages.info(request,'Contacted!!')
                return redirect('/tutors')
            else:
                messages.info(request,'Teacher cannot book another teacher!!')
                return redirect('/tutors')

    ums=userModel.objects.filter(status='Teacher').count()
    if ums>0:
        ums1 = userModel.objects.filter(status='Teacher')
    else:
        ums1=""
    content = {
        'um': um,
        'ums':ums1
    }
    return render(request,'webpages/book.html',content)