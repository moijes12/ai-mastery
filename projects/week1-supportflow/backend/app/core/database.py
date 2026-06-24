import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel
from .config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    """Initialize database with retry"""
    for attempt in range(10):  # retry up to 10 times
        try:
            async with engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            print("✅ Database tables created successfully")
            return
        except Exception as e:
            print(f"⏳ Database not ready yet (attempt {attempt + 1}/10): {e}")
            await asyncio.sleep(3)
    raise Exception("❌ Could not connect to database after retries")
