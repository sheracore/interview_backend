# Generated by Django 3.2.19 on 2023-06-05 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import skyloov.shops.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('shops', '0007_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('price', skyloov.shops.fields.PriceField(decimal_places=0, default=0, max_digits=20, verbose_name='Price')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('object_id', models.PositiveIntegerField(verbose_name='Object id')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shops.cart', verbose_name='Cart')),
                ('content_type', models.ForeignKey(limit_choices_to=models.Q(('app_label', 'shops'), ('model', 'product')), on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Cart item',
                'verbose_name_plural': 'Cart items',
                'unique_together': {('cart', 'object_id', 'content_type')},
            },
        ),
    ]