import os
from dotenv import load_dotenv
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
import asyncio
from datetime import datetime
import keyboards as kb

async def send_to_group_transaction(bot: Bot, tg_id: int, tarif: str, payment_id: str):
        await bot.send_message(chat_id=os.getenv("GROUP_ID"), 
                           text=f"<b>[ИНФО][{tarif}]\nПользователь:</b> <code>{tg_id}</code>\n<b>Дата:</b> <code>{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</code>\n<b>ID Платежа:</b> <code>{payment_id}</code>", 
                           message_thread_id=os.getenv("TOPIC_ID_INFO"),parse_mode="HTML") 
  

        

async def send_to_group_error(bot: Bot, tg_id: int, error_body: str, e: Exception, payment_id: str = None):
    if payment_id is not None:
        await bot.send_message(chat_id=os.getenv("GROUP_ID"), text=f"<b>[ОШИБКА][{error_body}]\nПользователь:</b> <code>{tg_id}</code>\nДата: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\nТранзакция: <code>{payment_id}</code>\nОшибка: <code>{e}</code>",message_thread_id=os.getenv("TOPIC_ID_ERROR"), parse_mode="HTML") 
    else:
        await bot.send_message(chat_id=os.getenv("GROUP_ID"), text=f"<b>[ОШИБКА][{error_body}]\nПользователь:</b> <code>{tg_id}</code>\nДата: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\nОшибка: <code>{e}</code>",message_thread_id=os.getenv("TOPIC_ID_ERROR"), parse_mode="HTML") 

async def send_to_client_error(message: Message, star: bool = False, yookassa: bool = False):
    if star:
        client_error_msg = await message.answer(f"<b>Ошибка на стороне сервера</b>\nЗвезды вернулись на ваш счет ⭐️\nСообщите в поддержку для ускорения решения проблемы\nДанное сообщение временное и удалится через 2 минуты",parse_mode="HTML",reply_markup=kb.support_kb)
    elif yookassa:
        client_error_msg = await message.answer(f"<b>Ошибка на стороне сервера</b>\nДля возврата денежных средств обратитесь в поддержку\nДанное сообщение временное и удалится через 2 минуты",parse_mode="HTML",reply_markup=kb.support_kb)
    else:
        client_error_msg = await message.answer(f"<b>Ошибка на стороне сервера</b>\nСообщите в поддержку для ускорения решения проблемы\nДанное сообщение временное и удалится через 2 минуты",parse_mode="HTML",reply_markup=kb.support_kb)
    
    asyncio.create_task(delete_message(client_error_msg, 120))

async def delete_message(message: Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await message.delete()

async def error_refund(bot: Bot, tg_id: int, payment_id: str):
    try:
        await bot.refund_star_payment(
            user_id=tg_id,
            telegram_payment_charge_id=payment_id,
        )
    except Exception as error:
        await send_to_group_error(bot=bot,tg_id=tg_id,error_body="КРИТИЧЕСКАЯ ОШИБКА ВОЗВРАТА",e=error,payment_id=payment_id)