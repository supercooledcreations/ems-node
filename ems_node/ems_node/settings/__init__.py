from .base import *

try:
    from django_produciton_settings import *

except ImportError:
    from .development import *