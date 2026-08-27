"""
Packages (Package) — Feature is inline only (no separate menu).

Visibility:
- show_on_home → home page «Xüsusi paketlər»
- Services page shows all active packages automatically
"""

from django.contrib import admin

from core.models import Package, PackageFeature

from .admin_help import PACKAGE_HELP, AdminPageHelpMixin


class PackageFeatureInline(admin.TabularInline):
    """What's included items."""

    model = PackageFeature
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Element'
    verbose_name_plural = 'Nələr daxildir'
    fields = ('text_az', 'text_en', 'text_ru', 'sort_order')


@admin.register(Package)
class PackageAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    """Package cards — price, visibility, and features."""

    admin_page_help = PACKAGE_HELP
    list_display = (
        'name_az',
        'price',
        'price_from',
        'show_on_home',
        'is_active',
        'sort_order',
    )
    list_filter = ('show_on_home', 'is_active')
    list_editable = ('show_on_home', 'is_active', 'sort_order')
    search_fields = ('name_az', 'name_en', 'name_ru', 'description_az')
    ordering = ('sort_order', 'id')
    inlines = [PackageFeatureInline]
    fieldsets = (
        ('Əsas', {
            'fields': (
                'name_az',
                'is_active',
                'sort_order',
            ),
        }),
        ('Qiymət', {
            'fields': (
                'price',
                'currency',
                'price_from',
            ),
        }),
        ('Görünürlük', {
            'fields': (
                'show_on_home',
            ),
            'description': (
                'Ana səhifə — seçilmiş paketlər. '
                'Xidmətlər səhifəsində bütün aktiv paketlər avtomatik görünür.'
            ),
        }),
        ('Azərbaycan', {
            'fields': ('description_az',),
            'classes': ('wide',),
            'description': 'Adın altındakı qısa mətn.',
        }),
        ('English', {
            'fields': ('name_en', 'description_en'),
            'classes': ('wide', 'g-lang-en'),
        }),
        ('Русский', {
            'fields': ('name_ru', 'description_ru'),
            'classes': ('wide', 'g-lang-ru'),
        }),
    )
