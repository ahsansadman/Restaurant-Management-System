# Generated by Django 3.1.7 on 2021-04-16 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20210416_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catagory',
            name='cooking_station',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='cooking_station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='restaurant.cookingstation', verbose_name='Cooking Station'),
        ),
    ]
