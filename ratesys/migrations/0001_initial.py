# Generated by Django 3.2.12 on 2022-03-21 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('m_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('m_code', models.CharField(max_length=64)),
                ('m_name', models.CharField(max_length=256)),
                ('ac_year', models.PositiveIntegerField()),
                ('semester', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('p_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('p_code', models.CharField(max_length=64)),
                ('p_name', models.CharField(max_length=128)),
                ('m_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ratesys.module')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('u_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=75)),
                ('password', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('r_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('rate', models.DecimalField(decimal_places=1, max_digits=4)),
                ('m_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ratesys.module')),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ratesys.professor')),
            ],
        ),
    ]
