# Generated by Django 4.2.4 on 2023-08-17 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_app', '0016_remove_category_category_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sub_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category_name', models.CharField(max_length=100)),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecom_app.category')),
            ],
        ),
    ]
