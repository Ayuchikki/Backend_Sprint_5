from database import engine, packages, dispatches
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
import jwt

USERNAME = "Ayushman"
PASSWORD = "12345"
ACCESS_TOKEN_EXP = 1
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"


def add_package(data):
    session = Session(engine)

    result = session.execute(
        insert(packages).values(
            package_name=data["package_name"],
            destination=data["destination"],
            weight=data["weight"],
            arrival_date=str(date.today()),
            status="Pending",
            dispatch_id=None
        )
    )

    package_id = result.inserted_primary_key[0]

    session.commit()
    session.close()

    return package_id


def get_packages():
    session = Session(engine)

    result = session.execute(select(packages))

    data = [dict(row._mapping) for row in result]

    session.close()

    return data


def get_package(package_id):
    session = Session(engine)

    result = session.execute(
        select(packages).where(packages.c.id == package_id)
    )

    row = result.fetchone()

    session.close()

    if row:
        return dict(row._mapping)

    return None


def update_package(package_id, data):
    session = Session(engine)

    result = session.execute(
        update(packages)
        .where(packages.c.id == package_id)
        .values(**data)
    )

    session.commit()

    count = result.rowcount

    session.close()

    return count


def delete_package(package_id):
    session = Session(engine)

    result = session.execute(
        delete(packages).where(packages.c.id == package_id)
    )

    session.commit()

    count = result.rowcount

    session.close()

    return count


def search_packages(name):
    session = Session(engine)

    result = session.execute(
        select(packages).where(
            packages.c.package_name.like(f"%{name}%")
        )
    )

    data = [dict(row._mapping) for row in result]

    session.close()

    return data


def add_dispatch(data):
    session = Session(engine)

    result = session.execute(
        insert(dispatches).values(
            destination=data["destination"],
            vehicle=data["vehicle"],
            dispatch_status="Created",
            dispatch_date=str(date.today())
        )
    )

    dispatch_id = result.inserted_primary_key[0]

    for package_id in data["package_ids"]:
        session.execute(
            update(packages)
            .where(packages.c.id == package_id)
            .values(
                status="Dispatched",
                dispatch_id=dispatch_id
            )
        )

    session.commit()
    session.close()

    return dispatch_id


def get_dispatches():
    session = Session(engine)

    result = session.execute(select(dispatches))

    data = [dict(row._mapping) for row in result]

    session.close()

    return data


def verify_login(username, password):
    if username == USERNAME and password == PASSWORD:
        access_token = create_token(username=username, token_type="access")
        refresh_token = create_token(username=username, token_type="refresh")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    return False


def create_token(username, token_type):
    time = ACCESS_TOKEN_EXP

    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY

    payload = {
        "username": username,
        "token_type": token_type,
        "exp": datetime.now() + timedelta(minutes=time)
    }

    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(token, token_type):
    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except:
        return False

    if payload["token_type"] == token_type:
        return payload["username"]

    return False