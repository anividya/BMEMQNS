import django_filters
from .models import *

class AssetFilter(django_filters.FilterSet):
    assetname = django_filters.CharFilter(field_name = 'assetname', lookup_expr='iexact')
    Make = django_filters.CharFilter(field_name = 'asset_make', lookup_expr='iexact')
    Model = django_filters.CharFilter(field_name = 'asset_model', lookup_expr='icontains')
    Dept = django_filters.CharFilter(field_name = 'dept', lookup_expr='icontains')
    Seral_No = django_filters.CharFilter(field_name = 'slno', lookup_expr='icontains')
    pmstat = django_filters.CharFilter(field_name = 'pmstat', lookup_expr='icontains')
    pmdue = django_filters.NumberFilter(field_name='pmdue', lookup_expr='month')
    pmduerange = django_filters.DateTimeFromToRangeFilter(field_name='pmdue' )
    
    class Meta:
        models = Asset

class WOFilter(django_filters.FilterSet):
    wo_id = django_filters.CharFilter(field_name = 'wo_id', lookup_expr='iexact')
    asset_id = django_filters.CharFilter(field_name = 'asset_id', lookup_expr='iexact')
    slno = django_filters.CharFilter(field_name = 'slno', lookup_expr='iexact')
    make = django_filters.CharFilter(field_name = 'make', lookup_expr='icontains')
    model = django_filters.CharFilter(field_name = 'model', lookup_expr='icontains')
    dept = django_filters.CharFilter(field_name = 'dept', lookup_expr='icontains')

    class Meta:
        models = Workbook

class CalFilter(django_filters.FilterSet):

    assetname = django_filters.CharFilter(field_name = 'assetname', lookup_expr='icontains')
    Make = django_filters.CharFilter(field_name = 'asset_make', lookup_expr='iexact')
    Model = django_filters.CharFilter(field_name = 'asset_model', lookup_expr='icontains')
    Dept = django_filters.CharFilter(field_name = 'dept', lookup_expr='icontains')
    calstat = django_filters.CharFilter(field_name = 'calstat', lookup_expr='icontains')
    caldue = django_filters.NumberFilter(field_name='caldue', lookup_expr='month')
    calduerange = django_filters.DateTimeFromToRangeFilter(field_name='caldue' )
    
    class Meta:
        models = Asset

class NmFilter(django_filters.FilterSet):

    assetname = django_filters.CharFilter(field_name = 'assetname', lookup_expr='icontains')
    make = django_filters.CharFilter(field_name = 'assetname', lookup_expr='icontains')
    
    
    class Meta:
        models = Asset
        

