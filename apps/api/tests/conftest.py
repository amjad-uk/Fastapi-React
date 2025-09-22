import os
import re
import importlib
import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

# ---- Auto-discovery helpers -----------------------------------------------

def _import_first(candidates):
    last_err = None
    for modpath, attr in candidates:
        try:
            m = importlib.import_module(modpath)
            if attr is None:
                return getattr(m, "app")  # conventional app variable
            return getattr(m, attr)
        except Exception as e:
            last_err = e
            continue
    raise ImportError(f"None of the candidates could be imported: {candidates!r}; last error: {last_err!r}")

def resolve_create_app_or_app():
    """
    Try to resolve a FastAPI app factory (create_app) first; if unavailable,
    fall back to a module-level `app` instance.
    """
    candidates = [
        ("app.main", "create_app"),
        ("app.api.main", "create_app"),
        ("app.main", None),       # module-level app
        ("app.api.main", None),   # module-level app
    ]
    return _import_first(candidates)

def resolve_get_db():
    """
    Try typical locations for the FastAPI `get_db` dependency.
    """
    candidates = [
        ("app.dependencies", "get_db"),
        ("app.api.dependencies", "get_db"),
        ("app.db.deps", "get_db"),
        ("app.api.deps", "get_db"),
        ("app.db.session", "get_db"),
    ]
    return _import_first(candidates)

def resolve_base_metadata():
    """
    Resolve SQLAlchemy Base metadata (used to create tables for tests).
    """
    candidates = [
        ("app.db.base", "Base"),
        ("app.db.models", "Base"),
        ("app.models", "Base"),
    ]
    return _import_first(candidates)

# ---- DB URL / Schema / Engine ---------------------------------------------

def _worker_id(request) -> str:
    return getattr(request.config, "workerinput", {}).get("workerid", "gw0")

def _schema_name(worker_id: str) -> str:
    return f"test_{re.sub(r'[^0-9a-zA-Z_]', '_', worker_id)}"

def _base_db_url() -> str:
    return os.getenv(
        "DATABASE_URL_TEST",
        os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/app"),
    )

@pytest.fixture(scope="session")
def engine():
    url = _base_db_url()
    eng = sa.create_engine(url, future=True, pool_pre_ping=True)
    try:
        yield eng
    finally:
        eng.dispose()

@pytest.fixture(scope="session")
def _create_schema(request, engine):
    schema = _schema_name(_worker_id(request))
    with engine.connect() as conn:
        conn.execute(sa.text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        conn.commit()
    return schema

@pytest.fixture(scope="session", autouse=True)
def _migrate_schema(engine, _create_schema):
    # For tests, create tables from metadata (faster + no Alembic dependency).
    Base = resolve_base_metadata()
    with engine.connect() as conn:
        conn.execute(sa.text(f'SET search_path TO "{_create_schema}", public'))
        Base.metadata.create_all(bind=conn)
        conn.commit()

@pytest.fixture()
def db_session(engine, _create_schema):
    connection = engine.connect()
    connection.execute(sa.text(f'SET search_path TO "{_create_schema}", public'))
    trans = connection.begin()

    SessionLocal = sessionmaker(bind=connection, expire_on_commit=False, future=True)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()

# ---- FastAPI app + client -------------------------------------------------

@pytest.fixture()
def app(db_session):
    # Resolve app factory or existing app instance
    maybe_factory = resolve_create_app_or_app()
    # If this is a callable (factory), call it; else it should be an app instance
    app = maybe_factory() if callable(maybe_factory) else maybe_factory

    # Resolve get_db and override to inject the test session
    get_db = resolve_get_db()
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    return app

@pytest.fixture()
def client(app):
    return TestClient(app)
