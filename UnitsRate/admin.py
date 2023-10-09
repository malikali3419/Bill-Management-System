from django.contrib import admin
from  .models import *

admin.site.register(FineAfterDueDate)
admin.site.register(MiscellaneousCharges)
admin.site.register(FirstRangeOfUnitValue)
admin.site.register(SecondRangeOfUnitValue)
admin.site.register(ThirdRangeOfUnitValue)
admin.site.register(FouthRangeOfUnitValue)
admin.site.register(DueDateForFine)

