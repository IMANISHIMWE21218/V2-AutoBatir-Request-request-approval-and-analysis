# Generated by Django 3.1.13 on 2023-08-31 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AutoBatirApp', '0003_auto_20230831_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivedpermit',
            name='Archivedid',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='archivedpermit',
            unique_together=set(),
        ),
    ]
