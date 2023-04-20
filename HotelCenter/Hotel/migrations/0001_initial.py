

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('name', models.CharField(max_length=70)),
                ('address', models.CharField(max_length=70)),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('floor_count', models.IntegerField(blank=True, null=True)),
                ('country', models.CharField(max_length=55)),
                ('city', models.CharField(max_length=55)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('check_in', models.TimeField(blank=True, null=True)),
                ('check_out', models.TimeField(blank=True, null=True)),
                ('rate', models.FloatField(default=2.5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='HotelManager', to=settings.AUTH_USER_MODEL)),

            ],
            options={
                'ordering': ['-rate'],
            },
        ),
        migrations.CreateModel(
            name='HotelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='hotel')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='images', to='Hotel.hotel')),
            ],
        ),


    ]
