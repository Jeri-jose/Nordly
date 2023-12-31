from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm
# Create your views here.

def loginPage(request):
    page= 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        username= request.POST.get('username').lower()
        password= request.POST.get('password')

        try:
            user= user.objects.get(username= username)
        except:
            messages.error(request,"user not found")
        
        user =authenticate(request,username=username, password= password)

        if user is not None:
            login(request, user)
            return  redirect('home')
        else:
            messages.error(request," user password not match")
    context= {"page":page}

    return render(request,'base/login_registar.html', context)


def logoutPage(request):
    logout(request)
    return redirect ('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method =='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit= False)
            user.username= user.username.lower()
            user.save()
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request,'error occur while creation')
    context= {'form':form}

    return render(request,'base/login_registar.html', context)





def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    rooms= Room.objects.filter(Q(topic__name__icontains =q)|
                               Q(name__icontains =q)|
                               Q(host__username__icontains =q)|
                               Q(description__icontains =q)
                                )
    topics= Topic.objects.all()
    roomcounts= rooms.count()
    room_message= Message.objects.filter(Q(room__topic__name__icontains=q)|
                                         Q(user__username__icontains =q)
                                            )
    context= {'rooms':rooms,
              'topics': topics,
              'roomcount': roomcounts,
              'room_message':room_message  
            }
    return render(request,'base/home.html', context)




def room(request,pk):
    room= Room.objects.get(id= pk)
    room_message= room.message_set.all().order_by('-created')
    participants= room.participants.all()
    
    if request.method == 'POST':
        message= Message.objects.create(
                user= request.user,
                room= room,
                body= request.POST.get('body')
        )
        return redirect ('room', pk= room.id )
    room.participants.add(request.user)

    context= {'room':room,
              'room_message': room_message,
              'participants': participants
                }
    return render (request,'base/room.html', context)




def userProfile(request, pk):
    user= User.objects.get(id= pk)
    rooms= user.room_set.all()
    room_message= user.message_set.all()
    topics=Topic.objects.all()
    #topics= user.topic_set.all()
    context= {'user':user,
               'rooms':rooms,
               'room_message':room_message,
               'topics':topics
            }
    return render(request,'base/profile.html', context)

@login_required(login_url ='login')
def CreateRoom(request):
    form= RoomForm()
    if request.method =='POST':
        form= RoomForm(request.POST)
        if form.is_valid():
            room= form.save(commit= False)
            room.host= request.user
            room.save()
            return redirect( 'home')
    context= {'form': form}
    return render(request, 'base/room_form.html', context)




@login_required(login_url ='login')
def updateRoom(request,pk):
    room= Room.objects.get(id= pk)
    form = RoomForm(instance= room)
    if request.user != room.host:
        return HttpResponse('is not allowed tp update')

    if request.method =='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect( 'home')
    context= {'form': form}
    return render(request, 'base/room_form.html', context)

        
@login_required(login_url ='login')
def DeleteRoom(request, pk):
    room= Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('is not allowed tp delete')
    if request.method =='POST':
        room.delete()
        return redirect ('home')
    
    context= {'obj':room}
    return render(request,'base/delete.html', context)



@login_required(login_url ='login')
def DeleteMessage(request, pk):
    message= Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('is not allowed tp delete')
    if request.method =='POST':
        message.delete()
        return redirect ('home' )
    
    context= {'obj':message}
    return render(request,'base/delete.html', context)
