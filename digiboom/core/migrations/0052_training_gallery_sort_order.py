from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_projectservicetag_link_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='traininggalleryimage',
            name='sort_order',
            field=models.PositiveIntegerField(
                db_index=True,
                default=0,
                help_text='0 = ilk. Frontend-də bu rəqəm görünür.',
                verbose_name='Sıra',
            ),
        ),
        migrations.AlterModelOptions(
            name='traininggalleryimage',
            options={
                'ordering': ('sort_order', 'id'),
                'verbose_name': 'Təlimdən kadr',
                'verbose_name_plural': 'Təlimdən kadrlar',
            },
        ),
        migrations.AlterField(
            model_name='traininggalleryimage',
            name='is_cover',
            field=models.BooleanField(
                default=False,
                help_text=(
                    'İşarələsəniz bu şəkil təlim kartında görünəcək (tanıtım videosu kimi birini seçin). '
                    'Seçilməzsə ilk kadr və ya tanıtım videosunun ilk kadrı istifadə olunur. '
                    'Bir təlimdə yalnız biri.'
                ),
                verbose_name='Kart şəkli?',
            ),
        ),
        migrations.AlterField(
            model_name='trainingcurriculumitem',
            name='sort_order',
            field=models.PositiveIntegerField(
                db_index=True,
                default=0,
                help_text='0 = ilk. Frontend-də bu rəqəm görünür.',
                verbose_name='Sıra',
            ),
        ),
    ]
