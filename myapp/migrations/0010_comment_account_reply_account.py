# Generated by Django 4.2.4 on 2023-08-12 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_rename_acount_post_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='account',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='reply',
            name='account',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
