# Generated by Django 4.2 on 2023-08-11 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidadMigratoria', models.CharField(max_length=30, verbose_name='Unidad Migratoria')),
                ('fechaEntrega', models.DateField(verbose_name='Fecha Entrega')),
                ('horaEntrega', models.DateTimeField(verbose_name='Hora Entrega')),
            ],
        ),
        migrations.CreateModel(
            name='Valores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.DateField(max_length=100, verbose_name='Descripcion')),
                ('cantidad', models.FloatField(verbose_name='Cantidad')),
                ('Obsevaciones', models.CharField(max_length=100, verbose_name='Obervaciones')),
                ('delInventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pertenencias.inventario', verbose_name='Numero de Inventario')),
            ],
            options={
                'verbose_name_plural': 'Valores',
            },
        ),
        migrations.CreateModel(
            name='Pertenencias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.DateField(max_length=100, verbose_name='Descripcion')),
                ('cantidad', models.FloatField(verbose_name='Cantidad')),
                ('observaciones', models.CharField(max_length=100, verbose_name='Obervaciones')),
                ('delInventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pertenencias.inventario', verbose_name='Numero de Inventario')),
            ],
            options={
                'verbose_name_plural': 'Pertenencias',
            },
        ),
    ]
