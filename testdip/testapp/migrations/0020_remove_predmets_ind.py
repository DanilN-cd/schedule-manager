# Generated by Django 5.1.3 on 2025-02-18 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0019_alter_schedule_cabinet_alter_schedule_subject"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="predmets",
            name="ind",
        ),
    ]
