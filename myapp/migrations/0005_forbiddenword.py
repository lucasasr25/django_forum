# Generated by Django 4.2.4 on 2023-08-11 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_author_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForbiddenWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
