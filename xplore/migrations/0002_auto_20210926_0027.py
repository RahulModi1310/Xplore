# Generated by Django 3.2.7 on 2021-09-26 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xplore', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='courseName',
            new_name='coursename',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='coursePlatform',
            new_name='courseplatform',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='courseUrl',
            new_name='courseurl',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='imageUrl',
            new_name='imageurl',
        ),
    ]