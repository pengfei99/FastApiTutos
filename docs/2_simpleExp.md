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
                }}}}}}}}}
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
