# Generated by Django 4.2.4 on 2024-01-04 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogpost', '0021_alter_post_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
    ]
