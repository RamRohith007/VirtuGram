from django.urls import path
from . import views

######
urlpatterns = [
    path('',views.lobby, name='lobby'),
    path('room/',views.room, name='room'),
    path('get-token/',views.getToken),
    path('create-member/',views.createMember),
    path('get-member/',views.getMember),
    path('delete-member/',views.deleteMember),
]
