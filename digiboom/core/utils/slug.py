from django.utils.text import slugify


def unique_slug_for(instance, source_text, slug_field='slug'):
    """Averta-style: slug from source text (adətən name_az), unique within the same model."""
    base = slugify(source_text) or 'item'
    Model = instance.__class__
    slug = base
    n = 2
    qs = Model.objects.all()
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)
    while qs.filter(**{slug_field: slug}).exists():
        slug = f'{base}-{n}'
        n += 1
    return slug
