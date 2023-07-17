# Generated by Django 4.2.2 on 2023-07-17 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_endpoints', '0004_alter_weatherfc_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weatherfc',
            name='pop',
        ),
        migrations.AlterField(
            model_name='weatherfc',
            name='rain_1h',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherfc',
            name='snow_1h',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherfc',
            name='wind_gust',
            field=models.FloatField(),
        ),
        migrations.AlterModelTable(
            name='weatherfc',
            table='cityframe.weather_fc',
        ),
    ]
