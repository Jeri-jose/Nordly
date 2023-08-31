from django.urls import path, include
from  . import views
urlpatterns = [
    path('login/', views.loginPage, name= 'login'),
    path('logout/', views.logoutPage, name= 'logout'),
    path('register/', views.registerPage, name= 'register'),


    path('', views.home, name='home'),

    path('room/<str:pk>', views.room, name= 'room'),
    path('create-room/', views.CreateRoom, name= 'create-room'),
    path('update-room/<str:pk>', views.updateRoom, name= 'update-room'),
    path('delete-room/<str:pk>', views.DeleteRoom, name= 'delete-room'),
    path('delete-message/<str:pk>', views.DeleteMessage, name= 'delete-message'),
]