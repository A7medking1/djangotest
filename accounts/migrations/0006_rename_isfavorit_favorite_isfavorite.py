# Generated by Django 4.1.3 on 2022-11-11 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_rename_favorire_favorite'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='isFavorit',
            new_name='isFavorite',
        ),
    ]