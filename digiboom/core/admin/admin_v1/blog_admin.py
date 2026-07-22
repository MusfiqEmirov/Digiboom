"""
Blog + category.

BlogCategory is hidden from the left menu — added via FK «+» popup on Blog edit.
view_count is readonly — incremented automatically on the front detail page.
"""

from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from core.models import Blog, BlogCategory

from .admin_help import BLOG_CATEGORY_HELP, BLOG_HELP, AdminPageHelpMixin
from .mixins import AdminImageCompressMixin


class BlogAdminForm(forms.ModelForm):
    """CKEditor for blog content."""

    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'description_az': CKEditorWidget(),
            'description_en': CKEditorWidget(),
            'description_ru': CKEditorWidget(),
        }


@admin.register(BlogCategory)
class BlogCategoryAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    """Hidden from menu — related popup still works."""

    admin_page_help = BLOG_CATEGORY_HELP
    list_display = ('name_az', 'name_en', 'name_ru')
    search_fields = ('name_az', 'name_en', 'name_ru')
    ordering = ('name_az', 'id')
    fields = (
        'name_az',
        'name_en',
        'name_ru',
    )

    def has_module_permission(self, request):
        return False


@admin.register(Blog)
class BlogAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    """Blog posts — category, CKEditor, image compression."""

    admin_page_help = BLOG_HELP
    form = BlogAdminForm
    list_display = (
        'name_az',
        'category',
        'date',
        'view_count',
        'is_active',
    )
    list_filter = ('category', 'is_active')
    list_editable = ('date', 'is_active')
    search_fields = ('name_az', 'name_en', 'name_ru')
    ordering = ('-date', '-id')
    readonly_fields = ('view_count',)
    fieldsets = (
        ('Kateqoriya və status', {
            'fields': (
                'category',
                'date',
                'is_active',
                'view_count',
            ),
        }),
        ('Azərbaycan', {
            'fields': ('name_az', 'description_az'),
            'classes': ('wide',),
        }),
        ('English', {
            'fields': ('name_en', 'description_en'),
            'classes': ('wide', 'g-lang-en'),
        }),
        ('Русский', {
            'fields': ('name_ru', 'description_ru'),
            'classes': ('wide', 'g-lang-ru'),
        }),
        ('Şəkil', {
            'fields': ('image',),
            'description': 'Cover şəkil mütləqdir. Yükləyəndə avtomatik sıxılır.',
        }),
    )
