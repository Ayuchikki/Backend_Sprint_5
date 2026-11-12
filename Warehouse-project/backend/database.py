from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float

DATABASE_URL = "sqlite:///warehouse.db"

engine = create_engine(DATABASE_URL)

metadata = MetaData()

packages = Table(
    "packages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("package_name", String),
    Column("destination", String),
    Column("weight", Float),
    Column("arrival_date", String),
    Column("status", String),
    Column("dispatch_id", Integer)
)

dispatches = Table(
    "dispatches",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("destination", String),
    Column("vehicle", String),
    Column("dispatch_status", String),
    Column("dispatch_date", String)
)

metadata.create_all(engine)