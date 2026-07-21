from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about-us.html')


def portfolio(request):
    return render(request, 'portfolio.html')


def services(request):
    return render(request, 'services.html')


def services_detail(request):
    return render(request, 'services-detail.html')


def projects_detail(request):
    return render(request, 'projects-detail.html')


def training(request):
    return render(request, 'training.html')


def training_detail(request):
    return render(request, 'training-detail.html')


def blog(request):
    return render(request, 'blog.html')


def blog_detail(request):
    return render(request, 'blog-detail.html')


def contact(request):
    return render(request, 'contact.html')


def privacy(request):
    return render(request, 'privacy-policy.html')


def terms(request):
    return render(request, 'terms-and-conditions.html')


def sign_in(request):
    return render(request, 'sign-in.html')


def sign_up(request):
    return render(request, 'sign-up.html')


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)
