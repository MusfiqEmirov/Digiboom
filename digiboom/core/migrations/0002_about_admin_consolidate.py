import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_about_phase1'),
    ]

    operations = [
        # Orphan sətirlər About FK-siz qala bilməz — təmizlə
        migrations.RunSQL(
            sql='DELETE FROM core_partner; DELETE FROM core_statisticitem;',
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RemoveField(
            model_name='partner',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='name_az',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='name_ru',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='show_on_about',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='url',
        ),
        migrations.AddField(
            model_name='partner',
            name='about',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='partners',
                to='core.about',
                verbose_name='Haqqımızda səhifəsi',
            ),
        ),
        migrations.AlterModelOptions(
            name='partner',
            options={
                'ordering': ('sort_order', 'id'),
                'verbose_name': 'Tərəfdaş loqosu',
                'verbose_name_plural': 'Tərəfdaş loqoları',
            },
        ),
        migrations.RemoveField(
            model_name='statisticitem',
            name='show_on_about',
        ),
        migrations.AddField(
            model_name='statisticitem',
            name='about',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='statistics',
                to='core.about',
                verbose_name='Haqqımızda səhifəsi',
            ),
        ),
        migrations.AlterField(
            model_name='statisticitem',
            name='show_on_home',
            field=models.BooleanField(
                default=True,
                help_text='Ana səhifənin statistika blokunda da göstərilsin.',
                verbose_name='Ana səhifədə?',
            ),
        ),
    ]
