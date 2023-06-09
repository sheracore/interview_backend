# Generated by Django 3.2.19 on 2023-06-06 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import skyloov.core.files.utilities


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, default='', max_length=100, verbose_name='Title')),
                ('file', models.FileField(upload_to=skyloov.core.files.utilities.get_document_path, validators=[skyloov.core.files.utilities.validate_file], verbose_name='File')),
                ('size', models.IntegerField(default=0, verbose_name='File Size')),
                ('type', models.IntegerField(choices=[(1, 'Voice'), (2, 'Image'), (3, 'Movie'), (4, 'Pdf'), (5, 'Presentation'), (6, 'Spreadsheet'), (7, 'Word'), (8, 'Compress'), (9, 'Text'), (10, 'Css'), (11, 'Svg'), (12, 'Json'), (13, 'Ipa'), (14, 'Apk')], verbose_name='Type')),
                ('blur_hash', models.CharField(blank=True, max_length=40, null=True, verbose_name='Blur hash')),
                ('duration', models.PositiveIntegerField(default=0, verbose_name='Duration')),
                ('key', models.CharField(blank=True, max_length=16, null=True, verbose_name='Key')),
                ('status', models.IntegerField(choices=[(1, 'Waiting'), (2, 'Running'), (3, 'Finished'), (4, 'Failed'), (5, 'Timeout')], default=1, verbose_name='Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'File model',
                'verbose_name_plural': 'Files',
            },
        ),
    ]
