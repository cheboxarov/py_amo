from typing import Optional, Dict, Any


class PyAmoException(Exception):
    """Базовое исключение для py_amo"""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class AuthenticationError(PyAmoException):
    """Ошибка аутентификации (401)"""
    pass


class AuthorizationError(PyAmoException):
    """Ошибка авторизации (403)"""
    pass


class NotFoundError(PyAmoException):
    """Сущность не найдена (404)"""
    pass


class ValidationError(PyAmoException):
    """Ошибка валидации данных (400, 422)"""
    pass


class RateLimitError(PyAmoException):
    """Превышен лимит запросов (429)"""
    pass


class ServerError(PyAmoException):
    """Ошибка сервера (5xx)"""
    pass


class NetworkError(PyAmoException):
    """Ошибка сети или подключения"""
    pass


class TokenExpiredError(AuthenticationError):
    """Токен истек"""
    pass


class EntityNotFoundError(NotFoundError):
    """Конкретная сущность не найдена"""
    
    def __init__(self, entity_type: str, entity_id: int):
        self.entity_type = entity_type
        self.entity_id = entity_id
        message = f"{entity_type} with id {entity_id} not found"
        super().__init__(message, 404)


class InvalidFilterError(ValidationError):
    """Неверные параметры фильтрации"""
    pass


class DuplicateEntityError(ValidationError):
    """Попытка создать дубликат сущности"""
    pass


class QuotaExceededError(PyAmoException):
    """Превышена квота аккаунта"""
    pass


class UnsupportedOperationError(PyAmoException):
    """Операция не поддерживается для данного типа сущности"""
    
    def __init__(self, operation: str, entity_type: str):
        self.operation = operation
        self.entity_type = entity_type
        message = f"Operation '{operation}' is not supported for entity type '{entity_type}'"
        super().__init__(message)


def get_exception_from_status_code(status_code: int, message: str = None, response_data: Dict[str, Any] = None) -> PyAmoException:
    """Создает соответствующее исключение на основе HTTP статус-кода"""
    
    if message is None:
        message = f"HTTP {status_code} error"
    
    if status_code == 400:
        return ValidationError(message, status_code, response_data)
    elif status_code == 401:
        return AuthenticationError(message, status_code, response_data)
    elif status_code == 403:
        return AuthorizationError(message, status_code, response_data)
    elif status_code == 404:
        return NotFoundError(message, status_code, response_data)
    elif status_code == 422:
        return ValidationError(message, status_code, response_data)
    elif status_code == 429:
        return RateLimitError(message, status_code, response_data)
    elif 500 <= status_code < 600:
        return ServerError(message, status_code, response_data)
    else:
        return PyAmoException(message, status_code, response_data) 