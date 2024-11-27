from pydantic import BaseModel


class DialogPart(BaseModel):
    text: str
    duration: float
    raised_voice: bool
    gender: str


class ASRResponse(BaseModel):
    dialog: dict
    result_duration: dict
