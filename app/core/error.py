from fastapi import HTTPException

async def raise_error_event(status_code: int, message: str) -> HTTPException:
    raise HTTPException(status_code=status_code, detail=message)