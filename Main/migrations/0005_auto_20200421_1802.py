# Generated by Django 3.0 on 2020-04-21 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_eq_model_pq_curve_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eq_mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.CharField(blank=True, default='Unnamed', max_length=60)),
                ('pq_curve_points', models.CharField(blank=True, default='0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,;0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Eq_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eq_type', models.CharField(blank=True, default='Unnamed', max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='eq_model',
            name='name',
        ),
        migrations.RemoveField(
            model_name='eq_model',
            name='pq_curve_points',
        ),
        migrations.RemoveField(
            model_name='eq_model',
            name='type',
        ),
        migrations.AddField(
            model_name='eq_model',
            name='eq_model',
            field=models.CharField(blank=True, default='Unnamed', max_length=30),
        ),
        migrations.DeleteModel(
            name='Equipment_type',
        ),
        migrations.AddField(
            model_name='eq_type',
            name='eq_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Eq_model'),
        ),
        migrations.AddField(
            model_name='eq_mark',
            name='eq_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Eq_type'),
        ),
        migrations.AddField(
            model_name='eq_mark',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Manufacturer'),
        ),
    ]