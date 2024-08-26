import spacy
from typing import Dict, List, Tuple

class NLPEngine:
    def __init__(self):
        self.nlp = spacy.load("es_core_news_sm")

    def tokenize(self, text: str) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        Tokeniza el texto de entrada y extrae entidades clave.

        :param text: Texto de instrucción en lenguaje natural
        :return: Tupla con lista de tokens y lista de entidades extraídas
        """
        doc = self.nlp(text)
        tokens = [token.text for token in doc]
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return tokens, entities

    def analyze_syntax(self, instruction: str) -> List[Tuple[str, str, str]]:
        """
        Realiza un análisis sintáctico de la instrucción.

        :param instruction: Instrucción en lenguaje natural
        :return: Lista de tuplas (texto, etiqueta POS, dependencia)
        """
        doc = self.nlp(instruction)
        return [(token.text, token.pos_, token.dep_) for token in doc]

    def parse_crud_instruction(self, instruction: str) -> Dict[str, any]:
        """
        Analiza una instrucción CRUD y extrae información relevante.

        :param instruction: Instrucción en lenguaje natural
        :return: Diccionario con la operación CRUD y los detalles
        """
        doc = self.nlp(instruction)
        crud_ops = {"crear": "CREATE", "leer": "READ", "actualizar": "UPDATE", "eliminar": "DELETE"}
        
        operation = None
        model = None
        fields = []
        conditions = []
        current_field = []

        for token in doc:
            if token.lemma_.lower() in crud_ops:
                operation = crud_ops[token.lemma_.lower()]
            elif token.pos_ == "NOUN" and not model:
                model = token.text
            elif token.pos_ in ["ADJ", "NOUN"] and model:
                if token.dep_ in ["compound", "amod"] or (len(current_field) == 1 and current_field[0].lower() == "correo" and token.text.lower() == "electrónico"):
                    current_field.append(token.text)
                else:
                    if current_field:
                        fields.append("_".join(current_field).lower().replace(" ", "_"))
                        current_field = []
                    current_field.append(token.text)
            elif token.dep_ == "prep" and token.head.pos_ == "VERB":
                conditions.append(f"{token.text} {token.subtree}")

        if current_field:
            fields.append("_".join(current_field).lower().replace(" ", "_"))

        return {
            "operation": operation,
            "model": model,
            "fields": fields,
            "conditions": conditions
        }

    def generate_basic_code(self, crud_info: Dict[str, any]) -> str:
        """
        Genera código básico basado en la información CRUD extraída.

        :param crud_info: Diccionario con información CRUD
        :return: Código generado en forma de string
        """
        operation = crud_info["operation"]
        model = crud_info["model"]
        fields = crud_info["fields"]
        conditions = crud_info["conditions"]

        if operation == "CREATE":
            field_str = ", ".join(fields)
            value_str = ", ".join([f":{field}" for field in fields])
            return f"INSERT INTO {model} ({field_str}) VALUES ({value_str})"
        elif operation == "READ":
            field_str = ", ".join(fields) if fields else "*"
            condition_str = " AND ".join(conditions) if conditions else "1=1"
            return f"SELECT {field_str} FROM {model} WHERE {condition_str}"
        elif operation == "UPDATE":
            set_str = ", ".join([f"{field} = :{field}" for field in fields])
            condition_str = " AND ".join(conditions) if conditions else "1=1"
            return f"UPDATE {model} SET {set_str} WHERE {condition_str}"
        elif operation == "DELETE":
            condition_str = " AND ".join(conditions) if conditions else "1=1"
            return f"DELETE FROM {model} WHERE {condition_str}"
        else:
            return "Operación no reconocida"

# Ejemplo de uso
if __name__ == "__main__":
    engine = NLPEngine()
    instruction = "Crear un nuevo usuario con nombre, correo electrónico y edad"
    
    print("Tokenización:")
    tokens, entities = engine.tokenize(instruction)
    print(f"Tokens: {tokens}")
    print(f"Entidades: {entities}")
    
    print("\nAnálisis sintáctico:")
    syntax = engine.analyze_syntax(instruction)
    print(syntax)
    
    print("\nAnálisis CRUD:")
    crud_info = engine.parse_crud_instruction(instruction)
    print(crud_info)
    
    print("\nGeneración de código básico:")
    code = engine.generate_basic_code(crud_info)
    print(code)