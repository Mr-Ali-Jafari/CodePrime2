# Generated by Django 5.0.7 on 2024-08-06 11:08

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrimeCast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('banner', models.ImageField(upload_to='prime_cast/banner/%Y/')),
                ('desc', ckeditor.fields.RichTextField()),
                ('voice', models.FileField(upload_to='prime_cast/voice/%Y/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
