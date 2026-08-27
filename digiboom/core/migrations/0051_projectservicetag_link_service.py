# Generated manually for ProjectServiceTag → Service FK

from django.db import migrations, models
import django.db.models.deletion


def clear_old_tags(apps, schema_editor):
    ProjectServiceTag = apps.get_model('core', 'ProjectServiceTag')
    ProjectServiceTag.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_legal_content_help_text'),
    ]

    operations = [
        migrations.RunPython(clear_old_tags, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='projectservicetag',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='projectservicetag',
            name='name_az',
        ),
        migrations.RemoveField(
            model_name='projectservicetag',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='projectservicetag',
            name='name_ru',
        ),
        migrations.AddField(
            model_name='projectservicetag',
            name='service',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='project_tags',
                to='core.service',
                verbose_name='Xidmət',
                help_text='Mövcud xidmətlərdən seçin. Eyni xidməti bir layihəyə iki dəfə əlavə etmək olmaz.',
            ),
        ),
        migrations.AlterModelOptions(
            name='projectservicetag',
            options={
                'ordering': ('id',),
                'verbose_name': 'Daxil olan xidmət',
                'verbose_name_plural': 'Daxil olan xidmətlər',
            },
        ),
        migrations.AlterUniqueTogether(
            name='projectservicetag',
            unique_together={('project', 'service')},
        ),
    ]
