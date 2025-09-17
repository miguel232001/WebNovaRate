import json
from typing import Any, Optional


class ResponseModel:
    """
    Modelo de respuesta para operaciones de la API.
    """

    def __init__(self, success: int = 0, message: str = "", data: Any = None):
        """
        Constructor que permite inicializar las propiedades de la clase con valores específicos.

        Args:
            success: Estado de éxito de la operación (puede ser un código o bandera)
            message: Mensaje asociado a la respuesta (puede ser descriptivo o informativo)
            data: Datos asociados a la respuesta (puede ser cualquier tipo de datos)
        """
        self.success = success  # Inicializa el estado de éxito con el valor proporcionado.
        self.message = message  # Inicializa el mensaje con la cadena proporcionada.
        self.data = data  # Inicializa los datos con el objeto proporcionado.

    @property
    def success(self) -> int:
        """Propiedad que indica el estado de éxito de la operación."""
        return self._success

    @success.setter
    def success(self, value: int):
        self._success = value

    @property
    def message(self) -> str:
        """Propiedad que almacena un mensaje asociado a la respuesta."""
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = value

    @property
    def data(self) -> Any:
        """Propiedad que contiene los datos asociados a la respuesta."""
        return self._data

    @data.setter
    def data(self, value: Any):
        self._data = value

    def to_dict(self) -> dict:
        """
        Convierte el objeto a un diccionario para serialización JSON.

        Returns:
            dict: Diccionario con las propiedades del modelo
        """
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }

    def to_json(self) -> str:
        """
        Serializa el objeto a formato JSON.

        Returns:
            str: Representación JSON del objeto
        """
        return json.dumps(self.to_dict(), default=str, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'ResponseModel':
        """
        Crea una instancia de ResponseModel a partir de una cadena JSON.

        Args:
            json_str: Cadena JSON a deserializar

        Returns:
            ResponseModel: Instancia creada a partir del JSON
        """
        data = json.loads(json_str)
        return cls(
            success=data.get("success", 0),
            message=data.get("message", ""),
            data=data.get("data", None)
        )

    def __str__(self) -> str:
        """Representación en string del objeto."""
        return f"ResponseModel(success={self.success}, message='{self.message}', data={self.data})"

    def __repr__(self) -> str:
        """Representación oficial del objeto."""
        return self.__str__()