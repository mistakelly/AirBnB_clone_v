#!/usr/bin/python3
from models.base_model import BaseModel


class State(BaseModel):
    """
        name: string - empty string
    """

    name: str = ''


if __name__ == '__main__':
    model = State()
    print(model.name)
