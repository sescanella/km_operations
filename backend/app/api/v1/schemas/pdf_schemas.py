from pydantic import BaseModel

class PdfRequest(BaseModel):
    filename: str

class PdfResponse(BaseModel):
    status: str
    text: str