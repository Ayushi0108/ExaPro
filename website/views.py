from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from .models import Contact
from django.utils.timezone import utc
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from main.decorators import unauthenticated_user, allowed_users, admin_only 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import pytz


def contact(request):
    if request.method == "POST":
        name = request.POST['uname']
        email = request.POST['uemail']
        message = request.POST['umessage']
        ins = Contact(name=name, email=email, message=message)
        ins.save()
        return render(request, 'templates_website/thanks_for_contacting.html')


@login_required(login_url='admin-login')
@admin_only
def delete_contact(request, id):
    Contact.objects.get(id=id).delete()
    return redirect('/site/inbox')

@login_required(login_url='admin-login')
@admin_only
def inbox(request):
    i = 0
    all_msgs = {}
    for p in Contact.objects.raw('SELECT * FROM website_contact ORDER BY id DESC'):
        id = p.id
        name = p.name
        email = p.email
        message = p.message
        time = (p.time)
        fmt = '%d/%m/%Y'
        fmt2 = '%H:%M'
        date = time.replace(tzinfo=pytz.UTC)
        date = time.astimezone(timezone.get_current_timezone())
        date = time.strftime(fmt)
        time = time.replace(tzinfo=pytz.UTC)
        time = time.astimezone(timezone.get_current_timezone())
        time = time.strftime(fmt2)

        all_msgs.update({''+str(i): {'id': id, 'name': name, 'email': email,
                                     'message': message, 'date': date, 'time': time}, })
        i = i+1
    if len(all_msgs) == 0:
        return render(request, "templates_website/inbox.html", {'error': "No Data Found !"})
    else:
        return render(request, "templates_website/inbox.html", {'all_msgs': all_msgs})


def terms_conditions(request):
    return render(request, "templates_website/terms-conditions.html")


def privacy_policy(request):
    return render(request, "templates_website/privacy-policy.html")


def cookie_policy(request):
    return render(request, "templates_website/cookie-policy.html")

