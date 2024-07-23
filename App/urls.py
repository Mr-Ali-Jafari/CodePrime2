from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("all/package/",views.all_package,name="all_pkg"),
    path("all/blog/",views.all_blog,name="all_blog"),
    path("history/purchase/",views.send_reply,name="history"),
    path('reply/to/<int:pk>/',views.send_reply,name="reply"),


    path("detail/<str:slug>/",views.detail,name="detail"),
    path("detail/blog/<int:pk>/",views.detail,name="detail_blog"),

    path("detail/video/<int:pk>/",views.vid_detail,name="video_detail"),
    path("view/cart/",views.view_cart,name="view_cart"),
    path("add/to/cart/<int:pk>/",views.add_to_cart,name="add_to_cart"),
    path("remove/from/cart/<int:pk>/",views.remove_from_cart,name="remove_from_cart"),
    path('purchases/', views.list_purchases, name='list_purchases'),
    path('activate/<int:purchase_id>/', views.activate_purchase, name='activate_purchase'),
    path('purchase/<int:purchase_id>/', views.purchase, name='purchase'),



]