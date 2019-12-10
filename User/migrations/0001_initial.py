# Generated by Django 2.1.7 on 2019-12-10 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('initial', models.CharField(max_length=24)),
                ('photo', models.ImageField(blank=True, default='familyMember/wu.jpg', null=True, upload_to='familyMember/')),
            ],
        ),
    ]
