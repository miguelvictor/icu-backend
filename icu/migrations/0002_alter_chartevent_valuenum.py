# Generated by Django 3.2.4 on 2021-07-02 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartevent',
            name='valuenum',
            field=models.FloatField(blank=True, help_text='The numeric format of the same value. If data is not numeric, this field is null.', null=True, verbose_name='value (numeric)'),
        ),
    ]