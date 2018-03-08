from django.contrib import admin
from .models import Device, Object, Record
# Register your models here.
admin.site.register(Device)
admin.site.register(Object)
admin.site.register(Record)