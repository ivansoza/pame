# tu_app/management/commands/load_estados.py
from django.core.management.base import BaseCommand
from catalogos.models import Estado, Tipos, Estatus, Estancia, Relacion

class Command(BaseCommand):
    help = 'Carga de informacion por default'

    def handle(self, *args, **options):
        self.stdout.write('Cargando estados...')
        estados_command = cargar_estados()
        estados_command.cargar_estados()

        self.stdout.write('Cargando tipos...')
        tipos_command = cargar_tipos()
        tipos_command.cargar_tipos()

        self.stdout.write('Cargando estatus...')
        estatus_command = cargas_estatus()
        estatus_command.cargar_estatus()

        self.stdout.write('Cargando modalidades de ingreso...')
        modalidad_command = cargar_modalidad()
        modalidad_command.cargar_modalidad()

        self.stdout.write('Cargando Relaciones familiares...')
        relacion_command = cargar_relaciones()
        relacion_command.cargar_relacion()

        self.stdout.write(self.style.SUCCESS('Carga completa'))

class cargar_estados:
    help = 'Carga los estados de la República Mexicana'

    def cargar_estados(self):
        estados = [
            {'estado': 'Aguascalientes'},
            {'estado': 'Baja California'},
            {'estado': 'Baja California Sur'},
            {'estado': 'Campeche'},
            {'estado': 'Chiapas'},
            {'estado': 'Chihuahua'},
            {'estado': 'Coahuila'},
            {'estado': 'Colima'},
            {'estado': 'Durango'},
            {'estado': 'Guanajuato'},
            {'estado': 'Guerrero'},
            {'estado': 'Hidalgo'},
            {'estado': 'Jalisco'},
            {'estado': 'México'},
            {'estado': 'Michoacán'},
            {'estado': 'Morelos'},
            {'estado': 'Nayarit'},
            {'estado': 'Nuevo León'},
            {'estado': 'Oaxaca'},
            {'estado': 'Puebla'},
            {'estado': 'Querétaro'},
            {'estado': 'Quintana Roo'},
            {'estado': 'San Luis Potosí'},
            {'estado': 'Sinaloa'},
            {'estado': 'Sonora'},
            {'estado': 'Tabasco'},
            {'estado': 'Tamaulipas'},
            {'estado': 'Tlaxcala'},
            {'estado': 'Veracruz'},
            {'estado': 'Yucatán'},
            {'estado': 'Zacatecas'},
        ]

        for estado_data in estados:
            Estado.objects.get_or_create(estado=estado_data['estado'])

        print('Estados cargados exitosamente')

class cargar_tipos:
    help = 'Carga de tipos de estancia'

    def cargar_tipos(self):
        tipos = [
            {'tipo': 'Oficina de representacion'},
            {'tipo': 'Estancia provisional'},
            {'tipo':'Estación migratoria'},
            {'tipo':'Extención de estancia'},
        ]

        for tipo_data in tipos:
            Tipos.objects.get_or_create(tipo=tipo_data['tipo'])

        print('Tipos cargados exitosamente')

class cargas_estatus:
    help = 'Carga de tipos de estancia'

    def cargar_estatus(self):
        estatus = [
            {'tipoEstatus': 'Inactivo'},
            {'tipoEstatus': 'Activo'},
        ]

        for estatus_data in estatus:
            Estatus.objects.get_or_create(tipoEstatus=estatus_data['tipoEstatus'])

class cargar_modalidad:
    help = 'Carga de modalidad de ingreso'

    def cargar_modalidad(self):
        modalidades = [
            {'tipoEstancia': 'Por puesta'},
            {'tipoEstancia': 'Alojamiento'},
            {'tipoEstancia': 'Aislamiento'},
        ]

        for modalidades_data in modalidades:
            Estancia.objects.get_or_create(tipoEstancia=modalidades_data['tipoEstancia'])

class cargar_relaciones:
    help = 'Carga las relaciones'

    def cargar_relacion(self):
        relaciones = [
            {'tipoRelacion': 'Padre'},
            {'tipoRelacion': 'Madre'},
            {'tipoRelacion': 'Hijo'},
            {'tipoRelacion': 'Hija'},
            {'tipoRelacion': 'Abuelo'},
            {'tipoRelacion': 'Abuela'},
            {'tipoRelacion': 'Nieto'},
            {'tipoRelacion': 'Nieta'},
            {'tipoRelacion': 'Hermano'},
            {'tipoRelacion': 'Hermana'},
            {'tipoRelacion': 'Tío'},
            {'tipoRelacion': 'Tía'},
            {'tipoRelacion': 'Sobrino'},
            {'tipoRelacion': 'Sobrina'},
            {'tipoRelacion': 'Primo'},
            {'tipoRelacion': 'Prima'},
            {'tipoRelacion': 'Esposo'},
            {'tipoRelacion': 'Esposa'},
        ]

        for relaciones_data in relaciones:
            Relacion.objects.get_or_create(tipoRelacion=relaciones_data['tipoRelacion'])