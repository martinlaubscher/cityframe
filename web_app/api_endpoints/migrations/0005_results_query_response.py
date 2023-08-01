# Generated by Django 4.2.2 on 2023-07-30 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_endpoints', '0004_busyness_taxizones'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('taxi_zone', models.BigIntegerField()),
                ('prediction', models.FloatField()),
                ('bucket', models.IntegerField()),
                ('dt_iso', models.DateTimeField()),
            ],
            options={
                'db_table': 'cityframe"."Results',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('busyness', models.IntegerField()),
                ('trees', models.IntegerField()),
                ('time', models.CharField(max_length=255)),
                ('style', models.CharField(max_length=255)),
                ('query_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'cityframe"."user_query',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('zone_id', models.IntegerField()),
                ('zone', models.CharField(max_length=255)),
                ('dt_iso', models.CharField(max_length=255)),
                ('busyness', models.IntegerField()),
                ('trees', models.IntegerField()),
                ('style', models.IntegerField()),
                ('weather', models.JSONField()),
                ('rank', models.IntegerField()),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='api_endpoints.query')),
            ],
            options={
                'db_table': 'cityframe"."user_query_response',
            },
        ),
    ]
