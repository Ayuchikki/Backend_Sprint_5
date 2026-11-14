]from database import engine, packages, dispatches, users
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt
import bcrypt

ACCESS_TOKEN_EXP = 30
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"


def hash_password(password):
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_default_admin():
    session = Session(engine)

    result = session.execute(
        select(users).where(users.c.username == "Ayushman")
    )

    user = result.fetchone()

    if not user:
        session.execute(
            insert(users).values(
                username="Ayushman",
                password=hash_password("12345"),
                role="admin"
            )
        )

        session.commit()

    session.close()


def add_user(data):
    session = Session(engine)

    result = session.execute(
        select(users).where(users.c.username == data["username"])
    )

    if result.fetchone():
        session.close()
        return False

    session.execute(
        insert(users).values(
            username=data["username"],
            password=hash_password(data["password"]),
            role=data["role"]
        )
    )

    session.commit()
    session.close()

    return True


def verify_login(username, password):

    session = Session(engine)

    result = session.execute(
        select(users).where(users.c.username == username)
    )

    user = result.fetchone()

    session.close()

    if user and verify_password(password, user.password):

        access_token = create_token(
            username=username,
            role=user.role,
            token_type="access"
        )

        refresh_token = create_token(
            username=username,
            role=user.role,
            token_type="refresh"
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user.role
        }

    return False


def create_token(username, role, token_type):

    time = ACCESS_TOKEN_EXP

    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY

    payload = {
        "username": username,
        "role": role,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)
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

    except jwt.InvalidTokenError:
        return False

    if payload.get("token_type") == token_type:
        return payload

    return False


def check_role(user, role):

    if user["role"] != role:
        return False

    return True


def add_package(data):

    session = Session(engine)

    result = session.execute(
        insert(packages).values(
            package_name=data["package_name"],
            destination=data["destination"],
            weight=data["weight"],
            arrival_date=str(datetime.now().date()),
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

    count = result.rowcount

    session.commit()
    session.close()

    return count


def delete_package(package_id):

    session = Session(engine)

    result = session.execute(
        delete(packages).where(packages.c.id == package_id)
    )

    count = result.rowcount

    session.commit()
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
            dispatch_date=str(datetime.now().date())
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