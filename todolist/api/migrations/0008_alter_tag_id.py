# Generated by Django 5.0 on 2023-12-18 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_tag_value_alter_tag_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]