from django.contrib import admin

from .models import *

admin.site.register(Duser)
admin.site.register(Task)
admin.site.register(TaskReport)
admin.site.register(TaskAssign)
# Register your models here.
