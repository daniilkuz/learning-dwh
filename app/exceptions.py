from fastapi import HTTPException, status


class AlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "Запись уже существует"):
        super().__init__(status.HTTP_409_CONFLICT, detail=detail)


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Заказ не найден"):
        super().__init__(status.HTTP_404_NOT_FOUND, detail=detail)


class ItemNotFoundException(HTTPException):
    def __init__(self, item_id: int, detail: str | None = None):
        if not detail:
            detail = f"Продукт с id = {item_id} не найден"
        super().__init__(status.HTTP_404_NOT_FOUND, detail=detail)
