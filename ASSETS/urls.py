from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from django.conf.urls.static import static
from django.views.static import serve

from django.conf import settings
from django.views.static import serve


urlpatterns = [

    path('',views.index,name='index'),
    path('asset_insert',views.asset_form,name='asset_insert'),
    path('asset_list',views.index,name='asset_list'),
    path('<int:id>/',views.asset_form,name='asset_update'),
    path('addwo', views.addwo, name='addwo'),
    path('update/<str:id>',views.update,name='update'),
    path('update_wo/<str:id>',views.update_wo,name='update_wo'), 
    path('assethistory/<str:id>',views.assethistory,name='assethistory'),   
    path('get_data/', views.get_data, name='get_data'),
    path('woajax/', views.woajax, name='woajax'),
    path('viewwo', views.viewwo, name='viewwo'),
    path('my_wo', views.my_wo, name='my_wo'),
    path('workform/<str:id>/',views.workform,name='workform'), 
    path('woview/<str:id>/', views.woview, name='woview'),
    path('generate_pdf/<str:id>/', views.generate_pdf, name='generate_pdf'),
 
    ]

