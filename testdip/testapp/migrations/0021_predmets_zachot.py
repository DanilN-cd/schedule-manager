# Generated by Django 5.1.3 on 2025-02-25 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0020_remove_predmets_ind"),
    ]

    operations = [
        migrations.AddField(
            model_name="predmets",
            name="zachot",
            field=models.BooleanField(default=0),
        ),
    ]
