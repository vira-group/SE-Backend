# Generated by Django 4.0.3 on 2023-05-14 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0002_alter_roomimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomimage',
            name='image',
            field=models.ImageField(blank=True, default='/test_img/default.jpg', null=True, upload_to='test_img/'),
        ),
    ]
