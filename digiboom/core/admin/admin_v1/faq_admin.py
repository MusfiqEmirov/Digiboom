"""
FAQ (frequently asked questions).

Level 1 (FAQ) + level 2 answers (FAQSubItem inline).
JS: admin_faq_params_order.js — moves the «Parametrlər» fieldset after the inline.
"""

from django import forms
from django.contrib import admin
from django.db import models

from core.models import FAQ, FAQSubItem

from .admin_help import FAQ_HELP, AdminPageHelpMixin


class FAQSubItemInline(admin.TabularInline):
    """
    Level-2 question (optional) + answer.
    If title is empty, only the answer is shown (direct-answer mode).
    """

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
class FAQAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    """Home page FAQ accordion — level 1 + sub-questions."""

    admin_page_help = FAQ_HELP
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
        # admin_help.css — AdminPageHelpMixin.media property ilə gəlir
        js = ('js/admin_faq_params_order.js',)

    def get_queryset(self, request):
        """Annotates level-2 count (for list ordering)."""
        qs = super().get_queryset(request)
        return qs.annotate(_sub_count=models.Count('sub_items'))

    @admin.display(description='2-ci dərəcə', ordering='_sub_count')
    def sub_count(self, obj):
        """Sub-question count in the list view."""
        return getattr(obj, '_sub_count', obj.sub_items.count())
