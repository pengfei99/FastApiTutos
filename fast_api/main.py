from fastapi import FastAPI

# Import the FastAPI class which is a Python class that provides all the functionality for your API.


# create an instance of FastAPI
pengfei_fastapi_app = FastAPI()


@pengfei_fastapi_app.get("/messages/hello")
async def root():
    return {"message": "Hello World"}
