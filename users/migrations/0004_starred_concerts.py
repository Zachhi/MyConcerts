# Generated by Django 3.2.9 on 2021-11-17 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_spotifycred_spotify_notification_cred'),
    ]

    operations = [
        migrations.CreateModel(
            name='Starred_Concerts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('concert_id', models.CharField(max_length=100)),
            ],
        ),
    ]
