from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import escape


def _link_title(link) -> str:
    title = getattr(link, 'title_az', None) or getattr(link, 'title', None) or ''
    return (title or '').strip() or 'Material'


def send_training_order_drive_links(order) -> None:
    """Təlim access_links-lərini sifarişçinin Gmail-inə göndərir."""
    to_email = (order.gmail or '').strip()
    if not to_email:
        raise ValueError('Gmail ünvanı yoxdur.')

    links = order.get_access_links()
    if not links:
        raise ValueError(
            'Bu təlimdə göndəriləcək link yoxdur '
            '(Təlim → ödənişdən sonra göndərilən linklər).'
        )

    training = (order.training_name or '').strip() or 'təlim'
    site_name = getattr(settings, 'SITE_NAME', 'DigiBoom')
    from_email = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER
    safe_name = escape(order.full_name)
    safe_training = escape(training)
    safe_site = escape(site_name)

    lines = []
    for link in links:
        title = _link_title(link)
        lines.append(f'• {title}: {link.url}')

    links_text = '\n'.join(lines)
    subject = f'{site_name} — {training} materialları'
    text_body = (
        f'Salam, {order.full_name}!\n\n'
        f'«{training}» təlimi üçün material linkləriniz:\n\n'
        f'{links_text}\n\n'
        f'Uğurlar!\n'
        f'{site_name}'
    )
    html_items = ''.join(
        f'<li><strong>{escape(_link_title(link))}:</strong> '
        f'<a href="{escape(link.url)}">{escape(link.url)}</a></li>'
        for link in links
    )
    html_body = (
        f'<p>Salam, {safe_name}!</p>'
        f'<p>«{safe_training}» təlimi üçün material linkləriniz:</p>'
        f'<ul>{html_items}</ul>'
        f'<p>Uğurlar!<br>{safe_site}</p>'
    )

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[to_email],
    )
    message.attach_alternative(html_body, 'text/html')
    message.send(fail_silently=False)
