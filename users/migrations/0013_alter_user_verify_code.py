# Generated by Django 4.2.7 on 2023-11-28 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_user_verify_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verify_code',
            field=models.CharField(default='54201', max_length=5, verbose_name='Код верификации'),
        ),
    ]
