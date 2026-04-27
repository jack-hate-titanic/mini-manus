class AppException(RuntimeError):
    def __init__(self, message: str = "An error occurred.", status_code: int = 400, code: int = 400, data: any = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.data = data
        self.message = message
        super().__init__()

class BadRequestError(AppException):
    def __init__(self, message: str = "Bad request.", data: any = None):
        super().__init__(message, status_code=400, code=400, data=data)


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found.", data: any = None):
        super().__init__(message, status_code=404, code=404, data=data)

class ValidationError(AppException):
    def __init__(self, message: str = "Validation error.", data: any = None):
        super().__init__(message, status_code=422, code=422, data=data)

class TooManyRequestsError(AppException):
    def __init__(self, message: str = "Too many requests.", data: any = None):
        super().__init__(message, status_code=429, code=429, data=data)

class ServerRequestError(AppException):
    def __init__(self, message: str = "Server request error.", data: any = None):
        super().__init__(message, status_code=500, code=500, data=data)

