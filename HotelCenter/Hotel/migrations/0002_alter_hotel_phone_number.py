# Generated by Django 4.0.3 on 2023-04-21 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
