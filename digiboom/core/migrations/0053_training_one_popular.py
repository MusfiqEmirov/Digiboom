# Generated manually — Training.is_popular help text

from django.db import migrations, models


def keep_one_popular(apps, schema_editor):
    Training = apps.get_model('core', 'Training')
    popular = list(Training.objects.filter(is_popular=True).order_by('sort_order', 'id'))
    if len(popular) <= 1:
        return
    keep_id = popular[0].pk
    Training.objects.filter(is_popular=True).exclude(pk=keep_id).update(is_popular=False)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_training_gallery_sort_order'),
    ]

    operations = [
        migrations.RunPython(keep_one_popular, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='training',
            name='is_popular',
            field=models.BooleanField(
                default=False,
                help_text='Spotlight / «Ən populyar» işarəsi. Eyni anda yalnız bir təlim seçilə bilər.',
                verbose_name='Ən populyar?',
            ),
        ),
    ]
