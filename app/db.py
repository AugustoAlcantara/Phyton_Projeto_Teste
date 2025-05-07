from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, select
from datetime import datetime, timezone

Base = declarative_base()

class ConnectedUser(Base):
    __tablename__ = 'Usuarios'
    id = Column(Integer, primary_key=True, index=True)
    IdentificadorUsr = Column(String, unique=True, index=True)
    dtConectado = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(1), default="S")  # S = conectado, N = desconectado

class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(url, echo=False)
        self.SessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_user(self, IdentificadorUsr: str):
        async with self.SessionLocal() as session:
            result = await session.execute(
                select(ConnectedUser).where(ConnectedUser.IdentificadorUsr == IdentificadorUsr)
            )
            user = result.scalars().first()
            if user:
                user.status = "S"
            else:
                user = ConnectedUser(IdentificadorUsr=IdentificadorUsr, status="S")
                session.add(user)
            await session.commit()

    async def remove_user(self, IdentificadorUsr: str):
        async with self.SessionLocal() as session:
            result = await session.execute(
                select(ConnectedUser).where(ConnectedUser.IdentificadorUsr == IdentificadorUsr)
            )
            user = result.scalars().first()
            if user:
                user.status = "N"
                await session.commit()
