# Generated by Django 3.1.3 on 2023-10-08 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='user',
            new_name='username',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='user',
            new_name='username',
        ),
    ]