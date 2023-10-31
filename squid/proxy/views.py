import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Proxy
from . import squid

@login_required(login_url='/login')
def index(request):
    ctx = {
        'update': False,
        'id': 0
    }
    return render(request, 'proxy.html')

@login_required(login_url='/login')
def updateProxy(request, id):
    ctx = {
        'update': True,
        'id': id
    }
    return render(request, 'proxy.html', ctx)

@login_required(login_url='/login')
def deleteProxy(request, id):
    Proxy.objects.get(pk=id).delete()
    return redirect('index')

# Create your views here.
@login_required(login_url='/login')
def createProxy(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        bandwidth = request.POST['bandwidth']

        try:
            proxy = Proxy.objects.get(username=username)
        except Proxy.DoesNotExist:
            proxy = None

        if proxy is not None:
            return redirect('index')

        Proxy.objects.create(username=username, password=password, bandwidth=bandwidth)

        squid.addAuthentication(username, password)
        squid.limitBandwidth()
        squid.reconfigure()
        
    return redirect('index')

@login_required(login_url='/login')
def updateBandwidth(request):
    if request.method == 'POST':
        id = request.POST['id']
        bandwidth = request.POST['bandwidth']

        try:
            proxy = Proxy.objects.get(pk=id)
            proxy.bandwidth = bandwidth
            proxy.save()

            squid.limitBandwidth()
            squid.reconfigure()
        except:
            print("Error updating bandwidth")
        
    return redirect('index')