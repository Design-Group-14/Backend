# Generated by Django 5.1.6 on 2025-02-24 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='country',
        ),
        migrations.RemoveField(
            model_name='user',
            name='course_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='user',
            name='graduation_year',
        ),
        migrations.RemoveField(
            model_name='user',
            name='profile_picture_url',
        ),
        migrations.RemoveField(
            model_name='user',
            name='updated_at',
        ),
    ]
