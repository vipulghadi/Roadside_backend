# Generated by Django 5.1.1 on 2024-11-11 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0009_vendorprofile_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendorlikes',
            name='user',
        ),
        migrations.RemoveField(
            model_name='vendorlikes',
            name='vendor',
        ),
        migrations.RemoveField(
            model_name='vendorreviewlikes',
            name='review',
        ),
        migrations.RemoveField(
            model_name='vendorreviewlikes',
            name='user',
        ),
        migrations.RemoveField(
            model_name='vendrreviewdislikes',
            name='review',
        ),
        migrations.RemoveField(
            model_name='vendrreviewdislikes',
            name='user',
        ),
        migrations.RemoveField(
            model_name='vendorreview',
            name='item',
        ),
        migrations.RemoveField(
            model_name='vendorreview',
            name='rating',
        ),
        migrations.DeleteModel(
            name='VendorDislikes',
        ),
        migrations.DeleteModel(
            name='VendorLikes',
        ),
        migrations.DeleteModel(
            name='VendorReviewLikes',
        ),
        migrations.DeleteModel(
            name='VendrReviewDislikes',
        ),
    ]