# Generated by Django 4.2 on 2023-08-17 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Estatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoEstatus', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Estatus',
            },
        ),
        migrations.CreateModel(
            name='Puesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_oficio', models.CharField(max_length=20)),
                ('nombre_responsable', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Responsable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellidoPat', models.CharField(max_length=50)),
                ('apellidoMat', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Tipos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Tipos',
            },
        ),
        migrations.CreateModel(
            name='Extranjero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_extranjero', models.CharField(max_length=100)),
                ('edad', models.PositiveIntegerField()),
                ('puesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.puesta')),
            ],
        ),
        migrations.CreateModel(
            name='Estacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=50)),
                ('calle', models.CharField(max_length=50)),
                ('noext', models.CharField(max_length=5)),
                ('noint', models.CharField(default='sn', max_length=5)),
                ('colonia', models.CharField(max_length=50)),
                ('cp', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('capacidad', models.IntegerField()),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.estado')),
                ('estatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.estatus')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.responsable')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.tipos')),
            ],
            options={
                'verbose_name_plural': 'Estaciones',
            },
        ),
    ]
