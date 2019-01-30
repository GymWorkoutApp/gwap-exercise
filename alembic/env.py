from __future__ import with_statement
from alembic import context
from gwap_framework.models.base import BaseModel
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from src.settings import DatabaseConfig

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = BaseModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    alembic_config = config.get_section(config.config_ini_section)
    alembic_config['sqlalchemy.url'] = DatabaseConfig.get_uri()

    engine = engine_from_config(alembic_config)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # from gwa_common.settings import DatabaseConfig
    alembic_config = config.get_section(config.config_ini_section)
    alembic_config['sqlalchemy.url'] = DatabaseConfig.get_uri()

    print(f'Connection to {alembic_config["sqlalchemy.url"]}')

    # alembic_config['sqlalchemy.url'] = f"postgresql://gwa_common:D1685E7932B7B71F138CECE1C0300414" \
    #                                   f"@localhost:5432/gwa_common_db"

    engine = engine_from_config(alembic_config)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
