from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, select
from datetime import datetime, timezone

Base = declarative_base()

class ConnectedUser(Base):
    __tablename__ = 'Usuarios'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    connected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
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
            # Verifica se o usuário já está registrado
            result = await session.execute(
                select(ConnectedUser).where(ConnectedUser.address == address)
            )
            existing_user = result.scalars().first()
            if not existing_user:
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
