# Generated by Django 3.1.7 on 2021-03-20 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writecloud', '0007_auto_20210320_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='media/images/default-avatar.png', upload_to='images/'),
        ),
    ]
