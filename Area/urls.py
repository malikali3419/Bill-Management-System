
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('',Home.as_view(), name='Home'),
    path('blocks/<str:block_name>',ShowAreas.as_view(), name='blocks_areas'),
    path('area/<str:area_id>',ShowAreaDetails.as_view(), name='area_details'),
    path('Addhouse/',AddHouse.as_view(), name='Home'),
    path('logout/',Logout.as_view(), name='Home')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
