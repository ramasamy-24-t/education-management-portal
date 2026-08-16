from sqlalchemy import text

from app.database import engine


def ensure_schema() -> None:
    """Add columns introduced after the first seed without wiping data."""
    with engine.connect() as conn:
        exists = conn.execute(text("SHOW COLUMNS FROM users LIKE 'is_active'")).fetchone()
        if exists is None:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_active TINYINT(1) NOT NULL DEFAULT 1"))
            conn.commit()
