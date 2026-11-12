from fastapi import FastAPI, HTTPException, Header
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
def home(token=Header(None)):
    username = functions.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    return {"message": "Warehouse Dispatch System"}


@app.post("/packages")
def create_package(data: dict, token=Header(None)):
    username = functions.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    package_id = functions.add_package(data)

    return {"message": "Package added", "id": package_id}


@app.get("/packages")
def all_packages(token=Header(None)):
    username = functions.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    return functions.get_packages()


@app.get("/packages/{package_id}")
def package_details(package_id: int, token=Header(None)):
    username = functions.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    package = functions.get_package(package_id)

    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    return package


@app.patch("/packages/{package_id}")
def edit_package(package_id: int, data: dict, token=Header(None)):
    username = functions.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    result = functions.update_package(package_id, data)

    if result == 0:
        raise HTTPException(status_code=404, detail="Package not found")

    return {"message": "Package updated"}


@app.delete("/packages/{package_id}")
def remove_package(package_id: int, token=Header(None)):
    username = functions.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    result = functions.delete_package(package_id)

    if result == 0:
        raise HTTPException(status_code=404, detail="Package not found")

    return {"message": "Package deleted"}


@app.get("/search/{name}")
def search_package(name: str, token=Header(None)):
    username = functions.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    return functions.search_packages(name)


@app.post("/dispatches")
def create_dispatch(data: dict, token=Header(None)):
    username = functions.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    dispatch_id = functions.add_dispatch(data)

    return {"message": "Dispatch created", "id": dispatch_id}


@app.get("/dispatches")
def all_dispatches(token=Header(None)):
    username = functions.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    return functions.get_dispatches()


@app.post("/login")
def login(username: str, password: str):
    token = functions.verify_login(username=username, password=password)

    if token is None:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    return {token}

from fastapi import Header, HTTPException

@app.post("/refresh")
def refresh(refresh_token: str = Header(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    username = functions.verify_token(token=refresh_token, token_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    access_token = functions.create_token(username=username, token_type="access")
    return {"access_token": access_token}