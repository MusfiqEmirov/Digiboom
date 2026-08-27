"""
Projects / Portfolio (Project).

Card image is not a separate ImageField — selected in gallery via «Kart şəkli?»
(is_cover). Tag / WhatWeDid / Gallery are inlines on Project edit only.
"""

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget

from core.models import (
    Project,
    ProjectGalleryImage,
    ProjectServiceTag,
    ProjectWhatWeDid,
)

from .admin_help import PROJECT_HELP, AdminPageHelpMixin
from .mixins import AdminImageCompressMixin


class ProjectAdminForm(forms.ModelForm):
    """CKEditor for project description."""

    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'description_az': CKEditorWidget(),
            'description_en': CKEditorWidget(),
            'description_ru': CKEditorWidget(),
        }


class ProjectServiceTagInline(admin.TabularInline):
    """Layihəyə daxil olan xidmətlər — mövcud Service-lərdən seçilir; ilk 2 kartlarda görünür."""

    model = ProjectServiceTag
    extra = 0
    ordering = ('id',)
    classes = ('wide',)
    autocomplete_fields = ('service',)
    verbose_name = 'Xidmət'
    verbose_name_plural = (
        'Daxil olan xidmətlər — mövcud xidmətlərdən istədiyiniz qədər seçin; '
        'ilk 2-si portfolio kartlarında görünəcək'
    )
    fields = ('service',)


class ProjectWhatWeDidInline(admin.TabularInline):
    """What we did on the project list."""

    model = ProjectWhatWeDid
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Element'
    verbose_name_plural = 'Layihədə nələr etdik'
    fields = ('text_az', 'text_en', 'text_ru', 'sort_order')


class ProjectGalleryImageInline(admin.TabularInline):
    """Gallery — image with is_cover=True appears on the portfolio card."""

    model = ProjectGalleryImage
    extra = 1
    max_num = 40
    ordering = ('id',)
    classes = ('wide',)
    verbose_name = 'Şəkil'
    verbose_name_plural = 'Qalereya — «Kart şəkli?» işarələnən şəkil portfolio kartında görünür'
    fields = ('image_preview', 'image', 'is_cover')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """Gallery image preview."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = _('Önizləmə')


@admin.register(Project)
class ProjectAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    """Projects — main left-menu section."""

    admin_page_help = PROJECT_HELP
    form = ProjectAdminForm
    list_display = (
        'name_az',
        'is_active',
        'on_main_page',
    )
    list_filter = ('is_active', 'on_main_page')
    list_editable = ('is_active', 'on_main_page')
    search_fields = ('name_az', 'name_en', 'name_ru', 'subtitle_az')
    ordering = ('id',)
    inlines = [
        ProjectServiceTagInline,
        ProjectWhatWeDidInline,
        ProjectGalleryImageInline,
    ]
    fieldsets = (
        ('Status', {
            'fields': (
                'is_active',
                'on_main_page',
            ),
        }),
        ('Azərbaycan', {
            'fields': ('name_az', 'subtitle_az', 'description_az'),
            'classes': ('wide',),
            'description': 'Ad kart və detail h1-də; alt başlıq detail-də; təsvir CKEditor.',
        }),
        ('English', {
            'fields': ('name_en', 'subtitle_en', 'description_en'),
            'classes': ('wide', 'g-lang-en'),
        }),
        ('Русский', {
            'fields': ('name_ru', 'subtitle_ru', 'description_ru'),
            'classes': ('wide', 'g-lang-ru'),
        }),
        ('Video', {
            'fields': ('video',),
            'description': (
                'Tanıtım videosu optional — poster yoxdur, brauzer ilk kadra düşəcək. '
                'Kart şəkli qalereyada «Kart şəkli?» ilə seçilir.'
            ),
        }),
        ('Sosial linklər', {
            'fields': (
                'url_web',
                'url_instagram',
                'url_facebook',
                'url_tiktok',
                'url_linkedin',
                'url_youtube',
            ),
            'classes': ('collapse',),
            'description': 'Dolu olan linklər kartda ikon kimi görünəcək.',
        }),
    )
