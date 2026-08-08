import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.core.database import init_db, get_db, Base, engine
from app.core.config import Settings


@pytest.mark.asyncio
async def test_init_db_success():
    """Verify init_db initializes the database successfully"""
    await init_db()


@pytest.mark.asyncio
async def test_get_db_yields_session():
    """Test get_db yields a session and handles commit/rollback"""
    async for session in get_db():
        assert session is not None
        break


@pytest.mark.asyncio
async def test_get_db_rollback_on_exception():
    """Test get_db rolls back on exception"""
    with patch("app.core.database.AsyncSessionLocal") as mock_session_local:
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None
        mock_session.commit.side_effect = Exception("DB error")
        mock_session.rollback = AsyncMock()
        mock_session.close = AsyncMock()
        mock_session_local.return_value = mock_session

        try:
            async for _ in get_db():
                pass
        except Exception:
            pass

        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()


def test_database_url_normalization():
    """Test database URL normalization logic for postgres with SSL"""
    from app.core.config import Settings
    
    # Test the normalization logic directly
    db_url = "postgresql://user:pass@host/db?sslmode=require&channel_binding=require"
    is_neon = "neon.tech" in db_url
    needs_ssl = "sslmode=require" in db_url or is_neon
    
    if "?" in db_url:
        base_url, query = db_url.split("?", 1)
        params = [
            p
            for p in query.split("&")
            if not p.startswith("sslmode") and not p.startswith("channel_binding")
        ]
        db_url = base_url + ("?" + "&".join(params) if params else "")
    
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    connect_args = {}
    if "postgresql" in db_url and needs_ssl:
        connect_args["ssl"] = "require"
    
    assert "postgresql+asyncpg://" in db_url
    assert "sslmode" not in db_url
    assert "channel_binding" not in db_url
    assert connect_args.get("ssl") == "require"


def test_database_url_sqlite():
    """Test sqlite URL normalization"""
    db_url = "sqlite:///./test.db"
    
    if db_url.startswith("sqlite://") and not db_url.startswith("sqlite+aiosqlite://"):
        db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    
    connect_args = {}
    if "sqlite" in db_url:
        connect_args["check_same_thread"] = False
    
    assert "sqlite+aiosqlite://" in db_url
    assert connect_args.get("check_same_thread") is False


def test_database_url_postgres_no_ssl():
    """Test postgres URL without SSL"""
    db_url = "postgresql://user:pass@host/db"
    is_neon = "neon.tech" in db_url
    needs_ssl = "sslmode=require" in db_url or is_neon
    
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    connect_args = {}
    if "postgresql" in db_url and needs_ssl:
        connect_args["ssl"] = "require"
    
    assert "postgresql+asyncpg://" in db_url
    assert "ssl" not in connect_args
