# Generated by Django 4.2.5 on 2023-09-28 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_alter_category_options_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='overview',
            field=models.TextField(max_length=80),
        ),
    ]
