from models.base_model import BaseModel


class review(BaseModel):
    """
    Public class attributes:
        place_id: string - empty string: it will be the Place.id
        user_id: string - empty string: it will be the User.id
        text: string - empty string
    """

    place_id: str = ''
    user_id: str = ''
    text: str = ''
