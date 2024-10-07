from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import app.src.common.config.keyvault
from app.src.common.config import keyvault

username=keyvault.config_manager.get("username")
password=keyvault.config_manager.get("password")
# Declare postgres url in asynchronus way
SQL_ALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@localhost/itineraries"

# To manage connection to the db asynchronusly using create_async_engine
engine = create_async_engine(SQL_ALCHEMY_DATABASE_URL, echo=True, future=True)

# To create a factory for new Async sessions. expire_on_commit=False makes sure that instances are not expired after each commit
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()