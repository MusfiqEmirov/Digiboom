"""
FAQ — home page accordion.

Special rules:
- FAQ = level-1 question; FAQSubItem = level-2 (optional) + answer.
- If SubItem title is empty, the front shows only the answer (direct answer).
- Admin «Parametrlər» fieldset is repositioned after the inline via JS.
"""

from django.db import models


class FAQ(models.Model):
    """
    Frequently asked questions — home page accordion.

    Level-1 question + table below (FAQSubItem):
    - With level-2: title + answer (e.g. SEO / design / IT)
    - Without level-2: empty title, answer only (direct answer)
    """

    question_az = models.CharField(
        max_length=500,
        verbose_name='1-ci dərəcəli sual (AZ)',
        help_text='Ana accordion — məs. «Digiboom nə şirkətdir?»',
    )
    question_en = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='1-ci dərəcəli sual (EN)',
    )
    question_ru = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='1-ci dərəcəli sual (RU)',
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
    )

    class Meta:
        verbose_name = 'Tez-tez verilən sual'
        verbose_name_plural = 'Tez-tez verilən suallar'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.question_az or f'Sual #{self.pk}'


class FAQSubItem(models.Model):
    """Level-2 question (optional) + answer."""

    faq = models.ForeignKey(
        FAQ,
        on_delete=models.CASCADE,
        related_name='sub_items',
        verbose_name='1-ci dərəcəli sual',
    )
    title_az = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='2-ci dərəcəli sual (AZ)',
        help_text=(
            'Varsa yazın — məs. «Digiboom SEO olaraq?». '
            'Yoxdursa boş saxlayın, yalnız cavab doldurun.'
        ),
    )
    title_en = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='2-ci dərəcəli sual (EN)',
    )
    title_ru = models.CharField(
        max_length=500,
        blank=True,
        default='',
        verbose_name='2-ci dərəcəli sual (RU)',
    )
    answer_az = models.TextField(
        verbose_name='Cavab (AZ)',
    )
    answer_en = models.TextField(
        blank=True,
        default='',
        verbose_name='Cavab (EN)',
    )
    answer_ru = models.TextField(
        blank=True,
        default='',
        verbose_name='Cavab (RU)',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )

    class Meta:
        verbose_name = '2-ci dərəcəli sual və cavab'
        verbose_name_plural = '2-ci dərəcəli suallar və cavablar'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.title_az or (self.answer_az[:60] if self.answer_az else f'Alt #{self.pk}')
