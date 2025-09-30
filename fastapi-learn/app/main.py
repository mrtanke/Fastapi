# Entry point for FastAPI app
from fastapi import FastAPI, Depends

from .dependencies import get_token_header, get_query_token
from .internal import admin
from .routers import items, users

# Register child routes
app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(items.router)
app.include_router(users.router)
app.include_router(
    admin.router,
    dependencies=[Depends(get_token_header)],
    tags=["admin"],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

'''
.
├── app                  # "app" is a Python package
│   ├── __init__.py      # this file makes "app" a "Python package"
│   ├── main.py          # "main" module, e.g. import app.main
│   ├── dependencies.py  # "dependencies" module, e.g. import app.dependencies
│   └── routers          # "routers" is a "Python subpackage"
│   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   ├── items.py     # "items" submodule, e.g. import app.routers.items
│   │   └── users.py     # "users" submodule, e.g. import app.routers.users
│   └── internal         # "internal" is a "Python subpackage"
│       ├── __init__.py  # makes "internal" a "Python subpackage"
│       └── admin.py     # "admin" submodule, e.g. import app.internal.admin

module -> a .py file
package -> a folder containing __init__.py, a collection of Python modules
submodule -> a .py file in a package
subpackage -> a subfolder containing __init__.py
'''