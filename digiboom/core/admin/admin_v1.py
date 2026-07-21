from django import forms
from django.contrib import admin
from django.db import models
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html, strip_tags
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget

from core.models import (
    About,
    AboutGalleryImage,
    AboutSection,
    Blog,
    BlogCategory,
    Contact,
    FAQ,
    FAQSubItem,
    HomeHeroMedia,
    Package,
    PackageFeature,
    PackageOrder,
    PageHeader,
    Partner,
    Project,
    ProjectGalleryImage,
    ProjectServiceTag,
    ProjectWhatWeDid,
    Review,
    Service,
    ServiceCategory,
    ServiceGalleryImage,
    ServiceIncludeItem,
    ServiceWhyItem,
    StatisticItem,
    Training,
    TrainingAccessLink,
    TrainingCategory,
    TrainingCurriculumItem,
    TrainingGalleryImage,
    TrainingOrder,
    TrainingOrderDriveLink,
)

admin.site.site_header = 'DigiBoom — Sayt idarəetməsi'
admin.site.site_title = 'DigiBoom Admin'
admin.site.index_title = 'Bölmə seçin — hər biri saytın müəyyən hissəsini idarə edir'
admin.site.empty_value_display = '—'


class AdminImageCompressMixin:
    """Browser-side image compression for admin forms that upload images."""

    class Media:
        js = ('js/admin_image_compress.js',)


# ---------------------------------------------------------------------------
# Forms (CKEditor)
# ---------------------------------------------------------------------------

class AboutAdminForm(forms.ModelForm):
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
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'body_az': CKEditorWidget(),
            'body_en': CKEditorWidget(),
            'body_ru': CKEditorWidget(),
        }


# ---------------------------------------------------------------------------
# Inlines (hamısı About edit səhifəsində)
# ---------------------------------------------------------------------------

class AboutSectionInline(admin.StackedInline):
    model = AboutSection
    form = AboutSectionInlineForm
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Bölmə'
    verbose_name_plural = 'Bölmələr (Missiya / Agentlik / Academy…) — hansı ikon seçilsə, saytda həmin ikon görünəcək'
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
    model = AboutGalleryImage
    extra = 1
    max_num = 40
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Qaleriya şəkli'
    verbose_name_plural = 'Qaleriya şəkilləri'
    fields = ('image_preview', 'image', 'sort_order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = _('Önizləmə')


class PartnerInline(admin.TabularInline):
    model = Partner
    extra = 1
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Tərəfdaş loqosu'
    verbose_name_plural = 'Tərəfdaş loqoları'
    fields = ('logo_preview', 'logo', 'sort_order')
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height:48px;border-radius:4px;" />',
                obj.logo.url,
            )
        return '—'

    logo_preview.short_description = _('Önizləmə')


class StatisticItemInline(admin.TabularInline):
    model = StatisticItem
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Statistika'
    verbose_name_plural = 'Statistika elementləri — hansı ikon seçilsə, saytda həmin ikon görünəcək'
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
# About (singleton) — sol menyuda yalnız bu
# ---------------------------------------------------------------------------

@admin.register(About)
class AboutAdmin(AdminImageCompressMixin, admin.ModelAdmin):
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
        ('Azərbaycan — məzmun', {
            'fields': ('mezmun_az',),
            'classes': ('wide',),
            'description': 'Başlıq və mətn bir yerdə — CKEditor ilə yazın.',
        }),
        ('English — məzmun', {
            'fields': ('mezmun_en',),
            'classes': ('wide', 'g-lang-en'),
        }),
        ('Русский — məzmun', {
            'fields': ('mezmun_ru',),
            'classes': ('wide', 'g-lang-ru'),
        }),
        ('Tanıtım videosu', {
            'fields': ('video',),
            'description': (
                'Poster yoxdur — brauzer ilk kadra düşəcək. '
                'Aşağıda bölmələr, qalereya, tərəfdaş loqoları və statistika əlavə edin. '
                'Səhifə banner şəkli və devizi «Səhifə bannerləri» bölməsindədir.'
            ),
        }),
        ('Ana səhifə mətni', {
            'fields': ('ana_sehife_metn_az', 'ana_sehife_metn_en', 'ana_sehife_metn_ru'),
            'classes': ('wide',),
            'description': 'Ana səhifədəki «Haqqımızda» bloku — bir mətn bloku.',
        }),
    )

    def mezmun_qisa(self, obj):
        text = strip_tags(obj.mezmun_az or '').strip()
        return (text[:60] + '…') if len(text) > 60 else (text or '—')

    mezmun_qisa.short_description = 'Məzmun'

    def has_video(self, obj):
        return bool(obj.video)

    has_video.boolean = True
    has_video.short_description = 'Video'

    def has_add_permission(self, request):
        # Singleton: yalnız 1 qeyd
        if About.objects.exists():
            return False
        return super().has_add_permission(request)


# ---------------------------------------------------------------------------
# Əlaqə məlumatları (singleton) — ünvan, WhatsApp, email, sosial; ayrı SocialLink yox
# ---------------------------------------------------------------------------

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'whatsapp_number', 'address_az')
    search_fields = ('email', 'whatsapp_number', 'address_az', 'phone')
    fieldsets = (
        ('Ünvan / Xəritə', {
            'fields': (
                'address_az',
                'address_en',
                'address_ru',
                'map_url',
            ),
            'classes': ('wide',),
            'description': (
                'Burada yazılanlar əlaqə səhifəsi, footer və sağ tərəf ikonlarına '
                'avtomatik düşəcək (front sonra). Xəritə linki həm ofis xəritəsi, '
                'həm ünvana klik üçündür.'
            ),
        }),
        ('Sosial şəbəkələr', {
            'fields': (
                'whatsapp_number',
                'email',
                'phone',
                'facebook_url',
                'instagram_url',
                'tiktok_url',
                'linkedin_url',
                'youtube_url',
            ),
            'classes': ('wide',),
            'description': 'Sosial şəbəkə linkini yerləşdirin.',
        }),
    )

    def has_add_permission(self, request):
        # Singleton: yalnız 1 qeyd
        if Contact.objects.exists():
            return False
        return super().has_add_permission(request)


# ---------------------------------------------------------------------------
# Forms — Səhifə bannerləri
# ---------------------------------------------------------------------------

class PageHeaderAdminForm(forms.ModelForm):
    class Meta:
        model = PageHeader
        fields = '__all__'
        widgets = {
            'motto_az': CKEditorWidget(),
            'motto_en': CKEditorWidget(),
            'motto_ru': CKEditorWidget(),
        }


class HomeHeroMediaInlineForm(forms.ModelForm):
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
        # Admin-də kömək mətnləri qarışıqlıq yaradır — təmiz saxla
        for name in ('image', 'video', 'sort_order', 'media_type'):
            if name in self.fields:
                self.fields[name].help_text = ''


class HomeHeroMediaFormSet(BaseInlineFormSet):
    """Video yalnız bir dəfə ola bilər."""

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


# ---------------------------------------------------------------------------
# Inlines — Ana səhifə şəkil / video (yalnız home)
# ---------------------------------------------------------------------------

class HomeHeroMediaInline(admin.StackedInline):
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


# ---------------------------------------------------------------------------
# Səhifə bannerləri — sol menyuda tək giriş
# ---------------------------------------------------------------------------

@admin.register(PageHeader)
class PageHeaderAdmin(AdminImageCompressMixin, admin.ModelAdmin):
    form = PageHeaderAdminForm
    list_display = ('page', 'motto_preview', 'image_preview', 'home_media_count')
    list_filter = ('page',)
    search_fields = ('motto_az', 'motto_en', 'motto_ru')
    ordering = ('page',)
    inlines = [HomeHeroMediaInline]
    fieldsets = (
        ('Səhifə', {
            'fields': ('page',),
            'description': (
                'Hər səhifə üçün bir banner yaradın. '
                'Ana səhifədə «Şəkil əlavə et» və «Video əlavə et» düymələrindən istifadə edin '
                '(video yalnız bir dəfə). Hər slaydın «Sıra» sahəsinə rəqəm yazın — '
                '0 birinci başlayır. Digər səhifələrdə bir banner şəkli və deviz kifayətdir.'
            ),
        }),
        ('Banner şəkli', {
            'fields': ('image',),
            'classes': ('fieldset-banner-image',),
            'description': (
                'Ana səhifədən başqa səhifələr üçün fon şəkli. '
                'Ana səhifə seçilibsə bu sahə gizlədilir.'
            ),
        }),
        ('Azərbaycan — deviz', {
            'fields': ('motto_az',),
            'classes': ('wide',),
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
        css = {'all': ('css/admin_page_banner.css',)}
        js = (
            'js/admin_image_compress.js',
            'js/admin_page_banner.js',
        )

    def get_fieldsets(self, request, obj=None):
        return self.fieldsets

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        if obj.page != 'home':
            obj.home_media.all().delete()
        elif obj.image:
            obj.image = None
            obj.save(update_fields=['image'])

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
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:40px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = 'Şəkil'

    def home_media_count(self, obj):
        if obj.page != 'home':
            return '—'
        return obj.home_media.count()

    home_media_count.short_description = 'Media sayı'


# ---------------------------------------------------------------------------
# Forms — Xidmətlər
# ---------------------------------------------------------------------------

class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description_az': CKEditorWidget(),
            'description_en': CKEditorWidget(),
            'description_ru': CKEditorWidget(),
        }


# ---------------------------------------------------------------------------
# Inlines — Why / Include / Gallery (yalnız Service edit-də)
# ---------------------------------------------------------------------------

class ServiceWhyItemInline(admin.TabularInline):
    model = ServiceWhyItem
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Səbəb'
    verbose_name_plural = 'Niyə bu xidmət? — hansı ikon seçilsə, saytda həmin ikon görünəcək'
    fields = ('text_az', 'text_en', 'text_ru', 'icon', 'sort_order')


class ServiceIncludeItemInline(admin.TabularInline):
    model = ServiceIncludeItem
    extra = 0
    ordering = ('id',)
    classes = ('wide',)
    verbose_name = 'Element'
    verbose_name_plural = 'Xidmətə daxildir'
    fields = ('text_az', 'text_en', 'text_ru')


class ServiceGalleryImageInline(admin.TabularInline):
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
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = _('Önizləmə')


# ---------------------------------------------------------------------------
# Xidmət kateqoriyaları — sadə list (filter üçün)
# ---------------------------------------------------------------------------

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """Menyuda göstərilmir — Xidmət edit-də kateqoriya FK-nin «+» düyməsi ilə əlavə olunur."""

    list_display = ('name_az', 'name_en', 'name_ru')
    search_fields = ('name_az', 'name_en', 'name_ru')
    ordering = ('name_az', 'id')
    fields = (
        'name_az',
        'name_en',
        'name_ru',
    )

    def has_module_permission(self, request):
        # Sol menyudan («Sayt məzmunu») gizlət; related popup işləsin.
        return False


# ---------------------------------------------------------------------------
# Xidmətlər — sol menyuda əsas bölmə; Why/Include/Gallery inline
# ---------------------------------------------------------------------------

@admin.register(Service)
class ServiceAdmin(AdminImageCompressMixin, admin.ModelAdmin):
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


# ---------------------------------------------------------------------------
# Forms — Layihələr
# ---------------------------------------------------------------------------

class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'description_az': CKEditorWidget(),
            'description_en': CKEditorWidget(),
            'description_ru': CKEditorWidget(),
        }


# ---------------------------------------------------------------------------
# Inlines — Tag / WhatWeDid / Gallery (yalnız Project edit-də)
# ---------------------------------------------------------------------------

class ProjectServiceTagInline(admin.TabularInline):
    model = ProjectServiceTag
    extra = 0
    ordering = ('id',)
    classes = ('wide',)
    verbose_name = 'Xidmət teqi'
    verbose_name_plural = (
        'Daxil olan xidmət növləri — ilk 2-si kartlarda görünəcək; '
        'hansı ikon seçilsə, saytda həmin ikon görünəcək'
    )
    fields = ('name_az', 'name_en', 'name_ru', 'icon')


class ProjectWhatWeDidInline(admin.TabularInline):
    model = ProjectWhatWeDid
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Element'
    verbose_name_plural = 'Layihədə nələr etdik'
    fields = ('text_az', 'text_en', 'text_ru', 'sort_order')


class ProjectGalleryImageInline(admin.TabularInline):
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
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = _('Önizləmə')


# ---------------------------------------------------------------------------
# Layihələr — sol menyuda əsas bölmə; Tag/WhatWeDid/Gallery inline
# ---------------------------------------------------------------------------

@admin.register(Project)
class ProjectAdmin(AdminImageCompressMixin, admin.ModelAdmin):
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


# ---------------------------------------------------------------------------
# Paketlər — Feature yalnız inline (ayrı menyu yox)
# ---------------------------------------------------------------------------

class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 0
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Element'
    verbose_name_plural = 'Nələr daxildir'
    fields = ('text_az', 'text_en', 'text_ru', 'sort_order')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        'name_az',
        'price',
        'price_from',
        'show_on_home',
        'show_in_footer',
        'is_active',
        'sort_order',
    )
    list_filter = ('show_on_home', 'is_active')
    list_editable = ('show_on_home', 'show_in_footer', 'is_active', 'sort_order')
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
                'show_in_footer',
            ),
            'description': (
                'Ana səhifə — seçilmiş paketlər. '
                'Xidmətlər səhifəsində bütün aktiv paketlər avtomatik görünür. '
                'Footer — ayrıca checkbox (adətən ana səhifədəkilər).'
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


# ---------------------------------------------------------------------------
# Forms — Bloq
# ---------------------------------------------------------------------------

class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'description_az': CKEditorWidget(),
            'description_en': CKEditorWidget(),
            'description_ru': CKEditorWidget(),
        }


# ---------------------------------------------------------------------------
# Bloq kateqoriyaları — sadə list
# ---------------------------------------------------------------------------

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_az', 'name_en', 'name_ru')
    search_fields = ('name_az', 'name_en', 'name_ru')
    ordering = ('name_az', 'id')
    fields = (
        'name_az',
        'name_en',
        'name_ru',
    )


# ---------------------------------------------------------------------------
# Bloqlar — kateqoriya dropdown, CKEditor, image compress
# ---------------------------------------------------------------------------

@admin.register(Blog)
class BlogAdmin(AdminImageCompressMixin, admin.ModelAdmin):
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


# ---------------------------------------------------------------------------
# Inlines — Access links / Curriculum / Gallery (yalnız Training edit-də)
# ---------------------------------------------------------------------------

class TrainingAccessLinkInline(admin.TabularInline):
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
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = _('Önizləmə')


# ---------------------------------------------------------------------------
# Təlim kateqoriyaları — sadə list (filter üçün)
# ---------------------------------------------------------------------------

@admin.register(TrainingCategory)
class TrainingCategoryAdmin(admin.ModelAdmin):
    """Menyuda göstərilmir — Təlim edit-də kateqoriya FK-nin «+» düyməsi ilə əlavə olunur."""

    list_display = ('name_az', 'name_en', 'name_ru')
    search_fields = ('name_az', 'name_en', 'name_ru')
    ordering = ('name_az',)
    fields = (
        'name_az',
        'name_en',
        'name_ru',
    )

    def has_module_permission(self, request):
        # Sol menyudan gizlət; related popup işləsin.
        return False


# ---------------------------------------------------------------------------
# Təlimlər — sol menyuda əsas bölmə; Links/Curriculum/Gallery inline
# ---------------------------------------------------------------------------

@admin.register(Training)
class TrainingAdmin(AdminImageCompressMixin, admin.ModelAdmin):
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


# ---------------------------------------------------------------------------
# Paket sifarişləri — yalnız sayt formasından; admin baxış / status
# ---------------------------------------------------------------------------

@admin.register(PackageOrder)
class PackageOrderAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone_link',
        'email_link',
        'package_name',
        'is_read',
        'is_customer',
        'created_at',
    )
    list_editable = ('is_read', 'is_customer')
    list_filter = (
        'is_read',
        'is_customer',
        'package_name',
        ('created_at', admin.DateFieldListFilter),
    )
    search_fields = ('full_name', 'phone', 'email', 'package_name', 'message')
    ordering = ('-created_at',)
    readonly_fields = (
        'full_name',
        'phone_link',
        'email_link',
        'package_name',
        'message',
        'created_at',
        'updated_at',
    )
    actions = ('mark_as_read', 'mark_as_unread')
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 4, 'cols': 80})},
    }
    fieldsets = (
        ('Müştəri / sifariş', {
            'fields': (
                'full_name',
                'phone_link',
                'email_link',
                'package_name',
                'message',
                'created_at',
                'updated_at',
            ),
        }),
        ('Status', {
            'fields': (
                'is_read',
                'is_customer',
            ),
        }),
    )

    @staticmethod
    def _whatsapp_digits(phone):
        digits = ''.join(c for c in (phone or '') if c.isdigit())
        return digits or None

    @admin.display(description='Nömrə')
    def phone_link(self, obj):
        phone = (obj.phone or '').strip()
        if not phone:
            return '—'
        digits = self._whatsapp_digits(phone)
        if not digits:
            return phone
        return format_html(
            '<a href="https://wa.me/{}" target="_blank" rel="noopener noreferrer">{}</a>',
            digits,
            phone,
        )

    @admin.display(description='Email')
    def email_link(self, obj):
        email = (obj.email or '').strip()
        if not email:
            return '—'
        return format_html(
            '<a href="mailto:{}">{}</a>',
            email,
            email,
        )

    @admin.action(description='Seçilmişləri oxunmuş et')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} sifariş oxunmuş kimi işarələndi.')

    @admin.action(description='Seçilmişləri oxunmamış et')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} sifariş oxunmamış kimi işarələndi.')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# ---------------------------------------------------------------------------
# Təlim sifarişləri — form/ödəniş sonra; admin Drive + status
# ---------------------------------------------------------------------------

class TrainingOrderDriveLinkInline(admin.TabularInline):
    model = TrainingOrderDriveLink
    extra = 1
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = 'Link'
    verbose_name_plural = (
        'Drive materialları — hər sətirdə bir Google Drive / material URL. '
        'Email göndərmə növbəti fazada bağlanacaq; indi yalnız linkləri saxlayın.'
    )
    fields = ('title', 'url', 'sort_order')


@admin.register(TrainingOrder)
class TrainingOrderAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'gmail_link',
        'training_name',
        'payment_status',
        'is_read',
        'is_customer',
        'is_links_sent',
        'created_at',
    )
    list_editable = ('is_read', 'is_customer')
    list_filter = (
        'payment_status',
        'is_read',
        'is_customer',
        'is_links_sent',
        'training',
        ('created_at', admin.DateFieldListFilter),
    )
    search_fields = (
        'full_name',
        'phone',
        'gmail',
        'training_name',
        'payment_id',
    )
    ordering = ('-created_at',)
    readonly_fields = (
        'full_name',
        'phone_link',
        'gmail_link',
        'training',
        'training_name',
        'amount',
        'payment_id',
        'paid_at',
        'created_at',
        'updated_at',
        'links_sent_at',
    )
    inlines = (TrainingOrderDriveLinkInline,)
    actions = (
        'mark_as_read',
        'mark_as_unread',
        'mark_links_sent',
    )
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 4, 'cols': 80})},
    }
    fieldsets = (
        ('Sifariş / müştəri', {
            'fields': (
                'full_name',
                'phone_link',
                'gmail_link',
                'training',
                'training_name',
                'created_at',
                'updated_at',
            ),
            'description': (
                'Form (#trainingOrderForm) və ödəniş gateway sonra bağlanacaq. '
                'Bu sahələr yalnız oxunur.'
            ),
        }),
        ('Ödəniş', {
            'fields': (
                'payment_status',
                'amount',
                'payment_id',
                'provider_ref',
                'paid_at',
            ),
            'description': (
                'Gateway bu fazada YOX. Test üçün payment_status dəyişmək olar. '
                'Sonra yalnız paid sifarişlər işlənəcək.'
            ),
        }),
        ('Status', {
            'fields': (
                'is_read',
                'is_customer',
                'is_deleted',
                'is_links_sent',
                'links_sent_at',
            ),
            'description': (
                'Drive linkləri aşağıdakı inline-dədir. '
                'Email göndərmə növbəti fazada bağlanacaq — indi yalnız linkləri '
                'saxlayın; is_links_sent-i əl ilə və ya action ilə işarələyin.'
            ),
        }),
        ('Admin qeydi', {
            'fields': ('admin_note',),
        }),
    )

    @staticmethod
    def _whatsapp_digits(phone):
        digits = ''.join(c for c in (phone or '') if c.isdigit())
        return digits or None

    @admin.display(description='Nömrə')
    def phone_link(self, obj):
        phone = (obj.phone or '').strip()
        if not phone:
            return '—'
        digits = self._whatsapp_digits(phone)
        if not digits:
            return phone
        return format_html(
            '<a href="https://wa.me/{}" target="_blank" rel="noopener noreferrer">{}</a>',
            digits,
            phone,
        )

    @admin.display(description='Gmail')
    def gmail_link(self, obj):
        gmail = (obj.gmail or '').strip()
        if not gmail:
            return '—'
        return format_html(
            '<a href="mailto:{}">{}</a>',
            gmail,
            gmail,
        )

    @admin.action(description='Seçilmişləri oxunmuş et')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} sifariş oxunmuş kimi işarələndi.')

    @admin.action(description='Seçilmişləri oxunmamış et')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} sifariş oxunmamış kimi işarələndi.')

    @admin.action(description='Göndərildi kimi işarələ (email YOX — test)')
    def mark_links_sent(self, request, queryset):
        from django.utils import timezone

        updated = queryset.update(
            is_links_sent=True,
            links_sent_at=timezone.now(),
        )
        self.message_user(
            request,
            f'{updated} sifariş «linklər göndərilib» kimi işarələndi '
            '(real email növbəti fazada).',
        )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# ---------------------------------------------------------------------------
# Rəylər — yalnız sayt formasından; admin təsdiq/redaktə/silmə
# ---------------------------------------------------------------------------

@admin.register(Review)
class ReviewAdmin(AdminImageCompressMixin, admin.ModelAdmin):
    list_display = (
        'name',
        'message_preview',
        'rating',
        'service',
        'training',
        'is_active',
        'is_read',
        'created_at',
    )
    list_filter = (
        'is_active',
        'category_type',
        'service',
        'training',
        'rating',
        ('created_at', admin.DateFieldListFilter),
        'is_read',
    )
    list_editable = ('is_active',)
    search_fields = ('name', 'message', 'category_label')
    ordering = ('-created_at',)
    readonly_fields = ('image_preview', 'created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 6, 'cols': 80})},
    }
    fieldsets = (
        ('Şəxs', {
            'fields': ('name',),
        }),
        ('Kateqoriya', {
            'fields': (
                'category_type',
                'service',
                'training',
                'category_label',
            ),
        }),
        ('Rəy', {
            'fields': ('rating', 'message', 'image_preview', 'image'),
            'classes': ('wide',),
        }),
        ('Görünürlük', {
            'fields': (
                'is_active',
                'is_read',
                'created_at',
                'updated_at',
            ),
        }),
    )

    @admin.display(description='Rəy')
    def message_preview(self, obj):
        text = (obj.message or '').strip()
        if not text:
            return '—'
        if len(text) > 120:
            return text[:120] + '…'
        return text

    @admin.display(description='Şəkil önizləmə')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:160px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


# ---------------------------------------------------------------------------
# Tez-tez verilən suallar — 1-ci dərəcə / 2-ci dərəcə + cavab
# ---------------------------------------------------------------------------

class FAQSubItemInline(admin.TabularInline):
    model = FAQSubItem
    extra = 1
    ordering = ('sort_order', 'id')
    classes = ('wide',)
    verbose_name = '2-ci dərəcəli sual və cavab'
    verbose_name_plural = '2-ci dərəcəli suallar və cavablar'
    fields = (
        'title_az',
        'title_en',
        'title_ru',
        'answer_az',
        'answer_en',
        'answer_ru',
        'sort_order',
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        'question_az',
        'is_active',
        'sort_order',
        'sub_count',
    )
    list_editable = ('is_active', 'sort_order')
    list_filter = ('is_active',)
    search_fields = (
        'question_az',
        'question_en',
        'question_ru',
        'sub_items__title_az',
        'sub_items__title_en',
        'sub_items__title_ru',
        'sub_items__answer_az',
        'sub_items__answer_en',
        'sub_items__answer_ru',
    )
    ordering = ('sort_order', 'id')
    inlines = [FAQSubItemInline]
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 4, 'cols': 80})},
    }
    fieldsets = (
        ('1-ci dərəcəli sual', {
            'fields': (
                'question_az',
                'question_en',
                'question_ru',
            ),
            'description': (
                'Ana sual — məs. «Digiboom nə şirkətdir?» '
                'Aşağıdakı cədvəldə: 2-ci dərəcə varsa sual + cavab yazın; '
                'yoxdursa 2-ci dərəcəni boş saxlayıb yalnız cavab yazın.'
            ),
        }),
        ('Parametrlər', {
            'fields': (
                'is_active',
                'sort_order',
            ),
            'classes': ('faq-params-after-inline',),
        }),
    )

    class Media:
        js = ('js/admin_faq_params_order.js',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_sub_count=models.Count('sub_items'))

    @admin.display(description='2-ci dərəcə', ordering='_sub_count')
    def sub_count(self, obj):
        return getattr(obj, '_sub_count', obj.sub_items.count())

