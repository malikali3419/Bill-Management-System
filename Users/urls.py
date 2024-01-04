
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('login',Login.as_view(), name='login'),
    path('logout',Login.as_view(), name='login'),
    path('Add/',AddUser.as_view(), name='Add'),
    path('AllUsers/',ShowAllUsers.as_view(), name='All_Users'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
