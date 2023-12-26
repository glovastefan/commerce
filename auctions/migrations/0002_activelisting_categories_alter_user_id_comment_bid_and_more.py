# Generated by Django 4.2.7 on 2023-12-26 00:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveListing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=250)),
                ('url_photo', models.URLField(blank=True, max_length=250)),
                ('starting_bid', models.DecimalField(decimal_places=2, max_digits=6)),
                ('current_bid', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(choices=[('F', 'Fasion'), ('T', 'Toys'), ('O', 'Others')], max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('detailed_comment', models.TextField(max_length=250)),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.activelisting')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bid_value', models.DecimalField(decimal_places=2, max_digits=6)),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.activelisting')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='activelisting',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.categories'),
        ),
        migrations.AddField(
            model_name='activelisting',
            name='current_bid_user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activelisting',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_as_seller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activelisting',
            name='watchlisted',
            field=models.ManyToManyField(blank=True, related_name='user_watching', to=settings.AUTH_USER_MODEL),
        ),
    ]