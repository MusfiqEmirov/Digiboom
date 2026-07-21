from django.db import models
from django.utils.translation import get_language, gettext as _

from core.utils import unique_slug_for


CURRENCY_CHOICES = [
    ('AZN', 'AZN'),
    ('USD', 'USD'),
    ('EUR', 'EUR'),
]

# Son rəqəmin AZ oxunuşuna görə ablativ: dan (arka) / dən (ön).
_AZ_ABLATIVE_BY_DIGIT = {
    '0': 'dan',  # sıfır / on…
    '1': 'dən',  # bir
    '2': 'dən',  # iki
    '3': 'dən',  # üç
    '4': 'dən',  # dörd
    '5': 'dən',  # beş
    '6': 'dan',  # altı
    '7': 'dən',  # yeddi
    '8': 'dən',  # səkkiz
    '9': 'dan',  # doqquz
}


class Package(models.Model):
    """Paket — ana səhifə / xidmətlər / footer kartları."""

    name_az = models.CharField(max_length=160, verbose_name='Ad (AZ)')
    name_en = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='Ad (EN)',
    )
    name_ru = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='Ad (RU)',
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
        verbose_name='Slug',
        help_text='Avtomatik name_az-dan yaranır.',
    )
    description_az = models.TextField(
        verbose_name='Təsvir (AZ)',
        help_text='Paket adının altındakı qısa mətn.',
    )
    description_en = models.TextField(
        null=True,
        blank=True,
        verbose_name='Təsvir (EN)',
    )
    description_ru = models.TextField(
        null=True,
        blank=True,
        verbose_name='Təsvir (RU)',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Qiymət',
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='AZN',
        verbose_name='Valyuta',
    )
    price_from = models.BooleanField(
        default=False,
        verbose_name='Qiymətə dan/dən?',
        help_text='İşarələsəniz qiymətə «-dan/-dən» əlavə olunur (məs: 565-dən).',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktiv?',
        help_text='Söndürsəniz heç yerdə görünməz.',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )
    show_on_home = models.BooleanField(
        default=False,
        verbose_name='Ana səhifədə?',
        help_text='Ana səhifə «Xüsusi paketlər» blokunda göstərilsin.',
    )
    show_in_footer = models.BooleanField(
        default=False,
        verbose_name='Footer-də?',
        help_text='Footer Xidmətlər/Paketlər siyahısında.',
    )

    class Meta:
        verbose_name = 'Paket'
        verbose_name_plural = 'Paketlər'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.name_az or f'Paket #{self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.name_az)
        super().save(*args, **kwargs)

    def _az_price_from_suffix(self):
        """Qiymətin tam hissəsinin son rəqəminə görə dan/dən."""
        digit = str(int(self.price))[-1]
        return _AZ_ABLATIVE_BY_DIGIT.get(digit, 'dən')

    def get_price_display(self):
        """
        Lokalizə olunmuş qiymət mətni.
        AZ: 565-dən azn | EN: from 565 azn | RU: от 565 azn
        """
        if self.price == self.price.to_integral_value():
            amount = str(int(self.price))
        else:
            amount = format(self.price, 'f').rstrip('0').rstrip('.')
        currency = (self.currency or 'AZN').lower()
        if not self.price_from:
            return f'{amount} {currency}'

        lang = (get_language() or 'az')[:2]
        if lang == 'en':
            return f'{_("from")} {amount} {currency}'
        if lang == 'ru':
            return f'{_("от")} {amount} {currency}'
        return f'{amount}-{self._az_price_from_suffix()} {currency}'


class PackageFeature(models.Model):
    """«Nələr daxildir» — Package edit-də inline."""

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name='Paket',
    )
    text_az = models.CharField(max_length=255, verbose_name='Mətn (AZ)')
    text_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Mətn (EN)',
    )
    text_ru = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Mətn (RU)',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )

    class Meta:
        verbose_name = 'Nələr daxildir'
        verbose_name_plural = 'Nələr daxildir'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.text_az or f'Feature #{self.pk}'
