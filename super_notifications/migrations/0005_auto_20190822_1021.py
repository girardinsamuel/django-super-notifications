# Generated by Django 2.2 on 2019-08-22 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('super_notifications', '0004_auto_20180315_0954'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=40, verbose_name='Label')),
                ('description', models.CharField(max_length=150, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Notification type',
                'verbose_name_plural': 'Notification types',
            },
        ),
        migrations.AddField(
            model_name='notification',
            name='level',
            field=models.CharField(choices=[('success', 'success'), ('info', 'info'), ('warning', 'warning'), ('error', 'error')], default='info', max_length=20),
        ),
        migrations.AlterField(
            model_name='notification',
            name='nf_type',
            field=models.CharField(default='default', max_length=40, verbose_name='Label du type de notification'),
        ),
        migrations.CreateModel(
            name='NotificationSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channels', multiselectfield.db.fields.MultiSelectField(choices=[('dashboard', 'super_notifications.backends.dashboard.BaseBackend'), ('email', 'super_notifications.backends.email.EmailBackend')], default='dashboard', max_length=20, verbose_name='Canaux autorisés pour ce type de notification')),
                ('disabled', models.BooleanField(default=False, verbose_name='Désactivation de ce type de notification')),
                ('notification_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='super_notifications.NotificationType', verbose_name='Type de notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_settings', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Notification setting',
                'verbose_name_plural': 'Notification settings',
                'unique_together': {('user', 'notification_type')},
            },
        ),
    ]
