class BaseModel:
    """Minimal pydantic.BaseModel replacement for tests."""
    model_fields: dict[str, object] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        ann = getattr(cls, '__annotations__', {})
        cls.model_fields = {}
        for k in ann:
            default = getattr(cls, k, None)
            cls.model_fields[k] = default

    def __init__(self, **data):
        for k in self.__class__.model_fields:
            if k in data:
                setattr(self, k, data[k])
            else:
                setattr(self, k, self.__class__.model_fields.get(k))

    def model_dump(self, *, exclude_none=False):
        data = {k: getattr(self, k) for k in self.__class__.model_fields}
        if exclude_none:
            data = {k: v for k, v in data.items() if v is not None}
        return data


def Field(default=None, **kwargs):
    return default
