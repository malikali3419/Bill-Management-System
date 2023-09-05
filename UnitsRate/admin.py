from django.contrib import admin
from  .models import *

admin.site.register(FineAfterDueDate)
admin.site.register(MiscellaneousCharges)
admin.site.register(FirstRangeOfUnitValues)
admin.site.register(SecondtRangeOfUnitValues)
admin.site.register(ThirdRangeOfUnitValues)
admin.site.register(FouthRangeOfUnitValues)
admin.site.register(DueDateForFine)

