# Generated by Django 2.2.4 on 2023-08-11 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_auto_20230811_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='customer',
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='Active',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isActive', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ActiveCustomers', to='app1.Customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ActiveServices', to='app1.Service')),
            ],
        ),
    ]
