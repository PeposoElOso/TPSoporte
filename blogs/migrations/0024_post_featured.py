# Generated by Django 4.2.5 on 2023-10-26 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0023_alter_post_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured',
            field=models.FloatField(default=0),
        ),
    ]
