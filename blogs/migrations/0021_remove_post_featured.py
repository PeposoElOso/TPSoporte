# Generated by Django 4.2.5 on 2023-10-26 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0020_post_lecturas_alter_post_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='featured',
        ),
    ]
