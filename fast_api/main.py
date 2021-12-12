# Import the FastAPI class which is a Python class that provides all the functionality for your API.
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
