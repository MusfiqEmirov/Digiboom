from django.core.exceptions import ValidationError
from django.db import models


class TrainingOrder(models.Model):
    """
    Təlim sifarişi — training-detail.html #trainingOrderForm.

    Biznes axını (növbəti fazalarda bağlanacaq):
    1) Müştəri form doldurur → «Ödənişə keçin»
    2) Ödəniş uğurlu olanda sifariş DB-yə düşür (payment_status=paid)
    3) Admin Google Drive link(lər)ini əlavə edir (TrainingOrderDriveLink inline)
    4) Admin «Linkləri göndər» → müştərinin Gmail-inə mail (sonra implement)
    5) is_links_sent / links_sent_at qeyd olunur

    Bu fazada: yalnız MODEL + ADMIN. Gateway / form POST / email YOX.
    Admin-dən yeni sifariş əlavə edilmir (has_add_permission=False).
    """

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Gözləyir'
        PAID = 'paid', 'Ödənib'
        FAILED = 'failed', 'Uğursuz'
        REFUNDED = 'refunded', 'Geri qaytarılıb'

    training = models.ForeignKey(
        'core.Training',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Təlim',
    )
    training_name = models.CharField(
        max_length=160,
        blank=True,
        default='',
        verbose_name='Təlim adı',
        help_text='Formadan gələn təlim adı (snapshot) — təlim silinsə belə qalır.',
    )

    full_name = models.CharField(
        max_length=120,
        verbose_name='Ad və soyad',
        help_text='Form: name="name"',
    )
    phone = models.CharField(
        max_length=40,
        verbose_name='Nömrə',
        help_text='Form: name="phone"',
    )
    gmail = models.EmailField(
        verbose_name='Gmail',
        help_text=(
            'Form: name="gmail". Yalnız @gmail.com ünvanları qəbul olunur. '
            'Digiboom-da digər email istifadə olunmur.'
        ),
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name='Ödəniş statusu',
        help_text=(
            'Gateway sonra bağlanacaq. Test üçün admin-dən dəyişmək olar. '
            'Sonra yalnız paid sifarişlər «işlənəcək» siyahıda önə çıxacaq.'
        ),
    )
    payment_id = models.CharField(
        max_length=120,
        blank=True,
        default='',
        verbose_name='Ödəniş ID',
        help_text='Gateway transaction id (sonra).',
    )
    provider_ref = models.CharField(
        max_length=120,
        blank=True,
        default='',
        verbose_name='Provider ref',
        help_text='Gateway provider referansı (sonra).',
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Ödəniş vaxtı',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Məbləğ (AZN)',
        help_text='Ödənilən məbləğ snapshot; Training.price-dan kopyalana bilər.',
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name='Oxunub?',
        help_text='Sifarişi oxuduqdan sonra işarələyin.',
    )
    is_customer = models.BooleanField(
        default=False,
        verbose_name='Müştərimizdir?',
        help_text='Bu şəxs müştəri olubsa işarələyin.',
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Silinib?',
        help_text='Fiziki silmək əvəzinə işarələyin.',
    )
    is_links_sent = models.BooleanField(
        default=False,
        verbose_name='Linklər göndərilib?',
        help_text=(
            'Email göndərmə növbəti fazada bağlanacaq. '
            'İndi yalnız Drive linklərini saxlayın; '
            'is_links_sent-i əl ilə və ya «Göndərildi kimi işarələ» action ilə qeyd edə bilərsiniz.'
        ),
    )
    links_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Linklər göndərilmə vaxtı',
    )
    admin_note = models.TextField(
        blank=True,
        default='',
        verbose_name='Admin qeydi',
        help_text='Daxili qeyd — müştəriyə göndərilmir.',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yenilənmə',
    )

    class Meta:
        verbose_name = 'Təlim sifarişi'
        verbose_name_plural = 'Təlim sifarişləri'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.full_name} — {self.training_name or self.training}'

    def clean(self):
        super().clean()
        gmail = (self.gmail or '').strip().lower()
        if gmail and not gmail.endswith('@gmail.com'):
            raise ValidationError({
                'gmail': 'Yalnız @gmail.com ünvanı qəbul olunur.',
            })
        if gmail:
            self.gmail = gmail


class TrainingOrderDriveLink(models.Model):
    """Sifarişə bağlı Google Drive / material linkləri (admin inline)."""

    order = models.ForeignKey(
        TrainingOrder,
        on_delete=models.CASCADE,
        related_name='drive_links',
        verbose_name='Sifariş',
    )
    title = models.CharField(
        max_length=160,
        blank=True,
        default='',
        verbose_name='Başlıq',
        help_text='Məsələn: «Modul 1», «Materiallar».',
    )
    url = models.URLField(
        max_length=500,
        verbose_name='Google Drive linki',
        help_text='Müştəriyə göndəriləcək Drive / material URL.',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Sıra',
    )

    class Meta:
        verbose_name = 'Drive linki'
        verbose_name_plural = 'Drive materialları'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.title or self.url or f'Link #{self.pk}'
