from django.http import HttpResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.decorators import unauthenticated_user, allowed_users, admin_only
from django.views.decorators.csrf import csrf_protect
import random
import datetime
from .forms import UserProfForm
from .models import UserProf


otp_global = 0
register = None
email = ''
form_gb = None
details_list = []
##################################### ADMIN ######################################

# ADMIN LOGIN
@csrf_protect
@unauthenticated_user
def admin_login(request):
    if request.method == 'POST':
        globals()['email'] = request.POST['email']
        password = request.POST['password']
        try:
            admin = User.objects.get(email=globals()['email'])
            if admin is not None:
                if admin.check_password(password):
                    login(request, admin)
                    return redirect('admin-home')
                else:
                    err_msg = "Incorrect password"
                    return render(request,
                                  'templates_authentication/admin_login.html',
                                  {'err_msg': err_msg})
        except ObjectDoesNotExist:
            err_msg = "Account doesn't exist"
            return render(request, 'templates_authentication/admin_login.html',
                          {'err_msg': err_msg})
    else:
        return render(request, 'templates_authentication/admin_login.html')

# ADMIN LOGOUT
def admin_logout(request):
    logout(request)
    return redirect('admin-login')


@csrf_protect
@login_required(login_url='admin-login')
@admin_only
def admin_home(request):
    return redirect('view-customers')


##################################### USER #######################################


# USER SIGNUP
@unauthenticated_user
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        globals()['email'] = request.POST['email']
        globals()['password'] = request.POST['password']
        conf = request.POST['conf_pass']
        try:
            globals()['register'] = User.objects.get(email=globals()['email'])
            err_message = "Account already exists"
            return render(request, 'templates_authentication/user_signup.html',
                          {'err_message': err_message})
        except ObjectDoesNotExist:
            if len(globals()['password']) <= 4 or len(
                    globals()['password']) > 16:
                err_pass = "Password must be more than 4 and less than 16 characters"
                return render(request,
                              'templates_authentication/user_signup.html',
                              {'err_pass': err_pass})
            else:
                if globals()['password'] == conf:
                    globals()['register'] = User(username=username,
                                                 email=globals()['email'])
                    comm_otp_generation()
                    return render(request, 'templates_authentication/otp.html')
                else:
                    err_pass = "Passwords doesn't match"
                    return render(request,
                                  'templates_authentication/user_signup.html',
                                  {'err_pass': err_pass})
    else:
        return render(request, 'templates_authentication/user_signup.html')


# USER LOGIN
@csrf_protect
@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        globals()['email'] = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=globals()['email'])
            if user is not None:
                if user.check_password(password):
                    user_check = UserProf.objects.filter(email=globals()['email'])
                    # user_prof = UserProf.objects.get(email=globals()['email'])
                    if user_check.exists():
                        login(request, user)
                        request.session['user'] = globals()['email']
                        #return render(request,'templates_panels/user/create_exam.html',
                        #   {'prof':user_prof,'media_url':settings.MEDIA_URL})
                        return render(request,'templates_panels/user/create_exam.html')
                    else:
                        print(user_check)
                        return render(request,
                            'templates_authentication/add_details.html',{'user':user,'user_prof':user_check,'password':password})
                else:
                    err_msg = "Incorrect password"
                    return render(request,
                                  'templates_authentication/user_login.html',
                                  {'err_msg': err_msg})
        except ObjectDoesNotExist:
            err_msg = "Account doesn't exist"
            return render(request, 'templates_authentication/user_login.html',
                          {'err_msg': err_msg})
    else:
        return render(request, 'templates_authentication/user_login.html')


# USER HOME
@login_required(login_url="user-login")
def user_home(request):
    return render(request, 'templates_panels/user/create_exam.html')


# USER LOGOUT
def user_logout(request):
    logout(request)
    return redirect("user-login")


##################################################################################

def regi(request):
    if request.method == "POST":        
        form = UserProfForm(request.POST, request.FILES)
        p = globals()['register']
        if form.is_valid():
            image = form.cleaned_data['image']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            globals()['form_gb'] = UserProf(image=image,username=username,email=email,password=password,
                                    address=address,city=city,phone=phone,state=state)
            globals()['form_gb'] .save()
            return render(request, 'templates_authentication/user_login.html')
           
        else:
            print(form.errors)
            return render(request, 'templates_authentication/add_details.html',{'err_msg':"Invalid Form Data",'email':p.email,'name':p.username,'password':p.password})


def verify(request):
    err_msg = ""
    try:
        if request.method == 'POST':
            # try:
            otp = int(request.POST.get('otp', 0))
            if globals()['otp_global'] == otp:
                globals()['register'].set_password(globals()['password'])
                globals()['register'].save()
                group = Group.objects.get(name='user')
                globals()['register'].groups.add(group)
                user = User.objects.get(email=globals()['email'])
                print(user.password)
                return render(request,
                                'templates_authentication/add_details.html',{'user':user,'password':globals()['password']})
            else:
                err_msg = "Incorrect OTP"
                return render(request, 'templates_authentication/otp.html',
                                {'err_msg': err_msg})
            # except ValueError:
            #     err_msg = "Only numbers allowed"
            #     return render(request, 'templates_authentication/otp.html',
            #                   {'err_msg': err_msg})

    except IntegrityError:
        err_msg = "Account already exists"
        return render(request, 'templates_authentication/otp.html',
                      {'err_msg': err_msg})


def generate(request):
    comm_otp_generation()
    return render(request, 'templates_authentication/otp.html')


def change_pass(request):
    if request.method == 'POST':
        globals()['email'] = request.POST['email']
        globals()['password'] = request.POST['pass']
        conf_pass = request.POST['conf_pass']

        try:
            globals()['register'] = User.objects.get(email=globals()['email'])
            if globals()['password'] == conf_pass:
                if len(globals()['password']) <= 4 or len(
                        globals()['password']) > 16:
                    err_msg = "Password must be more than 4 and less than 16 characters"
                    return render(request,
                                  'templates_authentication/changepass.html',
                                  {'err_msg': err_msg})
                else:
                    globals()['register'].password = globals()['password']
                    comm_otp_generation()
                    return render(request, 'templates_authentication/otp.html')

            else:
                err_msg = "Passwords doesn't match"

                return render(request,
                              'templates_authentication/changepass.html',
                              {'err_msg': err_msg})

        except ObjectDoesNotExist:
            err_msg = "Account doesn't exist"

            return render(request, 'templates_authentication/changepass.html',
                          {'err_msg': err_msg})

    else:
        return render(request, 'templates_authentication/changepass.html')


def comm_otp_generation():
    otp_rand = random.randint(1000, 9999)
    globals()['otp_global'] = otp_rand
    print(globals()['otp_global'])
    otp_msg = f"Email-Verification OTP : {otp_rand}"
    send_mail("Welcome to ExaPro",
              otp_msg,
              'ExaPro<exapro.official@gmail.com>', [(globals()['email'])],
              fail_silently=False)
