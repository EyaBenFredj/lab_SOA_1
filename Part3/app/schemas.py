from pydantic import BaseModel, conint, confloat

class ProductBase(BaseModel):
    name: str
    quantity: conint(ge=0)
    price: confloat(ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
