# Generated by Django 5.0.2 on 2024-07-21 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0009_alter_share_news_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='follower',
            new_name='followers',
        ),
    ]
