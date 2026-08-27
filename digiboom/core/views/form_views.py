"""
Site form APIs — save inbound submissions to admin models.

Endpoints (POST, multipart/form-data or form-urlencoded):
  /api/appeal/          → AppealContact (home + contact page)
  /api/consultation/    → ConsultationAppeal (service contact modal)
  /api/package-order/   → PackageOrder
  /api/training-order/  → TrainingOrder (pre-payment record)
  /api/review/          → Review (is_active=False until admin approves)
"""

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core.models import (
    AppealContact,
    ConsultationAppeal,
    Package,
    PackageOrder,
    Review,
    Service,
    Training,
    TrainingOrder,
)


def _json_error(message, status=400, errors=None):
    payload = {'ok': False, 'message': message}
    if errors:
        payload['errors'] = errors
    return JsonResponse(payload, status=status)


def _json_ok(message='OK'):
    return JsonResponse({'ok': True, 'message': message})


def _clean(value, max_len=None):
    text = (value or '').strip()
    if max_len:
        return text[:max_len]
    return text


def _require_fields(data, *names):
    missing = [n for n in names if not _clean(data.get(n))]
    return missing


@require_POST
def api_appeal_contact(request):
    """General contact forms → AppealContact."""
    data = request.POST
    missing = _require_fields(data, 'name', 'phone', 'message')
    if missing:
        return _json_error('Zəhmət olmasa mütləq sahələri doldurun.', errors=missing)

    AppealContact.objects.create(
        full_name=_clean(data.get('name'), 120),
        phone=_clean(data.get('phone'), 40),
        email=_clean(data.get('email'), 254),
        message=_clean(data.get('message')),
    )
    return _json_ok('Müraciətiniz qəbul olundu.')


@require_POST
def api_consultation_appeal(request):
    """Service-detail contact modal → ConsultationAppeal."""
    data = request.POST
    missing = _require_fields(data, 'name', 'phone', 'message')
    if missing:
        return _json_error('Zəhmət olmasa mütləq sahələri doldurun.', errors=missing)

    service = None
    service_id = _clean(data.get('service_id'))
    service_name = _clean(data.get('service') or data.get('service_name'), 160)
    if service_id.isdigit():
        service = Service.objects.filter(pk=int(service_id), is_active=True).first()
        if service:
            service_name = service.name_az or service_name

    ConsultationAppeal.objects.create(
        full_name=_clean(data.get('name'), 120),
        phone=_clean(data.get('phone'), 40),
        email=_clean(data.get('email'), 254),
        message=_clean(data.get('message')),
        service=service,
        service_name=service_name,
    )
    return _json_ok('Konsultasiya müraciətiniz qəbul olundu.')


@require_POST
def api_package_order(request):
    """Package order modal → PackageOrder."""
    data = request.POST
    missing = _require_fields(data, 'name', 'phone', 'email')
    if missing:
        return _json_error('Zəhmət olmasa mütləq sahələri doldurun.', errors=missing)

    package = None
    package_id = _clean(data.get('package_id'))
    package_name = _clean(data.get('package') or data.get('package_name'), 160)
    if package_id.isdigit():
        package = Package.objects.filter(pk=int(package_id), is_active=True).first()
        if package:
            package_name = package.name_az or package_name

    if not package_name:
        return _json_error('Paket seçilməyib.')

    PackageOrder.objects.create(
        full_name=_clean(data.get('name'), 120),
        phone=_clean(data.get('phone'), 40),
        email=_clean(data.get('email'), 254),
        package=package,
        package_name=package_name,
        message=_clean(data.get('message')),
    )
    return _json_ok('Sifarişiniz qəbul olundu.')


@require_POST
def api_training_order(request):
    """Training detail form → TrainingOrder (before payment gateway)."""
    data = request.POST
    missing = _require_fields(data, 'name', 'phone', 'gmail')
    # Also accept email field name
    gmail = _clean(data.get('gmail') or data.get('email'), 254)
    if not gmail:
        missing = list(set(missing + ['gmail']))
    if missing:
        return _json_error('Zəhmət olmasa mütləq sahələri doldurun.', errors=missing)

    if not gmail.lower().endswith('@gmail.com'):
        return _json_error('Yalnız @gmail.com ünvanı qəbul olunur.')

    training = None
    training_id = _clean(data.get('training_id'))
    training_name = _clean(data.get('training') or data.get('training_name'), 160)
    if training_id.isdigit():
        training = Training.objects.filter(pk=int(training_id), is_active=True).first()
        if training:
            training_name = training.name_az or training_name

    TrainingOrder.objects.create(
        training=training,
        training_name=training_name,
        full_name=_clean(data.get('name'), 120),
        phone=_clean(data.get('phone'), 40),
        gmail=gmail,
    )
    return _json_ok('Sifarişiniz qəbul olundu.')


@require_POST
def api_review(request):
    """Review modal → Review (pending admin approval)."""
    data = request.POST
    message = _clean(data.get('message') or data.get('text') or data.get('review'))
    missing = _require_fields(data, 'name', 'rating')
    if not message:
        missing = list(set(missing + ['message']))
    if missing:
        return _json_error('Zəhmət olmasa mütləq sahələri doldurun.', errors=missing)

    try:
        rating = int(data.get('rating') or 0)
    except (TypeError, ValueError):
        rating = 0
    if rating < 1 or rating > 5:
        return _json_error('Reytinq 1–5 arasında olmalıdır.')

    category = _clean(data.get('category'))
    category_label = _clean(data.get('categoryLabel') or data.get('category_label'), 200)
    category_type = Review.CategoryType.OTHER
    service = None
    training = None

    # Values: service:<id>, training:<id>, consultation, other / diger / konsultasiya
    if category in ('konsultasiya', 'consultation'):
        category_type = Review.CategoryType.CONSULTATION
        category_label = category_label or 'Konsultasiya'
    elif category in ('diger', 'other', 'digər'):
        category_type = Review.CategoryType.OTHER
        category_label = category_label or 'Digər'
    elif category.startswith('service:'):
        category_type = Review.CategoryType.SERVICE
        pk = category.split(':', 1)[1]
        if pk.isdigit():
            service = Service.objects.filter(pk=int(pk), is_active=True).first()
            if service:
                category_label = service.name_az
    elif category.startswith('training:'):
        category_type = Review.CategoryType.TRAINING
        pk = category.split(':', 1)[1]
        if pk.isdigit():
            training = Training.objects.filter(pk=int(pk), is_active=True).first()
            if training:
                category_label = training.name_az
    elif category.startswith('xidmet') or category.startswith('service'):
        category_type = Review.CategoryType.SERVICE
    elif category.startswith('telim') or category.startswith('training'):
        category_type = Review.CategoryType.TRAINING

    review = Review(
        name=_clean(data.get('name'), 120),
        category_type=category_type,
        service=service,
        training=training,
        category_label=category_label,
        rating=rating,
        message=message,
        is_active=False,
    )
    image = request.FILES.get('image') or request.FILES.get('photo')
    if image:
        review.image = image
    review.save()
    return _json_ok('Rəyiniz qəbul olundu. Təsdiqdən sonra dərc olunacaq.')
