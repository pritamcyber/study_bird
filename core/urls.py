from django.urls import path


from . import views as v
urlpatterns = [
    path('',v.home,name="home"),
    path('room/<str:pk>',v.room,name="room"),
    path('house/<str:alfa>/<str:king>',v.house.as_view(),name='alfa'),
    path('update-room/<str:pk>',v.updateRoom, name="update-rooms"),
    path('create-room/',v.createRoom,name="create-room"),
    path('delete-room/<str:pk>',v.deleteRoom, name="delete-room"),
    path('login/',v.loginPage,name = 'login'),
    path('logout/',v.logoutUser,name = 'logout'),
    path('register/',v.registerUser,name = 'register'),
    path('profile/<str:pk>',v.userProfile,name = 'user-profile'),

    path('delete_message/<str:pk>',v.deleteMessage,name = 'delete_message'),

    
    
    

    
    
]
