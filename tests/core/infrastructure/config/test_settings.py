import pytest

from src.core.infrastructure.config.settings import Settings


class TestSettings:
    """Test suite for application settings validation."""

    def test_settings_in_memory_mode_generates_sqlite_url(self) -> None:
        """
        Test if in-memory mode returns the correct
        SQLite URL and ignores missing DB vars.
        """
        settings = Settings(test_in_memory=True)
        assert settings.database_url == "sqlite+aiosqlite:///:memory:"

    def test_settings_production_mode_generates_postgres_url(self) -> None:
        """Test if valid credentials generate the correct PostgreSQL URL."""
        settings = Settings(
            test_in_memory=False,
            db_host="localhost",
            db_port=5432,
            db_name="supply_db",
            db_user="admin",
            db_password="super_secret_password",
        )
        expected_url = (
            "postgresql+asyncpg://admin:super_secret_password@localhost:5432/supply_db"
        )
        assert settings.database_url == expected_url

    def test_settings_production_mode_without_credentials_raises_error(self) -> None:
        """Test if missing credentials in production mode raise validation errors."""
        with pytest.raises(ValueError) as exc_info:
            Settings(
                test_in_memory=False,
                db_name=None,
                db_user="admin",
                db_password="password",
            )

        assert "Missing required database settings: DB_NAME" in str(exc_info.value)

    def test_database_settings_incomplete_raises_runtime_error(self) -> None:
        """Test if missing database credentials raise a RuntimeError."""

        settings = Settings.model_construct(
            test_in_memory=False,
            db_host=None,
            db_port=None,
            db_name=None,
            db_user=None,
            db_password=None,
        )

        with pytest.raises(RuntimeError) as exc_info:
            _ = settings.database_url

        assert "Database settings are incomplete." in str(exc_info.value)
