from django.contrib import admin
from .models import Asset
from .models import Workbook

class AssetAdmin(admin.ModelAdmin):
    list_display = ('assetid','assetname','asset_make','asset_model','slno','dept','pmstat','calstat','stat')

class WorkbookAdmin(admin.ModelAdmin):
    list_display = (
    'wo_id',
    'asset_id',
    'description',
    'action',
    'wo_date',
    'wo_attended',
    'wo_done',
    'status',
    'eng_id',
    'SR_report',
    'invoice' )


# Register your models here.

admin.site.register(Asset,AssetAdmin)
admin.site.register(Workbook,WorkbookAdmin)