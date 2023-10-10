from pydantic import BaseModel

def map_data_to_model(model: BaseModel, data: list) -> list:
    keys = model.__annotations__.keys()
    mapper = lambda row: model(**{key: value for key, value in zip(keys, row)})
    return [mapper(row) for row in data]
