# Generated by Django 4.1.4 on 2023-03-06 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("adan", "0014_prayerevent_scheduled"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="prayerevent",
            name="scheduled",
        ),
    ]