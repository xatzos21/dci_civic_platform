# Generated by Django 4.1.7 on 2023-05-08 09:44

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):
    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        ("the_archive", "0001_initial"),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name="bookmark",
        #     name="tags",
        #     field=taggit.managers.TaggableManager(
        #         help_text="A comma-separated list of tags.",
        #         through="taggit.TaggedItem",
        #         to="taggit.Tag",
        #         verbose_name="Tags",
        #     ),
        # ),
        migrations.RemoveField(
            model_name="upload",
            name="tags",
        ),
        migrations.AddField(
            model_name="upload",
            name="tags",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.RemoveField(
            model_name="bookmark",
            name="tags",
        ),
        migrations.AddField(
            model_name="bookmark",
            name="tags",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
