from logging.config import fileConfig
from alembic import context
import os
from app.db.base import Base
from app.models import user  # noqa: F401


config = context.config
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg://postgres:postgres@db:5432/app')
config.set_main_option('sqlalchemy.url', DATABASE_URL)

if config.config_file_name is not None: fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction(): context.run_migrations()

def run_migrations_online():
    from sqlalchemy import create_engine
    connectable = create_engine(DATABASE_URL)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction(): context.run_migrations()

if context.is_offline_mode(): run_migrations_offline()
else: run_migrations_online()
