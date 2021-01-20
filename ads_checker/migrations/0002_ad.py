# Generated by Django 3.1.5 on 2021-01-16 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads_checker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=300)),
                ('price', models.FloatField()),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ads_checker.target')),
            ],
        ),
    ]
