import os
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader

class CodeGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))

    def generate_model(self, model_name: str, fields: List[Dict[str, str]]) -> str:
        """
        Genera el código para un modelo de datos simple.
        
        :param model_name: Nombre del modelo
        :param fields: Lista de diccionarios con los campos y sus tipos
        :return: Código del modelo generado
        """
        template = self.env.get_template('model_template.py')
        return template.render(model_name=model_name, fields=fields)

    def generate_crud_operations(self, model_name: str, fields: List[Dict[str, str]]) -> str:
        """
        Genera el código para las operaciones CRUD de un modelo.
        
        :param model_name: Nombre del modelo
        :param fields: Lista de diccionarios con los campos y sus tipos
        :return: Código de las operaciones CRUD generado
        """
        template = self.env.get_template('crud_template.py')
        return template.render(model_name=model_name, fields=fields)

    def generate_database_schema(self, model_name: str, fields: List[Dict[str, str]]) -> str:
        """
        Genera el esquema de base de datos SQLite para un modelo.
        
        :param model_name: Nombre del modelo
        :param fields: Lista de diccionarios con los campos y sus tipos
        :return: Código SQL para crear la tabla
        """
        template = self.env.get_template('sqlite_schema_template.sql')
        return template.render(model_name=model_name, fields=fields)

    def generate_restful_api(self, model_name: str, fields: List[Dict[str, str]]) -> str:
        """
        Genera una plantilla de API RESTful para un modelo.
        
        :param model_name: Nombre del modelo
        :param fields: Lista de diccionarios con los campos y sus tipos
        :return: Código de la API RESTful generado
        """
        template = self.env.get_template('restful_api_template.py')
        return template.render(model_name=model_name, fields=fields)

    def generate_unit_tests(self, model_name: str, fields: List[Dict[str, str]]) -> str:
        """
        Genera pruebas unitarias básicas para las operaciones CRUD de un modelo.
        
        :param model_name: Nombre del modelo
        :param fields: Lista de diccionarios con los campos y sus tipos
        :return: Código de las pruebas unitarias generado
        """
        template = self.env.get_template('unit_tests_template.py')
        return template.render(model_name=model_name, fields=fields)

# Ejemplo de uso
if __name__ == "__main__":
    generator = CodeGenerator()
    model_name = "Usuario"
    fields = [
        {"name": "id", "type": "int", "primary_key": True},
        {"name": "nombre", "type": "str"},
        {"name": "correo_electronico", "type": "str"},
        {"name": "edad", "type": "int"}
    ]

    print("Modelo generado:")
    print(generator.generate_model(model_name, fields))

    print("\nOperaciones CRUD generadas:")
    print(generator.generate_crud_operations(model_name, fields))

    print("\nEsquema de base de datos generado:")
    print(generator.generate_database_schema(model_name, fields))

    print("\nAPI RESTful generada:")
    print(generator.generate_restful_api(model_name, fields))

    print("\nPruebas unitarias generadas:")
    print(generator.generate_unit_tests(model_name, fields))