# Generated by Django 4.1.5 on 2023-01-12 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASSETS', '0004_alter_workbook_action_alter_workbook_eng_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workbook',
            name='reporter',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
