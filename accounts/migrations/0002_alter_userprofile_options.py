# Generated by Django 4.0.1 on 2022-01-17 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربران'},
        ),
    ]
