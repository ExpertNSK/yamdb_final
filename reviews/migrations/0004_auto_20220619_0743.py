# Generated by Django 2.2.16 on 2022-06-19 00:43

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220619_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[reviews.validators.UsernameValidator], verbose_name='Имя пользователя'),
        ),
    ]
