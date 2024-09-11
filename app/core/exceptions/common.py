from typing import Any
from fastapi import HTTPException, status


class ResourceNotFoundException(HTTPException):
    def __init__(self, id: Any = "", resourceType: str = "Resource"):
        idString = id if f" with id {id}" else ""
        detail = f"{resourceType} {idString} does not exists"

        super().__init__(
            status.HTTP_404_NOT_FOUND,
            detail,
        )
        self.id = id
