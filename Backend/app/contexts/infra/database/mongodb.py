# app/contexts/infra/database/mongodb.py
import os
from pymongo import MongoClient
from flask import current_app, g


def _get_mongo_uri() -> str:
    # env first, then flask config, then default
    return (
        os.getenv("MONGO_URI")
        or current_app.config.get("MONGO_URI")
        or "mongodb://localhost:27017/hrms"
    )


def _get_db_name(uri: str) -> str:
    # env first, then flask config, then parse from URI, else fallback
    name = os.getenv("MONGO_DB_NAME") or current_app.config.get("MONGO_DB_NAME")
    if name:
        return name

    # Try to parse db name from uri path: mongodb://host:27017/mydb
    try:
        path = uri.split("?", 1)[0].rsplit("/", 1)[1]
        return path if path else "hrms"
    except Exception:
        return "hrms"


def get_mongo_client() -> MongoClient:
    if "mongo_client" not in g:
        uri = _get_mongo_uri()
        g.mongo_client = MongoClient(uri)
    return g.mongo_client


def get_db():
    """
    Returns a pymongo database object.
    Usage:
      db = get_db()
      db["collection"].find_one(...)
    """
    uri = _get_mongo_uri()
    db_name = _get_db_name(uri)
    client = get_mongo_client()
    return client[db_name]