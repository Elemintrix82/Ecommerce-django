# Generated by Django 4.2.1 on 2023-06-28 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_orderproduct_variation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='oder',
            new_name='order',
        ),
    ]