# Generated by Django 4.2.5 on 2023-10-20 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0015_alter_album_author_alter_album_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='album',
        ),
        migrations.AddField(
            model_name='post',
            name='album',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='blogs.album'),
            preserve_default=False,
        ),
    ]