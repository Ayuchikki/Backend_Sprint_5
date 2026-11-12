from database import engine, packages, dispatches
from sqlalchemy import select, insert, update, delete
from datetime import datetime, date, timedelta
import jwt 

USERNAME = "Ayushman"
PASSWORD = "12345"
ACCESS_TOKEN_EXP = 1
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_KEY = "SECRET123" 
ALGORITHM = "HS256"

def add_package(data):
    with engine.begin() as conn:
        result = conn.execute(
            insert(packages).values(
                package_name=data["package_name"],
                destination=data["destination"],
                weight=data["weight"],
                arrival_date=str(date.today()),
                status="Pending",
                dispatch_id=None
            )
        )

        return result.inserted_primary_key[0]


def get_packages():
    with engine.connect() as conn:
        result = conn.execute(select(packages))
        return [dict(row._mapping) for row in result]


def get_package(package_id):
    with engine.connect() as conn:
        result = conn.execute(
            select(packages).where(packages.c.id == package_id)
        )

        row = result.fetchone()

        if row:
            return dict(row._mapping)

        return None
def update_package(package_id, data):
    with engine.begin() as conn:
        result = conn.execute(
            update(packages)
            .where(packages.c.id == package_id)
            .values(**data)
        )

        return result.rowcount
def delete_package(package_id):
    with engine.begin() as conn:
        result = conn.execute(
            delete(packages).where(packages.c.id == package_id)
        )

        return result.rowcount
def search_packages(name):
    with engine.connect() as conn:
        result = conn.execute(
            select(packages).where(
                packages.c.package_name.like(f"%{name}%")
            )
        )

        return [dict(row._mapping) for row in result]


def add_dispatch(data):
    with engine.begin() as conn:
        result = conn.execute(
            insert(dispatches).values(
                destination=data["destination"],
                vehicle=data["vehicle"],
                dispatch_status="Created",
                dispatch_date=str(date.today())
            )
        )

        dispatch_id = result.inserted_primary_key[0]
        for package_id in data["package_ids"]:
            conn.execute(
                update(packages)
                .where(packages.c.id == package_id)
                .values(
                    status="Dispatched",
                    dispatch_id=dispatch_id
                )
            )
        return dispatch_id


def get_dispatches():
    with engine.connect() as conn:
        result = conn.execute(select(dispatches))

        return [dict(row._mapping) for row in result]

def verify_login(username, password):
    if username == USERNAME and password == PASSWORD:
        access_token = create_token(username=username, token_type = "access")
        refresh_token = create_token(username=username, token_type = "refresh")
        return {"access_token": access_token, "refresh_token": refresh_token}
    return False 

def create_token(username, token_type):
    time = ACCESS_TOKEN_EXP
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload ={
        "username":username,
        "token_type": token_type,
        "exp": datetime.now() + timedelta(minutes=time)
    }
    token = jwt.encode(payload = payload, key = SECRET_KEY, algorithm = ALGORITHM)
    return token

def verify_token (token, token_type):
    try:
        payload = jwt.decode(jwt= token, key= SECRET_KEY, algorithms= [ALGORITHM])
    except:
        return False 

    if payload ["token_type"]== token_type:
        return payload ["username"]
    
