
from yookassa import Payment, Configuration, Refund
import uuid
import asyncio
import os
Configuration.account_id = os.getenv("TEST_ID")
Configuration.secret_key = os.getenv("TEST_TOKEN")

async def create_invoice(amount, chat_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
    "amount": {
        "value": amount,
        "currency": "RUB"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "-"
    },
    "capture": True,
    "metadata": {
        'chat_id' : chat_id
    },
    "description": "Оплата подписки",
   
    "receipt": {
        'customer':{
            'email': "void@proton.me"
        },
        'items': [
            {
                "description": "Оплата подписки",
                "quantity": 1,
                "amount": {
                    "value": amount,
                    "currency": "RUB"
                },
                "vat_code": 1
            },
        ]
    }
	
    
    }, idempotency_key=id_key)

    return payment.confirmation.confirmation_url, payment.id

async def check_payment(payment_id):
    find = Payment.find_one(payment_id)
    count = 0
    while find.status == "pending":
        if count >= 120:
            break
        await asyncio.sleep(5)
        find = Payment.find_one(payment_id)
        count+=1
    if (find.status == "succeeded"):
        return find.metadata
    else:
        return False

async def manual_check_payment(payment_id):
    find = Payment.find_one(payment_id)
    if find.status == "succeeded":
        return find.metadata
    else:
        return False

#---------------------------------------------------
async def create_refund(amount, payment_id):
    refund = Refund.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "payment_id": payment_id
    })
    if (refund.status == "succeeded"):
        return True
    else:
        return False
