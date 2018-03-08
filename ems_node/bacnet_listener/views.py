from pybacnet import PyBacNet

from django.shortcuts import render, reverse
from django.views import View

from .models import Device, Object, Record, Timestamp


# Create your views here.
class SimpleRecordTableView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'bacnet_listener/record_table.html'

        active_objects = Object.objects.filter(active=True).order_by('object_name')
        perm_records = Record.objects.filter(permanent=True)
        timestamps = Timestamp.objects.all()

        record_table_header = ["Timestamp"]
        for obj in active_objects:
            record_table_header.append(obj)

        record_table_data = []
        for ts in timestamps:
            ts_row = [ts.value]
            for obj in active_objects:
                obj_perm_records = perm_records.filter(object=obj, timestamp=ts)

                if len(obj_perm_records) > 0:
                    ts_row.append(obj_perm_records.first().present_value)
                else:
                    ts_row.append('')

            record_table_data.append(ts_row)

        context = {'record_table_header': record_table_header, 'record_table_data': record_table_data}

        return render(request, template_name, context)
