# Generated by Django 4.1.4 on 2023-02-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("adan", "0012_alter_liveevent_audio_alter_prayeraudio_audio"),
    ]

    operations = [
        migrations.AddField(
            model_name="liveevent",
            name="downloaded",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="prayeraudio",
            name="downloaded",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="prayerevent",
            name="downloaded",
            field=models.BooleanField(default=False),
        ),
    ]
