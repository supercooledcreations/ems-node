# Imports
# Django
from django.urls import path, reverse
from django.views.generic.base import RedirectView

# App
from .views import SimpleRecordTableView

# Urls
app_name = 'bacnet_listener'
urlpatterns = [
    # Metrics
    path('records/', SimpleRecordTableView.as_view(), name='record_table'),
]