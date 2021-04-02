from django.shortcuts import render, HttpResponse
from django.template import RequestContext


def index(request):
    return render(request, "templates_website/index.html")