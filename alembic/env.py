from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.core.config import settings  # Импортируем настройки
from app.models.referral import ReferralCode
from app.models.users import Base  # Импортируем метаданные моделей

# Interpret the config file for Python logging.
fileConfig(context.config.config_file_name)

# Добавляем базовый класс declarative_base
target_metadata = Base.metadata

# Функция для получения URL базы данных


def get_url():
    return settings.DATABASE_URL.replace("+asyncpg", "")  # Убираем +asyncpg


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Получаем конфигурацию Alembic
    alembic_config = context.config.get_section(
        context.config.config_ini_section)
    if alembic_config is None:
        raise RuntimeError(
            "Alembic configuration section is missing or invalid.")

    # Устанавливаем SQLAlchemy URL
    alembic_config["sqlalchemy.url"] = get_url()

    # Создаем движок SQLAlchemy
    connectable = engine_from_config(
        alembic_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
