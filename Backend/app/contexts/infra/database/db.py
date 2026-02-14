from app.contexts.infra.database import extensions
import logging

def get_db(name: str | None = None):
    if extensions.mongo_client is None:
        raise RuntimeError("MongoClient not initialized. Did you forget to call init_extensions(app)?")

    db_name = name or getattr(extensions, "DATABASE_NAME", None) or "mvp-lite"
    logging.debug(f"Accessing MongoDB database: {db_name}")
    return extensions.mongo_client[db_name]