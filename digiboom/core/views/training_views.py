"""
Training list + detail views.
"""

from django.shortcuts import render

from core.utils.i18n import get_language_from_request, get_lang_field
from core.utils.page_header_queries import page_header_context
from core.utils.training_queries import (
    get_training_by_slug,
    get_training_categories,
    get_training_page_extras,
    get_trainings,
)


def training(request):
    """Training catalog + why/stats from PageHeader(training)."""
    lang = get_language_from_request(request)
    ctx = page_header_context('training', request, lang=lang)
    extras = get_training_page_extras()
    header = extras.get('training_header')
    ctx.update(extras)
    ctx['training_why_title'] = (
        get_lang_field(header, 'why_title', lang) if header else ''
    )
    trainings = get_trainings()
    popular = [t for t in trainings if t.is_popular]
    ctx.update({
        'trainings': trainings,
        'training_categories': get_training_categories(),
        'featured_training': popular[0] if popular else (trainings[0] if trainings else None),
    })
    return render(request, 'training.html', ctx)


def training_detail(request, slug):
    """Single training by slug."""
    lang = get_language_from_request(request)
    item = get_training_by_slug(slug)
    ctx = {
        'training': item,
        'training_name': get_lang_field(item, 'name', lang),
        'training_description': get_lang_field(item, 'description', lang),
        'language': lang,
    }
    return render(request, 'training-detail.html', ctx)
