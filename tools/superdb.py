import os
from supabase import create_client, Client
from dotenv import load_dotenv
import asyncio


load_dotenv()


supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

###### USER TABLE  ###############

async def add_user(username:str,password:str)-> bool:
    check= await check_user(username)
    if check:
        return False
    supabase.table("users").insert(json={
        "username":username,
        "password":password
    }).execute()
    await add_pico(username)
    return True

async  def check_user(username:str)-> dict|None:
    response=supabase.table("users").select("username,password").eq("username",username).execute().data
    if not response:
        return None
    return response[0]

async def get_all_users()-> list|None:
    response=supabase.table("users").select("username,password")
    return response.execute().data

########### AI CHAT ####################

async def check_pico(username:str)->bool:
    response=supabase.table("pico").select("username").eq("username",username).execute().data
    if response:
        return True
    return False

async def add_pico(username:str)-> bool|None:
    check=await check_pico(username)
    if not check:
        supabase.table("pico").insert({"username":username,"chat_history":[]}).execute()
        return True

async def update_pico_chat(username:str,chat:list)-> bool|None:
    supabase.table("pico").update({"chat_history":chat}).eq("username",username).execute()
    return True

async def get_pico(username:str) -> dict|None:
    response=supabase.table("pico").select("chat_history").eq("username",username).execute().data
    if not response:
        return None
    return response[0]

############## PUBLIC CHAT ###############################

async def add_public_message(username:str,message:str)->bool|None:
    try:
        supabase.table("publicchat").insert({"username": username, "message": message}).execute()
        return True
    except Exception as e:
        print(f"Failed to insert message: {e}")
        return None

async def get_public_chats()->list|None:
    response=supabase.table("publicchat").select("username","message","created_at").execute().data
    if not response:
        return  None
    return response

############## PRIVATE CHAT ###############################

async def add_private_message(sender:str,receiver:str,message:str)->bool|None:
    supabase.table("privatechat").insert({"sender":sender,"receiver":receiver,"message":message}).execute()
    return True

async def get_private_chats(user1:str,user2:str)->list|None:
    response=supabase.table("privatechat").select("sender","receiver","message","created_at").or_(f"and(sender.eq.{user1},receiver.eq.{user2}),and(sender.eq.{user2},receiver.eq.{user1})").execute().data
    if not response:
        return  None
    return response


async def test_all():
    data1=await get_public_chats()
    data2=await get_private_chats("thejus","superman")
    data3=await get_pico("thejus")
    data4=await check_pico('thejus')
    print(f"Punlic chat:{data1}")
    print(f"Private chat:{data2}")
    print(f"Pico chat:{data3}")
    print(f"Pico user:{data4}")

if __name__=="__main__":
    asyncio.run(test_all())
