# Import the FastAPI class which is a Python class that provides all the functionality for your API.
from typing import Optional

from fastapi import FastAPI

from modelname import ModelName
from product import Product

# create an instance of FastAPI
pengfei_fastapi_app = FastAPI()


@pengfei_fastapi_app.get("/messages/hello")
async def hello():
    return {"message": "Hello World"}


@pengfei_fastapi_app.get("/items/{item_id}")
async def get_item(item_id: int):
    # return a dict
    return {"item": item_id}


@pengfei_fastapi_app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user id"}


@pengfei_fastapi_app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@pengfei_fastapi_app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@pengfei_fastapi_app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@pengfei_fastapi_app.get("/calculator/addition")
async def addition(x: int = 0, y: int = 0):
    return x + y


@pengfei_fastapi_app.get("/calculator/soustraction")
async def soustraction(x: int, y: int):
    return x + y


@pengfei_fastapi_app.get("/products/{product_id}")
async def read_product(product_id: str, product_name: Optional[str] = None):
    if product_name:
        return {"product_id": product_id, "product_name": product_name}
    return {"product_id": product_id}


@pengfei_fastapi_app.get("/product-nums/{product_id}")
async def product_number(product_id: str, product_name: Optional[str] = None, warehouse: bool = False):
    if warehouse:
        product_num = 18
    else:
        product_num = 8
    if product_name:
        return {"product_id": product_id, "product_name": product_name, "product_number": product_num}
    return {"product_id": product_id, "product_number": product_num}


@pengfei_fastapi_app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@pengfei_fastapi_app.post("/products/")
async def create_product(product: Product):
    return product


@pengfei_fastapi_app.post("/products_price/")
async def create_product_price(product: Product):
    product_dict = product.dict()
    if product.tax:
        total_price = product.price + product.tax
        product_dict.update({"Total_price": total_price})
    return product_dict


@pengfei_fastapi_app.post("/products_id/{product_id}")
async def create_product_with_id(product_id: int, product: Product):
    return {"product_id": product_id, **product.dict()}


@pengfei_fastapi_app.post("/products_attrs/{product_id}")
async def create_product_with_id(product_id: int, product: Product, supplier: Optional[str]):
    if supplier:
        return {"product_id": product_id, **product.dict(), "supplier": supplier}
    return {"product_id": product_id, **product.dict()}
