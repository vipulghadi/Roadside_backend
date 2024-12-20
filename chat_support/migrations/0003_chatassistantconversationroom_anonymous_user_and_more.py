# Generated by Django 5.1.1 on 2024-11-21 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_support', '0002_alter_chatassistantconversationroom_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatassistantconversationroom',
            name='anonymous_user',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='chatassistantconversationroom',
            name='is_anonymous_user',
            field=models.BooleanField(blank=True, default=False, help_text='Indicates if the user is anonymous.', null=True),
        ),
    ]
