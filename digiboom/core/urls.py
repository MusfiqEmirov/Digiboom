from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('services/', views.services, name='services'),
    path('services/detail/', views.services_detail, name='services_detail'),
    path('projects/detail/', views.projects_detail, name='projects_detail'),
    path('training/', views.training, name='training'),
    path('training/detail/', views.training_detail, name='training_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/detail/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-up/', views.sign_up, name='sign_up'),
]
