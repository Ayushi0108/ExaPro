from django.shortcuts import render
from authentication.models import UserProf
from authentication.forms import UserProfForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.decorators import  admin_only 
from django.contrib.auth.models import User, Group

@login_required(login_url='admin-login')
@admin_only
def view_customers(request):
    
    #Code to dlt the obj which does not exist in Django admin Users
    # email = request.session['user'] 
    # user = User.objects.get(email=email)
    # if user is not None:

    all_details = {}
    i = 0
    for u in UserProf.objects.raw('SELECT id,username,email,password,address,city,phone,state FROM user_details'):
        id = u.id
        name = u.username
        email = u.email
        password = u.password
        add = u.address
        city = u.city
        ph = u.phone
        state = u.state
        all_details.update({''+str(i):{'name':name,'email':email,'pass':password,'add':add,'city':city,'ph':ph,'state':state}})
        i = i + 1
    if len(all_details) == 0:
        return render(request,'templates_panels/admin/view_customers.html',{'err_msg':'No Records Found'})

    else:
        return render(request,'templates_panels/admin/view_customers.html',{'all_details':all_details})

    # else:
    #     user = UserProf.objects.get(email=email)
    #     if user is not None:
    #       user.delete()
    #     return render(request,'templates_panels/admin/view_customers.html',{'err_msg':'No Records Found'})
