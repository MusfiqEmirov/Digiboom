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


class PageHeader(models.Model):
    """Səhifə banneri + çoxdilli deviz — hər səhifə üçün bir qeyd."""

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

    class Meta:
        verbose_name = 'Səhifə banneri'
        verbose_name_plural = 'Səhifə bannerləri'
        ordering = ('page',)

    def __str__(self):
        return self.get_page_display()


class HomeHeroMedia(models.Model):
    """Ana səhifə banner slaydları — şəkil və ya video; sıra özü seçilir."""

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
        # Ana səhifə deyilsə media saxlanılmır — admin siləcək; burda bloklama
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
