from pydantic import BaseModel, ConfigDict


class AccessToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str
    type: str
