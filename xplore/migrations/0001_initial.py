# Generated by Django 3.2.7 on 2021-09-25 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseName', models.CharField(max_length=50, null=True)),
                ('coursePlatform', models.CharField(max_length=50, null=True)),
                ('imageUrl', models.TextField(null=True)),
                ('courseUrl', models.TextField(null=True)),
                ('rating', models.IntegerField(null=True)),
                ('details', models.TextField(null=True)),
                ('status', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, null=True)),
                ('password', models.CharField(max_length=65, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('accountActive', models.BooleanField(null=True)),
            ],
        ),
    ]
