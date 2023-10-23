
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
   
    path('<int:area_id>',ShowMeters.as_view(), name='meters'),
    path('details/<int:meter_id>',ShowMetersDetails.as_view(), name='meters_details'),
    # path('bill/<int:meter_id>',GetbBill.as_view(), name='get_bill'),
    # path('bills/',GetAllBill.as_view(), name='get_all_bill')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
