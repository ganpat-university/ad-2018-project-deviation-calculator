# Generated by Django 3.0.6 on 2020-05-12 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devcal', '0002_remove_duser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='duser',
            name='phone',
            field=models.CharField(max_length=200, null=True),
        ),
    ]