from pydantic import BaseModel
from typing import Union, Any, Optional

class ResponseDTO(BaseModel):
    status: str     
    message: str
    data: Optional[Any] = None
