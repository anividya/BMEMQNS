# Generated by Django 4.1.5 on 2023-02-05 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASSETS', '0018_alter_workbook_downtime_alter_workbook_rsndtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workbook',
            name='downtime',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='workbook',
            name='rsndtime',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
