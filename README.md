# Fast API tutorial

## Introduction

FastAPI is a Python-based web framework based on ASGI (Starlette) that is used to make APIs, mostly. As the name
suggests, it is much faster than Django and Flask, and comes with a few features (as compared to the star-studded
Django)
such as **pydantic typing, and OpenAPI documentation**. More
detailed [doc](https://medium.com/swlh/python-frameworks-and-rest-api-7fa9168b9c67)

## 1. Build a fast api project with poetry

In this project, we use two dependencies:

- fastapi : is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard
  Python type hints
- uvicorn : It is a lightning-fast **ASGI server implementation**, using uvloop and httptools.

Read [this](https://medium.com/analytics-vidhya/difference-between-wsgi-and-asgi-807158ed1d4c), if you want to know the
difference between WSGI ("synchron" Web Server Gateway Interface) and ASGI (Asynchronous Server Gateway Interface)

```shell
# make a new project and create the project folder
poetry new FastApiTutos

# add dependencies
poetry add fastapi[all] uvicorn[standard]
```

By default, poetry will create a source package with your project name (i.e. fastapitutos). If you don't like the naming
convention(project name may be not suit for your code source directory), you can change it. In this tutorial, I name the
source directory as "fast_api"

## 2. Simple example

Go to your source directory, and create **main.py**. Then copy the following content in it.

### 2.1 Add an app

```python
from fastapi import FastAPI

# Import the FastAPI class which is a Python class that provides all the functionality for your API.


# create an instance of FastAPI
pengfei_fastapi_app = FastAPI()


# use the fastapi instance to define a rest api
# get is the http request method
# "/" is the name of the endpoint
@pengfei_fastapi_app.get("/")
async def root():
    return {"message": "Hello World"}
```

FastAPI is a class that inherits directly from [Starlette](https://www.starlette.io/). Starlette is a lightweight ASGI
framework/toolkit, which is ideal for building high performance asyncio services.

### 2.2 Run the app

Now you can run the app by using **uvicorn**

```shell
uvicorn main:pengfei_fastapi_app --reload
```

- main : is the file name where your app is located.
- pengfei_fastapi_app: is the name of your app
- --reload: means restart the server after code changes. Only use for development.

After running the above command, you should see below output

```text
INFO:     Will watch for changes in these directories: ['/home/pliu/git/FastApiTutos/fast_api']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13158] using watchgod
INFO:     Started server process [13160]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:58278 - "GET / HTTP/1.1" 200 OK
```

### 2.3 Interactive docs

#### 2.3.1 Swagger

By using below url, you will see the automatic interactive API documentation (provided by Swagger UI):

```text
http://127.0.0.1:8000/docs
```

#### 2.3.2 ReDoc

You will see the alternative automatic documentation (provided by ReDoc):

```text
http://127.0.0.1:8000/redoc
```

#### 2.3.3 OpenAPI

**FastAPI generates a "schema" with all your API using the OpenAPI standard for defining APIs.**

- **Schema** : A "schema" is a definition or description of something. Not the code that implements it, but just an
  abstract description.
- **API "schema"** : In this case, OpenAPI is a specification that dictates how to define a schema of your API. This
  schema definition includes your API paths, the possible parameters they take, etc.

- **Data "schema"**: The term "schema" might also refer to the shape of some data, like a JSON content. In that case, it
  would mean the JSON attributes, and data types they have, etc.

##### OpenAPI and JSON Schema

OpenAPI defines **an API schema for your API. And that schema includes definitions (or "schemas") of the data sent and
received by your API using JSON Schema, the standard for JSON data schemas**.

To view this OpenAPI schema of your api, you can use the below url:

```text
 http://127.0.0.1:8000/openapi.json
```

You should see a json file like this

```json
{
  "openapi": "3.0.2",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {
    "/": {
      "get": {
        "summary": "Root",
        "operationId": "root__get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                }
              }
            }
          }
        }
      }
    }
  }
}

```

##### What is OpenAPI for?

The OpenAPI schema shows to others how to consume your api. There are dozens of alternatives implementation, all based
on OpenAPI. You could easily add any of those alternatives implementations to your application built with FastAPI.

You could also use **OpenAPI schema** to generate code automatically, for clients(e.g. frontend, mobile or IoT
applications)
that communicate with your API.

### 2.4  Path

The "path" is the main way to separate "concerns" and "resources" inside your api. A "path" is also commonly called an "
endpoint", or a "route".

In the origin code, we use the "/" (root of the application) as the endpoint to print hello world. It's not a good
practice, so we want to use a path that is more appropriate, for instance, we want to use "messages/hello"

```text
# change your code in main.py
@pengfei_fastapi_app.get("/messages/hello")

# the new endpoint url
http://127.0.0.1:8000/messages/hello 
```

### 2.5 Operation

Here, **Operation** refers to one of the HTTP "methods":

- POST
- GET
- PUT
- DELETE ...and the more exotic ones:
- OPTIONS
- HEAD
- PATCH
- TRACE

**In the HTTP protocol, you can communicate to each path using one (or more) of the above http "methods".**

The common convention for these methods are:

- POST: to create data.
- GET: to read data.
- PUT: to update data.
- DELETE: to delete data.

You can notice **each http method correspond to a Data crud operation**. So, in OpenAPI, each of the HTTP methods is
called an "operation".

In FastAPI, we use below decorators(@something) to express the http method with a specific path.

- @app.get(path)
- @app.post(path)
- @app.put(path)
- @app.delete(path)
  And the more exotic ones:
- @app.options(path)
- @app.head(path)
- @app.patch(path)
- @app.trace(path)

Here **app is the name of the fastapi class instance**, **path is the path of the endpoint, for example "
/messages/hello"**

Important Note:

**The above Http methods utility description is a guideline and commonly agreed convention, but not a requirement.
FastAPI doesn't enforce any specific meaning for any http methods.** For example, when using GraphQL you normally
perform all the actions using only POST operations.

### 2.6 Define the path operation function

```python
@pengfei_fastapi_app.get("/")
async def root():
    return {"message": "Hello World"}
```

Below code describes a tuple of "path operation function":

- **path**: is /.
- **operation**: is get.
- **function**: is root() the function below the "decorator".

You can notice that **root() is a normal python function, root() will be called by FastAPI whenever it receives a
request to the URL "/" using a GET operation**.

In the example, we declare root as an **async function**, the async is not required, the root function can be a sync
function too. check [async](https://fastapi.tiangolo.com/async/#in-a-hurry), if you don't know the diff.

### 2.7: return the content

In below code, the root() function returns a dict. It can also return a list, singular values as str, int, etc.

```python
@pengfei_fastapi_app.get("/")
async def root():
    return {"message": "Hello World"}
```

It can also return Pydantic models (you'll see more about that later).

There are many other objects and models that will be automatically converted to JSON (including ORMs, etc). Try using
your favorite ones, it's highly probable that they are already supported.

## 3. Path parameters

You can declare path "parameters" or "variables" with the same syntax used by Python format strings. Add the following
code to your main.py.

```python
@pengfei_fastapi_app.get("/items/{item_id}")
async def get_item(item_id):
    # return a dict
    return {"item": item_id}
```

```text
# Now start your uvicorn server
uvicorn main:pengfei_fastapi_app --reload

# Go to http://127.0.0.1:8000/items/foo, you will see a response of:
{"item_id":"foo"}
```

You can notice the path parameter that you enter in the url is passed to the function get_item().

### 3.1 Types of the parameter

Modify the get_item function by adding a type descriptor

```python
@pengfei_fastapi_app.get("/items/{item_id}")
async def get_item(item_id: int):
    # return a dict
    return {"item": item_id}
```

#### 3.1.2 Data validation

Now retry the url http://127.0.0.1:8000/items/foo, you will get a nice http error:

```json
{
  "detail": [
    {
      "loc": [
        "path",
        "item_id"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

This error is raised, because the path parameter item_id had a value of "foo", which can not be converted to int.

The same error would appear if you provided a float, for example with http://127.0.0.1:8000/items/3.8 ,you will get the
same error

##### Pydantic

All the data validation is performed under the hood by **Pydantic**, so you get all the benefits from it. And you know
you are in good hands.

You can use the same type declarations with str, float, bool and many other complex data types. Several of these are
explored in **the next chapters of the tutorial**.

#### 3.1.3 Data conversion

With http://127.0.0.1:8000/items/8 ,you will get

```json
{
  "item": 8
}
```

Notice that the value that the function get_item() received (and returned) is 8, **as a Python int, not a string "8"**.
**So, with that type declaration, FastAPI gives you automatic request "parsing"**.

### 3.2 Documentation

The Swagger API doc can be found at **http://127.0.0.1:8000/docs** .

And because the generated schema is from the **OpenAPI standard**, there are many compatible tools. Because of this,
FastAPI itself provides an alternative API documentation (using ReDoc), which you can access
at **http://127.0.0.1:8000/redoc**

### 3.3 The order of path operations

When creating path operations, you can find situations where you have a fixed path.

For example,

- /users/me :  returns the data about the current user.
- /users/{user_id} : returns the data about a specific user by its ID.

Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the
one for /users/{user_id}:

```python
@pengfei_fastapi_app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user id"}


@pengfei_fastapi_app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

Try to put the path /users/{user_id} before /users/me, when you put /users/me, you will get "me" as output. That's
because /users/me match also for /users/{user_id}, "me" is taking as the parameter user_id.

### 3.4 Parameter with predefined values

If you have a path operation that receives a path parameter, but you want the possible valid path parameter values to be
predefined, you can use **a standard Python Enum**.

#### 3.4.1 Create an Enum class in python

Import Enum and create a sub-class that inherits from str and from Enum.

By inheriting from str the API docs will be able to know that the values must be of type string and will be able to
render correctly.

Then create class attributes with fixed values, which will be the available valid values

```python
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
```

#### 3.4.2 Use the enum type inside a path operation

Note we add ModelName class as type annotation for parameter model_name in function get_model()

```python
from modelname import ModelName


@pengfei_fastapi_app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```
As we declare model_name as Type ModelName, the input will be converted automatically from str to Enum ModelName. The same 
conversion also applied to the return value model_name. You can notice in the api schema, the type of model_name in
returned json data is str. So the ModelName Enum type is automatically converted to str. 

Note, if you want to use str as the type of model_name, you only need to remove the type annotation of model_name in
the function declaration. In the comparison, you use str value instead of Enum type. Enum class can return a str 
value to by using "model_name.value"

### 3.5 Path parameter that contains path

Imagine that you have a path operation with a path /files/{file_path}, this operation allows you to get files of 
a certain path (e.g. /home/johndoe/myfile.txt) from the server.

So, the URL for that file would be something like: /files/home/johndoe/myfile.txt.

#### 3.5.1 OpenAPI support
**OpenAPI doesn't support a way to declare a path parameter to contain a path inside**, as that could lead to 
scenarios that are difficult to test and define.

**Nevertheless, you can still do it in FastAPI, using one of the internal tools from Starlette**.
And the docs would still work, although not adding any documentation telling that the parameter should contain a path.

#### 3.5.2 Path convertor
Using an option directly from Starlette you can declare a path parameter containing a path using a URL like:
**/files/{file_path:path}**. In this case, **the name of the parameter is file_path, and the last part, :path, tells 
it that the parameter should match any path**.

Check the below example

```python
@pengfei_fastapi_app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

Check the url : http://127.0.0.1:8000/files//home/johndoe/myfile.txt

Note the double slash (//) between files and home indicates the start of the value for file_path