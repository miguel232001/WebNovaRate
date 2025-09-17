import json
import logging
from typing import Optional
import aiohttp
from model import RequestModel, ResponseModel


class APIService:
    """
    Servicio para ejecutar solicitudes HTTP a una API.
    """

    @staticmethod
    async def execute_request(request_model: RequestModel) -> ResponseModel:
        """
        Método para ejecutar una solicitud HTTP y obtener una respuesta asincrónica.

        Args:
            request_model: Modelo de solicitud con método, ruta y datos

        Returns:
            ResponseModel: Modelo de respuesta con los datos de la API
        """
        # Se crea una instancia de la clase ResponseModel para almacenar la respuesta
        response_model = ResponseModel()

        # Se serializa el objeto RequestModel.Data a formato JSON
        data = json.dumps(request_model.data, default=str, ensure_ascii=False)
        logging.debug(f"Datos serializados: {data}")

        # Configuración del cliente HTTP
        timeout = aiohttp.ClientTimeout(total=30)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Se crea una nueva solicitud HTTP con el método y la ruta especificados
                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }

                # Preparar los datos para la solicitud
                request_data = {
                    'method': request_model.method.upper(),
                    'url': request_model.route,
                    'headers': headers,
                    'data': data if request_model.data and request_model.method.upper() in ['POST', 'PUT',
                                                                                            'PATCH'] else None
                }

                # Log de la solicitud
                logging.debug(f"Enviando solicitud: {request_data['method']} {request_data['url']}")

                # Enviar la solicitud según el método HTTP
                method = request_model.method.upper()
                async with session.request(
                        method=method,
                        url=request_model.route,
                        headers=headers,
                        data=data if method in ['POST', 'PUT', 'PATCH', 'DELETE'] else None,
                        params=request_model.data if method == 'GET' else None
                ) as response:

                    # Si la respuesta es exitosa
                    if response.status >= 200 and response.status < 300:
                        # Se lee la respuesta como una cadena JSON
                        string_response = await response.text()
                        if string_response:
                            try:
                                # Se deserializa la cadena JSON en un objeto ResponseModel
                                response_data = json.loads(string_response)
                                response_model = ResponseModel(
                                    success=response_data.get('success', 0),
                                    message=response_data.get('message', ''),
                                    data=response_data.get('data', None)
                                )

                                # Se imprime la respuesta en el log
                                logging.debug(f"Respuesta desde la API: {string_response}")

                            except json.JSONDecodeError as json_error:
                                logging.error(f"Error al decodificar JSON: {json_error}")
                                response_model.message = f"Error en formato de respuesta: {json_error}"
                                response_model.success = 0
                    else:
                        # Si la respuesta no es exitosa, se imprime el código de estado
                        error_text = await response.text()
                        logging.error(f"Error HTTP {response.status}: {error_text}")
                        response_model.message = f"Error {response.status}: {error_text}"
                        response_model.success = 0

        except aiohttp.ClientError as client_error:
            # Si se produce un error de cliente HTTP
            logging.error(f"Error de conexión: {client_error}")
            response_model.message = f"Error de conexión: {client_error}"
            response_model.success = 0

        except Exception as ex:
            # Si se produce una excepción durante la solicitud
            logging.error(f"Error inesperado al enviar la solicitud a la API: {ex}")
            response_model.message = f"Error inesperado: {ex}"
            response_model.success = 0

        # Se devuelve el objeto ResponseModel, que contiene la respuesta de la API
        return response_model