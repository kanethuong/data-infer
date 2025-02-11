# Generated by Django 5.0.7 on 2024-07-15 05:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=255)),
                ('data_type', models.CharField(max_length=255)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.uploadedfile')),
            ],
        ),
        migrations.DeleteModel(
            name='InferredDataType',
        ),
    ]
