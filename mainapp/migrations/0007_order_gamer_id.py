# Generated by Django 5.0.4 on 2024-04-14 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_cards_description_alter_userlangauth_tg_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='gamer_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
