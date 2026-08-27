"""
About page models.

Special rules:
- About is a singleton (only one record in admin).
- Section / gallery / partner / statistics are FK-linked to About (inlines).
- Banner image and mottos live on PageHeader (page=about) — not here.
- show_on_home=True statistics also appear on the home page.
"""

from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models
from django.utils.html import strip_tags


# Front Iconify/Lucide names — selected value is rendered as an icon on the site.
ABOUT_SECTION_ICON_CHOICES = [
    ('lucide:briefcase', 'Agentlik / iş'),
    ('lucide:graduation-cap', 'Academy / təlim'),
    ('lucide:sparkles', 'Missiya / dəyərlər'),
    ('lucide:target', 'Hədəf'),
    ('lucide:users', 'Komanda'),
    ('lucide:lightbulb', 'İdeya'),
    ('lucide:rocket', 'Artım / start'),
    ('lucide:heart', 'Dəyərlər'),
    ('lucide:award', 'Mükafat / keyfiyyət'),
    ('lucide:globe', 'Qlobal / region'),
    ('lucide:code-2', 'Texnologiya'),
    ('lucide:palette', 'Dizayn / brend'),
]

STAT_ICON_CHOICES = [
    ('lucide:calendar-check', 'Təcrübə / illər'),
    ('lucide:users', 'Müştərilər / komanda'),
    ('lucide:briefcase', 'Layihələr'),
    ('lucide:award', 'Mükafat'),
    ('lucide:trending-up', 'Artım'),
    ('lucide:globe', 'Ölkə / region'),
    ('lucide:thumbs-up', 'Məmnuniyyət'),
    ('lucide:star', 'Reytinq'),
    ('lucide:handshake', 'Tərəfdaşlıq'),
    ('lucide:rocket', 'Start / sürət'),
    ('lucide:graduation-cap', 'Təlim / Academy'),
    ('lucide:heart', 'Sevgi / loyallıq'),
]


class About(models.Model):
    """About page — typically only one record (singleton)."""

    mezmun_az = models.TextField(
        validators=[MaxLengthValidator(8000)],
        verbose_name='Məzmun (AZ)',
        help_text='Video yanındakı blok: başlıq və mətn bir yerdə (CKEditor).',
    )
    mezmun_en = models.TextField(
        validators=[MaxLengthValidator(8000)],
        null=True,
        blank=True,
        verbose_name='Məzmun (EN)',
    )
    mezmun_ru = models.TextField(
        validators=[MaxLengthValidator(8000)],
        null=True,
        blank=True,
        verbose_name='Məzmun (RU)',
    )
    video = models.FileField(
        upload_to='videos/about/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=('mp4', 'webm', 'mov', 'ogg', 'mkv'),
                message='İcazə verilən formatlar: mp4, webm, mov, ogg, mkv.',
            )
        ],
        verbose_name='Tanıtım videosu',
        help_text='Haqqımızda səhifəsində play düyməsi ilə açılan video. Yalnız bir fayl.',
    )
    ana_sehife_metn_az = models.TextField(
        validators=[MaxLengthValidator(5000)],
        verbose_name='Ana səhifə mətni (AZ)',
        help_text='Ana səhifədəki «Haqqımızda» bloku — bir mətn bloku (HTML).',
    )
    ana_sehife_metn_en = models.TextField(
        validators=[MaxLengthValidator(5000)],
        null=True,
        blank=True,
        verbose_name='Ana səhifə mətni (EN)',
    )
    ana_sehife_metn_ru = models.TextField(
        validators=[MaxLengthValidator(5000)],
        null=True,
        blank=True,
        verbose_name='Ana səhifə mətni (RU)',
    )

    class Meta:
        verbose_name = 'Haqqımızda səhifəsi'
        verbose_name_plural = 'Haqqımızda səhifəsi'

    def __str__(self):
        text = strip_tags(self.mezmun_az or '').strip()
        return (text[:60] + '…') if len(text) > 60 else (text or 'Haqqımızda')


class AboutSection(models.Model):
    """Text cards such as Mission / Agency / DigiBoom Academy."""

    about = models.ForeignKey(
        About,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name='Haqqımızda səhifəsi',
    )
    title_az = models.CharField(
        max_length=120,
        verbose_name='Başlıq (AZ)',
    )
    title_en = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Başlıq (EN)',
    )
    title_ru = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Başlıq (RU)',
    )
    body_az = models.TextField(
        validators=[MaxLengthValidator(5000)],
        verbose_name='Məzmun (AZ)',
        help_text='Kartın içindəki mətn (HTML).',
    )
    body_en = models.TextField(
        validators=[MaxLengthValidator(5000)],
        null=True,
        blank=True,
        verbose_name='Məzmun (EN)',
    )
    body_ru = models.TextField(
        validators=[MaxLengthValidator(5000)],
        null=True,
        blank=True,
        verbose_name='Məzmun (RU)',
    )
    icon = models.CharField(
        max_length=64,
        choices=ABOUT_SECTION_ICON_CHOICES,
        blank=True,
        null=True,
        verbose_name='İkon',
        help_text='Hansı ikon seçilsə, saytda həmin ikon görünəcək.',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )

    class Meta:
        verbose_name = 'Haqqımızda bölməsi'
        verbose_name_plural = 'Haqqımızda bölmələri'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.title_az or f'Bölmə #{self.pk}'


class AboutGalleryImage(models.Model):
    """About page gallery images — any number allowed."""

    about = models.ForeignKey(
        About,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Haqqımızda səhifəsi',
    )
    image = models.ImageField(
        upload_to='images/about/gallery/',
        verbose_name='Şəkil',
        help_text='Qalereya şəkli. Yükləyəndə avtomatik sıxılır.',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )

    class Meta:
        verbose_name = 'Qaleriya şəkli'
        verbose_name_plural = 'Qaleriya şəkilləri'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return f'Qaleriya #{self.pk}' if self.pk else 'Qaleriya şəkli'


class Partner(models.Model):
    """Partner / client logo — inline on the About edit page."""

    about = models.ForeignKey(
        About,
        on_delete=models.CASCADE,
        related_name='partners',
        verbose_name='Haqqımızda səhifəsi',
    )
    logo = models.ImageField(
        upload_to='images/partners/',
        verbose_name='Loqo',
        help_text='Tərəfdaş/müştəri loqosu. Yükləyəndə avtomatik sıxılır.',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )

    class Meta:
        verbose_name = 'Tərəfdaş loqosu'
        verbose_name_plural = 'Tərəfdaş loqoları'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return f'Loqo #{self.pk}' if self.pk else 'Tərəfdaş loqosu'


class StatisticItem(models.Model):
    """Number + label + icon — inline on the About edit page."""

    about = models.ForeignKey(
        About,
        on_delete=models.CASCADE,
        related_name='statistics',
        verbose_name='Haqqımızda səhifəsi',
    )
    value = models.CharField(
        max_length=32,
        verbose_name='Rəqəm / dəyər',
        help_text='Məsələn: 25, 90+, 150.',
    )
    label_az = models.CharField(
        max_length=120,
        verbose_name='Alt yazı (AZ)',
        help_text='Rəqəmin altında görünən qısa mətn. Məs: Tamamlanmış layihə',
    )
    label_en = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Alt yazı (EN)',
    )
    label_ru = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Alt yazı (RU)',
    )
    icon = models.CharField(
        max_length=64,
        choices=STAT_ICON_CHOICES,
        blank=True,
        null=True,
        verbose_name='İkon',
        help_text='Hansı ikon seçilsə, saytda həmin ikon görünəcək.',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Saytda göstərilsin?',
        help_text='Söndürsəniz heç yerdə görünməz.',
    )
    show_on_home = models.BooleanField(
        default=True,
        verbose_name='Ana səhifədə?',
        help_text='Ana səhifənin statistika blokunda da göstərilsin.',
    )

    class Meta:
        verbose_name = 'Statistika elementi'
        verbose_name_plural = 'Statistika elementləri'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return f'{self.value} — {self.label_az}' if self.label_az else self.value
