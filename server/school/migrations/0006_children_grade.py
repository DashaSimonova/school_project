# Generated by Django 3.2.8 on 2021-11-01 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_alter_classes_letter'),
    ]

    operations = [
        migrations.AddField(
            model_name='children',
            name='grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.classes'),
        ),
    ]