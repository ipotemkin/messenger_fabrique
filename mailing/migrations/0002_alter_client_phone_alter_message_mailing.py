# Generated by Django 4.0.4 on 2022-04-19 22:56

from django.db import migrations, models
import django.db.models.deletion
import mailing.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=11, validators=[mailing.validators.PhoneNumberValidator], verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='message',
            name='mailing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='mailing.mailing', verbose_name='ID рассылки'),
        ),
    ]
