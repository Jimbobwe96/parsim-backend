# Generated by Django 4.2.16 on 2024-10-22 05:45

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('condition', models.CharField(choices=[('new', 'New'), ('like_new', 'Like New'), ('gently_used', 'Gently Used'), ('worn', 'Worn')], max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('available', 'Available'), ('pending', 'Pending'), ('sold', 'Sold')], default='available', max_length=50)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings', to='marketplace.category')),
            ],
            options={
                'verbose_name': 'Listing',
                'verbose_name_plural': 'Listings',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('bio', models.TextField(blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('geolocation', models.CharField(blank=True, max_length=255)),
                ('groups', models.ManyToManyField(blank=True, related_name='marketplace_users', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='marketplace_users', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='marketplace.user')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='marketplace.listing')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='marketplace.user')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='marketplace.user')),
            ],
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='listing_images/')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_images', to='marketplace.listing')),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='listings', to='marketplace.user'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_written', to='marketplace.user')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_received', to='marketplace.user')),
            ],
            options={
                'unique_together': {('reviewer', 'seller')},
            },
        ),
    ]
