from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("create/edit/profile/",views.create_or_edit_profile,name="create_profile"),
    path("create/participate/",views.create_participate,name="create_participate"),
    path("profile/@<str:username>/",views.profile_detail,name="profile_detail"),
]