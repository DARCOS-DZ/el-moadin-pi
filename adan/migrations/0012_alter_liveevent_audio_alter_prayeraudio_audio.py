# Generated by Django 4.1.4 on 2023-01-19 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("adan", "0011_alter_liveevent_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="liveevent",
            name="audio",
            field=models.FileField(upload_to="live_event"),
        ),
        migrations.AlterField(
            model_name="prayeraudio",
            name="audio",
            field=models.FileField(upload_to="prayer_audio"),
        ),
    ]
