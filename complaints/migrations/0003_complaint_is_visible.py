# Generated by Django 3.0.5 on 2022-10-08 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0002_auto_20221006_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='is_visible',
            field=models.BooleanField(default=False),
        ),
    ]