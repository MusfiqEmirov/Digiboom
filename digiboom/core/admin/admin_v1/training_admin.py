"""
Trainings (Training) + category.

TrainingCategory is hidden from the left menu.
Card image via gallery is_cover; promo video via curriculum is_promo.
AccessLinks are URLs sent to the customer after payment.
"""

from django import forms
from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.models import (
    Training,
    TrainingAccessLink,
    TrainingCategory,
    TrainingCurriculumItem,
    TrainingGalleryImage,
)

from .admin_help import (
    TRAINING_CATEGORY_HELP,
    TRAINING_HELP,
    AdminPageHelpMixin,
)
from .mixins import AdminImageCompressMixin


class TrainingAccessLinkInline(admin.TabularInline):
    """Links sent to the customer after successful payment (Zoom, materials, etc.)."""

    model = TrainingAccessLink
    extra = 0
    ordering = ('id',)
    classes = ('wide',)
    verbose_name = 'Link'
    verbose_name_plural = (
        'Ödənişdən sonra müştəriyə göndərilən linklər '
        '(Zoom, material, Telegram və s.)'
    )
    fields = (
        'title_az',
        'title_en',
        'title_ru',
        'url',
    )


class TrainingCurriculumItemInline(admin.TabularInline):
    """Course overview — is_promo=True video becomes the detail-page promo."""

    model = TrainingCurriculumItem
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'İcmal'
    verbose_name_plural = (
        'Kurs məzmunu — icmal; «Tanıtım videosu?» işarələnən detail-də tanıtım olur'
    )
    fields = (
        'title_az',
        'title_en',
        'title_ru',
        'text_az',
        'text_en',
        'text_ru',
        'video',
        'is_promo',
        'sort_order',
    )


class TrainingGalleryImageInline(admin.TabularInline):
    """Training gallery frames — is_cover=True becomes the card image."""

    model = TrainingGalleryImage
    extra = 1
    max_num = 40
    ordering = ('id',)
    classes = ('wide',)
    verbose_name = 'Kadr'
    verbose_name_plural = (
        'Təlimdən kadrlar — «Kart şəkli?» işarələnən şəkil kartında görünür'
    )
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


@admin.register(TrainingCategory)
class TrainingCategoryAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    """Hidden from menu — related popup still works."""

    admin_page_help = TRAINING_CATEGORY_HELP
    list_display = ('name_az', 'name_en', 'name_ru')
    search_fields = ('name_az', 'name_en', 'name_ru')
    ordering = ('name_az',)
    fields = (
        'name_az',
        'name_en',
        'name_ru',
    )

    def has_module_permission(self, request):
        return False


@admin.register(Training)
class TrainingAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    """Trainings — main left-menu section; Links/Curriculum/Gallery as inlines."""

    admin_page_help = TRAINING_HELP
    list_display = (
        'name_az',
        'category',
        'price',
        'level',
        'is_popular',
        'is_active',
        'sort_order',
    )
    list_filter = ('category', 'level', 'is_popular', 'is_active')
    list_editable = ('sort_order', 'is_active', 'is_popular')
    search_fields = ('name_az', 'name_en', 'name_ru')
    ordering = ('sort_order', 'id')
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 4, 'cols': 80})},
    }
    inlines = [
        TrainingAccessLinkInline,
        TrainingCurriculumItemInline,
        TrainingGalleryImageInline,
    ]
    fieldsets = (
        ('Kateqoriya və status', {
            'fields': (
                'category',
                'level',
                'is_popular',
                'is_active',
                'sort_order',
            ),
        }),
        ('Azərbaycan', {
            'fields': ('name_az', 'description_az'),
            'classes': ('wide',),
            'description': 'Ad kart və detail-də; təsvir kart + detail eyni.',
        }),
        ('English', {
            'fields': ('name_en', 'description_en'),
            'classes': ('wide', 'g-lang-en'),
        }),
        ('Русский', {
            'fields': ('name_ru', 'description_ru'),
            'classes': ('wide', 'g-lang-ru'),
        }),
        ('Müddət və qiymət', {
            'fields': (
                'duration_hours',
                'lesson_count',
                'price',
            ),
        }),
    )
