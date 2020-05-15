import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class UserFilter(django_filters.FilterSet):
    dusername = CharFilter(field_name='user__username', lookup_expr='icontains')

    class Meta:
        model = Duser
        fields = ['dusername']