# Generated by Django 3.1.5 on 2021-03-28 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tokens', '0006_auto_20210328_0339'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='owner',
            field=models.CharField(default='charles', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auction',
            name='id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='tokens.token', unique=True),
        ),
        migrations.AlterField(
            model_name='auction',
            name='n_bids',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='auction',
            name='time_start',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
