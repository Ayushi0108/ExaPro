import random
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from main.decorators import unauthenticated_user, allowed_users, admin_only
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from authentication.models import UserProf
from authentication.forms import UserProfForm
from django.contrib.auth.models import User, Group
from django.conf import settings

@login_required(login_url="user-login")
def create_exam(request):

    if request.method=="POST" and 'create-exam' in request.POST:
        eid1 = request.POST['eid']
        email = request.session['user']
        exname = request.POST['exam-name']
        sub=request.POST['subject']
        dur = request.POST['time']
        tmark = request.POST['total-marks']
        if eid1=="":
            eid = create_eid()
            ins = CreateExam(eid=eid,email=email,exam_name=exname,subject=sub,duration=dur,tmarks=tmark,status=False)
            ins.save()
            sd = CreateExam.objects.get(eid=eid)
            action = "Exam Created Successfully"
        else:
            eid1 = request.POST['eid']
            sd = CreateExam.objects.get(eid=eid1)
            sd.exam_name = exname
            sd.subject = sub
            sd.duration = dur
            sd.tmarks = tmark
            sd.save()
            globals()['max'] = max_marks(eid1)
            action = "Exam Updated Successfully"
        try:
            ins = Eligibility.objects.get(eid=eid1)
        except ObjectDoesNotExist:
            ins = None

        ins2 = SetQPaper.objects.filter(eid=eid1)
        return render(request,"templates_panels/user/create_exam.html",{"cr":sd,"ins":ins,"ins2":ins2, "action":action})

    elif request.method=="POST" and 'add-mails' in request.POST:
        eid1 = request.POST['eid1']
        eid = request.POST['eid']
        all_emails = request.POST['emails']
        try:
            sd = CreateExam.objects.get(eid=eid)
            if eid1=="":
                ins = Eligibility(eid=eid,all_emails=all_emails)
                ins.save()
               
                action = "Email List Added Successfully"
            else:
                ins = Eligibility.objects.get(eid=eid)
                ins.all_emails = all_emails
                ins.save()
               
                action = "Email List Updated Successfully"
        except ObjectDoesNotExist:
            sd = None
            ins = None
            action = "Oops! No Exam Created"
        ins2 = SetQPaper.objects.filter(eid=eid)
        return render(request,"templates_panels/user/create_exam.html",{"cr":sd,"ins":ins,"ins2":ins2, "action":action})

    elif request.method=="POST" and 'set-que' in request.POST: 

        eid = request.POST['eid']
        que = request.POST['que']
        op1 = request.POST['op1']
        op2 = request.POST['op2']
        op3 = request.POST['op3']
        op4 = request.POST['op4']
        ans = request.POST['ans']
        marks = request.POST['marks']
        try:
          sd = CreateExam.objects.get(eid=eid)
          ins = SetQPaper(eid=eid,questions=que,option1=op1,option2=op2,option3=op3,option4=op4,corr_ans=ans, marks=marks)
          ins.save()
          action = max_marks(eid)
        except ObjectDoesNotExist:
            sd = None
            action = "Oops! No Exam Created"
        try:
            ins = Eligibility.objects.get(eid=eid)
        except ObjectDoesNotExist:
            ins = None
      
        ins2 = SetQPaper.objects.filter(eid=eid)
        return render(request,"templates_panels/user/create_exam.html",{"cr":sd,"ins":ins,"ins2":ins2,"action":action})
        
    elif request.method=="POST" and 'update-que' in request.POST: 
        id = request.POST['id']
        eid = request.POST['eid']
        ins3 = SetQPaper.objects.get(id=id)
        old_marks = ins3.marks
        ins3.questions = request.POST['que']
        ins3.option1 = request.POST['op1']
        ins3.option2 = request.POST['op2']
        ins3.option3 = request.POST['op3']
        ins3.option4 = request.POST['op4']
        ins3.corr_ans = request.POST['ans']
        ins3.marks = request.POST['marks']
        ins3.save()
        action = max_marks(eid)
        if action == None:
            action = "Question Updated Successfully"
        else:
            ins3 = SetQPaper.objects.get(id=id)
            ins3.marks = old_marks
            ins3.save()


        sd = CreateExam.objects.get(eid=eid)
        try:
            ins = Eligibility.objects.get(eid=eid)
        except ObjectDoesNotExist:
            ins = None
      
        ins2 = SetQPaper.objects.filter(eid=eid)
        return render(request,"templates_panels/user/create_exam.html",{"cr":sd,"ins":ins,"ins2":ins2,  "action":action})

    elif request.method=="POST" and 'delete-que' in request.POST: 
        id = request.POST['id']
        eid = request.POST['eid']
        ins3 = SetQPaper.objects.get(id=id)
        ins3.delete()
        sd = CreateExam.objects.get(eid=eid)
       
        try:
            ins = Eligibility.objects.get(eid=eid)
        except ObjectDoesNotExist:
            ins = None
      
        ins2 = SetQPaper.objects.filter(eid=eid)
        action = "Question Deleted Successfully"
        return render(request,"templates_panels/user/create_exam.html",{"cr":sd,"ins":ins,"ins2":ins2, "action":action})

    return render(request,"templates_panels/user/create_exam.html")


def create_eid():
    def eids():
        eid = ""
        char = "asdfhjklpoiuytrewqzxvbnmQWERTYUIOPLKJHGFDSAZXCVBNM1234567890"
        for j in range (0,4):       
            eid = eid + random.choice(char)
        return eid.upper()
    eid = eids()+"-"+eids()+"-"+eids()+"-"+eids()

   
    try:
        ins = CreateExam.objects.get(eid=eid)
    except ObjectDoesNotExist as e:
        return eid
    
    for i in ins:
        if i.eid == eid:
            create_eid()
        else:
            return eid
    return None

def max_marks(eid):
    sd = CreateExam.objects.get(eid=eid)
    ins2 = SetQPaper.objects.filter(eid=eid)
    total_marks = sd.tmarks
    curr_marks= 0
    try:
        for i in ins2:
            curr_marks = curr_marks + i.marks
    except AttributeError:
        curr_marks = 1
    val = total_marks - curr_marks
    if val < 0:
        action = "Marks limit exceeded by "+ str(abs(val)) 
    else:
        action = None
    return action
    
@login_required(login_url="user-login")
def view_exam(request):
    sd = CreateExam.objects.filter(email=request.session['user'])
    return render(request, "templates_panels/user/view_exam.html",{"sd":sd})


@login_required(login_url="user-login")
def edit_exam(request,eid):
    sd = CreateExam.objects.get(eid=eid)
    if sd.email == request.session['user']:
        try:
            ins = Eligibility.objects.get(eid=eid)
        except ObjectDoesNotExist:
            ins = None
    
        ins2 = SetQPaper.objects.filter(eid=eid)
        return render(request, "templates_panels/user/edit_exam.html",{"cr":sd,"ins":ins,"ins2":ins2})
    else:
        return HttpResponse("Page Not Found!")

def update_profile(request):
    email = request.session['user']
    user_prof = UserProf.objects.get(email=email)
    if request.method == "POST":
        form = UserProfForm(request.POST, request.FILES)
        if form.is_valid():
            s = User.objects.get(email=email)        
            user_prof.image = form.cleaned_data['image']
            user_prof.username = form.cleaned_data['username']
            user_prof.address = form.cleaned_data['address']
            user_prof.phone = form.cleaned_data['phone']
            user_prof.city = form.cleaned_data['city']
            user_prof.state = form.cleaned_data['state']
            user_prof.save()
            s.username = user_prof.username
            s.save()
            return render(request, 'templates_panels/user/update_profile.html',{'succ_msg':"Profile Updated",'user':user_prof,'media_url':settings.MEDIA_URL})
            
        else:
            return render(request, 'templates_panels/user/update_profile.html',{'err_msg':"Invalid Form",'user':user_prof,'media_url':settings.MEDIA_URL})

    return render(request, "templates_panels/user/update_profile.html",{'user':user_prof,'media_url':settings.MEDIA_URL})