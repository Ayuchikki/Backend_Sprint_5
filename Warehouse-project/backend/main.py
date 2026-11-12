from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {"message": "Warehouse Dispatch System"}


@app.post("/packages")
def create_package(data: dict):
    package_id = functions.add_package(data)

    return {"message": "Package added", "id": package_id}


@app.get("/packages")
def all_packages():
    return functions.get_packages()


@app.get("/packages/{package_id}")
def package_details(package_id: int):
    package = functions.get_package(package_id)

    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    return package


@app.patch("/packages/{package_id}")
def edit_package(package_id: int, data: dict):
    result = functions.update_package(package_id, data)

    if result == 0:
        raise HTTPException(status_code=404, detail="Package not found")

    return {"message": "Package updated"}


@app.delete("/packages/{package_id}")
def remove_package(package_id: int):
    result = functions.delete_package(package_id)

    if result == 0:
        raise HTTPException(status_code=404, detail="Package not found")

    return {"message": "Package deleted"}


@app.get("/search/{name}")
def search_package(name: str):
    return functions.search_packages(name)


@app.post("/dispatches")
def create_dispatch(data: dict):
    dispatch_id = functions.add_dispatch(data)

    return {"message": "Dispatch created", "id": dispatch_id}


@app.get("/dispatches")
def all_dispatches():
    return functions.get_dispatches()