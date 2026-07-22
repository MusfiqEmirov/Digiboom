"""
Page banners (PageHeader) — one banner per page.

Special cases:
- page=home → HomeHeroMedia inline (image/video slides); banner image is cleared
- page=training → «Niyə biz?» title + reasons (icons) + statistics (max 3)
- other pages → single banner image + mottos

JS/CSS: admin_page_banner.js / admin_page_banner.css — show/hide fields by page
and move training blocks above the page selector.
"""

from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html, strip_tags
from ckeditor.widgets import CKEditorWidget

from core.models import (
    HomeHeroMedia,
    PageHeader,
    TrainingStatItem,
    TrainingWhyItem,
)

from .admin_help import PAGE_HEADER_HELP, AdminPageHelpMixin
from .mixins import AdminImageCompressMixin


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------

class PageHeaderAdminForm(forms.ModelForm):
    """Motto via CKEditor."""

    class Meta:
        model = PageHeader
        fields = '__all__'
        widgets = {
            'motto_az': CKEditorWidget(),
            'motto_en': CKEditorWidget(),
            'motto_ru': CKEditorWidget(),
        }


class HomeHeroMediaInlineForm(forms.ModelForm):
    """
    Home page media row.
    media_type is stored hidden — JS sets it via «Add image» / «Add video» buttons.
    """

    class Meta:
        model = HomeHeroMedia
        fields = '__all__'
        widgets = {
            'media_type': forms.HiddenInput(),
            'sort_order': forms.NumberInput(attrs={
                'style': 'width: 5em;',
                'min': '0',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('image', 'video', 'sort_order', 'media_type'):
            if name in self.fields:
                self.fields[name].help_text = ''


class HomeHeroMediaFormSet(BaseInlineFormSet):
    """Allows only one video row per banner."""

    def clean(self):
        super().clean()
        video_count = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data') or not form.cleaned_data:
                continue
            if form.cleaned_data.get('DELETE'):
                continue
            if form.cleaned_data.get('media_type') == 'video':
                video_count += 1
        if video_count > 1:
            raise forms.ValidationError(
                'Video yalnız bir dəfə əlavə edilə bilər. Artıq video sətiri var.'
            )


class TrainingStatFormSet(BaseInlineFormSet):
    """Maximum 3 items in the training statistics block."""

    def clean(self):
        super().clean()
        count = 0
        for form in self.forms:
            if not hasattr(form, 'cleaned_data') or not form.cleaned_data:
                continue
            if form.cleaned_data.get('DELETE'):
                continue
            if form.cleaned_data.get('value') or form.cleaned_data.get('label_az'):
                count += 1
        if count > 3:
            raise forms.ValidationError(
                'Statistika maksimum 3 ədəd ola bilər.'
            )


# ---------------------------------------------------------------------------
# Inlines
# ---------------------------------------------------------------------------

class HomeHeroMediaInline(admin.StackedInline):
    """Only for page=home — image/video slides."""

    model = HomeHeroMedia
    form = HomeHeroMediaInlineForm
    formset = HomeHeroMediaFormSet
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide', 'home-banner-media')
    verbose_name = 'Slayd'
    verbose_name_plural = 'Ana səhifə — şəkil və videolar'
    fields = (
        'media_type',
        'image_preview',
        'image',
        'video',
        'sort_order',
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.pk and obj.media_type == 'image' and obj.image:
            return format_html(
                '<img src="{}" style="max-height:64px;border-radius:4px;" />',
                obj.image.url,
            )
        if obj.pk and obj.media_type == 'video' and obj.video:
            return format_html(
                '<span style="font-size:12px;">{}</span>',
                obj.video.name.rsplit('/', 1)[-1],
            )
        return '—'

    image_preview.short_description = 'Önizləmə'


class TrainingWhyItemInline(admin.TabularInline):
    """Only for page=training — «Niyə biz?» reasons (icon + short text)."""

    model = TrainingWhyItem
    extra = 2
    ordering = ('sort_order', 'id')
    classes = ('wide', 'training-banner-block')
    verbose_name = 'Səbəb'
    verbose_name_plural = 'Təlim — səbəblər (ikon + mətn)'
    fields = ('text_az', 'text_en', 'text_ru', 'icon', 'sort_order')


class TrainingStatItemInline(admin.TabularInline):
    """Only for page=training — statistics (max 3)."""

    model = TrainingStatItem
    formset = TrainingStatFormSet
    extra = 3
    max_num = 3
    ordering = ('sort_order', 'id')
    classes = ('wide', 'training-banner-block')
    verbose_name = 'Statistika'
    verbose_name_plural = 'Təlim — statistika (maksimum 3 ədəd)'
    fields = ('value', 'label_az', 'label_en', 'label_ru', 'sort_order')


# ---------------------------------------------------------------------------
# ModelAdmin
# ---------------------------------------------------------------------------

@admin.register(PageHeader)
class PageHeaderAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    """
    Single left-menu entry: all page banners.
    On save, save_related clears inline/fields that do not match the page type.
    """

    admin_page_help = PAGE_HEADER_HELP
    form = PageHeaderAdminForm
    list_display = ('page', 'motto_preview', 'image_preview', 'home_media_count')
    list_filter = ('page',)
    search_fields = ('motto_az', 'motto_en', 'motto_ru', 'why_title_az')
    ordering = ('page',)
    # Training inlines first — JS also moves them to the top
    inlines = [
        TrainingWhyItemInline,
        TrainingStatItemInline,
        HomeHeroMediaInline,
    ]
    fieldsets = (
        ('Səhifə', {
            'fields': ('page',),
            'description': (
                'Hansı səhifənin bannerini redaktə edirsiniz? '
                '«Ana səhifə» → şəkil və video slaydlar. '
                '«Təlimlər» → «Niyə biz?» başlığı, ikonlu səbəblər və 3 statistik. '
                'Digər səhifələr → bir banner şəkli + deviz.'
            ),
        }),
        ('Təlim — Niyə biz? (yalnız başlıq)', {
            'fields': (
                'why_title_az',
                'why_title_en',
                'why_title_ru',
            ),
            'classes': ('wide', 'fieldset-training-why'),
            'description': (
                'Yalnız «Təlimlər» seçiləndə yuxarıda açılır. '
                'Buraya panel başlığını yazın (məsələn: «Niyə biz?»). '
                'Əlavə mətn yoxdur — səbəblər ikonla aşağıdakı cədvəldə, '
                'rəqəmlər isə statistika cədvəlində (maks. 3) əlavə olunur. '
                'Nümunə səbəb: «Video dərslər və canlı sessiyalar» + video ikonu. '
                'Nümunə statistika: 8+ / Aktiv kurs.'
            ),
        }),
        ('Banner şəkli', {
            'fields': ('image',),
            'classes': ('fieldset-banner-image',),
            'description': (
                'Ana səhifədən başqa səhifələrin fon şəkli. '
                'Ana səhifə seçilibsə bu sahə gizlədilir.'
            ),
        }),
        ('Azərbaycan — deviz', {
            'fields': ('motto_az',),
            'classes': ('wide',),
            'description': 'Səhifə bannerində görünən qısa şüar / tagline.',
        }),
        ('English — motto', {
            'fields': ('motto_en',),
            'classes': ('wide', 'g-lang-en'),
        }),
        ('Русский — девиз', {
            'fields': ('motto_ru',),
            'classes': ('wide', 'g-lang-ru'),
        }),
    )

    class Media:
        # admin_help.css — AdminPageHelpMixin.media property ilə gəlir
        css = {'all': ('css/admin_page_banner.css',)}
        js = (
            'js/admin_image_compress.js',
            'js/admin_page_banner.js',
        )

    def get_fieldsets(self, request, obj=None):
        return self.fieldsets

    def save_related(self, request, form, formsets, change):
        """
        Removes data that does not match the page type:
        - not home → delete home_media
        - home → clear single banner image + training fields/inlines
        - not training → clear training why/stats and why_title
        """
        super().save_related(request, form, formsets, change)
        obj = form.instance
        if obj.page != 'home':
            obj.home_media.all().delete()
        else:
            if obj.image:
                obj.image = None
                obj.save(update_fields=['image'])
            obj.training_why_items.all().delete()
            obj.training_stats.all().delete()
            PageHeader.objects.filter(pk=obj.pk).update(
                why_title_az='',
                why_title_en='',
                why_title_ru='',
            )

        if obj.page != 'training':
            obj.training_why_items.all().delete()
            obj.training_stats.all().delete()
            if obj.page != 'home':
                PageHeader.objects.filter(pk=obj.pk).update(
                    why_title_az='',
                    why_title_en='',
                    why_title_ru='',
                )

    def motto_preview(self, obj):
        text = (obj.motto_az or obj.motto_en or obj.motto_ru or '').strip()
        if not text:
            return '—'
        plain = ' '.join(strip_tags(text).split())
        return plain[:80] + ('…' if len(plain) > 80 else '')

    motto_preview.short_description = 'Deviz'

    def image_preview(self, obj):
        if obj.page == 'home':
            return 'şəkil/video siyahısı'
        if obj.page == 'training':
            return 'təlim paneli'
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:40px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = 'Şəkil'

    def home_media_count(self, obj):
        if obj.page == 'home':
            return obj.home_media.count()
        if obj.page == 'training':
            return f'{obj.training_why_items.count()} səbəb / {obj.training_stats.count()} stat'
        return '—'

    home_media_count.short_description = 'Əlavələr'
