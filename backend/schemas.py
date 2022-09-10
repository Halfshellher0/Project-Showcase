import datetime as _dt
import pydantic as _pydantic

class _UserBase(_pydantic.BaseModel):
    username: str

class UserCreate(_UserBase):
    password: str

    class Config:
        orm_mode = True

class User(_UserBase):
    id: int

    class Config:
        orm_mode = True

class _ProjectBase(_pydantic.BaseModel):
    name: str
    description: str
    github: str
    iconPath: str

class Project(_ProjectBase):
    id: int

    class Config:
        orm_mode = True
