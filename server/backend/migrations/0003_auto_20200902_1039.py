# Generated by Django 3.1 on 2020-09-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20200902_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shorturlmodel',
            name='access_limit',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
