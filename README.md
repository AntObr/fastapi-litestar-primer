# Overview

This repository contains sample code demonstrating FastAPI and Litestars functionality and how they compare.

Key features explored:

* Wrapping a Flask application and serving it through FastAPI/Litestar
* Dependency injection
* Exception handling

# Setup

```sh
pip install -r requirements.txt
```

# Running the FastAPI application

```sh
uvicorn src.fastapi_main:app --reload
```

Interactive documentation can be accessed via `localhost:8080/docs`

# Running the Litestar application

```sh
uvicorn src.litestar_main:app --reload
```

Interactive documentation can be accessed via `localhost:8080/schema/swagger`
