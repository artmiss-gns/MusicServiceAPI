from pydantic import BaseModel
from passlib.context import CryptContext

class Password :
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls, password: str) :
        return cls.password_context.hash(password)
    
    @classmethod
    def validate_password(cls, password: str, hashed_password: str) :
        return cls.password_context.verify(password, hashed_password)


def map_data_to_model(model: BaseModel, data: list) -> list:
    keys = model.__annotations__.keys()
    mapper = lambda row: model(**{key: value for key, value in zip(keys, row)})
    return [mapper(row) for row in data]


