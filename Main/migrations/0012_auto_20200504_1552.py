# Generated by Django 3.0 on 2020-05-04 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0011_auto_20200502_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='eq_mark',
            name='eq_model',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='Main.Eq_model'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eq_type',
            name='manufacturer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Main.Manufacturer'),
            preserve_default=False,
        ),
    ]
