from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models

from core.utils import unique_slug_for


class TrainingCategory(models.Model):
    """Təlim kateqoriyası — filter və qruplaşdırma üçün."""

    name_az = models.CharField(max_length=120, verbose_name='Ad (AZ)')
    name_en = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Ad (EN)',
    )
    name_ru = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Ad (RU)',
    )
    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
        verbose_name='Slug',
        help_text='Avtomatik name_az-dan yaranır.',
    )

    class Meta:
        verbose_name = 'Təlim kateqoriyası'
        verbose_name_plural = 'Təlim kateqoriyaları'
        ordering = ('name_az',)

    def __str__(self):
        return self.name_az or f'Kateqoriya #{self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.name_az)
        super().save(*args, **kwargs)


class Training(models.Model):
    """Təlim / kurs — kart + detail məzmunu."""

    class Level(models.TextChoices):
        BEGINNER = 'beginner', 'Başlanğıc'
        INTERMEDIATE = 'intermediate', 'Orta'
        ADVANCED = 'advanced', 'İrəli'

    category = models.ForeignKey(
        TrainingCategory,
        on_delete=models.PROTECT,
        related_name='trainings',
        verbose_name='Kateqoriya',
    )
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
        validators=[MaxLengthValidator(12000)],
        verbose_name='Təsvir (AZ)',
        help_text='Kart və detail üçün eyni mətn.',
    )
    description_en = models.TextField(
        validators=[MaxLengthValidator(12000)],
        null=True,
        blank=True,
        verbose_name='Təsvir (EN)',
    )
    description_ru = models.TextField(
        validators=[MaxLengthValidator(12000)],
        null=True,
        blank=True,
        verbose_name='Təsvir (RU)',
    )
    duration_hours = models.PositiveIntegerField(
        verbose_name='Müddət (saat)',
    )
    lesson_count = models.PositiveIntegerField(
        verbose_name='Dərs sayı',
    )
    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        verbose_name='Səviyyə',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Qiymət (AZN)',
    )
    is_popular = models.BooleanField(
        default=False,
        verbose_name='Ən populyar?',
        help_text='Spotlight / «Ən populyar» işarəsi.',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktiv?',
        help_text='Söndürsəniz saytda görünməz.',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )

    class Meta:
        verbose_name = 'Təlim'
        verbose_name_plural = 'Təlimlər'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.name_az or f'Təlim #{self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.name_az)
        super().save(*args, **kwargs)

    @property
    def cover_image(self):
        """Kart şəkli — qalereyada «Kart şəkli?» seçilmiş şəkil (yoxdursa ilk)."""
        cover = self.gallery_images.filter(is_cover=True).first()
        if cover:
            return cover.image
        first = self.gallery_images.first()
        return first.image if first else None

    @property
    def promo_video(self):
        """Tanıtım videosu — icmalda «Tanıtım videosu?» seçilmiş element."""
        item = self.curriculum_items.filter(is_promo=True).first()
        return item.video if item else None


class TrainingAccessLink(models.Model):
    """Ödənişdən sonra müştəriyə göndərilən linklər (Training edit-də inline)."""

    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='access_links',
        verbose_name='Təlim',
    )
    title_az = models.CharField(max_length=200, verbose_name='Başlıq (AZ)')
    title_en = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Başlıq (EN)',
    )
    title_ru = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Başlıq (RU)',
    )
    url = models.URLField(
        max_length=500,
        verbose_name='Link',
        help_text='Ödəniş uğurlu olanda müştəriyə göndəriləcək URL.',
    )

    class Meta:
        verbose_name = 'Müştəri linki'
        verbose_name_plural = 'Ödənişdən sonra göndərilən linklər'
        ordering = ('id',)

    def __str__(self):
        return self.title_az or f'Link #{self.pk}'


class TrainingCurriculumItem(models.Model):
    """Kurs məzmunu — icmal videoları (Training edit-də inline)."""

    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='curriculum_items',
        verbose_name='Təlim',
    )
    title_az = models.CharField(max_length=200, verbose_name='Başlıq (AZ)')
    title_en = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Başlıq (EN)',
    )
    title_ru = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Başlıq (RU)',
    )
    text_az = models.CharField(
        max_length=255,
        verbose_name='İzah (AZ)',
    )
    text_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='İzah (EN)',
    )
    text_ru = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='İzah (RU)',
    )
    video = models.FileField(
        upload_to='videos/trainings/curriculum/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=('mp4', 'webm', 'mov', 'ogg', 'mkv'),
                message='İcazə verilən formatlar: mp4, webm, mov, ogg, mkv.',
            )
        ],
        verbose_name='Önizləmə',
    )
    is_promo = models.BooleanField(
        default=False,
        verbose_name='Tanıtım videosu?',
        help_text='İşarələsəniz bu video detail-də tanıtım kimi görünəcək. Bir təlimdə yalnız biri.',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )

    class Meta:
        verbose_name = 'İcmal'
        verbose_name_plural = 'Kurs məzmunu — icmal'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.title_az or f'İcmal #{self.pk}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_promo and self.training_id:
            (
                TrainingCurriculumItem.objects
                .filter(training_id=self.training_id, is_promo=True)
                .exclude(pk=self.pk)
                .update(is_promo=False)
            )


class TrainingGalleryImage(models.Model):
    """Təlimdən kadrlar — Training edit-də inline."""

    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Təlim',
    )
    image = models.ImageField(
        upload_to='images/trainings/gallery/',
        verbose_name='Şəkil',
        help_text='Təlimdən kadr. Yükləyəndə avtomatik sıxılır.',
    )
    is_cover = models.BooleanField(
        default=False,
        verbose_name='Kart şəkli?',
        help_text='İşarələsəniz bu şəkil təlim kartında görünəcək. Bir təlimdə yalnız biri.',
    )

    class Meta:
        verbose_name = 'Təlimdən kadr'
        verbose_name_plural = 'Təlimdən kadrlar'
        ordering = ('id',)

    def __str__(self):
        return f'Qaleriya #{self.pk}' if self.pk else 'Qaleriya şəkli'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_cover and self.training_id:
            (
                TrainingGalleryImage.objects
                .filter(training_id=self.training_id, is_cover=True)
                .exclude(pk=self.pk)
                .update(is_cover=False)
            )
