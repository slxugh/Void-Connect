from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, ForeignKey, Enum, TIMESTAMP
import datetime
import os
import enum
from dotenv import load_dotenv


load_dotenv()
engine = create_async_engine(url=os.getenv("SQLALCHEMY"), connect_args={"password": os.getenv("POSTGRES_PASS")})

async_session = async_sessionmaker(engine)


@enum.unique
class sub_types(enum.Enum):
    Trial = 0,
    OneMonth = 1,
    ThreeMonth = 2,
    SixMonth = 3,
    OneYear = 4,
    Manual = 5

@enum.unique
class tr_types(enum.Enum):
    Trial = 0
    Debid = 1,
    Refund = 2


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_tg_id = mapped_column(BigInteger)
    trial_sub: Mapped[bool] = mapped_column(default=True)

class Transaction(Base):
    __tablename__ = "transactions"
    tr_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    sub_type = mapped_column(Enum(sub_types))
    tr_type= mapped_column(Enum(tr_types))
    tr_date: Mapped[datetime.date] = mapped_column(TIMESTAMP)
    payment_id: Mapped[str] = mapped_column()
    
class Promo(Base):
    __tablename__ = "promo"
    promo_id: Mapped[int] = mapped_column(primary_key=True)
    promo_name: Mapped[str] = mapped_column()
    promo_description: Mapped[str] = mapped_column()
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 