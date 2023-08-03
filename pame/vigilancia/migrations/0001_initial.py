# Generated by Django 4.2 on 2023-08-03 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Extranjero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaRegistro', models.DateField(verbose_name='Fecha de Registro')),
                ('horaRegistro', models.DateTimeField(verbose_name='Hora de Registro')),
                ('numeroE', models.IntegerField(verbose_name='Numero')),
                ('nombreE', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellidoPaternoE', models.CharField(max_length=50, verbose_name='Apellido Paterno')),
                ('apellidoMaternoE', models.CharField(max_length=50, verbose_name='Apellido Materno')),
                ('firmaE', models.FileField(upload_to='', verbose_name='Firma')),
                ('huellaE', models.FileField(upload_to='', verbose_name='Huella')),
                ('fechaNacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('documentoIdentidad', models.FileField(upload_to='', verbose_name='Documento Identidad')),
                ('fotografiaExtranjero', models.FileField(upload_to='', verbose_name='fotografia')),
                ('viajaSolo', models.BooleanField(verbose_name='¿Viaja solo?')),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genero', models.CharField(max_length=100, verbose_name='Genero')),
            ],
        ),
        migrations.CreateModel(
            name='Nacionalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nacionalidad')),
                ('Abreviatura', models.CharField(max_length=200, verbose_name='Abreviatura')),
            ],
        ),
        migrations.CreateModel(
            name='OficioPuestaDisposicionINM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroOficio', models.IntegerField(verbose_name='Numero Oficial')),
                ('fechaOficio', models.DateField(verbose_name='Fecha de Oficio')),
                ('nombreAutoridadSigna', models.CharField(max_length=100, verbose_name='Nombre de la Autoridad Asignada')),
                ('cargoAutoridadSigna', models.CharField(max_length=100, verbose_name='Cargo de la Autoridad Asignada')),
                ('puntoRevision', models.CharField(max_length=100, verbose_name='Punto de Revisión')),
                ('oficioPuesta', models.FileField(upload_to='', verbose_name='Oficio Puesta')),
                ('oficioComision', models.FileField(upload_to='', verbose_name='Oficio Comisión')),
                ('delExtranjero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vigilancia.extranjero', verbose_name='Numero del Extranjero')),
            ],
        ),
        migrations.CreateModel(
            name='OficioPuestaDisposicionAC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroOficio', models.IntegerField(verbose_name='Numero Oficio')),
                ('fechaOficio', models.DateField(verbose_name='Fecha Oficio')),
                ('dependencia', models.CharField(max_length=100, verbose_name='Dependencia')),
                ('numeroCarpeta', models.CharField(max_length=30, verbose_name='Numero de Carpeta')),
                ('nombreAutoridadSigna', models.CharField(max_length=100, verbose_name='Nombre de la Autoridad Asignada')),
                ('cargoAutoridadSigna', models.CharField(max_length=100, verbose_name='Cargo de la Autoridad Asignada')),
                ('entidadFederativa', models.CharField(max_length=100, verbose_name='Entidad Federativa')),
                ('oficioPuesta', models.FileField(upload_to='', verbose_name='Oficio Puesta')),
                ('certificadoMedico', models.FileField(upload_to='', verbose_name='Certificado Medico')),
                ('delExtranjero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vigilancia.extranjero', verbose_name='Numero del Extranjero')),
            ],
        ),
        migrations.AddField(
            model_name='extranjero',
            name='genero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vigilancia.genero', verbose_name='Genero'),
        ),
        migrations.AddField(
            model_name='extranjero',
            name='nacionalidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vigilancia.nacionalidad', verbose_name='Nacionalidad'),
        ),
        migrations.CreateModel(
            name='Acompanante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delExtranjero', models.IntegerField(verbose_name='Numero del Acompañante')),
                ('relacion', models.CharField(max_length=30, verbose_name='Relación')),
                ('delAcompanante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vigilancia.extranjero', verbose_name='Numero del Extranjero')),
            ],
        ),
    ]
