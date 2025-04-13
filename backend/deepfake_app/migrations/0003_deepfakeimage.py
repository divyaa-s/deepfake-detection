# Generated by Django 5.1.7 on 2025-04-13 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deepfake_app', '0002_auto_20250311_2208'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeepfakeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/')),
                ('prediction', models.CharField(max_length=10)),
                ('confidence', models.FloatField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
