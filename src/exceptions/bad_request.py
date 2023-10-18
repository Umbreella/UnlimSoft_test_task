from fastapi import HTTPException, status


class BadRequest(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
