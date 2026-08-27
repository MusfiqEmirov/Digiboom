from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_training_one_popular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='sort_order',
            field=models.PositiveIntegerField(
                db_index=True,
                default=0,
                help_text='0 = ilk. Kiçik rəqəm siyahıda əvvəl gəlir.',
                verbose_name='Sıra',
            ),
        ),
        migrations.AlterField(
            model_name='trainingcurriculumitem',
            name='sort_order',
            field=models.PositiveIntegerField(
                db_index=True,
                default=0,
                help_text='Detail icmal siyahısında başlıq yanında görünür (məs: 1. Giriş).',
                verbose_name='Sıra',
            ),
        ),
        migrations.AlterField(
            model_name='traininggalleryimage',
            name='sort_order',
            field=models.PositiveIntegerField(
                db_index=True,
                default=0,
                help_text='0 = ilk. Kiçik rəqəm qalereyada əvvəl gəlir.',
                verbose_name='Sıra',
            ),
        ),
    ]
