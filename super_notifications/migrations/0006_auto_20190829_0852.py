# Generated by Django 2.2 on 2019-08-29 06:52

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('super_notifications', '0005_auto_20190822_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='target_object_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ID of the target object'),
        ),
        migrations.AlterField(
            model_name='notificationsetting',
            name='channels',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('dashboard', 'super_notifications.backends.dashboard.BaseBackend'), ('email', 'notifications.backends.email.EmailBackend')], default='dashboard', max_length=20, verbose_name='Canaux autorisés pour ce type de notification'),
        ),
    ]
