import base64
import json
from ASSETS.decorators import allowed_users
from ASSETS.models import Asset
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import AssetForm
from .forms import updateForm
from django.contrib.auth.models import User
from .models import Asset
from .models import Workbook
from .filter import AssetFilter
from .forms import WOForm
from .forms import WOForm2
from .forms import WOForm3
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filter import CalFilter
from .filter import WOFilter
from datetime import datetime, date
from django.http import JsonResponse
from django.contrib import messages
from django.core.files.base import ContentFile
import base64
from datetime import datetime,timedelta
from django.contrib.auth.models import Group

def loginpage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request, 'Username or Password incorrect')
            return render(request, 'login.html')
    
    else:
        return render(request, "login.html")

def logoutuser(request):
    logout(request)
    return redirect('login/?next=/')

@login_required(login_url="/login/")
def index(request):

    Asset.objects.filter(pmdue__lte= date.today()).update(pmstat="OVER DUE")
    Asset.objects.filter(pmdue__gte= date.today()).update(pmstat="NOT DUE")
    Asset.objects.filter(caldue__lte= date.today()).update(calstat="OVER DUE")
    Asset.objects.filter(caldue__gte= date.today()).update(calstat="NOT DUE")
    Asset.objects.filter(mcend__lte= date.today()).update(amc_cmc="DUE")
    Asset.objects.filter(mcend__gte= date.today()).update(amc_cmc="INCONTRACT")
    queryset = Asset.objects.filter(pmstat='OVER DUE')
    pmduecount = queryset.count()
    queryset_cal = Asset.objects.filter(calstat='OVER DUE')
    calduecount = queryset_cal.count()
    assetlist = Asset.objects.all()
    form = AssetForm()
    user_group = None
    for group in request.user.groups.all():
        user_group = group.name
        
    if user_group == 'Admin':
        return render(request, 'table.html', {'index':assetlist,'form':form,'pmdues':pmduecount,'caldues':calduecount})
    else:
        return redirect('login/?next=/')

@login_required(login_url="/login/")
@allowed_users('Admin')
def asset_form(request,id=0):
    if request.method == "GET":
        if id==0:
            if Asset.objects.exists():
                last_pk = Asset.objects.latest('pk').pk
            else:
                last_pk = 0
            form = AssetForm(initial={'assetid': 'ME0'+str(last_pk+1)}) 
        return render(request, "assetform.html", {'form':form})
    
    if request.method == "POST":
        if id == 0:
            form = AssetForm(request.POST, request.FILES)
        else:
            assetcontent = Asset.objects.get(pk=id)
            form = AssetForm(request.POST,request.FILES,instance=assetcontent)
        if form.is_valid():
            form.save()
            messages.success(request, 'The form was saved successfully!')
            return redirect('index')
        else:
            return redirect("assetform.html")

@login_required(login_url="/login/")
@allowed_users('Admin')
def calfilter(request):
    assetlist = Asset.objects.filter(calstat='OVER DUE')
    myFilter = CalFilter(request.GET, queryset=assetlist)
    return render(request, 'cal.html', {'filter':myFilter, 'index':assetlist})

@login_required(login_url="/login/")
@allowed_users('Admin')
def pmfilter(request):
    assetlist = Asset.objects.filter(pmstat='OVER DUE')
    myFilter = AssetFilter(request.GET, queryset=assetlist)
    return render(request, 'pm.html', {'filter':myFilter, 'index':assetlist})

@login_required(login_url="/login/")
def addwo(request):
    if request.method == "GET":
        assetlist = Asset.objects.all()
        wolist = Workbook.objects.all()
        myFilter = AssetFilter(request.GET,queryset=assetlist)
        form = WOForm()
        return render(request, 'wo.html', {'filter':myFilter,'form':form,'index':wolist})
    if request.method == "POST":
        canvas_data = request.POST.get('canvas_data', None)
        if canvas_data:
            format, imgstr = canvas_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            # do something with the image file
        else:
                return HttpResponse(status=505)
        
        assetcontent = Workbook(sign=data)
        now = datetime.now()
        wodate = Workbook(wo_date=now)
        form = WOForm(request.POST, request.FILES,instance=assetcontent)
        if form.is_valid():
            form.save() 
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return render(request, 'woform.html', {'form': form})

@login_required(login_url="/login/")
@allowed_users('Admin')
def update(request,id):
    if request.method == "POST":
      assetcontent = Asset.objects.get(pk=id)
      form = updateForm(request.POST,request.FILES,instance=assetcontent)
      if form.is_valid():
        form.save() 
        return redirect('asset_list')
      else:
        return redirect('add')

@login_required(login_url="/login/")
def get_data(request):
    if Workbook.objects.exists():
        last_pk = Workbook.objects.latest('pk').pk
    else:
        last_pk=0
    print(last_pk)
    woid='WO'+str(last_pk+1)
    now = datetime.now()
    data2 = {'key': woid,
            'date': now
            }
    return JsonResponse(data2)

def viewwo(request):
     if request.method == "GET":
        wolist = Workbook.objects.all()
        myFilter = WOFilter(request.GET,queryset=wolist)
        form = WOForm()
        return render(request, 'wotable.html', {'index':wolist,'form':form,'filter':myFilter})

@login_required(login_url="/login/")
@allowed_users('Admin')
def update_wo(request,id):
    if request.method == "POST":
      content = Workbook.objects.get(pk=id)
      attended = request.POST.get('wo_attended')
      print(attended)
      form = WOForm2(request.POST,request.FILES,instance=content)
      if form.is_valid():
        form.save() 
        return redirect('viewwo')
      else:
        return redirect('add')

@login_required(login_url="/login/")
def woajax(request):
    now = datetime.now()
    data = {
            'keydata': now
            }
    return JsonResponse(data)

@login_required(login_url="/login/")
def my_wo(request):
    current_user = request.user
    wolist = Workbook.objects.filter(eng_id__icontains = current_user,status__icontains = "ASSIGNED")
    return render(request, 'wo_process.html', {'index':wolist})

@login_required(login_url="/login/")
def workform(request,id):
    if request.method == "GET":
        content = Workbook.objects.get(pk=id)
        ct = content.wo_date
        print(ct)
        form = WOForm3(instance=content)
        return render(request, "workform.html", {'form':form,'ct':ct})
    
    if request.method == "POST":
        canvas_data = request.POST.get('canvas_data', None)
        if canvas_data:
            format, imgstr = canvas_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        else:
                return HttpResponse(status=505)
        content = Workbook.objects.get(pk=id)
        content.eng_sign = data
        form = WOForm3(request.POST,request.FILES,instance=content)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, "workform.html", {'form':form})

@login_required(login_url="/login/")
def assethistory(request,id):
    
    if request.method == "GET":
        content = Asset.objects.get(pk=id)
        assetid = content.assetid
        print(assetid)
        wolist = Workbook.objects.filter(asset_id__icontains = assetid)
        form = AssetForm(instance=content)
        return render(request, "assethistory.html", {'form':form,'wolist':wolist})

@login_required(login_url="/login/")
def woview(request,id):
    if request.method == "GET":
        content = Workbook.objects.get(pk=id)
        assetid = content.asset_id
        action = content.action
        eng = content.eng_id
        attended = content.wo_attended
        form = WOForm(instance=content)
        form2 = WOForm3(instance=content)
        return render(request, "wovew.html", {'form':form,'assetid':assetid,'action':action,'form2':form2,'eng':eng,'attended':attended})

def generate_pdf(request,id):
    indata = Workbook.objects.get(pk=id)
    form_data = {
        'assetid': indata.asset_id,
        'wo_id': indata.wo_id,
        'wo_date': indata.wo_date,
        'asset_name': indata.asset_name,
        'make': indata.make,
        'model': indata.model,
        'description': indata.description,
        'action': indata.action,
        'wo_done': indata.wo_done,
        'reporter': indata.reporter,
        'dept': indata.dept,
        'wo_attended': indata.wo_attended,
        'eng_id': indata.eng_id,
        'sign': indata.sign,
        'downtime':indata.downtime,
        'eng_sign':indata.eng_sign
        }
    return render(request, "wovew.html", {'form':form_data})


    


