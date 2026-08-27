"""
About — singleton admin.

Single entry in the left menu. Sections, gallery, partners, and statistics are
inlines on the About edit page. Banner/motto live under «Səhifə bannerləri»
(page=about).
"""

from django import forms
from django.contrib import admin
from django.utils.html import format_html, strip_tags
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget

from core.models import (
    About,
    AboutGalleryImage,
    AboutSection,
    Partner,
    StatisticItem,
)

from .admin_help import ABOUT_HELP, AdminPageHelpMixin
from .mixins import AdminImageCompressMixin


# ---------------------------------------------------------------------------
# Forms — rich text via CKEditor
# ---------------------------------------------------------------------------

class AboutAdminForm(forms.ModelForm):
    """CKEditor widgets for About main fields."""

    class Meta:
        model = About
        fields = '__all__'
        widgets = {
            'mezmun_az': CKEditorWidget(),
            'mezmun_en': CKEditorWidget(),
            'mezmun_ru': CKEditorWidget(),
            'ana_sehife_metn_az': CKEditorWidget(),
            'ana_sehife_metn_en': CKEditorWidget(),
            'ana_sehife_metn_ru': CKEditorWidget(),
        }


class AboutSectionInlineForm(forms.ModelForm):
    """Body field for Mission / Agency / Academy cards."""

    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'body_az': CKEditorWidget(),
            'body_en': CKEditorWidget(),
            'body_ru': CKEditorWidget(),
        }


# ---------------------------------------------------------------------------
# Inlines — all on the About edit page
# ---------------------------------------------------------------------------

class AboutSectionInline(admin.StackedInline):
    """Text cards of type Mission / Agency / Academy."""

    model = AboutSection
    form = AboutSectionInlineForm
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Bölmə'
    verbose_name_plural = (
        'Bölmələr (Missiya / Agentlik / Academy…) — '
        'hansı ikon seçilsə, saytda həmin ikon görünəcək'
    )
    fields = (
        'title_az',
        'title_en',
        'title_ru',
        'body_az',
        'body_en',
        'body_ru',
        'icon',
        'sort_order',
    )


class AboutGalleryImageInline(admin.TabularInline):
    """Gallery images — About hero + home about carousel."""

    model = AboutGalleryImage
    extra = 1
    max_num = 40
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Qaleriya şəkli'
    verbose_name_plural = (
        'Qaleriya — Haqqımızda böyük şəkil (ilk) + ana səhifə karuseli'
    )
    fields = ('image_preview', 'image', 'sort_order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """Small preview of the uploaded image."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = _('Önizləmə')


class PartnerInline(admin.TabularInline):
    """Partner logos — About + home marquee."""

    model = Partner
    extra = 1
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Tərəfdaş loqosu'
    verbose_name_plural = 'Tərəfdaş loqoları — Haqqımızda və ana səhifə marquee'
    fields = ('logo_preview', 'logo', 'sort_order')
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        """Logo preview."""
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height:48px;border-radius:4px;" />',
                obj.logo.url,
            )
        return '—'

    logo_preview.short_description = _('Önizləmə')


class StatisticItemInline(admin.TabularInline):
    """Number + label + icon (About + home page statistics block)."""

    model = StatisticItem
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Statistika'
    verbose_name_plural = (
        'Statistika — Haqqımızda səhifəsi; '
        '«Ana səhifədə?» işarələnənlər ana səhifədə də görünür'
    )
    fields = (
        'value',
        'label_az',
        'label_en',
        'label_ru',
        'icon',
        'is_active',
        'show_on_home',
        'sort_order',
    )


# ---------------------------------------------------------------------------
# ModelAdmin — singleton (only one About record)
# ---------------------------------------------------------------------------

@admin.register(About)
class AboutAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    """
    All content for the About page.
    Add button is enabled only when no record exists yet.
    """

    admin_page_help = ABOUT_HELP
    form = AboutAdminForm
    list_display = ('mezmun_qisa', 'has_video')
    search_fields = ('mezmun_az', 'mezmun_en', 'mezmun_ru')
    inlines = [
        AboutSectionInline,
        AboutGalleryImageInline,
        PartnerInline,
        StatisticItemInline,
    ]
    fieldsets = (
        ('Azərbaycan — məzmun (Haqqımızda səhifəsi)', {
            'fields': ('mezmun_az',),
            'classes': ('wide',),
            'description': (
                'Yalnız /about/ — video yanındakı başlıq və mətn (CKEditor). '
                'Ana səhifə mətni aşağıdakı «Ana səhifə» blokundadır.'
            ),
        }),
        ('English — məzmun (About page)', {
            'fields': ('mezmun_en',),
            'classes': ('wide', 'g-lang-en'),
        }),
        ('Русский — məzmun (страница О нас)', {
            'fields': ('mezmun_ru',),
            'classes': ('wide', 'g-lang-ru'),
        }),
        ('Tanıtım videosu', {
            'fields': ('video',),
            'description': (
                'Yalnız Haqqımızda səhifəsi. Poster yoxdur — brauzer ilk kadra düşəcək. '
                'Banner şəkli/deviz «Səhifə bannerləri» (page=about) bölməsindədir.'
            ),
        }),
        ('Ana səhifə — Haqqımızda bloku', {
            'fields': ('ana_sehife_metn_az', 'ana_sehife_metn_en', 'ana_sehife_metn_ru'),
            'classes': ('wide',),
            'description': (
                'Ana səhifədəki «Haqqımızda» mətn bloku (HTML). '
                'Qalereya şəkilləri karusel, tərəfdaş loqoları marquee, '
                'statistika isə aşağıda «Ana səhifədə?» işarəsi olan sətirlərdir. '
                'Eyni model həm /about/, həm də gələcəkdə ana səhifə üçün istifadə olunur.'
            ),
        }),
    )

    def mezmun_qisa(self, obj):
        """Short list preview of content (without HTML tags)."""
        text = strip_tags(obj.mezmun_az or '').strip()
        return (text[:60] + '…') if len(text) > 60 else (text or '—')

    mezmun_qisa.short_description = 'Məzmun'

    def has_video(self, obj):
        """Shows whether a video has been uploaded."""
        return bool(obj.video)

    has_video.boolean = True
    has_video.short_description = 'Video'

    def has_add_permission(self, request):
        # Singleton: hide «Add» when a record already exists.
        if About.objects.exists():
            return False
        return super().has_add_permission(request)
