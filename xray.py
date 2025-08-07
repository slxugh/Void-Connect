from py3xui import AsyncApi, Inbound, Client
from datetime import datetime, timedelta
import uuid
import os
from py3xui import AsyncApi
from dotenv import load_dotenv
import asyncio

async def get_client(api: AsyncApi, tg_id: int, inbound_id: int) -> Client:
    inbound = await api.inbound.get_by_id(inbound_id)
    clients =  inbound.settings.clients
    
    user = None
    for i in clients:
        if i.email == str(tg_id):
            user = i
            break

    return user

async def del_test_connect(api: AsyncApi, inbound_id:int, test_id: int):
    await asyncio.sleep(3)
    await api.client.delete(inbound_id=inbound_id,client_uuid=test_id)


async def test_connect(api: AsyncApi, test_id: int, inbound_id:int):
    try:
        new_client = Client(id=str(test_id), email=str(test_id), enable=True, flow="xtls-rprx-vision", expiryTime=0)
        await api.client.add(inbound_id, [new_client])
        return True
    except Exception as error:
        print(error)
        return False

async def add_client(api: AsyncApi,tg_id: int, inbound_id: int, day: int):
    id = uuid.uuid4()
    next_unix_time = convert_date(day)
    new_client = Client(id=str(id), email=str(tg_id), enable=True, flow="xtls-rprx-vision", expiryTime=next_unix_time)
    await api.client.add(inbound_id, [new_client])

async def change_client(api: AsyncApi,tg_id: int, inbound_id: int, day: int):
    user = await get_client(api, tg_id, inbound_id)
    client = await api.client.get_by_email(tg_id)
    client.expiry_time = deconvert_and_convert_date(client.expiry_time, day)
    client.id = user.id
    await api.client.update(client.id, client)

def get_conection_str(user_uuid: str, tg_id: str) -> str:
    load_dotenv()
    conf = f"vless://{user_uuid}@{os.getenv('HOST')}:443?type=tcp&security=reality&pbk=sSap216ztDCrxUoWhO0yl70MzUIMqviRVAP6idOBtlQ&fp=chrome&sni={os.getenv('HOST')}&sid=80&spx=%2F&flow=xtls-rprx-vision#{os.getenv('INBOUND_DE1')}-{tg_id}"
    return conf



def convert_date(day: int) -> int:
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    date_obj = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")
    next_datetime = date_obj + timedelta(days=day)
    next_unix_time = int(next_datetime.timestamp()) * 1000
    return next_unix_time

def deconvert_and_convert_date(time: int, day: int) -> int:
    client_datetime = datetime.fromtimestamp(time / 1000)
    formatted_datetime = client_datetime.strftime('%Y-%m-%d %H:%M:%S')
    date_obj = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")
    client_datetime_add = date_obj + timedelta(days=day)
    client_unix_add = int(client_datetime_add.timestamp()) * 1000
    return client_unix_add







