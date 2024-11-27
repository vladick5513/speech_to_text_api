from pydantic import BaseModel


class ASRResponse(BaseModel):
    dialog: dict
    result_duration: dict
