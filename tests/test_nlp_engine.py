import sys
import os

# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from naturalcode.nlp_engine import NLPEngine

@pytest.fixture
def nlp_engine():
    return NLPEngine()

def test_tokenize(nlp_engine):
    instruction = "Crear un nuevo usuario con nombre y correo electrónico"
    tokens, entities = nlp_engine.tokenize(instruction)
    
    assert len(tokens) > 0
    assert isinstance(tokens, list)
    assert isinstance(entities, list)
    assert "Crear" in tokens
    assert "usuario" in tokens

def test_analyze_syntax(nlp_engine):
    instruction = "Crear un nuevo usuario con nombre y correo electrónico"
    syntax = nlp_engine.analyze_syntax(instruction)
    
    assert len(syntax) > 0
    assert isinstance(syntax, list)
    assert all(isinstance(item, tuple) and len(item) == 3 for item in syntax)
    assert any(item[1] == "VERB" for item in syntax)  # Debe haber al menos un verbo
    assert any(item[1] == "NOUN" for item in syntax)  # Debe haber al menos un sustantivo

def test_parse_crud_instruction(nlp_engine):
    instruction = "Crear un nuevo usuario con nombre y correo electrónico"
    crud_info = nlp_engine.parse_crud_instruction(instruction)
    
    assert isinstance(crud_info, dict)
    assert crud_info["operation"] == "CREATE"
    assert crud_info["model"] == "usuario"
    assert "nombre" in crud_info["fields"]
    assert "correo_electrónico" in crud_info["fields"]

def test_generate_basic_code(nlp_engine):
    crud_info = {
        "operation": "CREATE",
        "model": "usuario",
        "fields": ["nombre", "correo_electrónico", "edad"],
        "conditions": []
    }
    code = nlp_engine.generate_basic_code(crud_info)
    
    assert isinstance(code, str)
    assert "INSERT INTO usuario" in code
    assert "nombre" in code
    assert "correo_electrónico" in code
    assert "edad" in code

def test_complete_workflow(nlp_engine):
    instruction = "Crear un nuevo usuario con nombre, correo electrónico y edad"
    
    # Tokenización
    tokens, entities = nlp_engine.tokenize(instruction)
    assert len(tokens) > 0
    
    # Análisis sintáctico
    syntax = nlp_engine.analyze_syntax(instruction)
    assert len(syntax) > 0
    
    # Parseo de instrucción CRUD
    crud_info = nlp_engine.parse_crud_instruction(instruction)
    assert crud_info["operation"] == "CREATE"
    assert crud_info["model"] == "usuario"
    assert set(crud_info["fields"]) == set(["nombre", "correo_electrónico", "edad"])
    
    # Generación de código
    code = nlp_engine.generate_basic_code(crud_info)
    assert "INSERT INTO usuario (nombre, correo_electrónico, edad) VALUES (:nombre, :correo_electrónico, :edad)" in code

if __name__ == "__main__":
    pytest.main([__file__])