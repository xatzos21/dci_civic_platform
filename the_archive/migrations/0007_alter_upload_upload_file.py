# Generated by Django 4.1.7 on 2023-05-05 19:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("the_archive", "0006_alter_upload_upload_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="upload",
            name="upload_file",
            field=models.FileField(upload_to=""),
        ),
    ]