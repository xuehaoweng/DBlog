# Generated by Django 4.1.7 on 2023-05-12 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='accesstimeoutlogs',
            table='access_timeout_logs',
        ),
        migrations.AlterModelTable(
            name='oplogs',
            table='op_logs',
        ),
    ]