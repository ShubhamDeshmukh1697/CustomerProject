# Generated by Django 3.1 on 2020-12-16 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201216_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='tag',
            field=models.ManyToManyField(to='accounts.Tag'),
        ),
    ]
