# Generated by Django 4.1.5 on 2023-03-26 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reply',
            field=models.BooleanField(default=False),
        ),
    ]