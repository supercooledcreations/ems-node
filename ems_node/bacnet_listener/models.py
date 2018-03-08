from django.db import models


# Create your models here.
class Device(models.Model):
    description = models.CharField(max_length=280, null=True)
    device_id = models.IntegerField(unique=True)
    device_name = models.CharField(max_length=280)
    href = models.URLField()
    model_name = models.CharField(max_length=280, null=True)
    vendor_identifier = models.IntegerField(null=True)
    vendor_name = models.CharField(max_length=280, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.device_name


class Object(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    href = models.URLField()
    object_id = models.CharField(max_length=140)
    object_instance = models.IntegerField()
    object_name = models.CharField(max_length=280)
    object_type = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{device}: {obj}'.format(device=self.device.description, obj=self.object_name)

    class Meta:
        ordering = ['device', 'object_name']


class Timestamp(models.Model):
    value = models.DateTimeField(auto_now_add=True, unique=True)


class Record(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    timestamp = models.ForeignKey(Timestamp, on_delete=models.CASCADE)
    present_value = models.FloatField()
    permanent = models.BooleanField(default=False)

    def __str__(self):
        return '{time}: {obj}'.format(time=self.timestamp, obj=self.object.object_name)