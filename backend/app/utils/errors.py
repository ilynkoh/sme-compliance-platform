class APIException(Exception):
    """Base API exception"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationException(APIException):
    """Data validation error"""
    def __init__(self, message: str):
        super().__init__(message, 422)

class AuthenticationException(APIException):
    """Authentication error"""
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, 401)

class AuthorizationException(APIException):
    """Authorization error"""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, 403)

class ResourceNotFoundException(APIException):
    """Resource not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)

class FileProcessingException(APIException):
    """File processing error"""
    def __init__(self, message: str):
        super().__init__(message, 400)