# Generated by Django 3.2.25 on 2024-09-19 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20240919_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounthistory',
            name='account',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='core.account'),
        ),
    ]
