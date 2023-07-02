# Generated by Django 4.2.1 on 2023-07-02 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_productgallery_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boutique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boutique_name', models.CharField(max_length=100)),
                ('boutique_address', models.CharField(max_length=255)),
                ('boutique_logo', models.ImageField(blank=True, upload_to='photos/boutiques/')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='boutiques',
            field=models.ManyToManyField(related_name='categories', to='store.boutique'),
        ),
    ]
