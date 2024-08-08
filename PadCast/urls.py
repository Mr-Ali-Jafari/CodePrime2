from django.urls import path
from . import views
urlpatterns = [
    path("",views.index_primecast,name="primecast"),
    path("create/primecast/",views.create_primecast,name="create_primecast"),
    path("<str:slug>/",views.detail_padcast,name="detail_padcast"),
]