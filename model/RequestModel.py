import json

# Agregar estos métodos a la clase RequestModel si necesitas JSON:
def to_json(self) -> str:
    """Serializa el objeto a formato JSON."""
    return json.dumps(self.to_dict(), default=str, ensure_ascii=False)

@classmethod
def from_json(cls, json_str: str) -> 'RequestModel':
    """Crea una instancia a partir de una cadena JSON."""
    data = json.loads(json_str)
    return cls(
        method=data.get("method", ""),
        route=data.get("route", ""),
        data=data.get("data", None)
    )