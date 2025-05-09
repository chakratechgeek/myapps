# Generated by Django 5.2 on 2025-05-04 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoftwareCatalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('requires_license', models.BooleanField(default=False)),
                ('is_metered', models.BooleanField(default=False)),
                ('reclaim_after_days', models.IntegerField(default=30)),
            ],
        ),
    ]
