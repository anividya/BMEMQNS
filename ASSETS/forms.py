from django import forms
from django.db.models import fields
from django.db.models.base import Model
from django.forms import widgets
from .models import Asset
from .models import Workbook
from django.forms import ModelForm
from datetime import datetime, date
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        queryset = Asset.objects.filter(pmstat='OVER DUE')
        total_entries = queryset.count()
        fields = ( 'assetid','assetname','asset_make','asset_model','slno','dept','pmdone','pmdue','caldone','caldue','wrstart','wrend','mcstart','mcend','stat','doc','invoice')
        success_url = '/success/'
        widgets = {
            'pmdue': DateInput(),
            'caldue' : DateInput(),
            'pmdone' : DateInput(),
            'caldone' : DateInput(),
            'wrstart' : DateInput(),
            'wrend' : DateInput(),
            'mcstart' : DateInput(),
            'mcend' : DateInput(),
        }
    def __init__(self, *arg, **kwargs):
        super(AssetForm,self).__init__(*arg, **kwargs)
    
    def form_valid(self, form):
        # Save the form
        response = super().form_valid(form)
        # Add a success message
        messages.success(self.request, 'Your form was successfully submitted!')
        return response

class updateForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('assetname','doc')
        
        #signature = SignatureField()

    def __init__(self, *arg, **kwargs):
        super(updateForm,self).__init__(*arg, **kwargs)

class WOForm(forms.ModelForm):
    class Meta:
        model = Workbook
        fields = ('wo_id','asset_name','make','model','slno','dept','asset_id','description','wo_date','sign','reporter','status')
    def __init__(self, *arg, **kwargs):
        super(WOForm,self).__init__(*arg, **kwargs)

class WOForm2(forms.ModelForm):
    class Meta:
        model = Workbook
        fields = ('wo_attended','eng_id','status')
    def __init__(self, *arg, **kwargs):
        super(WOForm2,self).__init__(*arg, **kwargs)

class WOForm3(forms.ModelForm):
    class Meta:
        model = Workbook
        fields = ('action','wo_done','description','status','eng_sign','downtime')
    def __init__(self, *arg, **kwargs):
        super(WOForm3,self).__init__(*arg, **kwargs)