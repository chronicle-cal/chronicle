from pydantic import BaseModel, Field


class Profile(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=64)


class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
