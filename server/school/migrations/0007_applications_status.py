# Generated by Django 3.2.8 on 2021-11-02 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_children_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
