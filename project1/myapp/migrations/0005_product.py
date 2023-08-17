# Generated by Django 4.2.3 on 2023-07-24 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_contect_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_brand', models.CharField(choices=[('Puma', 'Puma'), ('Adidas', 'Adidas'), ('Nike', 'Nike'), ('Bata', 'Bata')], max_length=100)),
                ('product_price', models.PositiveIntegerField()),
                ('product_size', models.CharField(choices=[('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11')], max_length=100)),
                ('product_pic', models.ImageField(upload_to='product_pic/')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
