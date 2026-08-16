from sqlalchemy import text

from app.database import engine


def _add_column_if_missing(conn, table: str, column: str, ddl: str) -> None:
    exists = conn.execute(text(f"SHOW COLUMNS FROM `{table}` LIKE '{column}'")).fetchone()
    if exists is None:
        conn.execute(text(f"ALTER TABLE `{table}` ADD COLUMN {ddl}"))
        conn.commit()


def ensure_schema() -> None:
    """Add columns introduced after the first seed without wiping data."""
    with engine.connect() as conn:
        _add_column_if_missing(conn, "users", "is_active", "is_active TINYINT(1) NOT NULL DEFAULT 1")
        _add_column_if_missing(conn, "ai_insights", "trend", "trend VARCHAR(32) NULL")
        _add_column_if_missing(conn, "ai_insights", "trend_reason", "trend_reason TEXT NULL")
