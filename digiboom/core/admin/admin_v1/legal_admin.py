"""
Legal content — singleton admin.

Terms of Use and Privacy Policy in one record. Banner/motto live under
«Səhifə bannerləri» (page=terms / page=privacy). Front pages: /terms/, /privacy/.
"""

from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from core.models import LegalContent

from .admin_help import LEGAL_HELP, AdminPageHelpMixin

_TERMS_DESC = (
    'Admin-də Şərtlər mətni yaradılsa/doldurulsa — footer-də «Şərtlər» keçidi görünəcək '
    'və /terms/ səhifəsi açılacaq. Heç nə yaradılmasa və ya mətn boş qalsa — '
    'footer-də «Şərtlər» sözü olmaz, səhifə də göstərilməz.'
)
_PRIVACY_DESC = (
    'Admin-də Məxfilik mətni yaradılsa/doldurulsa — footer-də «Məxfilik» keçidi görünəcək '
    'və /privacy/ səhifəsi açılacaq. Heç nə yaradılmasa və ya mətn boş qalsa — '
    'footer-də «Məxfilik» sözü olmaz, səhifə də göstərilməz.'
)


class LegalContentAdminForm(forms.ModelForm):
    """CKEditor widgets for all six legal text fields."""

    class Meta:
        model = LegalContent
        fields = '__all__'
        widgets = {
            'terms_az': CKEditorWidget(),
            'terms_en': CKEditorWidget(),
            'terms_ru': CKEditorWidget(),
            'privacy_az': CKEditorWidget(),
            'privacy_en': CKEditorWidget(),
            'privacy_ru': CKEditorWidget(),
        }


@admin.register(LegalContent)
class LegalContentAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    """
    Terms + Privacy in one place.
    Add button is enabled only when no record exists yet.
    """

    admin_page_help = LEGAL_HELP
    form = LegalContentAdminForm
    list_display = ('__str__', 'terms_filled', 'privacy_filled')
    fieldsets = (
        ('İstifadə şərtləri', {
            'fields': ('terms_az', 'terms_en', 'terms_ru'),
            'classes': ('wide',),
            'description': _TERMS_DESC,
        }),
        ('Məxfilik siyasəti', {
            'fields': ('privacy_az', 'privacy_en', 'privacy_ru'),
            'classes': ('wide',),
            'description': _PRIVACY_DESC,
        }),
    )

    @admin.display(boolean=True, description='Şərtlər dolu?')
    def terms_filled(self, obj):
        return obj.has_terms

    @admin.display(boolean=True, description='Məxfilik dolu?')
    def privacy_filled(self, obj):
        return obj.has_privacy

    def has_add_permission(self, request):
        # Singleton: only one LegalContent record.
        if LegalContent.objects.exists():
            return False
        return super().has_add_permission(request)
