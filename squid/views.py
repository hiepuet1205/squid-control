from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from squid.proxy import squid
from squid.proxy.models import Proxy

# Create your views here.

@login_required(login_url='/login')
def index(request):
    proxies = Proxy.objects.all()
    proxy_list = []
    for proxy in proxies:
        proxy_info = {
            'id': proxy.id,
            'username': proxy.username,
            'password': proxy.password,
            'bandwidth': proxy.bandwidth * 8 / 1000000
        }
        proxy_list.append(proxy_info)
    ctx = {
        'num_proxies': proxies.count(),
        'proxies': proxy_list
    }
    return render(request, 'index.html', ctx)

@login_required(login_url='/login')
def createUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        bandwidth = request.POST['bandwidth']

        squid.addAuthentication(username, password)
        squid.reconfigure()
    
    return redirect('index')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            return redirect('index') 
    return render(request, 'login.html')

@login_required(login_url='/login')
def custom_logout(request):
    logout(request)
    return redirect('login')