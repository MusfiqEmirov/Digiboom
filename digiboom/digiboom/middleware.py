from django.utils import translation
from django.conf import settings


class CustomLocaleMiddleware:
    """Force active language from session (Averta pattern)."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.supported = {code for code, _ in settings.LANGUAGES}

    def __call__(self, request):
        admin_url = (settings.ADMIN_URL or 'admin/').strip('/')
        admin_prefix = f'/{admin_url}'
        if request.path.startswith(admin_prefix):
            admin_lang = (
                request.session.get('admin_language')
                or getattr(settings, 'ADMIN_LANGUAGE_CODE', 'az')
            )
            if admin_lang not in self.supported:
                admin_lang = getattr(settings, 'ADMIN_LANGUAGE_CODE', 'az')
            translation.activate(admin_lang)
            request.LANGUAGE_CODE = admin_lang
            return self.get_response(request)

        language = request.session.get('django_language') or request.session.get('language')
        if language and language in self.supported:
            translation.activate(language)
            request.LANGUAGE_CODE = language
        else:
            site_default = getattr(settings, 'LANGUAGE_CODE', 'az')
            if site_default not in self.supported:
                site_default = 'az'
            translation.activate(site_default)
            request.LANGUAGE_CODE = site_default

        return self.get_response(request)
