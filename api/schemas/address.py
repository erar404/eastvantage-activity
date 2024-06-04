from pydantic import BaseModel, Field
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.address import Address
from typing import Literal


GetAddress = pydantic_model_creator(Address, name="Address")


class SearchChoices(BaseModel):
    choice: Literal['city',
                    'province',
                    'region',
                    'country',
                    'street',
                    'zipcode'] = 'city'
    search_value: str


class PostAddress(BaseModel):
    # Class for adding Address.
    name: str = Field(..., max_length=50, examples=["Address Name"])
    country: str = Field(..., max_length=50, examples=["Philippines"])
    region: str = Field(..., max_length=50, examples=["NCR"])
    province: str = Field(..., max_length=50, examples=["Metro Manila"])
    city: str = Field(..., max_length=50, examples=["Taguig City"])
    street: str = Field(..., max_length=50, examples=["3rd Avenue"])
    unit_name: str = Field(..., max_length=50, examples=["Legend Tower"])
    zipcode: int = Field(0, examples=[1634])
    longtitude: float = Field(0, examples=[121.046857])
    latitude: float = Field(0, examples=[14.553988])


class UpdateAddress(BaseModel):
    # Class for Updating Address.
    name: Optional[str] = Field(None, max_length=50, examples=[""])
    country: Optional[str] = Field(None, max_length=50, examples=[""])
    region: Optional[str] = Field(None, max_length=50, examples=[""])
    province: Optional[str] = Field(None, max_length=50, examples=[""])
    city: Optional[str] = Field(None, max_length=50, examples=[""])
    street: Optional[str] = Field(None, max_length=50, examples=[""])
    unit_name: Optional[str] = Field(None, max_length=50, examples=[""])
    zipcode: Optional[int] = Field(0)
    longtitude: Optional[float] = Field(0)
    latitude: Optional[float] = Field(0)
