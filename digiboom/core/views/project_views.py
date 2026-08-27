"""
Portfolio list + project detail views.
"""

from django.shortcuts import render

from core.utils.i18n import get_language_from_request, get_lang_field
from core.utils.page_header_queries import page_header_context
from core.utils.project_queries import get_project_by_slug, get_projects


def portfolio(request):
    """Portfolio grid — all active projects."""
    lang = get_language_from_request(request)
    ctx = page_header_context('portfolio', request, lang=lang)
    ctx['projects'] = get_projects()
    return render(request, 'portfolio.html', ctx)


def projects_detail(request, slug):
    """Single project by slug."""
    lang = get_language_from_request(request)
    project = get_project_by_slug(slug)
    ctx = {
        'project': project,
        'project_name': get_lang_field(project, 'name', lang),
        'project_subtitle': get_lang_field(project, 'subtitle', lang),
        'project_description': get_lang_field(project, 'description', lang),
        'language': lang,
    }
    return render(request, 'projects-detail.html', ctx)
