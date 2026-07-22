"""
Page banners and related inline models.

Special rules:
- Only one PageHeader per page (unique).
- page=home → HomeHeroMedia (image/video); single banner image is not used.
- page=training → TrainingWhyItem + TrainingStatItem (max 3) + why_title_*.
- Other pages → image + motto.
- Admin save_related removes inline/fields that do not match the page type.
- HomeHeroMedia: only one video per banner (formset validation).
"""

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models


PAGE_CHOICES = [
    ('home', 'Ana səhifə'),
    ('about', 'Haqqımızda'),
    ('services', 'Xidmətlər'),
    ('portfolio', 'Portfolio'),
    ('training', 'Təlimlər'),
    ('blog', 'Bloq'),
    ('contact', 'Əlaqə'),
    ('privacy', 'Məxfilik siyasəti'),
    ('terms', 'İstifadə şərtləri'),
]

HOME_MEDIA_TYPE_CHOICES = [
    ('image', 'Şəkil'),
    ('video', 'Video'),
]

TRAINING_WHY_ICON_CHOICES = [
    ('lucide:video', 'Video / dərs'),
    ('lucide:file-check', 'Sertifikat / təsdiq'),
    ('lucide:users', 'Komanda / qrup'),
    ('lucide:infinity', 'Limitsiz giriş'),
    ('lucide:graduation-cap', 'Academy / təlim'),
    ('lucide:sparkles', 'Missiya / dəyərlər'),
    ('lucide:target', 'Hədəf'),
    ('lucide:lightbulb', 'İdeya'),
    ('lucide:rocket', 'Artım / start'),
    ('lucide:award', 'Mükafat / keyfiyyət'),
    ('lucide:clock', 'Vaxt'),
    ('lucide:book-open', 'Material / kitab'),
    ('lucide:headphones', 'Dəstək'),
    ('lucide:check-circle', 'Keyfiyyət'),
]


class PageHeader(models.Model):
    """Page banner + multilingual motto — one record per page."""

    page = models.CharField(
        max_length=32,
        choices=PAGE_CHOICES,
        unique=True,
        verbose_name='Səhifə',
        help_text='Hansı səhifənin banneri. Hər səhifə üçün yalnız bir qeyd ola bilər.',
    )
    motto_az = models.TextField(
        validators=[MaxLengthValidator(5000)],
        blank=True,
        verbose_name='Deviz (AZ)',
        help_text='Bannerin altındakı qısa şüar (HTML).',
    )
    motto_en = models.TextField(
        validators=[MaxLengthValidator(5000)],
        blank=True,
        null=True,
        verbose_name='Deviz (EN)',
    )
    motto_ru = models.TextField(
        validators=[MaxLengthValidator(5000)],
        blank=True,
        null=True,
        verbose_name='Deviz (RU)',
    )
    image = models.ImageField(
        upload_to='images/page_headers/',
        blank=True,
        null=True,
        verbose_name='Banner şəkli',
        help_text=(
            'Ana səhifədən başqa səhifələrin banner fon şəkli. '
            'Ana səhifə seçildikdə bu sahə lazım deyil — şəkil və videoları '
            'aşağıdakı «Ana səhifə — şəkil və videolar» siyahısından əlavə edin.'
        ),
    )
    # Training page — «Niyə biz?» title (only when page=training)
    why_title_az = models.CharField(
        max_length=120,
        blank=True,
        verbose_name='Niyə biz — başlıq (AZ)',
        help_text='Panel başlığı. Məsələn: Niyə biz?',
    )
    why_title_en = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Niyə biz — başlıq (EN)',
    )
    why_title_ru = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Niyə biz — başlıq (RU)',
    )

    class Meta:
        verbose_name = 'Səhifə banneri'
        verbose_name_plural = 'Səhifə bannerləri'
        ordering = ('page',)

    def __str__(self):
        return self.get_page_display()


class HomeHeroMedia(models.Model):
    """Home page banner slides — image or video; order is user-defined."""

    header = models.ForeignKey(
        PageHeader,
        on_delete=models.CASCADE,
        related_name='home_media',
        verbose_name='Ana səhifə banneri',
        limit_choices_to={'page': 'home'},
    )
    media_type = models.CharField(
        max_length=16,
        choices=HOME_MEDIA_TYPE_CHOICES,
        verbose_name='Tip',
        help_text='Bu sətir şəkil, yoxsa video olacaq?',
    )
    image = models.ImageField(
        upload_to='images/page_headers/home/',
        blank=True,
        null=True,
        verbose_name='Şəkil',
        help_text='Tip «Şəkil» olduqda mütləq yükləyin. Fayl avtomatik sıxılır.',
    )
    video = models.FileField(
        upload_to='videos/page_headers/home/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=('mp4', 'webm', 'mov', 'ogg', 'mkv'),
                message='İcazə verilən formatlar: mp4, webm, mov, ogg, mkv.',
            )
        ],
        verbose_name='Video',
        help_text='Tip «Video» olduqda mütləq yükləyin (məsələn mp4, webm).',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='Özünüz seçin: kiçik rəqəm əvvəl başlayır (0 = birinci slayd).',
    )

    class Meta:
        verbose_name = 'Ana səhifə media'
        verbose_name_plural = 'Ana səhifə — şəkil və videolar'
        ordering = ('sort_order', 'id')

    def __str__(self):
        label = self.get_media_type_display() if self.media_type else 'Media'
        return f'{label} #{self.pk}' if self.pk else label

    def clean(self):
        super().clean()
        if self.header_id and self.header.page != 'home':
            return

        errors = {}
        if self.media_type == 'image':
            if not self.image:
                errors['image'] = 'Tip «Şəkil» seçilib — şəkil faylı yükləyin.'
        elif self.media_type == 'video':
            if not self.video:
                errors['video'] = 'Tip «Video» seçilib — video faylı yükləyin.'

        if errors:
            raise ValidationError(errors)


class TrainingWhyItem(models.Model):
    """Training page — «Niyə biz?» reasons (icon + text)."""

    header = models.ForeignKey(
        PageHeader,
        on_delete=models.CASCADE,
        related_name='training_why_items',
        verbose_name='Təlim banneri',
        limit_choices_to={'page': 'training'},
    )
    text_az = models.CharField(
        max_length=200,
        verbose_name='Səbəb (AZ)',
        help_text='Məsələn: Video dərslər və canlı sessiyalar',
    )
    text_en = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Səbəb (EN)',
    )
    text_ru = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Səbəb (RU)',
    )
    icon = models.CharField(
        max_length=64,
        choices=TRAINING_WHY_ICON_CHOICES,
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
        verbose_name = 'Təlim — səbəb'
        verbose_name_plural = 'Təlim — səbəblər (Niyə biz?)'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.text_az or f'Səbəb #{self.pk}'

    def clean(self):
        super().clean()
        # Not training — not persisted; admin will delete it
        if self.header_id and self.header.page != 'training':
            return


class TrainingStatItem(models.Model):
    """Training page — statistics (maximum 3)."""

    header = models.ForeignKey(
        PageHeader,
        on_delete=models.CASCADE,
        related_name='training_stats',
        verbose_name='Təlim banneri',
        limit_choices_to={'page': 'training'},
    )
    value = models.CharField(
        max_length=32,
        verbose_name='Rəqəm / dəyər',
        help_text='Məsələn: 8+, 120+, 500+',
    )
    label_az = models.CharField(
        max_length=120,
        verbose_name='Alt yazı (AZ)',
        help_text='Məsələn: Aktiv kurs, Saat məzmun, Məzun',
    )
    label_en = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Alt yazı (EN)',
    )
    label_ru = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name='Alt yazı (RU)',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Maksimum 3 statistika.',
    )

    class Meta:
        verbose_name = 'Təlim — statistika'
        verbose_name_plural = 'Təlim — statistika (maks. 3)'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return f'{self.value} — {self.label_az}' if self.label_az else self.value

    def clean(self):
        super().clean()
        if self.header_id and self.header.page != 'training':
            return
