# Generated by Django 2.2.8 on 2020-03-13 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_notifications', '0008_auto_20191003_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='obj_object_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ID of the target object'),
        ),
    ]
