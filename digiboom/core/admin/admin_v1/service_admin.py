"""
Services (Service) + category.

ServiceCategory is hidden from the left menu — added only via FK «+» popup on
Service edit. Why / Include / Gallery are inlines on Service edit only.
"""

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget

from core.models import (
    Service,
    ServiceCategory,
    ServiceGalleryImage,
    ServiceIncludeItem,
    ServiceWhyItem,
)

from .admin_help import (
    SERVICE_CATEGORY_HELP,
    SERVICE_HELP,
    AdminPageHelpMixin,
)
from .mixins import AdminImageCompressMixin


class ServiceAdminForm(forms.ModelForm):
    """CKEditor for detail description."""

    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description_az': CKEditorWidget(),
            'description_en': CKEditorWidget(),
            'description_ru': CKEditorWidget(),
        }


class ServiceWhyItemInline(admin.TabularInline):
    """Why this service? reasons."""

    model = ServiceWhyItem
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Səbəb'
    verbose_name_plural = 'Niyə bu xidmət? — hansı ikon seçilsə, saytda həmin ikon görünəcək'
    fields = ('text_az', 'text_en', 'text_ru', 'icon', 'sort_order')


class ServiceIncludeItemInline(admin.TabularInline):
    """What's included list."""

    model = ServiceIncludeItem
    extra = 0
    ordering = ('id',)
    classes = ('wide',)
    verbose_name = 'Element'
    verbose_name_plural = 'Xidmətə daxildir'
    fields = ('text_az', 'text_en', 'text_ru')


class ServiceGalleryImageInline(admin.TabularInline):
    """Work-in-progress gallery frames."""

    model = ServiceGalleryImage
    extra = 1
    max_num = 40
    ordering = ('id',)
    classes = ('wide',)
    verbose_name = 'Kadr'
    verbose_name_plural = 'İş prosesindən kadrlar'
    fields = ('image_preview', 'image')
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


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    """
    Not shown in menu — added via category FK «+» on Service edit.
    has_module_permission=False hides the left menu; related popup still works.
    """

    admin_page_help = SERVICE_CATEGORY_HELP
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


@admin.register(Service)
class ServiceAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    """Services — main left-menu section; Why/Include/Gallery as inlines."""

    admin_page_help = SERVICE_HELP
    form = ServiceAdminForm
    list_display = (
        'name_az',
        'category',
        'is_active',
        'on_main_page',
        'sort_order',
    )
    list_filter = ('category', 'is_active', 'on_main_page')
    list_editable = ('is_active', 'on_main_page', 'sort_order')
    search_fields = ('name_az', 'name_en', 'name_ru', 'card_text_az')
    ordering = ('sort_order', 'id')
    inlines = [
        ServiceWhyItemInline,
        ServiceIncludeItemInline,
        ServiceGalleryImageInline,
    ]
    fieldsets = (
        ('Kateqoriya və status', {
            'fields': (
                'category',
                'is_active',
                'on_main_page',
                'sort_order',
            ),
        }),
        ('Azərbaycan', {
            'fields': ('name_az', 'card_text_az', 'description_az'),
            'classes': ('wide',),
        }),
        ('English', {
            'fields': ('name_en', 'card_text_en', 'description_en'),
            'classes': ('wide', 'g-lang-en'),
        }),
        ('Русский', {
            'fields': ('name_ru', 'card_text_ru', 'description_ru'),
            'classes': ('wide', 'g-lang-ru'),
        }),
        ('Şəkil və video', {
            'fields': ('image', 'video'),
            'description': (
                'Kart/siyahı şəkli mütləqdir. Video optional — poster yoxdur, '
                'brauzer ilk kadra düşəcək. Aşağıda «Niyə», «Daxildir» və qalereya əlavə edin.'
            ),
        }),
    )
