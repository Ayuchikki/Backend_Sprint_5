from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

import functions
from models import LoginModel, UserCreate, PackageCreate, PackageUpdate, DispatchCreate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def startup():
    functions.create_default_admin()


def get_current_user(token):

    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    user = functions.verify_token(
        token=token,
        token_type="access"
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

    return user


def admin_check(user):

    if not functions.check_role(user, "admin"):
        raise HTTPException(status_code=403, detail="Admin access required")


@app.post("/login")
def login(data: LoginModel):

    result = functions.verify_login(
        username=data.username,
        password=data.password
    )

    if not result:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    return result


@app.post("/refresh")
def refresh(refresh_token: str = Header(None)):

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    user = functions.verify_token(
        token=refresh_token,
        token_type="refresh"
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = functions.create_token(
        username=user["username"],
        role=user["role"],
        token_type="access"
    )

    return {"access_token": access_token}


@app.post("/users")
def create_user(data: UserCreate, token: str = Header(None)):

    user = get_current_user(token)

    admin_check(user)

    result = functions.add_user(data.model_dump())

    if not result:
        raise HTTPException(status_code=400, detail="Username already exists")

    return {"message": "User created successfully"}


@app.get("/")
def home(token: str = Header(None)):

    user = get_current_user(token)

    return {
        "message": "Warehouse Dispatch System",
        "username": user["username"],
        "role": user["role"]
    }


@app.post("/packages")
def create_package(data: PackageCreate, token: str = Header(None)):

    user = get_current_user(token)

    package_id = functions.add_package(data.model_dump())

    return {"message": "Package added", "id": package_id}


@app.get("/packages")
def all_packages(token: str = Header(None)):

    user = get_current_user(token)

    return functions.get_packages()


@app.get("/packages/{package_id}")
def package_details(package_id: int, token: str = Header(None)):

    user = get_current_user(token)

    package = functions.get_package(package_id)

    if package is None:
        raise HTTPException(status_code=404, detail="Package not found")

    return package


@app.patch("/packages/{package_id}")
def edit_package(package_id: int, data: PackageUpdate, token: str = Header(None)):

    user = get_current_user(token)

    result = functions.update_package(
        package_id,
        data.model_dump(exclude_unset=True, exclude_none=True)
    )

    if result == 0:
        raise HTTPException(status_code=404, detail="Package not found")

    return {"message": "Package updated"}


@app.delete("/packages/{package_id}")
def remove_package(package_id: int, token: str = Header(None)):

    user = get_current_user(token)

    admin_check(user)

    result = functions.delete_package(package_id)

    if result == 0:
        raise HTTPException(status_code=404, detail="Package not found")

    return {"message": "Package deleted"}


@app.get("/search/{name}")
def search_package(name: str, token: str = Header(None)):

    user = get_current_user(token)

    return functions.search_packages(name)


@app.post("/dispatches")
def create_dispatch(data: DispatchCreate, token: str = Header(None)):

    user = get_current_user(token)

    dispatch_id = functions.add_dispatch(data.model_dump())

    return {"message": "Dispatch created", "id": dispatch_id}


@app.get("/dispatches")
def all_dispatches(token: str = Header(None)):

    user = get_current_user(token)

    return functions.get_dispatches()