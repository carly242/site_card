# Generated by Django 5.0.4 on 2024-07-05 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_user_entreprise'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_views',
            field=models.IntegerField(default=0),
        ),
    ]