"""
Blog queries.
"""

from django.db.models import F
from django.shortcuts import get_object_or_404

from core.models import Blog, BlogCategory


def get_blog_categories():
    return list(BlogCategory.objects.order_by('name_az', 'id'))


def get_blogs(*, active_only=True, limit=None):
    qs = Blog.objects.select_related('category').order_by('-date', '-id')
    if active_only:
        qs = qs.filter(is_active=True)
    if limit:
        qs = qs[:limit]
    return list(qs)


def get_blog_by_slug(slug):
    blog = get_object_or_404(
        Blog.objects.select_related('category'),
        slug=slug,
        is_active=True,
    )
    Blog.objects.filter(pk=blog.pk).update(view_count=F('view_count') + 1)
    blog.refresh_from_db(fields=['view_count'])
    return blog


def get_related_blogs(blog, limit=3):
    return list(
        Blog.objects.filter(is_active=True)
        .exclude(pk=blog.pk)
        .select_related('category')
        .order_by('-date', '-id')[:limit]
    )
