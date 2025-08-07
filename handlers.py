#------------------------------------------------Импорты-----------------------------------------------
from aiogram import Router, F, Bot
from aiogram.filters import  Command, CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from database.models import sub_types, tr_types
import keyboards as kb
import database.requests as rq 
from datetime import datetime
from text import tariffs,tariffs_for_pay,tariffs_for_manual_refund, admin_list, about_void, support_void, main_void, connect_void
import os
import uuid
import time 
from py3xui import AsyncApi
import xray as x
import asyncio
from service import send_to_client_error, send_to_group_error, send_to_group_transaction, delete_message, error_refund
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CopyTextButton
from payment import create_invoice, check_payment, manual_check_payment
from aiogram.utils.keyboard import InlineKeyboardBuilder
#-----------------------------------------------Сервис----------------------------------------------------------
router = Router()
api = AsyncApi(f'http://{os.getenv("IP")}:{os.getenv("PORT")}/{os.getenv("SECRET")}', os.getenv("LOGIN") , os.getenv("PASSWD"))

#------------------------------------------------Хендлеры меню-----------------------------------------------

@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    tg_id = message.from_user.id
    try:
        await rq.add_user(tg_id=tg_id) 
        if not tg_id in admin_list:
            await message.answer(text=main_void,parse_mode="HTML", reply_markup=kb.main_kb)
        else:
            await message.answer(text=main_void,parse_mode="HTML", reply_markup=kb.main_for_infinity_kb)
    except Exception as error:
        await send_to_client_error(message=message)
        await send_to_group_error(bot=bot,tg_id=tg_id,error_body="СТАРТ",e=error)
     
@router.message(Command("refund"))
async def command_refund(message: Message, bot: Bot, command: CommandObject):
     
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        if command.args is None:
            await message.reply(text="Не переданы агрументы")
            return
        args = command.args.split()
        if len(args) != 2:
            await message.reply(text="Не 2 аргумента")
            return
        
        try:
            await bot.refund_star_payment(
                user_id=args[0],
                telegram_payment_charge_id=args[1],
            )
            await message.answer(f"<b>Успешный возврат\nПользователь: </b><code>{args[0]}</code>\n<b>ID Транзакции:</b> <code>{args[1]}</code>",parse_mode="HTML", message_effect_id="5104841245755180586")
            asyncio.create_task(delete_message(message=message,sleep_time=30))
            await rq.make_transaction(tg_id=message.from_user.id,sub_type=sub_types.Manual,tr_type=tr_types.Refund, payment_id=f"Ручной возврат ({args[1]})")
        except Exception as error:
            await message.answer(f"{error}", message_effect_id="5046589136895476101")

    else:
        await message.reply(text=f"Ваша команда некорректна")

@router.callback_query(F.data == "status")
async def status(callback: CallbackQuery, bot:Bot):
    await callback.answer()
    tg_id = callback.message.chat.id
    try:
        await api.login()
        inbound_id = 1
        user = await x.get_client(api,tg_id, inbound_id)
        if user:
            unix_time_now = int(time.time())
            unix_time_client = int(user.expiry_time / 1000)
            if unix_time_client > unix_time_now:
                config = x.get_conection_str(user.id,tg_id)
                builder_status = InlineKeyboardBuilder()
                builder_status.row(InlineKeyboardButton(text="Конфиг для подключения",copy_text=CopyTextButton(text=config)))
                builder_status.row(InlineKeyboardButton(text="↩️ Назад", callback_data="back"))
                date_time = datetime.fromtimestamp(user.expiry_time / 1000)
                await callback.message.edit_text(text=f"<b>ID аккаунта:</b> <code>{callback.message.chat.id}</code>\n<b>Статус:</b> Активен 🟢 \n<b>Подписка до:</b> {date_time.strftime('%d-%m-%Y %H:%M')}\n<b>Скопируйте конфиг для подключения по кнопке ниже 👇</b>",parse_mode="HTML", reply_markup=builder_status.as_markup())
            elif user.expiry_time == 0:
                config = x.get_conection_str(user.id,tg_id)
                builder_status = InlineKeyboardBuilder()
                builder_status.row(InlineKeyboardButton(text="Конфиг для подключения",copy_text=CopyTextButton(text=config)))
                builder_status.row(InlineKeyboardButton(text="↩️ Назад", callback_data="back"))
                
                await callback.message.edit_text(text=f"<b>ID аккаунта:</b> <code>{callback.message.chat.id}</code>\n<b>Статус:</b> Неограниченный ⚪ \n<b>Скопируйте конфиг для подключения по кнопке ниже 👇</b>", parse_mode="HTML", reply_markup=builder_status.as_markup())
            else:
                await callback.message.edit_text(text=f"<b>ID аккаунта:</b> <code>{callback.message.chat.id}</code>\n<b>Статус:</b> Остановлен 🟡 \n<b>Подписка не оплачена</b>",parse_mode="HTML", reply_markup=kb.status_kb)
        else:
            await callback.message.edit_text(text=f"<b>ID аккаунта:</b> <code>{callback.message.chat.id}</code>\n<b>Статус:</b> Не активен 🔴 \nДля оплаты подписки перейдите в тарифы",parse_mode="HTML", reply_markup=kb.status_kb)
    except Exception as e:
        print(e)
        await send_to_client_error(callback.message)
        await send_to_group_error(bot,tg_id,"ПРОФИЛЬ",e)
        
@router.callback_query(F.data == "tariffs")
async def tarif_h(callback: CallbackQuery, bot: Bot):
    await callback.answer()
    tg_id = callback.message.chat.id
    try:
        check =  await rq.get_trial_status(tg_id=tg_id)
        if check:
            await callback.message.edit_text(text=tariffs, parse_mode="HTML", reply_markup=kb.tariffs_kb_not_used)
        else:
            await callback.message.edit_text(text=tariffs,parse_mode="HTML", reply_markup=kb.tariffs_kb_used)
    except Exception as error:
        await send_to_client_error(message=callback.message)
        await send_to_group_error(bot=bot,tg_id=tg_id,error_body="ТАРИФЫ",e=error)   
@router.callback_query(F.data == "about")
async def about(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=about_void, parse_mode="HTML",reply_markup=kb.about_kb)



@router.callback_query(F.data == "connect")
async def connect_h(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=connect_void, parse_mode="HTML",reply_markup=kb.connect_kb)

@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    await callback.answer()
    tg_id = callback.message.chat.id
    if not tg_id in admin_list:
        await callback.message.edit_text(text=main_void, reply_markup=kb.main_kb)
    else:
        await callback.message.edit_text(text=main_void, reply_markup=kb.main_for_infinity_kb)
@router.callback_query(F.data == "support")
async def support_h(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=support_void, parse_mode="HTML",reply_markup=kb.support_kb)

#------------------------------------------------ПРОБНЫЙ ТАРИФ----------------------------------------------- 
@router.callback_query(F.data == "choice_tarif_Trial")
async def tarifTrial(callback: CallbackQuery, bot: Bot):
    callback.answer()
    tg_id = callback.message.chat.id
    try:
        if await rq.get_trial_status(tg_id=tg_id):
            await api.login()
            inbound_id = 1
            if not await api.client.get_by_email(email=tg_id):
                await x.add_client(api=api,tg_id=tg_id, inbound_id=inbound_id, day=7)
                await bot.send_message(chat_id=os.getenv("GROUP_ID"), text=f"<b>[ПРОБНЫЙ]</b>\nПользователь: <code>{tg_id}</code>\nДата: <code>{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</code>",message_thread_id=os.getenv("TOPIC_ID_INFO"), parse_mode="HTML") 
                await rq.set_trial_status(tg_id=tg_id)
                await callback.message.edit_text(text=f"<b>Бесплатная подписка на 7 дней успешно активирована</b>\nКонфиг для подключения находится в вашем профиле\n",parse_mode="HTML",reply_markup=kb.back)
            else:
                await x.change_client(api=api,tg_id=tg_id, inbound_id=inbound_id,day=7)
                await bot.send_message(chat_id=os.getenv("GROUP_ID"), text=f"<b>[ПРОБНЫЙ]</b>\nПользователь: <code>{tg_id}</code>\nДата: <code>{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</code>",message_thread_id=os.getenv("TOPIC_ID_INFO"), parse_mode="HTML") 
                await rq.set_trial_status(tg_id=tg_id)
                await callback.message.edit_text(text=f"<b>Бесплатная подписка на 7 дней успешно активирована</b>\n7 дней добавлены к вашей подписке\nКонфиг для подключения находится в вашем профиле\n",parse_mode="HTML",reply_markup=kb.back)
        else:
            await callback.message.edit_text(text=f"<b>Вы уже активировали бесплатную подписку</b>",parse_mode="HTML",reply_markup=kb.back)
    except Exception as error:
        await send_to_client_error(message=callback.message) 
        await send_to_group_error(bot=bot,tg_id=tg_id,error_body="ПРОБНЫЙ",e=error) 

#------------------------------------------------ВЫБОР ТАРИФА----------------------------------------------- 
async def choice_tarif_edit_media(callback: CallbackQuery, msg_info: str, keyboard: InlineKeyboardMarkup): # Переключение на выбор способа оплаты
    await callback.message.edit_text(text=f"<b>Выберете способ оплаты</b>\n{msg_info}", parse_mode="HTML",reply_markup=keyboard)

@router.callback_query(F.data.contains("choice_tarif"))
async def choice_tarif(callback: CallbackQuery):
    await callback.answer()
    tarif = callback.data.split("_")[-1]
    if tarif == "1M":
        await choice_tarif_edit_media(callback=callback,msg_info="Оплата подписки на 1 месяц (31 день)",keyboard=kb.pay_1M)
    elif tarif == "3M":
        await choice_tarif_edit_media(callback=callback,msg_info="Оплата подписки на 3 месяца (93 дня)",keyboard=kb.pay_3M)
    elif tarif == "6M":
        await choice_tarif_edit_media(callback=callback,msg_info="Оплата подписки на 6 месяцев (186 дней)",keyboard=kb.pay_6M)    
    elif tarif == "1Y":
         await choice_tarif_edit_media(callback=callback,msg_info="Оплата подписки на 1 год (372 дня)",keyboard=kb.pay_1Y)    

#------------------------------------------------ОПЛАТА ЗВЕЗДАМИ------------------------------------------------ 
@router.pre_checkout_query()
async def pre_checkout(event: PreCheckoutQuery) -> None:
    await event.answer(ok=True)

async def pay_stars_send_invoice(bot: Bot, callback: CallbackQuery,amount: int, description: str, payload: str): # Отправка инвойса на оплату звездами
    await api.login()
    test_id = uuid.uuid4()
    inbound_id = 1
    tg_id = callback.message.chat.id
    if await x.test_connect(api=api,test_id=test_id,inbound_id=inbound_id):
        prices = [LabeledPrice(label="XTR", amount=amount)]
        star_invoice = await callback.message.answer_invoice(
            title="Подписка Void Connect",
            description=description,
            prices=prices,
            provider_token="",
            payload=payload,
            currency="XTR"
        )
        asyncio.create_task(delete_message(message=star_invoice,sleep_time=180))
        asyncio.create_task(x.del_test_connect(api=api,inbound_id=inbound_id,test_id=test_id))
    else:
        await send_to_client_error(message=callback.message) 
        await send_to_group_error(bot=bot,tg_id=tg_id,error_body=f"ПЕРЕД ОПЛАТОЙ ЗВЕЗДАМИ",e="Недоступность сервера")  

@router.callback_query(F.data.contains("pay_stars"))
async def pay_stars(callback: CallbackQuery,bot: Bot):
    await callback.answer()
    tarif = callback.data.split("_")[-1]
    if tarif == "1M":
        await pay_stars_send_invoice(bot=bot,callback=callback,amount=150,description="Оплата подписки на 1 месяц (31 день)",payload="success_stars_31")
    elif tarif == "3M":
        await pay_stars_send_invoice(bot=bot,callback=callback,amount=350,description="Оплата подписки на 3 месяца (93 дня)",payload="success_stars_93")
    elif tarif == "6M":
        await pay_stars_send_invoice(bot=bot,callback=callback,amount=500,description="Оплата подписки на 6 месяцев (186 дней)",payload="success_stars_186")
    elif tarif == "1Y":
        await pay_stars_send_invoice(bot=bot,callback=callback,amount=750,description="Оплата подписки на 1 год (372 дня)",payload="success_stars_372")

#------------------------------------------------ПОДТВЕРЖДЕНИЕ ЗВЕЗД------------------------------------------------ 

@router.message(F.successful_payment.invoice_payload.contains("success_stars")) # Успешная оплата звездами
async def success_payment_stars(message: Message, bot: Bot):
    tg_id = message.from_user.id
    tr_tg_id = message.successful_payment.telegram_payment_charge_id
    days = int(message.successful_payment.invoice_payload.split("_")[-1])
    
    try:
        if days == 31:
            await activate_tarif(bot=bot,message=message,tg_id=tg_id,payment_id=tr_tg_id,days=days,
                                msg_info="Успешная оплата подписки на 1 месяц (31 день)")

            await send_to_group_transaction(bot=bot,tg_id=tg_id,tarif=tariffs_for_pay.get(days),payment_id=tr_tg_id)
            await rq.make_transaction(tg_id=tg_id,sub_type=sub_types.OneMonth,tr_type=tr_types.Debid,payment_id=tr_tg_id)
        elif days == 93:
            await activate_tarif(bot=bot,message=message,tg_id=tg_id,payment_id=tr_tg_id,days=days,
                                 msg_info="Успешная оплата подписки на 3 месяца (93 дня)")
            
            await send_to_group_transaction(bot=bot,tg_id=tg_id,tarif=tariffs_for_pay.get(days),payment_id=tr_tg_id)
            await rq.make_transaction(tg_id=tg_id,sub_type=sub_types.ThreeMonth,tr_type=tr_types.Debid,payment_id=tr_tg_id)
        elif days == 186:
            await activate_tarif(bot=bot,message=message,tg_id=tg_id,payment_id=tr_tg_id,days=days,
                                 msg_info="Успешная оплата подписки на 6 месяцев (186 дней)")

            await send_to_group_transaction(bot=bot,tg_id=tg_id,tarif=tariffs_for_pay.get(days),payment_id=tr_tg_id)
            await rq.make_transaction(tg_id=tg_id,sub_type=sub_types.SixMonth,tr_type=tr_types.Debid,payment_id=tr_tg_id)
        elif days == 372:
            await activate_tarif(bot=bot,message=message,tg_id=tg_id,payment_id=tr_tg_id,days=days,
                                 msg_info="Успешная оплата подписки на 1 год (372 дней)")
            
            await send_to_group_transaction(bot=bot,tg_id=tg_id,tarif=tariffs_for_pay.get(days),payment_id=tr_tg_id)
            await rq.make_transaction(tg_id=tg_id,sub_type=sub_types.OneYear,tr_type=tr_types.Debid,payment_id=tr_tg_id)
    except Exception as error:
        await error_refund(bot=bot,tg_id=tg_id, payment_id=tr_tg_id)
        await send_to_client_error(message=message, star=True) 
        await send_to_group_error(bot=bot,tg_id=tg_id,error_body=f"ПОСЛЕ ОПЛАТЫ ЗВЕЗДАМИ",e=f"Недоступнось сервера или\n{error}")  

#------------------------------------------------Создание клиента xray------------------------------------------------ 

async def activate_tarif(message: Message, tg_id: int, days: int,payment_id: str = None,bot: Bot = None, msg_info: str = None): 
        await api.login()
        inbound_id = 1
        if not await api.client.get_by_email(email=tg_id):
            await x.add_client(api=api,tg_id=tg_id, inbound_id=inbound_id, day=days)
            if payment_id != None and bot != None and msg_info != None:
                builder_post_pay = InlineKeyboardBuilder(markup=[[
                    InlineKeyboardButton(
                        text="ID Транзакции",
                        copy_text=CopyTextButton(
                            text=payment_id
                        )
                    )
                ]])
                invoice = await message.answer(text=f"<b>{msg_info}\nCтатус платежа:</b> Оплачен ✅\n<b>ID Транзакции:</b> <code>{payment_id}</code>\nКонфиг для подключения находится в вашем профиле\n",
                                               parse_mode="HTML",reply_markup=builder_post_pay.as_markup(), message_effect_id="5104841245755180586")  
                await bot.pin_chat_message(chat_id=message.chat.id,message_id=invoice.message_id)
        else:
            await x.change_client(api=api,tg_id=tg_id,inbound_id=inbound_id,day=days)
            if payment_id != None and bot != None and msg_info != None:
                builder_post_pay = InlineKeyboardBuilder(markup=[[
                    InlineKeyboardButton(
                        text="ID Транзакции",
                        copy_text=CopyTextButton(
                            text=payment_id
                        )
                    )
                ]])
                invoice = await message.answer(text=f"<b>{msg_info}\nCтатус платежа:</b> Оплачен ✅\n<b>ID Транзакции:</b> <code>{payment_id}</code>\nКонфиг для подключения находится в вашем профиле\n",parse_mode="HTML",reply_markup=builder_post_pay.as_markup())
                await bot.pin_chat_message(chat_id=message.chat.id,message_id=invoice.message_id)
#---------------------------------------------ОПЛАТА ЮКаssa----------------------------------------------------------------- 

async def pay_yookassa_send_invoice(callback: CallbackQuery,message: Message,bot: Bot,tg_id: int,days: int,
                                     price: float,msg_info: str,msg_success: str):
    await api.login()
    test_id = uuid.uuid4()
    inbound_id = 1
   
    tg_id = callback.message.chat.id
    if (await x.test_connect(api=api,test_id=test_id,inbound_id=inbound_id)):
        payment_url, payment_id = await create_invoice(amount=price,chat_id=callback.from_user.id)
        builder_pre_pay = InlineKeyboardBuilder()
        builder_pre_pay.row(InlineKeyboardButton(
                text="Оплатить",
                url=payment_url
            ))
        builder_pre_pay.row(InlineKeyboardButton(
                text="Ручная проверка платежа",
                callback_data=f"manual_check_{days}_{payment_id}"
            ))  
            
        invoice = await message.edit_text(text=f"<b>{msg_info}\nID платежа:</b> <code>{payment_id}</code>\n<b>Cтатус платежа:</b> Не оплачен ❌\n<b>Если у вас автоматически не подтвердился платеж, нажмите кнопку ручная проверка платежа</b>",
                                                     parse_mode="HTML", reply_markup=builder_pre_pay.as_markup())
       
        await x.del_test_connect(api=api,test_id=test_id,inbound_id=inbound_id)
        if await check_payment(payment_id=payment_id):
            builder_post_pay = InlineKeyboardBuilder(markup=[[
                InlineKeyboardButton(
                    text="🧾 Чек ",
                    url=payment_url
                )
            ]]
            )
            try:
                
                await activate_tarif(message=message,tg_id=tg_id,days=days,msg_info=msg_success)
                await bot.pin_chat_message(chat_id=callback.message.chat.id,message_id=invoice.message_id)

                await invoice.edit_text(text=f"<b>{msg_success}\nID платежа:</b> <code>{payment_id}</code>\n<b>Cтатус платежа:</b> Оплачен ✅\nКонфиг для подключения находится в вашем профиле\n",
                                                            parse_mode="HTML",reply_markup=builder_post_pay.as_markup())
                
                await send_to_group_transaction(bot=bot,tg_id=tg_id,tarif=tariffs_for_pay.get(days), payment_id=payment_id)
                await rq.make_transaction(tg_id=tg_id,sub_type=sub_types.OneYear,tr_type=tr_types.Debid,payment_id=payment_id)
            except Exception as error:
                await send_to_client_error(message=message, yookassa=True) 
                await send_to_group_error(bot=bot,tg_id=tg_id,error_body=f"ПОСЛЕ ОПЛАТЫ ЮKassa",e=f"Недоступность сервера или \n{error}")  
        else:
            asyncio.create_task(delete_message(invoice,1))
            
    else:
        await send_to_client_error(message=message) 
        await send_to_group_error(bot=bot,tg_id=tg_id,msg=f"ПЕРЕД ОПЛАТОЙ ЮKassa",e="Недоступность сервера")  
        
        

@router.callback_query(F.data.contains("pay_yookassa"))
async def pay_yookassa(callback: CallbackQuery, bot: Bot):
    await callback.answer()    
    days = int(callback.data.split("_")[-1])
    tg_id = callback.message.chat.id
    if days == 31:
        await pay_yookassa_send_invoice(callback=callback,message=callback.message,bot=bot,tg_id=tg_id,days=days,
                                        price=259.00,msg_info="Оплата подписки на 1 месяц (31 день)",
                                        msg_success="Успешная оплата подписки на 1 месяц (31 день)")
    elif days == 93:
        await pay_yookassa_send_invoice(callback=callback,message=callback.message,bot=bot,tg_id=tg_id,days=days,
                                        price=589.00,msg_info="Оплата подписки на 3 месяца (93 дня)",
                                        msg_success="Успешная оплата подписки на 3 месяца (93 дня)")
    elif days == 186:
        await pay_yookassa_send_invoice(callback=callback,message=callback.message,bot=bot,tg_id=tg_id,days=days,
                                        price=839.00,msg_info="Оплата подписки на 6 месяцев (186 дней)",
                                        msg_success="Успешная оплата подписки на 6 месяцев (186 дней)")
    elif days == 372:
        await pay_yookassa_send_invoice(callback=callback,message=callback.message,bot=bot,tg_id=tg_id,days=days,
                                        price=1249.00,msg_info="Оплата подписки на 1 год (372 дней)",
                                        msg_success="Успешная оплата подписки на 1 год (372 дней)")
        
#-----------------------------------------------------------------------------------------------------------------------------
    
@router.callback_query(F.data.contains("manual_check"))
async def manual_check(callback: CallbackQuery, bot:Bot):
    tg_id = callback.message.chat.id
    try:
        payment_id = callback.data.split("_")[-1]
        days = int(callback.data.split("_")[-2])
        result = await manual_check_payment(payment_id) 
        if result:
            builder_post_pay = InlineKeyboardBuilder(markup=[[
                    InlineKeyboardButton(
                        text="🧾 Чек",
                        url=f"https://yoomoney.ru/checkout/payments/v2/contract?orderId={payment_id}"
                    )
                ]]
                )
            await activate_tarif(message=callback.message,tg_id=tg_id,days=days)
            await callback.answer(text="Оплата прошла ✅", show_alert=True)
            invoice = await callback.message.edit_text(text=f"<b>Ручная проверка\nУспешная оплата подписки\nID платежа:</b> <code>{payment_id}</code>\n<b>Cтатус платежа:</b> Оплачен ✅\nКонфиг для подключения находится в вашем профиле\n",
                                                            parse_mode="HTML",reply_markup=builder_post_pay.as_markup())
           
            
            await bot.pin_chat_message(chat_id=callback.message.chat.id,message_id=invoice.message_id)
            await send_to_group_transaction(bot=bot,tg_id=tg_id,tarif=tariffs_for_pay.get(days), payment_id=payment_id)
            await rq.make_transaction(tg_id=tg_id,sub_type=tariffs_for_manual_refund.get(days),tr_type=tr_types.Debid,payment_id=payment_id)
        else:
            await callback.answer(text="Оплата еще не прошла ❌", show_alert=True)
    except Exception as error:
        await send_to_client_error(message=callback.message) 
        await send_to_group_error(bot=bot,tg_id=tg_id,error_body=f"ПРОВЕРКА ОПЛАТЫ ЮKassa",e=f"Недоступность сервера или\n {error}")  
        
#----------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------ECHO хендлеры-------------------------------------------------------------------------------

@router.message(F.message_thread_id == 102)
async def trust_broadcast_message(message: Message,bot: Bot) -> None:
    try:    
        users = await rq.get_all_users()
        if message.text:
            for user in users:
                await bot.send_message(chat_id=user.user_tg_id, text=f"{message.text}")
            await message.reply("Текстовое сообщение отправлено всем")
        elif message.photo:
            for user in users:
                await bot.send_photo(chat_id=user.user_tg_id, photo=message.photo[-1].file_id, caption=message.caption)
            await message.reply("Фото отправлено всем")
        elif message.video:
            for user in users:
                await bot.send_video(chat_id=user.user_tg_id, video=message.video.file_id, caption=message.caption)
            await message.reply("Видео отправлено всем")
        elif message.document:
            for user in users:
                await bot.send_document(chat_id=user.user_tg_id, document=message.document.file_id, caption=message.caption)
            await message.reply("Документ отправлен всем")
        elif message.sticker:
            for user in users:
                await bot.send_sticker(chat_id=user.user_tg_id, sticker=message.sticker.file_id)
            await message.reply("Стикер отправлен всем")
        else:
            await message.answer(f"⚠️ Этот тип контента пока не поддерживается {message.content_type}")
    except Exception as error:
        await message.answer(f"{error}")
        
@router.message(F.content_type == ContentType.PINNED_MESSAGE)
async def echo_pined(message: Message) -> None:
    pass


@router.message(F.content_type == ContentType.TEXT and F.chat.type == "private")
async def echo_text(message: Message) -> None:
    await message.reply(f"Ваша команда некорректна 😑 {message.content_type}")

@router.message(F.content_type == ContentType.PHOTO and F.chat.type == "private")
async def echo_photo(message: Message) -> None:
    await message.reply(f"Я не умею анализировать картинки 😢")

@router.message(F.content_type == ContentType.VIDEO and F.chat.type == "private")
async def echo_video(message: Message) -> None:
    await message.reply(f"Я не умею просматривать видео 😑")

@router.message(F.content_type == ContentType.VOICE and F.chat.type == "private")
async def echo_voice(message: Message) -> None:
    await message.reply(f"Я не умею распозновать речь 😑")
