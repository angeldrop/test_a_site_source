# Generated by Django 3.0.3 on 2020-03-09 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20200222_1826'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('list', 'text')},
        ),
    ]