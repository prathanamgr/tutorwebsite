from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# Create your views here.
from reg.models import *
from reg.utils import *


def login(request):
    if request.method == "POST":
        if request.POST.get('login'):
            un = request.POST['un']
            pw = request.POST['pw']
            user = auth.authenticate(username=un, password=pw)
            if user is not None:
                auth.login(request, user)
                um = userModel.objects.get(user=request.user)
                um.online = True

                um.save()

                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))

                else:
                    return redirect('/')
            else:
                messages.error(request, "Email or Password incorrect!!")
                return redirect('/reg')

    return render(request,'webpages/login.html')

def register(request):
    if request.method == "POST":
        if request.POST.get('registerStudent'):
            fn = request.POST['fn']
            ln = request.POST['ln']
            un = request.POST['un']
            em = request.POST['em']

            ph = request.POST['ph']

            pw = request.POST['pw']
            cpw = request.POST['cpw']
            myDetails = {
                "un": un,
                "em": em,
                "ph": ph,
                "pw": pw,
                "cpw": cpw
            }
            b = validation(myDetails)
            if b == True:
                uobj = User.objects.create_user(first_name=fn, last_name=ln, email=em, username=un, password=pw)
                uobj.save()
                umobj = User.objects.get(username=un)
                um = userModel(user=umobj, address="", ph=ph, online=False, profile="",
                               gender="",status="Student",experience="",prefer="",subject="")
                um.save()
                messages.success(request, "Registered Successfully!!")
                return redirect('/reg')
            else:
                messages.error(request, b)
                return redirect('/reg/register')

    return render(request,'webpages/register.html')

def teacherReg(request):
    if request.method == "POST":
        if request.POST.get('tutor'):
            fn = request.POST['fn']
            ln = request.POST['ln']
            un = request.POST['un']
            em = request.POST['em']

            ph = request.POST['ph']
            gender=request.POST['gender']
            pw = request.POST['pw']
            cpw = request.POST['cpw']
            place=request.POST['place']
            exp=request.POST['experience']
            prefer=request.POST['prefer']
            fs=FileSystemStorage()
            img=request.FILES['img']
            fs.save(img.name,img)
            subject=request.POST['subject']
            myDetails = {
                "un": un,
                "em": em,
                "ph": ph,
                "pw": pw,
                "cpw": cpw
            }
            b = validation(myDetails)
            if b == True:
                uobj = User.objects.create_user(first_name=fn, last_name=ln, email=em, username=un, password=pw)
                uobj.save()
                umobj = User.objects.get(username=un)
                um = userModel(user=umobj, address=place, ph=ph, online=False, profile=img.name,
                               gender=gender, status="Teacher", experience=exp, prefer=prefer, subject=subject)
                um.save()
                messages.success(request, "Registered Successfully!!")
                return redirect('/reg')
            else:
                messages.error(request, b)
                return redirect('/reg/register')

    return render(request, 'webpages/tutor.html')

def logout(request):
    um=userModel.objects.get(user=request.user)
    um.online=False
    um.save()
    auth.logout(request)
    return redirect('/reg')