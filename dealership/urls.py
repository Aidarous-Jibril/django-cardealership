# dealership/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'dealership'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('faq/', views.faq_view, name='faq'),

    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('auth/', include('authentication.urls', namespace='authentication')),

    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'), 
    path('cars/', views.car_search_view, name='car_search'), 
    path('reserve/<int:car_id>/', views.reserve_car, name='reserve_car'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),

]
