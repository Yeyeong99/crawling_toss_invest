# Generated by Django 4.2.11 on 2025-04-06 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawlings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('analysis_result', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
