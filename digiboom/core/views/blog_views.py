"""
Blog list + detail views.
"""

from django.shortcuts import render

from core.utils.blog_queries import (
    get_blog_by_slug,
    get_blog_categories,
    get_blogs,
    get_related_blogs,
)
from core.utils.i18n import get_language_from_request, get_lang_field
from core.utils.page_header_queries import page_header_context


def blog(request):
    """Blog listing."""
    lang = get_language_from_request(request)
    ctx = page_header_context('blog', request, lang=lang)
    ctx.update({
        'blogs': get_blogs(),
        'blog_categories': get_blog_categories(),
    })
    return render(request, 'blog.html', ctx)


def blog_detail(request, slug):
    """Single blog post by slug (increments view_count)."""
    lang = get_language_from_request(request)
    post = get_blog_by_slug(slug)
    ctx = {
        'blog': post,
        'blog_title': get_lang_field(post, 'name', lang),
        'blog_body': get_lang_field(post, 'description', lang),
        'other_blogs': get_related_blogs(post),
        'language': lang,
    }
    return render(request, 'blog-detail.html', ctx)
