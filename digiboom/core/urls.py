from django.urls import path

from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<slug:slug>/', views.projects_detail, name='projects_detail'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.services_detail, name='services_detail'),
    path('training/', views.training, name='training'),
    path('training/<slug:slug>/', views.training_detail, name='training_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-up/', views.sign_up, name='sign_up'),
    # Inbound forms → admin models
    path('api/appeal/', views.api_appeal_contact, name='api_appeal'),
    path('api/consultation/', views.api_consultation_appeal, name='api_consultation'),
    path('api/package-order/', views.api_package_order, name='api_package_order'),
    path('api/training-order/', views.api_training_order, name='api_training_order'),
    path('api/review/', views.api_review, name='api_review'),
]
