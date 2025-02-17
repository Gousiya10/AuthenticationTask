from django.contrib import admin
from django.urls import path
from . import view
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',view.index,name='base'),
    path('list/', item_list, name='item_list'),
    path('signup/',registration_view,name='registration_view'),
    path('signin/',login_user,name='login_view'),
    path('create/', create_item, name='create_item'), 
    path('detail/<slug:name>/', item_detail, name='item_detail'), # you have to use here slug instead of pk
    path('update/<slug:name>/', item_update, name='item_update'), # you have to use here slug instead of pk
    path('delete/<int:id>/', item_delete, name='item_delete'),  # you have to use here slug instead of pk
    path('logout/',logout_view,name='logout_view'),
    
]
