# Generated by Django 3.1.7 on 2021-04-16 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='photo',
        ),
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='photos/default-user-avatar.png', upload_to='User Photos/', verbose_name='Picture'),
        ),
    ]
