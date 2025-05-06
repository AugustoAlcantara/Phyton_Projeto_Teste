from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, select
from datetime import datetime

Base = declarative_base()

class ConnectedUser(Base):
    __tablename__ = 'connected_users'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    connected_at = Column(DateTime, default=lambda: datetime.now(datetime.timezone.utc))

class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(url, echo=False)
        self.SessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_user(self, address: str):
        async with self.SessionLocal() as session:
            user = ConnectedUser(address=address)
            session.add(user)
            await session.commit()

    async def remove_user(self, address: str):
        async with self.SessionLocal() as session:
            result = await session.execute(
                select(ConnectedUser).where(ConnectedUser.address == address)
            )
            user = result.scalars().first()
            if user:
                await session.delete(user)
                await session.commit()
