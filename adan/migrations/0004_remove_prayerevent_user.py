# Generated by Django 4.1.4 on 2022-12-20 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("adan", "0003_remove_topic_user_delete_mosque_delete_topic"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="prayerevent",
            name="user",
        ),
    ]
