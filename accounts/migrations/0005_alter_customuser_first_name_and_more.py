# Generated by Django 4.2.10 on 2024-02-14 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
    ]
