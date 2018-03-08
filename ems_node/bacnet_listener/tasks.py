from __future__ import absolute_import, unicode_literals
import pybacnet
from django.utils import timezone
from celery.decorators import task

from .models import Device, Object, Record, Timestamp


@task(name="register_devices")
def register_devices():
    known_devices = Device.objects.all()
    known_device_ids = [x.device_id for x in known_devices]
    pbn = pybacnet.PyBacNet()
    try:
        found_devices = pbn.get_device_list()['devices']

        # Add block to add/update new objects in known devices
        for device in found_devices:

            try:
                device_detail = pbn.get_device_detail(device['device-id'])
                print(device_detail)
                if not device['device-id'] in known_device_ids:
                    new_device = Device.objects.create(
                        description=device_detail['description'],
                        device_id=device_detail['device-id'],
                        device_name=device_detail['device-name'],
                        href=device_detail['href'],
                        model_name=device_detail['model-name'],
                        vendor_identifier=device_detail['vendor-identifier'],
                        vendor_name=device_detail['vendor-name'],
                        active=False,
                    )

                    try:
                        obj_list = pbn.get_object_list(device['device-id'])['objects']

                        for obj in obj_list:
                            Object.objects.create(
                                device=new_device,
                                href=obj['href'],
                                object_id=obj['object-id'],
                                object_instance=obj['object-instance'],
                                object_name=obj['object-name'],
                                object_type=obj['object-type'],
                                active=False,
                            )

                    except ConnectionError:
                        print("Could not gather objects from device: {device_id}".format(device_id=device['device-id']))

            except ConnectionError:
                print("Could not gather and save details from device: {device_id}".format(device_id=device['device-id']))

    except ConnectionError:
        print("Could not connect to Wacnet API, ensure that Wacnet is running")


@task(name="record_node_state")
def record_node_state():
    active_devices = Device.objects.filter(active=True)
    active_objects = Object.objects.filter(active=True)
    pbn = pybacnet.PyBacNet()
    t = timezone.now()
    timestamp = Timestamp.objects.create()
    for device in active_devices:
        device_active_objects = active_objects.filter(device=device)
        for obj in device_active_objects:
            try:
                response = pbn.get_object_detail(device.device_id, obj.object_id)
                value = float(response['present-value'])
                Record.objects.create(
                    object=obj,
                    timestamp=timestamp,
                    present_value=response['present-value'],
                    permanent=True
                )
            except ConnectionError:
                timestamp.delete()
                print('Could not connect to object')


# @task(name="store_permanent_data")
# def store_permanent_data():
#     active_objects = Object.objects.filter(active=True)
#     for obj in active_objects:
#         obj_temp_records = Record.objects.filter(permanent=False, object=obj)
#         values = [x.value for x in obj_temp_records]
#         if len(values) > 0:
#             average_value = sum(values)/len(values)
#             Record.objects.create(
#                 object=obj,
#                 timestamp=timezone.now(),
#                 present_value=average_value,
#                 permanent=True,
#             )
#
#             obj_temp_records.delete()