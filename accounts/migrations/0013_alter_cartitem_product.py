# Generated by Django 4.1.3 on 2022-12-18 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_cartitem_total_price_cartitem_total_price_old'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.product', unique=True),
        ),
    ]
