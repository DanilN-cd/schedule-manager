# Generated by Django 5.1.3 on 2025-01-26 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0011_predmets_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predmets',
            name='prepod',
        ),
        migrations.CreateModel(
            name='PredM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('prepod', models.ManyToManyField(blank=True, null=True, to='testapp.prepods')),
            ],
        ),
        migrations.AlterField(
            model_name='predmets',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.predm'),
        ),
    ]
