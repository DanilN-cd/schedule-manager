# Generated by Django 5.1.3 on 2025-01-28 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0013_alter_predm_prepod_alter_prepods_predmet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predm',
            name='prepod',
        ),
    ]
