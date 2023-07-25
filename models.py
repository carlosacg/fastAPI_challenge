from pydantic import BaseModel


class User(BaseModel):
    """
    Pydantic model representing a User.

    Attributes:
    id (int): The ID of the user.
    email (str): The email address of the user.
    password (str): The password of the user.
    """
    id: int
    email: str
    password: str


class People(BaseModel):
    """
    Pydantic model representing a People record.

    Attributes:
    id (int): The ID of the people record.
    name (str): The name of the person.
    age (int): The age of the person.
    """
    id: int
    name: str
    age: int
