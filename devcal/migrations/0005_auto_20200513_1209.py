# Generated by Django 3.0.6 on 2020-05-13 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devcal', '0004_taskassign'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='enddate',
        ),
        migrations.AddField(
            model_name='task',
            name='duration',
            field=models.IntegerField(null=True),
        ),
    ]