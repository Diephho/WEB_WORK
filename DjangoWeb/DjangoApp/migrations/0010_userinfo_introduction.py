# Generated by Django 5.0.3 on 2024-04-29 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjangoApp', '0009_alter_userinfo_firstname_alter_userinfo_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='introduction',
            field=models.CharField(max_length=200, null=True),
        ),
    ]