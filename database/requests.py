import database.models as dbm
from database.models import User, Transaction
from sqlalchemy import select, update, insert
from datetime import datetime
from database.models import sub_types, tr_types

 
async def add_user(tg_id: int):
    async with dbm.async_session() as session:
        user = await session.scalar(select(User).where(User.user_tg_id == tg_id))
        if not user:
            session.add(User(user_tg_id = tg_id))
            await session.commit()

async def get_trial_status(tg_id: int) -> bool:
    async with dbm.async_session() as session:
        user = await session.scalar(select(User).where(User.user_tg_id == tg_id))
        if user.trial_sub:
            return True
        else:
            return False

async def get_all_users():
    async with dbm.async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()  
        return users

async def set_trial_status(tg_id: int) -> None:
    
    async with dbm.async_session() as session:
        stmt = update(User).where(User.user_tg_id== tg_id).values(trial_sub=False)
        await session.execute(stmt)
        await session.commit()

async def make_transaction(tg_id: int, sub_type: sub_types, tr_type: tr_types, payment_id: str) -> None:
    async with dbm.async_session() as session:  
        user = await session.scalar(select(User).where(User.user_tg_id == tg_id))
        if user:
            current_datetime = datetime.now()
            current_datetime_clean = current_datetime.replace(microsecond=0)
            transaction = insert(Transaction).values(user_id = user.user_id , sub_type = sub_type, tr_date = current_datetime_clean,tr_type = tr_type, payment_id = payment_id)
            await session.execute(transaction)
            await session.commit()
    
