# Generated by Django 4.1 on 2022-09-03 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pipingsite', '0007_alter_cml_require_thickness_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test_point',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]
