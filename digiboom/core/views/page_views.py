"""
General pages: home, about, legal, auth stubs, 404.

CMS wiring lives in utils/*_queries.py (Averta-style thin views).
"""

from django.shortcuts import render

from core.utils.about_queries import build_about_page_context
from core.utils.home_queries import build_home_page_context
from core.utils.legal_queries import legal_page_context
from core.utils.page_header_queries import page_header_context


def home(request):
    """Home — hero, about, projects, services, packages, reviews, FAQ."""
    return render(request, 'index.html', build_home_page_context(request))


def about(request):
    """About — PageHeader(about) + About singleton + related."""
    return render(request, 'about-us.html', build_about_page_context(request))


def privacy(request):
    """Privacy policy — PageHeader(privacy) + LegalContent.privacy_*."""
    ctx = page_header_context('privacy', request)
    ctx.update(legal_page_context('privacy', request, lang=ctx.get('language')))
    return render(request, 'privacy-policy.html', ctx)


def terms(request):
    """Terms of use — PageHeader(terms) + LegalContent.terms_*."""
    ctx = page_header_context('terms', request)
    ctx.update(legal_page_context('terms', request, lang=ctx.get('language')))
    return render(request, 'terms-and-conditions.html', ctx)


def sign_in(request):
    return render(request, 'sign-in.html')


def sign_up(request):
    return render(request, 'sign-up.html')


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)
