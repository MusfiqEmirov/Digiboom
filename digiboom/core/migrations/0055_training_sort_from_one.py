from django.core.validators import MinValueValidator
from django.db import migrations, models


def renumber_from_one(apps, schema_editor):
    Training = apps.get_model('core', 'Training')
    TrainingCurriculumItem = apps.get_model('core', 'TrainingCurriculumItem')
    TrainingGalleryImage = apps.get_model('core', 'TrainingGalleryImage')

    for i, t in enumerate(Training.objects.order_by('sort_order', 'id'), start=1):
        if t.sort_order != i:
            Training.objects.filter(pk=t.pk).update(sort_order=i)

    for t in Training.objects.all():
        for i, item in enumerate(
            TrainingCurriculumItem.objects.filter(training_id=t.pk).order_by('sort_order', 'id'),
            start=1,
        ):
            if item.sort_order != i:
                TrainingCurriculumItem.objects.filter(pk=item.pk).update(sort_order=i)
        for i, img in enumerate(
            TrainingGalleryImage.objects.filter(training_id=t.pk).order_by('sort_order', 'id'),
            start=1,
        ):
            if img.sort_order != i:
                TrainingGalleryImage.objects.filter(pk=img.pk).update(sort_order=i)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_training_sort_help_texts'),
    ]

    operations = [
        migrations.RunPython(renumber_from_one, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='training',
            name='sort_order',
            field=models.PositiveIntegerField(
                db_index=True,
                default=1,
                help_text='1 = ilk. Kiçik rəqəm siyahıda əvvəl gəlir.',
                validators=[MinValueValidator(1)],
                verbose_name='Sıra',
            ),
        ),
        migrations.AlterField(
            model_name='trainingcurriculumitem',
            name='sort_order',
            field=models.PositiveIntegerField(
                db_index=True,
                default=1,
                help_text='1 = ilk. Detail icmal siyahısında başlıq yanında görünür (məs: 1. Giriş).',
                validators=[MinValueValidator(1)],
                verbose_name='Sıra',
            ),
        ),
        migrations.AlterField(
            model_name='traininggalleryimage',
            name='sort_order',
            field=models.PositiveIntegerField(
                db_index=True,
                default=1,
                help_text='1 = ilk. Kiçik rəqəm qalereyada əvvəl gəlir.',
                validators=[MinValueValidator(1)],
                verbose_name='Sıra',
            ),
        ),
    ]
