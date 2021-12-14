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

## Doc list

- Part 2: A simple fast api example
- Part 3: Shows you how to use path parameter to pass argumentes to your endpoint
- Part 4: If path parameters are not enough, you can use query parameters
- Part 5:

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

As we declare model_name as Type ModelName, the input will be converted automatically from str to Enum ModelName. The
same conversion also applied to the return value model_name. You can notice in the api schema, the type of model_name in
returned json data is str. So the ModelName Enum type is automatically converted to str.

Note, if you want to use str as the type of model_name, you only need to remove the type annotation of model_name in the
function declaration. In the comparison, you use str value instead of Enum type. Enum class can return a str value to by
using "model_name.value"

### 3.5 Path parameter that contains path

Imagine that you have a path operation with a path /files/{file_path}, this operation allows you to get files of a
certain path (e.g. /home/johndoe/myfile.txt) from the server.

So, the URL for that file would be something like: /files/home/johndoe/myfile.txt.

#### 3.5.1 OpenAPI support

**OpenAPI doesn't support a way to declare a path parameter to contain a path inside**, as that could lead to scenarios
that are difficult to test and define.

**Nevertheless, you can still do it in FastAPI, using one of the internal tools from Starlette**. And the docs would
still work, although not adding any documentation telling that the parameter should contain a path.

#### 3.5.2 Path convertor

Using an option directly from Starlette you can declare a path parameter containing a path using a URL like:
**/files/{file_path:path}**. In this case, **the name of the parameter is file_path, and the last part, :path, tells it
that the parameter should match any path**.

Check the below example

```python
@pengfei_fastapi_app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

Check the url : http://127.0.0.1:8000/files//home/johndoe/myfile.txt

Note the double slash (//) between files and home indicates the start of the value for file_path

## 4. Query parameter

In FastAPI, When you declare a function that represents a api endpoint, if the parameters of the function are not the
endpoint path parameter, they are automatically interpreted as "query" parameters.

### 4.1 First example

Add the below endpoint to the main.py

```python
@pengfei_fastapi_app.get("/calculator/addition")
async def addition(x: int = 0, y: int = 0):
    return x + y
```

Now, run the app by using **uvicorn**

```shell
uvicorn main:pengfei_fastapi_app --reload
```

Check the endpoint with following url, note **?x=2&y=6** is the query parameter specification.

```text
http://127.0.0.1:8000/calculator/addition?x=2&y=6
```

### 4.2 Data parsing, validation

Similar to the path parameters, the query parameters in the url are all strings. Without a type indication in the python
function, they will be considered as string. If you set a type indicator as the above example, FastApi will convert the
string to your desire type.

#### Data validation

If the parameter can not be converted correctly, you will get a http error. Try the below query

```text
http://127.0.0.1:8000/calculator/addition?x=2&y=6

# You will receive below error message
{"detail":[{"loc":["query","x"],"msg":"value is not a valid integer","type":"type_error.integer"}]}
```

### 4.3 Default values

**As query parameters are not a fixed part of a path, they can be optional and can have default values.**
In the example above they have default values of x=0 and y=0.

So, going to the URL: http://127.0.0.1:8000/calculator/addition, you will get 0 as result.

You can also give one parameter and let the other parameter takes the default value Check the below url, you will get 2
as result

```text
http://127.0.0.1:8000/calculator/addition?x=2
```

### 4.4 Optional parameters

We can also declare optional query parameters in your endpoints. For instance, add below endpoint to main.py:

```python
from typing import Optional


@pengfei_fastapi_app.get("/products/{product_id}")
async def read_product(product_id: str, product_name: Optional[str] = None):
    if product_name:
        return {"product_id": product_id, "product_name": product_name}
    return {"product_id": product_id}
```

Note the parameter product_name has type Optional[str] and has a default value None. You can also notice the function
read_product() test first if the optional parameter is empty or not to avoid null pointer.

**Note: FastAPI will know that product_name is optional because of the = None. The Optional in Optional[str] is not used
by FastAPI (FastAPI will only use the str part), but the Optional[str] will let your editor help you finding errors in
your code.**

### 4.5 Bool type conversion

Conversion from string to int is quite standard in FastAPI. But the bool conversion is a little special.

Add the following endpoint to the main.py

```python
@pengfei_fastapi_app.get("/product-nums/{product_id}")
async def product_number(product_id: str, product_name: Optional[str] = None, warehouse: bool = False):
    if warehouse:
        product_num = 18
    else:
        product_num = 8
    if product_name:
        return {"product_id": product_id, "product_name": product_name, "product_number": product_num}
    return {"product_id": product_id, "product_number": product_num}
```

Test the endpoint with the following urls

```text
http://127.0.0.1:8000/product-nums/p1?product_name=cat%20food&warehouse=true
http://127.0.0.1:8000/product-nums/p1?product_name=cat%20food&warehouse=True

http://127.0.0.1:8000/product-nums/p1?product_name=cat%20food&warehouse=1
http://127.0.0.1:8000/product-nums/p1?product_name=cat%20food&warehouse=on
http://127.0.0.1:8000/product-nums/p1?product_name=cat%20food&warehouse=yes
http://127.0.0.1:8000/product-nums/p1?product_name=cat%20food&warehouse=YES
```

They will all return the following response. Which means the string in the list ["true","True","1","on","yes"] are all
converted to True. Note the uppercase, or First letter uppercase will not affect the result.

```json
{
  "product_id": "p1",
  "product_name": "cat food",
  "product_number": 18
}
```

### 4.6 Multiple path and query parameters

You can declare multiple path parameters and query parameters at the same time, FastAPI knows which is which.

And you don't have to declare them in any specific order.

Add the following endpoint in main.py

```python
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

```

Test the above endpoint with this url "http://127.0.0.1:8000/users/123/items/pliu?q=toto&short=true"

### 4.7 Required query parameters

To make a parameter required, you only need to define a parameter without default value or None.

Check the below checkpoint, it has two parameters x,y.

```python
@pengfei_fastapi_app.get("/calculator/soustraction")
async def soustraction(x: int, y: int):
    return x + y
```

Test it with below urls:

```text
http://127.0.0.1:8000/calculator/soustraction?x=4
```

You will get an error:

```json
{
  "detail": [
    {
      "loc": [
        "query",
        "y"
      ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 4.8 Recap

You can mix required parameter, optional parameter, and parameter with default value inside one endpoint.

## 5. Request Body

When you need to send data from a client (let's say, a browser) to your API, you send it as a **request body**.

- A **request body** is data sent by the client to your API.
- A **response body** is the data your API sends to the client.

Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the
time.

To declare a request body, you use **Pydantic models** with all their power and benefits.

---
**NOTE**

With HTTP, to send data we can use

- POST
- PUT
- DELETE
- PATCH

Don't use GET to send request body
---

### 5.1 Data model for request body

Below is a data model written by using **Pydantic**. Note the data model class must inherit the **pydantic.BaseModel**
class Suppose you put it in file product.py

```python
from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

Now you can use this data model in an endpoint. Add below code to the main.py. **Note we use the data model as the 
input parameter type for the python function of the endpoint**

```python
from product import Product


@pengfei_fastapi_app.post("/products/")
async def create_product(product: Product):
    return product
```

This time, as we need to use Http post method to send data, we need a tool to send data via Post. In this tutorial, we
use curl. Below is an example of curl command to send a Post request.

```shell
curl -X 'POST' \
  'http://127.0.0.1:8000/products/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "name": "TV",
  "description": "great tv",
  "price": 18,
  "tax": 2
}'
```

In return, you should receive a response as below

```json
{
  "id": 1,
  "name": "TV",
  "description": "great tv",
  "price": 18,
  "tax": 2
}
```

### 5.2 Required and optional model attributes

Just as the path/query parameters, if an attribute has default value, then it's optional, otherwise it's required.

```python
from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
```

With the above example:

- id: required
- name : required
- description: optional
- price: required
- tax optional

For instance, use below command and check the returned response
```shell
curl -X 'POST' \
  'http://127.0.0.1:8000/products/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 2,
  "name": "PC",
  "price": 28
}'
```

You should see below json as response. You can notice the attribute description and tax used the default value.

```json
{"id":2,"name":"PC","description":null,"price":28.0,"tax":null}
```

### 5.3 Access the attribute of the model

Check the following endpoint, you can notice, we can access all attributes as a dictionary of a data 
model (e.g. product.dict()). We can also access attributes one by one (e.g. product.price)

```python
@pengfei_fastapi_app.post("/products_price/")
async def create_product(product: Product):
    product_dict = product.dict()
    if product.tax:
        total_price = product.price + product.tax
        product_dict.update({"Total_price": total_price})
    return product_dict
```
With the following command:
```shell
curl -X 'POST' \
  'http://pengfei.org:8000/products_price/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 3,
  "name": "string",
  "description": "string",
  "price": 20,
  "tax": 8
}'
```

You should receive below response

```json
{
  "id": 3,
  "name": "string",
  "description": "string",
  "price": 20,
  "tax": 8,
  "Total_price": 28
}
```

### 5.4 Request body and path parameters

You can declare path parameters and request body at the same time.

FastAPI will recognize that the function parameters that match path **parameters should be taken from the path**, and 
that function **parameters that are declared to be Pydantic models** should be taken from the request body.

For example, with below endpoint, we will receive product_id as path parameter, and use it to overwrite the attribute
id in the request body.

```python
@pengfei_fastapi_app.post("/products_id/{product_id}")
async def create_product_with_id(product_id: int, product: Product):
    return {"product_id": product_id, **product.dict()}
```

Test the endpoint with below curl command
```shell
curl -X 'POST' \
  'http://pengfei.org:8000/products_id/4' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "name": "nice car",
  "price": 88
}'
```

You will see below response body:
```json
{
  "product_id": 4,
  "id": 1,
  "name": "nice car",
  "description": null,
  "price": 88,
  "tax": null
}
```

### 5.5 Request body + path parameters + query parameters

You can also declare body, path and query parameters, all at the same time. FastAPI will recognize each of them 
and take the data from the correct place.

Check the below endpoint, it uses one path parameter (e.g. product_id), one query parameter (e.g. supplier) and one request
body (e.g. product)

```python
@pengfei_fastapi_app.post("/products_attrs/{product_id}")
async def create_product_with_id(product_id: int, product: Product, supplier: Optional[str]):
    if supplier:
        return {"product_id": product_id, **product.dict(), "supplier": supplier}
    return {"product_id": product_id, **product.dict()}
```
With below curl command, 
```shell
curl -X 'POST' \
  'http://pengfei.org:8000/products_attrs/5?supplier=INRIA' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1,
  "name": "Box",
  "description": "a box for fun",
  "price": 88,
  "tax": 100
}'
```

you should see a json response
```json
{
  "product_id": 5,
  "id": 1,
  "name": "Box",
  "description": "a box for fun",
  "price": 88,
  "tax": 100,
  "supplier": "INRIA"
}
```

The parameter of a python function with FastApi annotation will be recognized as follows with order:
1. If the parameter is also declared in the path, it will be used as a path parameter.
2. If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
3. If the parameter is declared to be of the type of Pydantic model, it will be interpreted as a request body.