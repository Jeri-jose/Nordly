from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# Create your views here.
def home(request):
    rooms= Room.objects.all()
    topics= Topic.objects.all()

    context= {'rooms':rooms,
              'topics': topics    
            }
    return render(request,'base/home.html', context)

def room(request, pk):
    room= Room.objects.get(id=pk)

    context= {'room':room}
    return render (request,'base/room.html', context)