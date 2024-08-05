# Generated by Django 5.0.7 on 2024-08-04 14:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
                ('family', models.CharField(max_length=350)),
                ('gender', models.CharField(choices=[('زن', 'زن'), ('مرد', 'مرد')], max_length=1000)),
                ('birthday', models.DateField()),
                ('city', models.CharField(max_length=1000)),
                ('participate_type', models.CharField(choices=[('برنامه نویسی', 'برنامه نویسی'), ('بازاریابی', 'بازاریابی'), ('ادیت', 'ادیت')], max_length=1000)),
                ('text', models.TextField()),
                ('info_card', models.ImageField(upload_to='info/cards/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]