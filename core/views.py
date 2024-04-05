from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from .models import Room,Topic,Messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout


from django.views import View
from .forms import Room_form

# Create your views here.

rooms = [
    {'id':1,  'name':'Django'},
    {'id':2,'name':'Front_end'},
    {'id':3,'name':'Back End'}
]

def registerUser(request):
    form  = UserCreationForm()
    context = {'form':form,'page': "register"}

    if  request.method == 'POST':
        form  = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print('no  login error')

            user.username = user.username.lower()
            user.save()
            login(request,user)
            
            return redirect('home')
        else:
            print('hello this is an error of  login')
            
            messages.error(request,'An error  occured  during  regitration ')


    
    return render(request,'base/login_register.html',context)
    


def loginPage(request):
    page = 'login'
    context  = {'page':page}
    if request.user.is_authenticated:
        return redirect('home')
        
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        print(username,password)
        try:
            user = User.objects.get(username = username)
            
        except:
            messages.error(request,'User does not exist.')
           
            
        user = authenticate(request,username=username ,password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username or password does not  exist')
            
    return render(request,'base/login_register.html' ,context= context)


def logoutUser(request):
    logout(request)
    messages.success(request,'successful logout')

    return redirect('home')

def userProfile(request,pk):
    print(pk)
    user = User.objects.get(id = pk)
    room_messages = user.messages_set.all()
    rooms = user.room_set.all()
    topic = Topic.objects.all()
    context = {'user': user,'room' :rooms,'room_messages':room_messages,'topic':topic}
    return render(request,'base/profile.html',context)
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    print('q')
        

    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q( name__icontains = q)|Q(description__icontains = q))
    
        
    

    # print(request)
    
    topic = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Messages.objects.filter(Q(room__topic__name__icontains=q) )
    
    context = {'room':rooms,'topic':topic,'count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context=context)


def room(request,pk):
    room = Room.objects.get(id = int(pk))
    room_messages  = room.messages_set.all().order_by('-created')
    participants =  room.participants.all()
    c = {'rooms':room,'room_messages':room_messages,'participants':participants}

    print(participants)

    if request.method == "POST":
        print('jgjf')
        
        mes =  request.GET.get('')
        user = request.user
        
        message = Messages.objects.create(user = request.user,room = room,body=request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    print('room')
    print(pk)
    return render(request,'base/room.html',context=c)


@login_required(login_url='login')
def createRoom(request):
    form = Room_form()
    topic =  Topic.objects.all()
    
    # if request.method =="POST":
    #     topic_name = request.POST.get('topic')
    #     request.POST.get('name')
    #     form = Room_form(request.POST)
    #     if form.is_valid():
    #         room =  form.save(commit=False)
    #         room.host = request.user
    #         form.save()
    #         return redirect('home') 

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form': form,'topics':topic}
        
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request,pk):
    room  = Room.objects.get(id = pk)
    form =  Room_form(instance =room )
    topics =  Topic.objects.all()

    if  request.user != room.host:
        return HttpResponse('you are not allowed')
    if request.method == 'POST':
        form = Room_form (request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form,'topic':topics,'room':room}
    return render(request , 'base/room_form.html',context)



def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)
    if  request.user != room.host:
        return HttpResponse('you are not allowed')
    if request.method == 'POST':
        print("this is delete method  in this  url has trigered")
        room.delete()
        return  redirect('home')
    return render(request,'base/delete.html',{'obj':room})

login_required(login_url='login')
def deleteMessage(request,pk):
    message = Messages.objects.get(id = pk)
    if  request.user != message.user:
        return HttpResponse('you are not allowed')
    if request.method == 'POST':
        print("message is deleted")
        message.delete()
        return  redirect('home')
    return render(request,'base/delete.html',{'obj':message})



class house(View):
    def get(request,*args,**kwargs):
        
        
        return HttpResponse('house')
    
