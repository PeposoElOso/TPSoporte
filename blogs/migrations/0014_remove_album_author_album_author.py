# Generated by Django 4.2.5 on 2023-10-19 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0013_remove_post_overview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='author',
        ),
        migrations.AddField(
            model_name='album',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blogs.artist'),
            preserve_default=False,
        ),
    ]
