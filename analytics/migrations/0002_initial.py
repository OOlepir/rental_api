# Generated by Django 4.2.7 on 2025-04-16 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properties', '0001_initial'),
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewhistory',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property'),
        ),
    ]
