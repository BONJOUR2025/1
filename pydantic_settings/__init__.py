from pydantic import BaseModel, Field
import os
from pathlib import Path


class BaseSettings(BaseModel):
    """Very small replacement for pydantic-settings BaseSettings."""

    class Config:
        env_file = None

    def __init__(self, **values):
        data = {}
        env_file = getattr(self.Config, "env_file", None)
        if env_file:
            path = Path(env_file)
            if path.exists():
                for line in path.read_text().splitlines():
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    key, val = line.split('=', 1)
                    data.setdefault(key, val)

        for name, field in self.__fields__.items():
            env_key = field.field_info.extra.get('env')
            if env_key and env_key in os.environ:
                data[name] = os.environ[env_key]
            elif env_key and env_key in data:
                data[name] = data[env_key]

        data.update(values)
        super().__init__(**data)

