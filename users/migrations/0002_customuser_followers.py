# Generated by Django 4.1.7 on 2023-05-23 12:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="followers",
            field=models.ManyToManyField(
                related_name="following", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
