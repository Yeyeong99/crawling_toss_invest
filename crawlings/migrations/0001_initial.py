# Generated by Django 4.2.9 on 2025-04-04 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('company_code', models.CharField(max_length=200)),
                ('comment', models.TextField()),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
