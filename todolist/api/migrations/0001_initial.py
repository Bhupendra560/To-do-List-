# Generated by Django 5.0 on 2023-12-09 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                (
                    'id',
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('WORKING', 'Working'), ('DONE', 'Done'), ('OVERDUE', 'Overdue')], default='OPEN', max_length=10)),
                ('tags', models.ManyToManyField(blank=True, to='api.tag')),
            ],
            options={
                'db_table': 'tbltask',
            },
        ),
    ]
