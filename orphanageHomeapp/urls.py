from django.urls import path

from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('agriculture/', views.agriculture, name='agriculture'),
	path('contact/', views.contact, name='contact'),
	path('career/', views.career, name='career'),
	path('donate/', views.donate, name='donate'),
	path('healthcare/', views.healthcare, name='healthcare'),
	path('privacy/', views.privacy, name='privacy'),
	path('skillshop/', views.skillshop, name='skillshop'),
	path('terms/', views.terms, name='terms'),
	path('otherpayment/', views.otherpayment, name='otherpayment'),
]