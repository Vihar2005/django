# Generated by Django 4.2.4 on 2023-08-04 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_user_usertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_brand', models.CharField(max_length=100)),
                ('product_price', models.PositiveIntegerField()),
                ('product_size', models.CharField(max_length=100)),
                ('product_pic', models.ImageField(upload_to='product_pic/')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
