# Generated by Django 4.2.2 on 2023-07-24 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_endpoints', '0003_alter_weathercurrent_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Busyness',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('prediction', models.FloatField()),
                ('bucket', models.IntegerField()),
            ],
            options={
                'db_table': 'cityframe"."Results',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TaxiZones',
            fields=[
                ('id', models.IntegerField(db_column='location_id', primary_key=True, serialize=False)),
                ('zone', models.CharField(max_length=100)),
                ('trees', models.IntegerField()),
                ('neo_georgian', models.IntegerField(db_column='neo-Georgian')),
                ('greek_revival', models.IntegerField(db_column='Greek Revival')),
                ('romanesque_revival', models.IntegerField(db_column='Romanesque Revival')),
                ('neo_grec', models.IntegerField(db_column='neo-Grec')),
                ('renaissance_revival', models.IntegerField(db_column='Renaissance Revival')),
                ('beaux_arts', models.IntegerField(db_column='Beaux-Arts')),
                ('queen_anne', models.IntegerField(db_column='Queen Anne')),
                ('italianate', models.IntegerField(db_column='Italianate')),
                ('federal', models.IntegerField(db_column='Federal')),
                ('neo_renaissance', models.IntegerField(db_column='neo-Renaissance')),
            ],
            options={
                'db_table': 'cityframe"."taxi_zones',
                'managed': False,
            },
        ),
    ]
