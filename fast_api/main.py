# Import the FastAPI class which is a Python class that provides all the functionality for your API.
from typing import Optional

from fastapi import FastAPI

from modelname import ModelName

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

