import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_banner_labels_az'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about',
            name='intro_title_az',
        ),
        migrations.RemoveField(
            model_name='about',
            name='intro_title_en',
        ),
        migrations.RemoveField(
            model_name='about',
            name='intro_title_ru',
        ),
        migrations.RenameField(
            model_name='about',
            old_name='intro_text_az',
            new_name='mezmun_az',
        ),
        migrations.RenameField(
            model_name='about',
            old_name='intro_text_en',
            new_name='mezmun_en',
        ),
        migrations.RenameField(
            model_name='about',
            old_name='intro_text_ru',
            new_name='mezmun_ru',
        ),
        migrations.RenameField(
            model_name='about',
            old_name='home_teaser_az',
            new_name='ana_sehife_metn_az',
        ),
        migrations.RenameField(
            model_name='about',
            old_name='home_teaser_en',
            new_name='ana_sehife_metn_en',
        ),
        migrations.RenameField(
            model_name='about',
            old_name='home_teaser_ru',
            new_name='ana_sehife_metn_ru',
        ),
        migrations.AlterField(
            model_name='about',
            name='mezmun_az',
            field=models.TextField(
                help_text='Video yanındakı blok: başlıq və mətn bir yerdə (CKEditor).',
                validators=[django.core.validators.MaxLengthValidator(8000)],
                verbose_name='Məzmun (AZ)',
            ),
        ),
        migrations.AlterField(
            model_name='about',
            name='mezmun_en',
            field=models.TextField(
                blank=True,
                null=True,
                validators=[django.core.validators.MaxLengthValidator(8000)],
                verbose_name='Məzmun (EN)',
            ),
        ),
        migrations.AlterField(
            model_name='about',
            name='mezmun_ru',
            field=models.TextField(
                blank=True,
                null=True,
                validators=[django.core.validators.MaxLengthValidator(8000)],
                verbose_name='Məzmun (RU)',
            ),
        ),
        migrations.AlterField(
            model_name='about',
            name='ana_sehife_metn_az',
            field=models.TextField(
                help_text='Ana səhifədəki «Haqqımızda» bloku — bir mətn bloku (HTML).',
                validators=[django.core.validators.MaxLengthValidator(5000)],
                verbose_name='Ana səhifə mətni (AZ)',
            ),
        ),
        migrations.AlterField(
            model_name='about',
            name='ana_sehife_metn_en',
            field=models.TextField(
                blank=True,
                null=True,
                validators=[django.core.validators.MaxLengthValidator(5000)],
                verbose_name='Ana səhifə mətni (EN)',
            ),
        ),
        migrations.AlterField(
            model_name='about',
            name='ana_sehife_metn_ru',
            field=models.TextField(
                blank=True,
                null=True,
                validators=[django.core.validators.MaxLengthValidator(5000)],
                verbose_name='Ana səhifə mətni (RU)',
            ),
        ),
    ]
