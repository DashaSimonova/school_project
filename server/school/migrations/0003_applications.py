# Generated by Django 3.2.8 on 2021-10-30 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_rename_parent_id_children_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.children')),
            ],
        ),
    ]
