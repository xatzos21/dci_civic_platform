# Generated by Django 4.1.7 on 2023-05-10 08:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("the_archive", "0002_delete_location_alter_upload_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="url",
            field=models.URLField(default="https://en.wikipedia.org/wiki/Parmenides"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="upload",
            name="file",
            field=models.CharField(max_length=250, null=True),
        ),
    ]
