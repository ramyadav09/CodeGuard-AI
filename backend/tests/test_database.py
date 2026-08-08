import pytest

from app.core.database import init_db


@pytest.mark.asyncio
async def test_init_db_success():
    """Verify init_db initializes the database successfully"""
    # Simply call it and verify it executes without throwing an exception
    await init_db()
