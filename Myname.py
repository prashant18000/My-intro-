import os, asyncio, time, requests
from telethon import TelegramClient, events, functions, types

# Aapki API Details
api_id = 31643839
api_hash = 'cb3f5e555c0b4fd0aa77ea7015bfce85'

client = TelegramClient('alpha_master', api_id, api_hash)

# --- Control Variables ---
tag_running = False
raids_running = False  # Sirf infinite wale ke liye
afk_status = False
afk_reason = ""
raids_msgs = ["Abey...", "Dum hai?", "Alpha is here!", "Tera baap aaya!", "Nikal lawde!", "Alpha power! ☠️"]

# 1. PING COMMAND
@client.on(events.NewMessage(pattern=r'^\.ping$'))
async def ping(event):
    start = time.time()
    msg = await event.edit("🚀 **Alpha is Online!**")
    end = time.time()
    ms = round((end - start) * 1000, 2)
    await msg.edit(f"🚀 **Alpha is Online!**\n`Latency: {ms}ms`")

# 2. HELP MENU
@client.on(events.NewMessage(pattern=r'^\.help$'))
async def help_menu(event):
    menu = """╔════════════════════════════╗
╠ 👑 𝕺𝖜𝖓𝖊𝖗 : ✨ ☠️𝓜𝓻. 𝓯𝓾𝓽𝓾𝓻𝓲𝓼𝓽𝓲𝓬 ☠️ ✨
╠ 🌐 𝖀𝖘𝖊𝖗𝖓𝖆𝖒𝖊 : @descent_boyy
╚════════════════════════════╝
📜 𝕮𝖔𝖒𝖒𝖆𝖓𝖉𝖘 𝕸𝖊𝖓𝖚 :
➪ .𝖆𝖘𝖐 | .𝖙𝖆𝖌 | .𝖙𝖆𝖌𝖆𝖑𝖑
➪ .𝖗𝖆𝖎𝖉 | .𝖗𝖆𝖎𝖉𝖘 | .𝖘𝖍𝖔𝖜𝖗𝖆𝖎𝖉
➪ .𝖈𝖑𝖔𝖓𝖊 | .𝖊𝖓𝖉𝖈𝖑𝖔𝖓𝖊 | .𝖕𝖚𝖗𝖌𝖊
➪ .𝖘𝖙𝖔𝖕 | .𝖘𝖙𝖔𝖕𝖆𝖑𝖑 | .𝖘𝖙𝖔𝖕𝖗𝖆𝖎𝖉"""
    await event.edit(menu)

# 3. SINGLE RAID (.raid) - Ek baar chalkar khud ruk jayega
@client.on(events.NewMessage(pattern=r'^\.raid$'))
async def single_raid(event):
    await event.edit("🔥 **𝕽𝖆𝖎𝖉 𝕾𝖙𝖆𝖗𝖙𝖊𝖉! (Single Mode)**")
    for msg in raids_msgs:
        try:
            await event.respond(msg)
            await asyncio.sleep(1.5)
        except:
            pass
    await event.respond("✅ **Single Raid Complete!**")

# 4. INFINITE RAID (.raids) - Repeat hota rahega
@client.on(events.NewMessage(pattern=r'^\.raids$'))
async def infinite_raids(event):
    global raids_running
    if raids_running:
        return await event.edit("⚠️ **Infinite Raid pehle se chal rahi hai!**")
    
    raids_running = True
    await event.edit("🔥 **𝕽𝖆𝖎𝖉 𝕾𝖙𝖆𝖗𝖙𝖊𝖉! (Infinite Mode)**")
    
    while raids_running:
        for msg in raids_msgs:
            if not raids_running: break
            try:
                await event.respond(msg)
                await asyncio.sleep(1.5)
            except:
                await asyncio.sleep(5)

# 5. SHOW RAID MESSAGES
@client.on(events.NewMessage(pattern=r'^\.showraid$'))
async def show_raid_list(event):
    msg_list = "\n".join([f"• {m}" for m in raids_msgs])
    await event.edit(f"📜 **Current Raid Messages:**\n\n{msg_list}")

# 6. STOP RAID / RAIDS
@client.on(events.NewMessage(pattern=r'^\.stopraids?$'))
async def stop_raid_cmd(event):
    global raids_running
    raids_running = False
    await event.edit("🛑 **𝕽𝖆𝖎𝖉 𝕾𝖙𝖔𝖕𝖕𝖊𝖉 Successfully.**")

# 7. TAG / TAGS (Spam)
@client.on(events.NewMessage(pattern=r'^\.tags?$'))
async def start_tags(event):
    global tag_running
    tag_running = True
    await event.edit("🚀 **𝕾𝖕𝖆𝖒 𝖙𝖆𝖌 𝕾𝖙𝖆𝖗𝖙𝖊𝖉...**")
    while tag_running:
        try:
            await event.respond("Oi! Suno @all 📢")
            await asyncio.sleep(2.5) 
        except:
            pass

# 8. STOP TAGS
@client.on(events.NewMessage(pattern=r'^\.stoptags$'))
async def stop_tags(event):
    global tag_running
    tag_running = False
    await event.edit("🛑 **𝕾𝖕𝖆𝖒 𝖙𝖆𝖌 𝕾𝖙𝖔𝖕℘𝖊𝖉.**")

# 9. MASTER STOP
@client.on(events.NewMessage(pattern=r'^\.stopall|\.stop$'))
async def stop_all(event):
    global raids_running, tag_running
    raids_running = False
    tag_running = False
    await event.edit("📴 **All Systems Stopped.**")

# 10. ASK AI
@client.on(events.NewMessage(pattern=r'^\.ask (.*)'))
async def ask_ai(event):
    question = event.pattern_match.group(1)
    await event.edit("🧠 **Thinking...**")
    try:
        url = f"https://chatgpt.apinepdev.workers.dev/?question={question}"
        response = requests.get(url).json()
        answer = response.get("answer", "No response.")
        await event.edit(f"🤖 **AI Answer:**\n{answer}")
    except:
        await event.edit("❌ **AI Busy hai.**")

# 11. PURGE
@client.on(events.NewMessage(pattern=r'^\.purge (.*)'))
async def purge_msgs(event):
    count = int(event.pattern_match.group(1))
    await event.edit(f"🗑️ **Purging {count} messages...**")
    msgs = []
    async for m in client.iter_messages(event.chat_id, limit=count+1):
        msgs.append(m)
    await client.delete_messages(event.chat_id, msgs)

# 12. CLONE (PFP + NAME + BIO)
@client.on(events.NewMessage(pattern=r'^\.clone$'))
async def clone_all(event):
    reply = await event.get_reply_message()
    if not reply: return await event.edit("Reply to someone!")
    await event.edit("👤 **Cloning EVERYTHING...**")
    user = await client.get_entity(reply.sender_id)
    full = await client(functions.users.GetFullUserRequest(user.id))
    await client(functions.account.UpdateProfileRequest(first_name=user.first_name or "", last_name=user.last_name or "", about=full.full_user.about or ""))
    photo = await client.download_profile_photo(user.id)
    if photo:
        await client(functions.photos.UploadProfilePhotoRequest(file=await client.upload_file(photo)))
        os.remove(photo)
    await event.edit("✅ **Cloned!**")

# 13. TAGALL
@client.on(events.NewMessage(pattern=r'^\.tagall$'))
async def tag_all(event):
    await event.delete()
    async for u in client.iter_participants(event.chat_id):
        if not u.bot:
            await client.send_message(event.chat_id, f"Hey [{u.first_name}](tg://user?id={u.id})")
            await asyncio.sleep(0.5)

# 14. AFK
@client.on(events.NewMessage(pattern=r'^\.afk(?: |$)(.*)'))
async def set_afk(event):
    global afk_status, afk_reason
    afk_status = True
    afk_reason = event.pattern_match.group(1) or "Busy hoon!"
    await event.edit(f"💤 **AFK ON:** `{afk_reason}`")

@client.on(events.NewMessage(incoming=True))
async def afk_rep(event):
    if afk_status and (event.is_private or event.mentioned):
        await event.reply(f"Owner AFK hai. **Reason:** `{afk_reason}`")

@client.on(events.NewMessage(outgoing=True))
async def off_afk(event):
    global afk_status
    if afk_status and not event.text.startswith(".afk"):
        afk_status = False
        await event.respond("✅ **Back Online!**")

print("Alpha Bot is LIVE and Ready!")
client.start()
client.run_until_disconnected()

