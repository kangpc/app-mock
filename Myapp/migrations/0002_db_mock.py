# Generated by Django 2.2 on 2021-12-05 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_mock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('state', models.BooleanField(default=False)),
                ('project_id', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]
