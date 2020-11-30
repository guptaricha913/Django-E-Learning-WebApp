from django.urls import path
from myapp import views
app_name = 'myapp'


urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:topic_id>',views.detail,name='detail'),
    path(r'findcourses',views.findcourses,name='findcourses'),
    path(r'placeOrder', views.place_order, name='placeOrder'),
    path(r'review',views.review, name='review'),
    path(r'user_login',views.user_login, name='user_login'),
    path(r'user_logout', views.user_logout,name='user_logout'),
    path(r'myaccount',views.myaccount,name='myaccount')
    ]