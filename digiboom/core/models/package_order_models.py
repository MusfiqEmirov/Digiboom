from django.db import models


class PackageOrder(models.Model):
    """
    Sayt «Paket sifarişi» formasından gələn sifarişlər.
    Admin yalnız baxış / status — yeni sifariş əlavə edilmir.
    """

    full_name = models.CharField(
        max_length=120,
        verbose_name='Ad və soyad',
    )
    phone = models.CharField(
        max_length=40,
        verbose_name='Nömrə',
    )
    email = models.EmailField(
        verbose_name='Email',
    )
    package = models.ForeignKey(
        'core.Package',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Paket',
    )
    package_name = models.CharField(
        max_length=160,
        blank=True,
        default='',
        verbose_name='Paket adı',
        help_text='Formadan gələn paket adı (snapshot) — paket silinsə belə qalır.',
    )
    message = models.TextField(
        blank=True,
        default='',
        verbose_name='Mesaj',
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name='Oxunub?',
        help_text='Sifarişi oxuduqdan sonra işarələyin.',
    )
    is_customer = models.BooleanField(
        default=False,
        verbose_name='Müştəri',
        help_text='Bu şəxs müştəri olubsa işarələyin.',
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
        verbose_name = 'Paket sifarişi'
        verbose_name_plural = 'Paket sifarişləri'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.full_name} — {self.package_name or self.package}'
