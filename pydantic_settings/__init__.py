from pydantic import BaseModel, Field

class BaseSettings(BaseModel):
    def __init__(self, **values):
        super().__init__(**values)

